"""
Database Backup Service
Automated backup and restore functionality for PGT TMS
"""
import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
import zipfile
import json
from typing import Optional

class BackupService:
    def __init__(self, db_path: str = "pgt_tms.db", backup_dir: str = "backups"):
        self.db_path = db_path
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        
    def create_backup(self, description: str = "") -> dict:
        """Create a full database backup"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}"
            backup_path = self.backup_dir / backup_name
            backup_path.mkdir(exist_ok=True)
            
            # Copy database file
            db_backup = backup_path / "pgt_tms.db"
            shutil.copy2(self.db_path, db_backup)
            
            # Create metadata
            metadata = {
                "timestamp": timestamp,
                "datetime": datetime.now().isoformat(),
                "description": description,
                "db_size": os.path.getsize(self.db_path),
                "backup_name": backup_name
            }
            
            with open(backup_path / "metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)
            
            # Create zip archive
            zip_path = self.backup_dir / f"{backup_name}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(db_backup, "pgt_tms.db")
                zipf.write(backup_path / "metadata.json", "metadata.json")
            
            # Clean up temporary files
            shutil.rmtree(backup_path)
            
            return {
                "success": True,
                "backup_file": str(zip_path),
                "metadata": metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def restore_backup(self, backup_file: str) -> dict:
        """Restore database from backup"""
        try:
            # Create safety backup before restore
            safety_backup = self.create_backup("Pre-restore safety backup")
            
            # Extract backup
            temp_dir = self.backup_dir / "temp_restore"
            temp_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Verify backup integrity
            restored_db = temp_dir / "pgt_tms.db"
            if not restored_db.exists():
                raise Exception("Backup file is corrupted")
            
            # Test database connection
            conn = sqlite3.connect(str(restored_db))
            conn.execute("SELECT 1")
            conn.close()
            
            # Replace current database
            shutil.copy2(restored_db, self.db_path)
            
            # Clean up
            shutil.rmtree(temp_dir)
            
            return {
                "success": True,
                "message": "Database restored successfully",
                "safety_backup": safety_backup
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_backups(self) -> list:
        """List all available backups"""
        backups = []
        for backup_file in self.backup_dir.glob("backup_*.zip"):
            try:
                with zipfile.ZipFile(backup_file, 'r') as zipf:
                    with zipf.open("metadata.json") as f:
                        metadata = json.load(f)
                        metadata["file_path"] = str(backup_file)
                        metadata["file_size"] = os.path.getsize(backup_file)
                        backups.append(metadata)
            except:
                continue
        
        return sorted(backups, key=lambda x: x["timestamp"], reverse=True)
    
    def delete_backup(self, backup_file: str) -> dict:
        """Delete a backup file"""
        try:
            os.remove(backup_file)
            return {"success": True, "message": "Backup deleted"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def cleanup_old_backups(self, keep_count: int = 10):
        """Keep only the most recent N backups"""
        backups = self.list_backups()
        if len(backups) > keep_count:
            for backup in backups[keep_count:]:
                self.delete_backup(backup["file_path"])

# Scheduled backup function
def scheduled_backup():
    """Run daily backup"""
    service = BackupService()
    result = service.create_backup("Automated daily backup")
    
    if result["success"]:
        # Keep only last 30 backups
        service.cleanup_old_backups(keep_count=30)
        print(f"✅ Backup created: {result['backup_file']}")
    else:
        print(f"❌ Backup failed: {result['error']}")
    
    return result

if __name__ == "__main__":
    # Test backup
    scheduled_backup()
