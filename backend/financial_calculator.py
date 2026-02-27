"""
Financial Calculator - Master financial calculations for PGT TMS
Provides real-time financial metrics and calculations
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func, extract
from typing import Dict, List, Optional, Any
from datetime import datetime, date, timedelta
import logging

from models import *
from ledger_engine import LedgerEngine, LedgerType
from database import SessionLocal

logger = logging.getLogger(__name__)

class FinancialCalculator:
    """
    Master financial calculator providing real-time calculations
    """
    
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()
        self.ledger_engine = LedgerEngine(self.db)
    
    def get_master_financial_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive financial summary for dashboard
        
        Returns:
            Dictionary with all master financial calculations
        """
        try:
            # Core financial metrics
            total_receivables = self.get_total_receivables()
            total_payables = self.get_total_payables()
            cash_bank_balance = self.get_cash_bank_balance()
            
            # Income and expense calculations
            total_income = self.get_total_income()
            total_expenses = self.get_total_expenses()
            net_profit = total_income - total_expenses
            
            # Today's cash flow
            today_cash_flow = self.get_daily_cash_flow(date.today())
            
            # Monthly calculations
            current_month_data = self.get_monthly_summary()
            
            # Fleet and operational metrics
            fleet_metrics = self.get_fleet_metrics()
            
            return {
                # Master Financial Calculations
                "total_receivables": total_receivables,
                "total_payables": total_payables,
                "cash_bank_balance": cash_bank_balance,
                "total_income": total_income,
                "total_expenses": total_expenses,
                "net_profit": net_profit,
                "profit_margin": (net_profit / total_income * 100) if total_income > 0 else 0,
                
                # Daily Cash Flow
                "daily_income": today_cash_flow["daily_income"],
                "daily_outgoing": today_cash_flow["daily_outgoing"],
                "daily_net": today_cash_flow["daily_net"],
                
                # Monthly Data
                "monthly_profit": current_month_data["profit"],
                "monthly_revenue": current_month_data["revenue"],
                "monthly_expenses": current_month_data["expenses"],
                "monthly_growth": current_month_data["growth_percentage"],
                
                # Fleet Metrics
                "active_vehicles": fleet_metrics["active_vehicles"],
                "total_trips": fleet_metrics["total_trips"],
                "monthly_trips": fleet_metrics["monthly_trips"],
                
                # Top entities
                "top_clients": self.get_top_clients(5),
                "top_vendors": self.get_top_vendors(5),
                
                # Alerts
                "alerts": self.get_financial_alerts()
            }
            
        except Exception as e:
            logger.error(f"Error calculating financial summary: {e}")
            return self._get_default_summary()
    
    def get_total_receivables(self) -> float:
        """
        Calculate total receivables (amounts clients owe us)
        
        Returns:
            Total amount receivable from clients
        """
        # Get all outstanding receivables (remove status filter for now)
        result = self.db.query(func.sum(Receivable.remaining_amount)).filter(
            Receivable.remaining_amount > 0
        ).scalar()
        
        return result or 0.0
    
    def get_total_payables(self) -> float:
        """
        Calculate total payables (sum of outstanding amounts - amounts we owe vendors)
        
        Returns:
            Total outstanding amount payable to vendors
        """
        # Get sum of outstanding amounts (not total amounts)
        result = self.db.query(func.sum(Payable.outstanding_amount)).filter(
            Payable.outstanding_amount > 0
        ).scalar()
        
        return result or 0.0
    
    def get_cash_bank_balance(self) -> float:
        """
        Calculate total cash and bank balance (placeholder for now)
        
        Returns:
            Total cash and bank balance
        """
        # Placeholder calculation - will be replaced with proper cash/bank ledger
        # For now, calculate as net profit accumulated
        net_profit = self.get_total_income() - self.get_total_expenses()
        return max(net_profit, 0.0)
    
    def get_total_income(self) -> float:
        """
        Calculate total income (client freight from SMART trips, excluding cancelled)
        
        Returns:
            Total income amount from client payments (excluding cancelled trips)
        """
        from models import TripStatus
        # SMART SYSTEM: Use client_freight as total income, exclude CANCELLED trips
        client_revenue = self.db.query(func.sum(Trip.client_freight)).filter(
            Trip.client_freight > 0,
            Trip.status != TripStatus.CANCELLED
        ).scalar() or 0.0
        
        return client_revenue
    
    def get_total_expenses(self) -> float:
        """
        Calculate total expenses (vendor freight + operational costs + office expenses, excluding cancelled)
        
        Returns:
            Total expenses amount (excluding cancelled trips)
        """
        from models import TripStatus
        # SMART SYSTEM: Vendor freight (what we pay vendors), exclude CANCELLED trips
        vendor_costs = self.db.query(func.sum(Trip.vendor_freight)).filter(
            Trip.vendor_freight > 0,
            Trip.status != TripStatus.CANCELLED
        ).scalar() or 0.0
        
        # Operational costs from trips (fuel, advance, munshiyana, other), exclude CANCELLED trips
        operational_costs = self.db.query(
            func.sum(Trip.fuel_cost + Trip.advance_paid + Trip.munshiyana_bank_charges + Trip.other_expenses)
        ).filter(
            Trip.status != TripStatus.CANCELLED
        ).scalar() or 0.0
        
        # Office expenses
        office_expenses = self.db.query(func.sum(Expense.amount)).scalar() or 0.0
        
        return vendor_costs + operational_costs + office_expenses
    
    def get_daily_cash_flow(self, target_date: date) -> Dict[str, float]:
        """
        Calculate daily cash flow for a specific date using SMART system data (excluding cancelled)
        
        Args:
            target_date: Date to calculate cash flow for
            
        Returns:
            Dictionary with daily_income, daily_outgoing, daily_net
        """
        from models import TripStatus
        # SMART SYSTEM: Daily income from client freight, exclude CANCELLED trips
        daily_income = self.db.query(func.sum(Trip.client_freight)).filter(
            func.date(Trip.date) == target_date,
            Trip.status != TripStatus.CANCELLED
        ).scalar() or 0.0
        
        # SMART SYSTEM: Daily outgoing = vendor freight + operational costs, exclude CANCELLED trips
        daily_vendor_costs = self.db.query(func.sum(Trip.vendor_freight)).filter(
            func.date(Trip.date) == target_date,
            Trip.status != TripStatus.CANCELLED
        ).scalar() or 0.0
        
        daily_operational_costs = self.db.query(
            func.sum(Trip.fuel_cost + Trip.advance_paid + Trip.munshiyana_bank_charges + Trip.other_expenses)
        ).filter(
            func.date(Trip.date) == target_date,
            Trip.status != TripStatus.CANCELLED
        ).scalar() or 0.0
        
        # Add office expenses for the day
        daily_office_expenses = self.db.query(func.sum(Expense.amount)).filter(
            func.date(Expense.date) == target_date
        ).scalar() or 0.0
        
        daily_outgoing = daily_vendor_costs + daily_operational_costs + daily_office_expenses
        daily_net = daily_income - daily_outgoing
        
        return {
            "daily_income": daily_income,
            "daily_outgoing": daily_outgoing,
            "daily_net": daily_net
        }
    
    def get_monthly_summary(self, target_month: date = None) -> Dict[str, Any]:
        """
        Get monthly financial summary using SMART system data (excluding cancelled)
        
        Args:
            target_month: Month to calculate for (defaults to current month)
            
        Returns:
            Monthly financial summary
        """
        from models import TripStatus
        if not target_month:
            target_month = date.today().replace(day=1)
        
        # Current month calculations
        current_month_start = target_month
        current_month_end = (current_month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # Previous month for comparison
        prev_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        prev_month_end = current_month_start - timedelta(days=1)
        
        # SMART SYSTEM: Current month metrics, exclude CANCELLED trips
        current_revenue = self.db.query(func.sum(Trip.client_freight)).filter(
            and_(
                func.date(Trip.date) >= current_month_start,
                func.date(Trip.date) <= current_month_end,
                Trip.status != TripStatus.CANCELLED
            )
        ).scalar() or 0.0
        
        current_vendor_costs = self.db.query(func.sum(Trip.vendor_freight)).filter(
            and_(
                func.date(Trip.date) >= current_month_start,
                func.date(Trip.date) <= current_month_end,
                Trip.status != TripStatus.CANCELLED
            )
        ).scalar() or 0.0
        
        current_operational_costs = self.db.query(
            func.sum(Trip.fuel_cost + Trip.advance_paid + Trip.munshiyana_bank_charges + Trip.other_expenses)
        ).filter(
            and_(
                func.date(Trip.date) >= current_month_start,
                func.date(Trip.date) <= current_month_end,
                Trip.status != TripStatus.CANCELLED
            )
        ).scalar() or 0.0
        
        current_office_expenses = self.db.query(func.sum(Expense.amount)).filter(
            and_(
                func.date(Expense.date) >= current_month_start,
                func.date(Expense.date) <= current_month_end
            )
        ).scalar() or 0.0
        
        current_expenses = current_vendor_costs + current_operational_costs + current_office_expenses
        current_profit = current_revenue - current_expenses
        
        # SMART SYSTEM: Previous month metrics for growth calculation, exclude CANCELLED trips
        prev_revenue = self.db.query(func.sum(Trip.client_freight)).filter(
            and_(
                func.date(Trip.date) >= prev_month_start,
                func.date(Trip.date) <= prev_month_end,
                Trip.status != TripStatus.CANCELLED
            )
        ).scalar() or 0.0
        
        # Growth calculation
        growth_percentage = 0.0
        if prev_revenue > 0:
            growth_percentage = ((current_revenue - prev_revenue) / prev_revenue) * 100
        
        return {
            "revenue": current_revenue,
            "expenses": current_expenses,
            "profit": current_profit,
            "growth_percentage": growth_percentage,
            "month": target_month.strftime("%B %Y")
        }
    
    def get_fleet_metrics(self) -> Dict[str, Any]:
        """
        Get fleet and operational metrics
        
        Returns:
            Fleet metrics dictionary
        """
        # Active fleet count - only DRAFT and ACTIVE trips (not COMPLETED, LOCKED, or CANCELLED)
        from models import TripStatus
        active_fleet = self.db.query(Trip).filter(
            Trip.status.in_([TripStatus.DRAFT, TripStatus.ACTIVE])
        ).count()
        
        # Total trips (all statuses)
        total_trips = self.db.query(Trip).count()
        
        # This month's trips (all statuses)
        current_month_start = date.today().replace(day=1)
        monthly_trips = self.db.query(Trip).filter(
            Trip.date >= current_month_start
        ).count()
        
        return {
            "active_vehicles": active_fleet,  # Renamed from active_vehicles to reflect it's active trips
            "total_trips": total_trips,
            "monthly_trips": monthly_trips
        }
    
    def get_top_clients(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get top clients by receivable balance
        
        Args:
            limit: Number of top clients to return
            
        Returns:
            List of top clients
        """
        top_clients = self.db.query(Client).filter(
            and_(Client.current_balance > 0, Client.is_active == True)
        ).order_by(desc(Client.current_balance)).limit(limit).all()
        
        return [
            {
                "id": client.id,
                "name": client.name,
                "code": client.client_code,
                "balance": client.current_balance,
                "contact": client.contact_person
            }
            for client in top_clients
        ]
    
    def get_top_vendors(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get top vendors by payable balance
        
        Args:
            limit: Number of top vendors to return
            
        Returns:
            List of top vendors
        """
        top_vendors = self.db.query(Vendor).filter(
            and_(Vendor.current_balance > 0, Vendor.is_active == True)
        ).order_by(desc(Vendor.current_balance)).limit(limit).all()
        
        return [
            {
                "id": vendor.id,
                "name": vendor.name,
                "code": vendor.vendor_code,
                "balance": vendor.current_balance,
                "contact": vendor.contact_person
            }
            for vendor in top_vendors
        ]
    
    def get_financial_alerts(self) -> List[Dict[str, Any]]:
        """
        Generate financial alerts and warnings
        
        Returns:
            List of financial alerts
        """
        alerts = []
        
        # High receivables alert (over 1M PKR)
        high_receivables = self.db.query(Client).filter(
            and_(Client.current_balance > 1000000, Client.is_active == True)
        ).count()
        
        if high_receivables > 0:
            alerts.append({
                "type": "warning",
                "title": "High Receivables",
                "message": f"{high_receivables} clients have outstanding balances over PKR 1M",
                "priority": "medium"
            })
        
        # High payables alert (over 500K PKR)
        high_payables = self.db.query(Vendor).filter(
            and_(Vendor.current_balance > 500000, Vendor.is_active == True)
        ).count()
        
        if high_payables > 0:
            alerts.append({
                "type": "error",
                "title": "High Payables",
                "message": f"{high_payables} vendors have balances over PKR 500K",
                "priority": "high"
            })
        
        # Negative cash flow alert
        today_cash_flow = self.get_daily_cash_flow(date.today())
        if today_cash_flow["daily_net"] < 0:
            alerts.append({
                "type": "warning",
                "title": "Negative Cash Flow",
                "message": f"Today's net cash flow is PKR {today_cash_flow['daily_net']:,.2f}",
                "priority": "high"
            })
        
        # Payroll processing reminder
        today = date.today()
        if today.day >= 25:  # Last week of month
            alerts.append({
                "type": "info",
                "title": "Payroll Processing",
                "message": "Monthly payroll processing needed",
                "priority": "medium"
            })
        
        return alerts
    
    def get_revenue_vs_expenses_chart_data(self, months: int = 6) -> Dict[str, Any]:
        """
        Get revenue vs expenses data for charts
        
        Args:
            months: Number of months to include
            
        Returns:
            Chart data dictionary
        """
        chart_data = {
            "labels": [],
            "revenue": [],
            "expenses": [],
            "profit": []
        }
        
        # Generate data for last N months
        for i in range(months):
            target_date = date.today().replace(day=1) - timedelta(days=i*30)
            target_date = target_date.replace(day=1)
            
            monthly_data = self.get_monthly_summary(target_date)
            
            chart_data["labels"].insert(0, target_date.strftime("%b %Y"))
            chart_data["revenue"].insert(0, monthly_data["revenue"])
            chart_data["expenses"].insert(0, monthly_data["expenses"])
            chart_data["profit"].insert(0, monthly_data["profit"])
        
        return chart_data
    
    def _get_default_summary(self) -> Dict[str, Any]:
        """
        Get default summary in case of errors
        
        Returns:
            Default financial summary
        """
        return {
            "total_receivables": 0.0,
            "total_payables": 0.0,
            "cash_bank_balance": 0.0,
            "total_income": 0.0,
            "total_expenses": 0.0,
            "net_profit": 0.0,
            "profit_margin": 0.0,
            "daily_income": 0.0,
            "daily_outgoing": 0.0,
            "daily_net": 0.0,
            "monthly_profit": 0.0,
            "monthly_revenue": 0.0,
            "monthly_expenses": 0.0,
            "monthly_growth": 0.0,
            "active_vehicles": 0,
            "total_trips": 0,
            "monthly_trips": 0,
            "top_clients": [],
            "top_vendors": [],
            "alerts": []
        }
    
    def close(self):
        """Close database connections"""
        if self.ledger_engine:
            self.ledger_engine.close()
        if self.db:
            self.db.close()