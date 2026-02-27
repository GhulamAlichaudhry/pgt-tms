import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { 
  Settings as SettingsIcon, 
  User, 
  Truck,
  Building2,
  Shield,
  Bell,
  Database,
  Download,
  Upload,
  Trash2,
  Save,
  RefreshCw,
  Plus,
  X
} from 'lucide-react';

const Settings = () => {
  const [activeTab, setActiveTab] = useState('company');
  const [loading, setLoading] = useState(false);
  const [vehicles, setVehicles] = useState([]);
  const [clients, setClients] = useState([]);
  const [vendors, setVendors] = useState([]);
  const [users, setUsers] = useState([]);
  const [showAddVehicleForm, setShowAddVehicleForm] = useState(false);
  const [showAddClientForm, setShowAddClientForm] = useState(false);
  const [showAddVendorForm, setShowAddVendorForm] = useState(false);
  const [showAddUserForm, setShowAddUserForm] = useState(false);
  const [editingUser, setEditingUser] = useState(null);

  const { register: registerVehicle, handleSubmit: handleVehicleSubmit, reset: resetVehicle, formState: { errors: vehicleErrors } } = useForm();
  const { register: registerClient, handleSubmit: handleClientSubmit, reset: resetClient, formState: { errors: clientErrors } } = useForm();
  const { register: registerVendor, handleSubmit: handleVendorSubmit, reset: resetVendor, formState: { errors: vendorErrors } } = useForm();
  const { register: registerUser, handleSubmit: handleUserSubmit, reset: resetUser, formState: { errors: userErrors } } = useForm();

  useEffect(() => {
    if (activeTab === 'vehicles') {
      fetchVehicles();
    } else if (activeTab === 'clients') {
      fetchClients();
    } else if (activeTab === 'vendors') {
      fetchVendors();
    } else if (activeTab === 'users') {
      fetchUsers();
    }
  }, [activeTab]);

  const fetchVehicles = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/vehicles/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setVehicles(response.data);
    } catch (error) {
      console.error('Error fetching vehicles:', error);
      toast.error('Failed to fetch vehicles');
    }
  };

  const fetchClients = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/clients/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setClients(response.data);
    } catch (error) {
      console.error('Error fetching clients:', error);
      toast.error('Failed to fetch clients');
    }
  };

  const fetchVendors = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/vendors/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setVendors(response.data);
    } catch (error) {
      console.error('Error fetching vendors:', error);
      toast.error('Failed to fetch vendors');
    }
  };

  const onSubmitVehicle = async (data) => {
    try {
      const token = localStorage.getItem('token');
      
      // Use custom vehicle type if "Custom" was selected
      const vehicleType = data.vehicle_type === 'Custom' && data.custom_vehicle_type 
        ? data.custom_vehicle_type 
        : data.vehicle_type;
      
      await axios.post('/vehicles/', {
        vehicle_no: data.vehicle_no,
        vehicle_type: vehicleType,
        capacity_tons: parseFloat(data.capacity_tons),
      }, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      toast.success('Vehicle added successfully!');
      resetVehicle();
      setShowAddVehicleForm(false);
      fetchVehicles();
    } catch (error) {
      console.error('Error adding vehicle:', error);
      toast.error('Failed to add vehicle');
    }
  };

  const onSubmitClient = async (data) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post('/clients/', {
        ...data,
        credit_limit: parseFloat(data.credit_limit || 0),
        payment_terms: parseInt(data.payment_terms || 30),
      }, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      toast.success('Client added successfully!');
      resetClient();
      setShowAddClientForm(false);
      fetchClients();
    } catch (error) {
      console.error('Error adding client:', error);
      toast.error('Failed to add client');
    }
  };

  const onSubmitVendor = async (data) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post('/vendors/', data, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      toast.success('Vendor added successfully!');
      resetVendor();
      setShowAddVendorForm(false);
      fetchVendors();
    } catch (error) {
      console.error('Error adding vendor:', error);
      toast.error('Failed to add vendor');
    }
  };

  // User Management Functions
  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/users/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
      toast.error('Failed to fetch users');
    }
  };

  const onSubmitUser = async (data) => {
    try {
      const token = localStorage.getItem('token');
      
      if (editingUser) {
        // Update existing user
        await axios.put(`/users/${editingUser.id}`, {
          full_name: data.full_name,
          email: data.email,
          role: data.role,
          is_active: data.is_active !== false
        }, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        toast.success('User updated successfully!');
      } else {
        // Create new user
        await axios.post('/users/', {
          username: data.username,
          email: data.email,
          full_name: data.full_name,
          role: data.role,
          password: data.password
        }, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        toast.success('User created successfully!');
      }
      
      resetUser();
      setShowAddUserForm(false);
      setEditingUser(null);
      fetchUsers();
    } catch (error) {
      console.error('Error saving user:', error);
      toast.error(error.response?.data?.detail || 'Failed to save user');
    }
  };

  const handleEditUser = (user) => {
    setEditingUser(user);
    setShowAddUserForm(true);
    resetUser({
      username: user.username,
      email: user.email,
      full_name: user.full_name,
      role: user.role,
      is_active: user.is_active
    });
  };

  const handleDeleteUser = async (userId, username) => {
    if (!window.confirm(`Are you sure you want to delete user "${username}"? This action cannot be undone.`)) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      await axios.delete(`/users/${userId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      toast.success('User deleted successfully!');
      fetchUsers();
    } catch (error) {
      console.error('Error deleting user:', error);
      toast.error(error.response?.data?.detail || 'Failed to delete user');
    }
  };

  const handleToggleUserStatus = async (userId, currentStatus) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(`/users/${userId}`, {
        is_active: !currentStatus
      }, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      toast.success(`User ${!currentStatus ? 'activated' : 'deactivated'} successfully!`);
      fetchUsers();
    } catch (error) {
      console.error('Error toggling user status:', error);
      toast.error(error.response?.data?.detail || 'Failed to update user status');
    }
  };

  const handleResetPassword = async (userId, username) => {
    const newPassword = prompt(`Enter new password for ${username}:`);
    if (!newPassword) return;

    if (newPassword.length < 6) {
      toast.error('Password must be at least 6 characters');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      await axios.put(`/users/${userId}/password`, {
        new_password: newPassword
      }, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      toast.success('Password reset successfully!');
    } catch (error) {
      console.error('Error resetting password:', error);
      toast.error('Failed to reset password');
    }
  };

  const getRoleBadgeColor = (role) => {
    switch (role) {
      case 'admin':
        return 'bg-red-100 text-red-800';
      case 'manager':
        return 'bg-blue-100 text-blue-800';
      case 'supervisor':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getRoleLabel = (role) => {
    switch (role) {
      case 'admin':
        return 'Administrator';
      case 'manager':
        return 'Manager';
      case 'supervisor':
        return 'Supervisor';
      default:
        return role;
    }
  };

  const handleExportData = async () => {
    try {
      toast.loading('Preparing complete data export...');
      const token = localStorage.getItem('token');
      
      // Export all data to Excel
      const response = await axios.get('/reports/export-all-data', {
        headers: { 'Authorization': `Bearer ${token}` },
        responseType: 'blob'
      });
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `PGT_Complete_Data_Export_${new Date().toISOString().split('T')[0]}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.dismiss();
      toast.success('Complete data exported successfully!');
    } catch (error) {
      console.error('Error exporting data:', error);
      toast.dismiss();
      toast.error('Failed to export data');
    }
  };

  const handleExportTripLogs = async () => {
    try {
      toast.loading('Exporting trip logs...');
      const token = localStorage.getItem('token');
      
      const response = await axios.get('/trips/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      // Convert to CSV
      const trips = response.data;
      if (trips.length === 0) {
        toast.dismiss();
        toast.error('No trip data to export');
        return;
      }
      
      const headers = ['Date', 'Vehicle', 'Client', 'Product', 'Destination', 'Freight In', 'Freight Out', 'Profit', 'Status'];
      const csvContent = [
        headers.join(','),
        ...trips.map(trip => [
          trip.date,
          trip.vehicle_no || '',
          trip.client_name || '',
          trip.product_name || '',
          trip.destination || '',
          trip.freight_amount_in || 0,
          trip.freight_amount_out || 0,
          trip.profit || 0,
          trip.status || 'completed'
        ].join(','))
      ].join('\n');
      
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Trip_Logs_${new Date().toISOString().split('T')[0]}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.dismiss();
      toast.success('Trip logs exported successfully!');
    } catch (error) {
      console.error('Error exporting trip logs:', error);
      toast.dismiss();
      toast.error('Failed to export trip logs');
    }
  };

  const handleExportStaffRecords = async () => {
    try {
      toast.loading('Exporting staff records...');
      const token = localStorage.getItem('token');
      
      const response = await axios.get('/staff/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      const staff = response.data;
      if (staff.length === 0) {
        toast.dismiss();
        toast.error('No staff data to export');
        return;
      }
      
      const headers = ['Employee ID', 'Name', 'Position', 'Phone', 'Gross Salary', 'Advance Balance', 'Monthly Deduction', 'Status'];
      const csvContent = [
        headers.join(','),
        ...staff.map(s => [
          s.employee_id || '',
          s.name || '',
          s.position || '',
          s.phone || '',
          s.gross_salary || 0,
          s.advance_balance || 0,
          s.monthly_deduction || 0,
          s.is_active ? 'Active' : 'Inactive'
        ].join(','))
      ].join('\n');
      
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Staff_Records_${new Date().toISOString().split('T')[0]}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.dismiss();
      toast.success('Staff records exported successfully!');
    } catch (error) {
      console.error('Error exporting staff records:', error);
      toast.dismiss();
      toast.error('Failed to export staff records');
    }
  };

  const handleExportFinancialLedgers = async () => {
    try {
      toast.loading('Exporting financial ledgers...');
      const token = localStorage.getItem('token');
      
      // Get receivables and payables
      const [receivablesRes, payablesRes] = await Promise.all([
        axios.get('/receivables/', { headers: { 'Authorization': `Bearer ${token}` } }),
        axios.get('/payables/', { headers: { 'Authorization': `Bearer ${token}` } })
      ]);
      
      const receivables = receivablesRes.data;
      const payables = payablesRes.data;
      
      // Create CSV content
      let csvContent = 'RECEIVABLES\n';
      csvContent += 'Client,Invoice Number,Date,Amount,Outstanding,Status\n';
      receivables.forEach(r => {
        csvContent += `${r.client_name || ''},${r.invoice_number || ''},${r.invoice_date || ''},${r.amount || 0},${r.remaining_amount || 0},${r.remaining_amount > 0 ? 'Pending' : 'Paid'}\n`;
      });
      
      csvContent += '\n\nPAYABLES\n';
      csvContent += 'Vendor,Invoice Number,Date,Amount,Outstanding,Status\n';
      payables.forEach(p => {
        csvContent += `${p.vendor_name || ''},${p.invoice_number || ''},${p.date || ''},${p.amount || 0},${p.outstanding_amount || 0},${p.outstanding_amount > 0 ? 'Pending' : 'Paid'}\n`;
      });
      
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Financial_Ledgers_${new Date().toISOString().split('T')[0]}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.dismiss();
      toast.success('Financial ledgers exported successfully!');
    } catch (error) {
      console.error('Error exporting financial ledgers:', error);
      toast.dismiss();
      toast.error('Failed to export financial ledgers');
    }
  };

  const handleImportData = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.xlsx,.xls,.csv';
    input.onchange = async (e) => {
      const file = e.target.files[0];
      if (!file) return;
      
      toast.loading('Importing data...');
      
      // For now, just show a message
      // In production, you would parse the file and send to backend
      setTimeout(() => {
        toast.dismiss();
        toast.info('Import functionality will be available in next update. Please use manual entry for now.');
      }, 1000);
    };
    input.click();
  };

  const handleResetAllData = async () => {
    // Show confirmation dialog
    const confirmed = window.confirm(
      '⚠️ DANGER: This will DELETE ALL DATA from the system!\n\n' +
      'This includes:\n' +
      '- All trips and fleet logs\n' +
      '- All clients and vendors\n' +
      '- All staff records and advances\n' +
      '- All financial transactions\n' +
      '- All receivables and payables\n\n' +
      'This action CANNOT be undone!\n\n' +
      'Type "DELETE ALL DATA" in the next prompt to confirm.'
    );

    if (!confirmed) return;

    // Second confirmation - require exact text
    const confirmText = prompt('Type "DELETE ALL DATA" to confirm (case sensitive):');
    
    if (confirmText !== 'DELETE ALL DATA') {
      toast.error('Reset cancelled - confirmation text did not match');
      return;
    }

    try {
      toast.loading('Resetting all data...');
      const token = localStorage.getItem('token');
      
      // Call backend endpoint to reset database
      await axios.post('/admin/reset-database', {}, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      toast.dismiss();
      toast.success('All data has been reset. Redirecting to login...');
      
      // Logout and redirect to login
      setTimeout(() => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }, 2000);
      
    } catch (error) {
      console.error('Error resetting data:', error);
      toast.dismiss();
      
      if (error.response?.status === 404) {
        // Endpoint doesn't exist, do manual reset
        toast.error('Backend reset endpoint not available. Please reset database manually.');
      } else {
        toast.error('Failed to reset data: ' + (error.response?.data?.detail || error.message));
      }
    }
  };

  const tabs = [
    { id: 'company', name: 'Company Info', icon: Building2 },
    { id: 'vehicles', name: 'Fleet Management', icon: Truck },
    { id: 'clients', name: 'Client Management', icon: User },
    { id: 'vendors', name: 'Vendor Management', icon: Building2 },
    { id: 'users', name: 'User Management', icon: User },
    { id: 'security', name: 'Security', icon: Shield },
    { id: 'notifications', name: 'Notifications', icon: Bell },
    { id: 'data', name: 'Data Management', icon: Database },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">System Settings</h1>
        <div className="flex items-center space-x-2 text-sm text-gray-500">
          <SettingsIcon className="h-4 w-4" />
          <span>PGT International TMS Configuration</span>
        </div>
      </div>

      {/* Settings Navigation */}
      <div className="glass-card rounded-xl">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8 px-6 overflow-x-auto">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm whitespace-nowrap flex items-center ${
                    activeTab === tab.id
                      ? 'border-red-500 text-red-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4 mr-2" />
                  {tab.name}
                </button>
              );
            })}
          </nav>
        </div>

        <div className="p-6">
          {/* Company Info Tab */}
          {activeTab === 'company' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">Company Information</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Company Name</label>
                    <input
                      type="text"
                      className="input-field"
                      defaultValue="PGT International (Private) Limited"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Registration Number</label>
                    <input
                      type="text"
                      className="input-field"
                      placeholder="Company registration number"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Tax ID / NTN</label>
                    <input
                      type="text"
                      className="input-field"
                      placeholder="National Tax Number"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                    <input
                      type="text"
                      className="input-field"
                      placeholder="+92-21-1234567"
                    />
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <input
                      type="email"
                      className="input-field"
                      placeholder="info@pgtinternational.com"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Website</label>
                    <input
                      type="url"
                      className="input-field"
                      placeholder="https://www.pgtinternational.com"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                    <textarea
                      className="input-field"
                      rows="4"
                      placeholder="Complete business address"
                    />
                  </div>
                </div>
              </div>
              
              <div className="flex justify-end">
                <button className="btn-primary flex items-center">
                  <Save className="h-4 w-4 mr-2" />
                  Save Company Info
                </button>
              </div>
            </div>
          )}

          {/* Fleet Management Tab */}
          {activeTab === 'vehicles' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium text-gray-900">Fleet Management</h3>
                <button
                  onClick={() => setShowAddVehicleForm(true)}
                  className="btn-primary flex items-center"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Add Vehicle
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {vehicles.map((vehicle) => (
                  <div key={vehicle.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center">
                        <Truck className="h-5 w-5 text-gray-400 mr-2" />
                        <span className="font-medium text-gray-900">{vehicle.vehicle_no}</span>
                      </div>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        vehicle.is_active 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        {vehicle.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">{vehicle.vehicle_type}</p>
                    <p className="text-sm text-gray-600">Capacity: {vehicle.capacity_tons} tons</p>
                  </div>
                ))}
              </div>

              {vehicles.length === 0 && (
                <div className="text-center py-8">
                  <Truck className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No vehicles registered</p>
                </div>
              )}
            </div>
          )}

          {/* Client Management Tab */}
          {activeTab === 'clients' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium text-gray-900">Client Management</h3>
                <button
                  onClick={() => setShowAddClientForm(true)}
                  className="btn-primary flex items-center"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Add Client
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {clients.map((client) => (
                  <div key={client.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center">
                        <User className="h-5 w-5 text-green-500 mr-2" />
                        <span className="font-medium text-gray-900">{client.name}</span>
                      </div>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        client.is_active 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        {client.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">{client.client_code}</p>
                    <p className="text-sm text-gray-600">Contact: {client.contact_person || 'N/A'}</p>
                    <p className="text-sm text-gray-600">Phone: {client.phone || 'N/A'}</p>
                    <p className="text-sm text-green-600 font-medium">Balance: PKR {client.current_balance?.toLocaleString() || '0'}</p>
                  </div>
                ))}
              </div>

              {clients.length === 0 && (
                <div className="text-center py-8">
                  <User className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No clients registered</p>
                </div>
              )}
            </div>
          )}

          {/* Vendor Management Tab */}
          {activeTab === 'vendors' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium text-gray-900">Vendor Management</h3>
                <button
                  onClick={() => setShowAddVendorForm(true)}
                  className="btn-primary flex items-center"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Add Vendor
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {vendors.map((vendor) => (
                  <div key={vendor.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center">
                        <Building2 className="h-5 w-5 text-red-500 mr-2" />
                        <span className="font-medium text-gray-900">{vendor.name}</span>
                      </div>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        vendor.is_active 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        {vendor.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">{vendor.vendor_code}</p>
                    <p className="text-sm text-gray-600">Contact: {vendor.contact_person || 'N/A'}</p>
                    <p className="text-sm text-gray-600">Phone: {vendor.phone || 'N/A'}</p>
                    <p className="text-sm text-red-600 font-medium">Balance: PKR {vendor.current_balance?.toLocaleString() || '0'}</p>
                  </div>
                ))}
              </div>

              {vendors.length === 0 && (
                <div className="text-center py-8">
                  <Building2 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No vendors registered</p>
                </div>
              )}
            </div>
          )}

          {/* User Management Tab */}
          {activeTab === 'users' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium text-gray-900">User Management</h3>
                <button
                  onClick={() => {
                    setEditingUser(null);
                    resetUser();
                    setShowAddUserForm(true);
                  }}
                  className="btn-primary flex items-center"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Add User
                </button>
              </div>
              
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-center">
                  <Shield className="h-5 w-5 text-blue-600 mr-2" />
                  <div>
                    <h4 className="font-medium text-blue-900">Role-Based Access Control</h4>
                    <p className="text-sm text-blue-700">
                      Admin: Full access + profit reports | Manager: Financial reports | Supervisor: Trip operations only
                    </p>
                  </div>
                </div>
              </div>

              {/* Users Table */}
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        User
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Email
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Role
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Status
                      </th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {users.map((user) => (
                      <tr key={user.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <User className="h-5 w-5 text-gray-400 mr-3" />
                            <div>
                              <div className="text-sm font-medium text-gray-900">{user.full_name}</div>
                              <div className="text-sm text-gray-500">@{user.username}</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900">{user.email || 'N/A'}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getRoleBadgeColor(user.role)}`}>
                            {getRoleLabel(user.role)}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            user.is_active 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-gray-100 text-gray-800'
                          }`}>
                            {user.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <div className="flex items-center justify-end gap-2">
                            <button
                              onClick={() => handleEditUser(user)}
                              className="text-blue-600 hover:text-blue-900"
                              title="Edit User"
                            >
                              Edit
                            </button>
                            <button
                              onClick={() => handleToggleUserStatus(user.id, user.is_active)}
                              className={`${user.is_active ? 'text-yellow-600 hover:text-yellow-900' : 'text-green-600 hover:text-green-900'}`}
                              title={user.is_active ? 'Deactivate' : 'Activate'}
                            >
                              {user.is_active ? 'Deactivate' : 'Activate'}
                            </button>
                            <button
                              onClick={() => handleResetPassword(user.id, user.username)}
                              className="text-purple-600 hover:text-purple-900"
                              title="Reset Password"
                            >
                              Reset Pwd
                            </button>
                            <button
                              onClick={() => handleDeleteUser(user.id, user.username)}
                              className="text-red-600 hover:text-red-900"
                              title="Delete User"
                            >
                              Delete
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {users.length === 0 && (
                <div className="text-center py-8">
                  <User className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No users found</p>
                </div>
              )}

              {/* Role Permissions Info */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                <div className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <span className="px-3 py-1 bg-red-100 text-red-800 text-sm rounded-full font-semibold">Administrator</span>
                  </div>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Full system access</li>
                    <li>• View profit margins</li>
                    <li>• Manage users</li>
                    <li>• Approve payments</li>
                    <li>• All financial reports</li>
                  </ul>
                </div>

                <div className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full font-semibold">Manager</span>
                  </div>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Financial reports (no profit)</li>
                    <li>• Approve payments</li>
                    <li>• Staff payroll</li>
                    <li>• View ledgers</li>
                    <li>• Expense management</li>
                  </ul>
                </div>

                <div className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <span className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full font-semibold">Supervisor</span>
                  </div>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Trip entry & management</li>
                    <li>• Fleet operations</li>
                    <li>• View trip logs</li>
                    <li>• Basic reports</li>
                    <li>• No financial access</li>
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* Security Tab */}
          {activeTab === 'security' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">Security Settings</h3>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div>
                    <h4 className="font-medium text-gray-900">Two-Factor Authentication</h4>
                    <p className="text-sm text-gray-600">Add extra security to your account</p>
                  </div>
                  <button className="btn-secondary">Enable 2FA</button>
                </div>

                <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div>
                    <h4 className="font-medium text-gray-900">Session Timeout</h4>
                    <p className="text-sm text-gray-600">Auto-logout after inactivity</p>
                  </div>
                  <select className="input-field w-32">
                    <option>30 minutes</option>
                    <option>1 hour</option>
                    <option>2 hours</option>
                    <option>4 hours</option>
                  </select>
                </div>

                <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div>
                    <h4 className="font-medium text-gray-900">Password Policy</h4>
                    <p className="text-sm text-gray-600">Minimum 8 characters, mixed case, numbers</p>
                  </div>
                  <span className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">Active</span>
                </div>
              </div>
            </div>
          )}

          {/* Notifications Tab */}
          {activeTab === 'notifications' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">Notification Settings</h3>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div>
                    <h4 className="font-medium text-gray-900">High Advance Balance Alert</h4>
                    <p className="text-sm text-gray-600">Notify when staff advance exceeds limit</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" defaultChecked />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div>
                    <h4 className="font-medium text-gray-900">Outstanding Receivables Alert</h4>
                    <p className="text-sm text-gray-600">Alert when receivables exceed 5M PKR</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" defaultChecked />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div>
                    <h4 className="font-medium text-gray-900">Payroll Processing Reminder</h4>
                    <p className="text-sm text-gray-600">Monthly reminder for payroll processing</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" defaultChecked />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>
              </div>
            </div>
          )}

          {/* Data Management Tab */}
          {activeTab === 'data' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">Data Management</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h4 className="font-medium text-gray-900">Export Data</h4>
                  
                  <button
                    onClick={handleExportData}
                    className="w-full flex items-center justify-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-gray-400 transition-colors"
                  >
                    <Download className="h-6 w-6 text-gray-400 mr-2" />
                    <div className="text-center">
                      <p className="text-sm font-medium text-gray-900">Export All Data</p>
                      <p className="text-xs text-gray-500">Download Excel format</p>
                    </div>
                  </button>

                  <div className="space-y-2">
                    <button onClick={handleExportTripLogs} className="w-full btn-secondary text-left flex items-center justify-between">
                      <span>Export Trip Logs</span>
                      <Download className="h-4 w-4" />
                    </button>
                    <button onClick={handleExportStaffRecords} className="w-full btn-secondary text-left flex items-center justify-between">
                      <span>Export Staff Records</span>
                      <Download className="h-4 w-4" />
                    </button>
                    <button onClick={handleExportFinancialLedgers} className="w-full btn-secondary text-left flex items-center justify-between">
                      <span>Export Financial Ledgers</span>
                      <Download className="h-4 w-4" />
                    </button>
                  </div>
                </div>

                <div className="space-y-4">
                  <h4 className="font-medium text-gray-900">Import Data</h4>
                  
                  <button
                    onClick={handleImportData}
                    className="w-full flex items-center justify-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-gray-400 transition-colors"
                  >
                    <Upload className="h-6 w-6 text-gray-400 mr-2" />
                    <div className="text-center">
                      <p className="text-sm font-medium text-gray-900">Import Excel Data</p>
                      <p className="text-xs text-gray-500">Upload existing records</p>
                    </div>
                  </button>

                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                    <div className="flex items-center">
                      <RefreshCw className="h-5 w-5 text-yellow-600 mr-2" />
                      <div>
                        <h5 className="font-medium text-yellow-900">Data Backup</h5>
                        <p className="text-sm text-yellow-700">
                          Last backup: {new Date().toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="border-t pt-6">
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <Trash2 className="h-5 w-5 text-red-600 mr-2" />
                      <div>
                        <h4 className="font-medium text-red-900">Danger Zone</h4>
                        <p className="text-sm text-red-700">Irreversible actions</p>
                      </div>
                    </div>
                    <button 
                      onClick={handleResetAllData}
                      className="px-4 py-2 bg-red-600 text-white text-sm rounded-lg hover:bg-red-700 transition-colors"
                    >
                      Reset All Data
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Add Vehicle Modal */}
      {showAddVehicleForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl w-full max-w-md overflow-hidden">
            
            {/* Modal Header */}
            <div className="bg-red-600 px-6 py-4 text-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Plus className="h-6 w-6" />
                  <h2 className="text-xl font-semibold">Add New Vehicle</h2>
                </div>
                <button
                  onClick={() => setShowAddVehicleForm(false)}
                  className="p-1 hover:bg-red-700 rounded transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            </div>

            {/* Modal Content */}
            <div className="p-6">
              <form onSubmit={handleVehicleSubmit(onSubmitVehicle)} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Vehicle Number *</label>
                  <input
                    type="text"
                    {...registerVehicle('vehicle_no', { required: 'Vehicle number is required' })}
                    className="input-field"
                    placeholder="e.g., KHI-123"
                  />
                  {vehicleErrors.vehicle_no && <p className="text-red-500 text-sm mt-1">{vehicleErrors.vehicle_no.message}</p>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Vehicle Type *</label>
                  <select
                    {...registerVehicle('vehicle_type', { required: 'Vehicle type is required' })}
                    className="input-field"
                    onChange={(e) => {
                      if (e.target.value === 'Custom') {
                        document.getElementById('custom-vehicle-type').style.display = 'block';
                      } else {
                        document.getElementById('custom-vehicle-type').style.display = 'none';
                      }
                    }}
                  >
                    <option value="">Select Type</option>
                    <option value="40 Ft Container">40 Ft Container</option>
                    <option value="20 Ft Container">20 Ft Container</option>
                    <option value="Flat Bed">Flat Bed</option>
                    <option value="Custom">Custom (Enter Manually)</option>
                  </select>
                  {vehicleErrors.vehicle_type && <p className="text-red-500 text-sm mt-1">{vehicleErrors.vehicle_type.message}</p>}
                </div>

                <div id="custom-vehicle-type" style={{ display: 'none' }}>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Custom Vehicle Type</label>
                  <input
                    type="text"
                    {...registerVehicle('custom_vehicle_type')}
                    className="input-field"
                    placeholder="Enter custom vehicle type"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Capacity (Tons) *</label>
                  <input
                    type="number"
                    step="0.1"
                    {...registerVehicle('capacity_tons', { required: 'Capacity is required', min: 0 })}
                    className="input-field"
                    placeholder="20.0"
                  />
                  {vehicleErrors.capacity_tons && <p className="text-red-500 text-sm mt-1">{vehicleErrors.capacity_tons.message}</p>}
                </div>

                <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
                  <button
                    type="button"
                    onClick={() => setShowAddVehicleForm(false)}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn-primary">
                    Add Vehicle
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Add Client Modal */}
      {showAddClientForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl w-full max-w-lg overflow-hidden">
            
            {/* Modal Header */}
            <div className="bg-green-600 px-6 py-4 text-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Plus className="h-6 w-6" />
                  <h2 className="text-xl font-semibold">Add New Client</h2>
                </div>
                <button
                  onClick={() => setShowAddClientForm(false)}
                  className="p-1 hover:bg-green-700 rounded transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            </div>

            {/* Modal Content */}
            <div className="p-6">
              <form onSubmit={handleClientSubmit(onSubmitClient)} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Client Name *</label>
                    <input
                      type="text"
                      {...registerClient('name', { required: 'Client name is required' })}
                      className="input-field"
                      placeholder="e.g., ABC Manufacturing Ltd"
                    />
                    {clientErrors.name && <p className="text-red-500 text-sm mt-1">{clientErrors.name.message}</p>}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Contact Person</label>
                    <input
                      type="text"
                      {...registerClient('contact_person')}
                      className="input-field"
                      placeholder="Contact person name"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                    <input
                      type="text"
                      {...registerClient('phone')}
                      className="input-field"
                      placeholder="+92-300-1234567"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <input
                      type="email"
                      {...registerClient('email')}
                      className="input-field"
                      placeholder="client@example.com"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                  <textarea
                    {...registerClient('address')}
                    className="input-field"
                    rows="2"
                    placeholder="Complete address"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Credit Limit (PKR)</label>
                    <input
                      type="number"
                      step="0.01"
                      {...registerClient('credit_limit')}
                      className="input-field"
                      placeholder="500000"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Payment Terms (Days)</label>
                    <input
                      type="number"
                      {...registerClient('payment_terms')}
                      className="input-field"
                      placeholder="30"
                      defaultValue="30"
                    />
                  </div>
                </div>

                <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
                  <button
                    type="button"
                    onClick={() => setShowAddClientForm(false)}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn-primary">
                    Add Client
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Add Vendor Modal */}
      {showAddVendorForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl w-full max-w-lg overflow-hidden">
            
            {/* Modal Header */}
            <div className="bg-red-600 px-6 py-4 text-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Plus className="h-6 w-6" />
                  <h2 className="text-xl font-semibold">Add New Vendor</h2>
                </div>
                <button
                  onClick={() => setShowAddVendorForm(false)}
                  className="p-1 hover:bg-red-700 rounded transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            </div>

            {/* Modal Content */}
            <div className="p-6">
              <form onSubmit={handleVendorSubmit(onSubmitVendor)} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Vendor Name *</label>
                    <input
                      type="text"
                      {...registerVendor('name', { required: 'Vendor name is required' })}
                      className="input-field"
                      placeholder="e.g., Reliable Transport Services"
                    />
                    {vendorErrors.name && <p className="text-red-500 text-sm mt-1">{vendorErrors.name.message}</p>}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Contact Person</label>
                    <input
                      type="text"
                      {...registerVendor('contact_person')}
                      className="input-field"
                      placeholder="Contact person name"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                    <input
                      type="text"
                      {...registerVendor('phone')}
                      className="input-field"
                      placeholder="+92-300-1234567"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <input
                      type="email"
                      {...registerVendor('email')}
                      className="input-field"
                      placeholder="vendor@example.com"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                  <textarea
                    {...registerVendor('address')}
                    className="input-field"
                    rows="2"
                    placeholder="Complete address"
                  />
                </div>

                <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
                  <button
                    type="button"
                    onClick={() => setShowAddVendorForm(false)}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn-primary">
                    Add Vendor
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Add/Edit User Modal */}
      {showAddUserForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl w-full max-w-lg overflow-hidden">
            
            {/* Modal Header */}
            <div className="bg-blue-600 px-6 py-4 text-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <User className="h-6 w-6" />
                  <h2 className="text-xl font-semibold">{editingUser ? 'Edit User' : 'Add New User'}</h2>
                </div>
                <button
                  onClick={() => {
                    setShowAddUserForm(false);
                    setEditingUser(null);
                    resetUser();
                  }}
                  className="p-1 hover:bg-blue-700 rounded transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            </div>

            {/* Modal Content */}
            <div className="p-6">
              <form onSubmit={handleUserSubmit(onSubmitUser)} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Username *</label>
                    <input
                      type="text"
                      {...registerUser('username', { required: 'Username is required' })}
                      className="input-field"
                      placeholder="e.g., john.doe"
                      disabled={editingUser !== null}
                    />
                    {userErrors.username && <p className="text-red-500 text-sm mt-1">{userErrors.username.message}</p>}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Full Name *</label>
                    <input
                      type="text"
                      {...registerUser('full_name', { required: 'Full name is required' })}
                      className="input-field"
                      placeholder="e.g., John Doe"
                    />
                    {userErrors.full_name && <p className="text-red-500 text-sm mt-1">{userErrors.full_name.message}</p>}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <input
                      type="email"
                      {...registerUser('email')}
                      className="input-field"
                      placeholder="user@example.com"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Role *</label>
                    <select
                      {...registerUser('role', { required: 'Role is required' })}
                      className="input-field"
                    >
                      <option value="">Select Role</option>
                      <option value="admin">Administrator</option>
                      <option value="manager">Manager</option>
                      <option value="supervisor">Supervisor</option>
                    </select>
                    {userErrors.role && <p className="text-red-500 text-sm mt-1">{userErrors.role.message}</p>}
                  </div>
                </div>

                {!editingUser && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Password *</label>
                    <input
                      type="password"
                      {...registerUser('password', { 
                        required: editingUser ? false : 'Password is required',
                        minLength: { value: 6, message: 'Password must be at least 6 characters' }
                      })}
                      className="input-field"
                      placeholder="Minimum 6 characters"
                    />
                    {userErrors.password && <p className="text-red-500 text-sm mt-1">{userErrors.password.message}</p>}
                  </div>
                )}

                {editingUser && (
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      {...registerUser('is_active')}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label className="ml-2 block text-sm text-gray-900">
                      Active User
                    </label>
                  </div>
                )}

                <div className="bg-gray-50 border border-gray-200 rounded-lg p-3">
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Role Permissions:</h4>
                  <ul className="text-xs text-gray-600 space-y-1">
                    <li><strong>Admin:</strong> Full access including profit reports and user management</li>
                    <li><strong>Manager:</strong> Financial reports (no profit), approve payments, staff payroll</li>
                    <li><strong>Supervisor:</strong> Trip entry, fleet operations, basic reports only</li>
                  </ul>
                </div>

                <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
                  <button
                    type="button"
                    onClick={() => {
                      setShowAddUserForm(false);
                      setEditingUser(null);
                      resetUser();
                    }}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn-primary">
                    {editingUser ? 'Update User' : 'Create User'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Settings;