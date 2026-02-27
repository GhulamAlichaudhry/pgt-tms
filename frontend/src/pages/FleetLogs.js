import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import toast from 'react-hot-toast';
import { useAuth } from '../contexts/AuthContext';
import { 
  Plus, 
  Search, 
  Filter,
  TrendingUp,
  DollarSign,
  Calculator,
  MapPin,
  FileText,
  X,
  Download,
  CheckCircle,
  XCircle,
  Eye,
  AlertTriangle
} from 'lucide-react';

const FleetLogs = () => {
  const location = useLocation();
  const { user } = useAuth(); // Get current user for role-based access
  const [trips, setTrips] = useState([]);
  const [vehicles, setVehicles] = useState([]);
  const [clients, setClients] = useState([]);
  const [vendors, setVendors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showAddClient, setShowAddClient] = useState(false);
  const [showAddVendor, setShowAddVendor] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [selectedTripDetails, setSelectedTripDetails] = useState(null);
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [selectedTripToCancel, setSelectedTripToCancel] = useState(null);
  const [cancelReason, setCancelReason] = useState('');
  
  // Filter states - Initialize from navigation state if available
  const [showFilters, setShowFilters] = useState(false);
  const [filterStartDate, setFilterStartDate] = useState('');
  const [filterEndDate, setFilterEndDate] = useState('');
  const [filterClient, setFilterClient] = useState(location.state?.clientId?.toString() || '');
  const [filterVendor, setFilterVendor] = useState(location.state?.vendorId?.toString() || '');
  const [filterStatus, setFilterStatus] = useState(''); // Trip status filter (DRAFT, ACTIVE, COMPLETED, CANCELLED)
  
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    reference_no: '',
    vehicle_id: '',
    category_product: '',
    source_location: '',
    destination_location: '',
    driver_operator: '',
    vendor_client: '',
    
    // SMART SYSTEM: Client and Vendor Selection
    client_id: '',
    vendor_id: '',
    
    // SMART FINANCIAL FIELDS
    freight_mode: 'total',
    total_tonnage: '',    // Total tonnage for all modes
    tonnage: '',          // For per-ton calculation
    rate_per_ton: '',     // Client rate per ton
    vendor_freight: '',   // Amount to pay vendor (lump sum)
    client_freight: '',   // Amount to charge client
    
    // Additional costs
    local_shifting_charges: '0',  // NEW: Local + Shifting charges (added to vendor freight)
    advance_paid: '0',
    fuel_cost: '0',
    munshiyana_bank_charges: '0',
    other_expenses: '0',
    notes: ''
  });

  // Common products list
  const commonProducts = [
    'Lactose',
    'Pumice Stone',
    'Cotton Bales',
    'Soyabeen Meal',
    'Feed',
    'Feed Pallets'
  ];

  const [showCustomProduct, setShowCustomProduct] = useState(false);

  // Client and Vendor form data
  const [clientFormData, setClientFormData] = useState({
    name: '',
    client_code: '',
    contact_person: '',
    phone: '',
    email: '',
    address: ''
  });

  const [vendorFormData, setVendorFormData] = useState({
    name: '',
    vendor_code: '',
    contact_person: '',
    phone: '',
    email: '',
    address: ''
  });

  useEffect(() => {
    fetchTrips();
    fetchVehicles();
    fetchClients();
    fetchVendors();
  }, []);

  // Show filters panel if coming from navigation with filters
  useEffect(() => {
    if (location.state?.clientId || location.state?.vendorId) {
      console.log('Navigation state detected:', location.state);
      console.log('Setting filters - Client:', location.state?.clientId, 'Vendor:', location.state?.vendorId);
      setShowFilters(true);
    }
  }, [location.state]);

  const fetchTrips = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/trips/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setTrips(response.data);
    } catch (error) {
      console.error('Error fetching trips:', error);
      toast.error('Failed to fetch trips');
    } finally {
      setLoading(false);
    }
  };

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
    }
  };

  const exportTripsToExcel = async () => {
    try {
      const token = localStorage.getItem('token');
      
      // Build query parameters from filters
      const params = new URLSearchParams();
      if (filterStartDate) params.append('start_date', filterStartDate);
      if (filterEndDate) params.append('end_date', filterEndDate);
      if (filterClient) params.append('client_id', filterClient);
      if (filterVendor) params.append('vendor_id', filterVendor);
      if (filterStatus) params.append('status', filterStatus);
      
      const queryString = params.toString();
      const url = `/reports/trips-excel${queryString ? `?${queryString}` : ''}`;
      
      const response = await axios.get(url, {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        responseType: 'blob'
      });
      
      // Create blob link to download
      const blobUrl = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = blobUrl;
      
      // Add filter info to filename
      let filename = 'trips_export';
      if (filterStatus) filename += `_${filterStatus}`;
      if (filterStartDate) filename += `_from_${filterStartDate}`;
      if (filterEndDate) filename += `_to_${filterEndDate}`;
      filename += `_${new Date().toISOString().split('T')[0]}.xlsx`;
      
      link.setAttribute('download', filename);
      
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(blobUrl);
      
      toast.success(`Trips data exported successfully!${hasActiveFilters ? ' (Filtered)' : ''}`);
    } catch (error) {
      console.error('Error exporting trips:', error);
      toast.error('Failed to export trips data');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => {
      const newData = {
        ...prev,
        [name]: value
      };
      
      // SMART SYSTEM: Auto-calculate client freight when in per_ton mode
      if (name === 'tonnage' || name === 'rate_per_ton' || name === 'freight_mode') {
        if (newData.freight_mode === 'per_ton' && newData.tonnage && newData.rate_per_ton) {
          // For per-ton mode: Client freight = tonnage × rate_per_ton
          // Vendor freight remains manual (lump sum deal)
          const clientAmount = (parseFloat(newData.tonnage) * parseFloat(newData.rate_per_ton));
          newData.client_freight = clientAmount.toString();
          // Don't auto-calculate vendor_freight - keep it manual for lump sum deals
        }
      }
      
      return newData;
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (submitting) return;
    
    // SMART SYSTEM Validation
    if (!formData.vehicle_id || !formData.category_product || !formData.destination_location || 
        !formData.client_id || !formData.vendor_id || !formData.vendor_freight || !formData.client_freight ||
        !formData.total_tonnage) {
      toast.error('Please fill in all required fields including total tonnage, client, vendor, and freight amounts');
      return;
    }

    // Validate freight amounts
    const vendorFreight = parseFloat(formData.vendor_freight);
    const clientFreight = parseFloat(formData.client_freight);
    
    if (vendorFreight <= 0 || clientFreight <= 0) {
      toast.error('Freight amounts must be greater than zero');
      return;
    }

    if (clientFreight < vendorFreight) {
      const confirmed = window.confirm(
        `Warning: Client freight (${formatCurrency(clientFreight)}) is less than vendor freight (${formatCurrency(vendorFreight)}). This will result in a loss. Continue?`
      );
      if (!confirmed) return;
    }

    setSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      
      const tripData = {
        date: new Date(formData.date).toISOString(),
        reference_no: formData.reference_no || `TRIP-${Date.now()}`,
        vehicle_id: parseInt(formData.vehicle_id),
        category_product: formData.category_product,
        source_location: formData.source_location,
        destination_location: formData.destination_location,
        driver_operator: formData.driver_operator,
        vendor_client: formData.vendor_client,
        
        // SMART SYSTEM: Client and Vendor IDs
        client_id: parseInt(formData.client_id),
        vendor_id: parseInt(formData.vendor_id),
        
        // SMART FINANCIAL FIELDS
        freight_mode: formData.freight_mode,
        total_tonnage: parseFloat(formData.total_tonnage),
        tonnage: formData.tonnage ? parseFloat(formData.tonnage) : null,
        rate_per_ton: formData.rate_per_ton ? parseFloat(formData.rate_per_ton) : null,
        vendor_freight: parseFloat(formData.vendor_freight),
        client_freight: parseFloat(formData.client_freight),
        
        // Additional costs
        local_shifting_charges: parseFloat(formData.local_shifting_charges) || 0,
        advance_paid: parseFloat(formData.advance_paid) || 0,
        fuel_cost: parseFloat(formData.fuel_cost) || 0,
        munshiyana_bank_charges: parseFloat(formData.munshiyana_bank_charges) || 0,
        other_expenses: parseFloat(formData.other_expenses) || 0,
        notes: formData.notes
      };

      console.log('Sending SMART trip data:', tripData);

      const response = await axios.post('/trips/', tripData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      const createdTrip = response.data;
      const profit = createdTrip.gross_profit || (clientFreight - vendorFreight);
      
      toast.success(
        `🚀 SMART Trip created successfully!\n` +
        `💰 Profit: ${formatCurrency(profit)}\n` +
        `📋 Receivable & Payable auto-created!`,
        { duration: 5000 }
      );
      
      setShowAddForm(false);
      resetForm();
      fetchTrips();
    } catch (error) {
      console.error('Error adding trip:', error);
      console.error('Error response:', error.response);
      toast.error('Failed to add trip. Please check all fields.');
    } finally {
      setSubmitting(false);
    }
  };

  const resetForm = () => {
    setFormData({
      date: new Date().toISOString().split('T')[0],
      reference_no: '',
      vehicle_id: '',
      category_product: '',
      source_location: '',
      destination_location: '',
      driver_operator: '',
      vendor_client: '',
      client_id: '',
      vendor_id: '',
      freight_mode: 'total',
      total_tonnage: '',
      tonnage: '',
      rate_per_ton: '',
      vendor_freight: '',
      client_freight: '',
      local_shifting_charges: '0',
      advance_paid: '0',
      fuel_cost: '0',
      munshiyana_bank_charges: '0',
      other_expenses: '0',
      notes: ''
    });
    setShowCustomProduct(false);
  };

  const handleClientSubmit = async (e) => {
    e.preventDefault();
    
    if (!clientFormData.name) {
      toast.error('Client name is required');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/clients/', clientFormData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      const newClient = response.data;
      setClients(prev => [...prev, newClient]);
      setFormData(prev => ({ ...prev, client_id: newClient.id.toString() }));
      setShowAddClient(false);
      setClientFormData({
        name: '',
        client_code: '',
        contact_person: '',
        phone: '',
        email: '',
        address: ''
      });
      toast.success(`Client "${newClient.name}" added successfully!`);
    } catch (error) {
      console.error('Error adding client:', error);
      toast.error('Failed to add client');
    }
  };

  const handleVendorSubmit = async (e) => {
    e.preventDefault();
    
    if (!vendorFormData.name) {
      toast.error('Vendor name is required');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/vendors/', vendorFormData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      const newVendor = response.data;
      setVendors(prev => [...prev, newVendor]);
      setFormData(prev => ({ ...prev, vendor_id: newVendor.id.toString() }));
      setShowAddVendor(false);
      setVendorFormData({
        name: '',
        vendor_code: '',
        contact_person: '',
        phone: '',
        email: '',
        address: ''
      });
      toast.success(`Vendor "${newVendor.name}" added successfully!`);
    } catch (error) {
      console.error('Error adding vendor:', error);
      toast.error('Failed to add vendor');
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-PK', {
      style: 'currency',
      currency: 'PKR',
      minimumFractionDigits: 0,
    }).format(amount || 0);
  };

  // SMART SYSTEM: Calculate profit and net amounts
  const calculateGrossProfit = () => {
    const clientFreight = parseFloat(formData.client_freight) || 0;
    const vendorFreight = parseFloat(formData.vendor_freight) || 0;
    const localShifting = parseFloat(formData.local_shifting_charges) || 0;
    // Total vendor cost = vendor_freight + local_shifting_charges
    return clientFreight - (vendorFreight + localShifting);
  };

  const calculateNetProfit = () => {
    const grossProfit = calculateGrossProfit();
    const advance = parseFloat(formData.advance_paid) || 0;
    const fuel = parseFloat(formData.fuel_cost) || 0;
    const munshiyana = parseFloat(formData.munshiyana_bank_charges) || 0;
    const other = parseFloat(formData.other_expenses) || 0;
    return grossProfit - (advance + fuel + munshiyana + other);
  };

  const calculateProfitMargin = () => {
    const clientFreight = parseFloat(formData.client_freight) || 0;
    const netProfit = calculateNetProfit();
    return clientFreight > 0 ? (netProfit / clientFreight * 100) : 0;
  };

  // Filter trips based on selected filters
  const filteredTrips = trips.filter(trip => {
    // Date filter
    if (filterStartDate && new Date(trip.date) < new Date(filterStartDate)) return false;
    if (filterEndDate && new Date(trip.date) > new Date(filterEndDate)) return false;
    
    // Client filter - handle both string and number comparison
    if (filterClient) {
      const clientMatch = trip.client_id === parseInt(filterClient) || 
                         trip.client_id?.toString() === filterClient;
      if (!clientMatch) return false;
    }
    
    // Vendor filter - handle both string and number comparison
    if (filterVendor) {
      const vendorMatch = trip.vendor_id === parseInt(filterVendor) || 
                         trip.vendor_id?.toString() === filterVendor;
      if (!vendorMatch) return false;
    }
    
    // Status filter - handle both uppercase and lowercase
    if (filterStatus) {
      const tripStatus = (trip.status || '').toUpperCase();
      if (tripStatus !== filterStatus) return false;
    }
    
    return true;
  });

  const clearFilters = () => {
    setFilterStartDate('');
    setFilterEndDate('');
    setFilterClient('');
    setFilterVendor('');
    setFilterStatus('');
    toast.success('Filters cleared');
  };

  const handleViewDetails = (trip) => {
    setSelectedTripDetails(trip);
    setShowDetailsModal(true);
  };

  const handleCompleteTrip = async (trip) => {
    const confirmed = window.confirm(
      `Mark trip ${trip.reference_no} as COMPLETED?\n\n` +
      `This will lock the financial values and prevent further changes.`
    );
    
    if (!confirmed) return;

    try {
      const token = localStorage.getItem('token');
      await axios.put(`/trips/${trip.id}/status`, 
        { status: 'COMPLETED' },
        { headers: { 'Authorization': `Bearer ${token}` } }
      );
      
      toast.success(`Trip ${trip.reference_no} marked as completed!`);
      fetchTrips();
    } catch (error) {
      console.error('Error completing trip:', error);
      toast.error('Failed to complete trip');
    }
  };

  const handleCancelTripModal = (trip) => {
    setSelectedTripToCancel(trip);
    setShowCancelModal(true);
    setCancelReason('');
  };

  const handleCancelTrip = async () => {
    if (!cancelReason.trim()) {
      toast.error('Please provide a cancellation reason');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      await axios.put(`/trips/${selectedTripToCancel.id}/cancel`, 
        { reason: cancelReason },
        { headers: { 'Authorization': `Bearer ${token}` } }
      );
      
      toast.success(
        `Trip ${selectedTripToCancel.reference_no} cancelled!\n` +
        `Financial records have been reversed.`,
        { duration: 5000 }
      );
      setShowCancelModal(false);
      setSelectedTripToCancel(null);
      setCancelReason('');
      fetchTrips();
    } catch (error) {
      console.error('Error cancelling trip:', error);
      toast.error('Failed to cancel trip');
    }
  };

  const hasActiveFilters = filterStartDate || filterEndDate || filterClient || filterVendor || filterStatus;

  // Debug logging for filters
  useEffect(() => {
    console.log('Filter state:', { filterClient, filterVendor, filterStatus, filterStartDate, filterEndDate });
    console.log('Total trips:', trips.length, 'Filtered trips:', filteredTrips.length);
    if (trips.length > 0 && filteredTrips.length === 0 && (filterClient || filterVendor)) {
      console.log('No trips match filters. Sample trip:', trips[0]);
    }
  }, [trips, filteredTrips.length, filterClient, filterVendor]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Fleet Operations</h1>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`btn-secondary flex items-center ${hasActiveFilters ? 'bg-blue-100 border-blue-300' : ''}`}
            title="Filter trips"
          >
            <Filter className="h-5 w-5 mr-2" />
            Filters {hasActiveFilters && '✓'}
          </button>
          <button
            onClick={exportTripsToExcel}
            className="btn-secondary flex items-center"
            title="Export to Excel"
          >
            <Download className="h-5 w-5 mr-2" />
            Export Excel
          </button>
          <button
            onClick={() => setShowAddForm(true)}
            className="btn-primary flex items-center"
          >
            <Plus className="h-5 w-5 mr-2" />
            Add Operation
          </button>
        </div>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <div className="glass-card rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <Filter className="h-5 w-5 mr-2 text-red-600" />
              Filter Trips
            </h3>
            <button
              onClick={() => setShowFilters(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
              <input
                type="date"
                value={filterStartDate}
                onChange={(e) => setFilterStartDate(e.target.value)}
                className="input-field"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
              <input
                type="date"
                value={filterEndDate}
                onChange={(e) => setFilterEndDate(e.target.value)}
                className="input-field"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Client</label>
              <select
                value={filterClient}
                onChange={(e) => setFilterClient(e.target.value)}
                className="input-field"
              >
                <option value="">All Clients</option>
                {clients.map(client => (
                  <option key={client.id} value={client.id}>{client.name}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Vendor</label>
              <select
                value={filterVendor}
                onChange={(e) => setFilterVendor(e.target.value)}
                className="input-field"
              >
                <option value="">All Vendors</option>
                {vendors.map(vendor => (
                  <option key={vendor.id} value={vendor.id}>{vendor.name}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="input-field"
              >
                <option value="">All Status</option>
                <option value="DRAFT">Draft</option>
                <option value="ACTIVE">Active / In Progress</option>
                <option value="COMPLETED">Completed</option>
                <option value="LOCKED">Locked</option>
                <option value="CANCELLED">Cancelled</option>
              </select>
            </div>
          </div>
          
          <div className="mt-4 flex justify-end space-x-2">
            <button
              onClick={clearFilters}
              className="btn-secondary"
            >
              Clear All
            </button>
            <button
              onClick={() => setShowFilters(false)}
              className="btn-primary"
            >
              Apply Filters
            </button>
          </div>
          
          {hasActiveFilters && (
            <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-blue-800">
                <strong>Showing {filteredTrips.length} of {trips.length} trips</strong>
                {filterStartDate && ` | From: ${filterStartDate}`}
                {filterEndDate && ` | To: ${filterEndDate}`}
                {filterClient && ` | Client: ${clients.find(c => c.id === parseInt(filterClient))?.name}`}
                {filterVendor && ` | Vendor: ${vendors.find(v => v.id === parseInt(filterVendor))?.name}`}
                {filterStatus && ` | Status: ${filterStatus}`}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card rounded-xl p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Operations</p>
              <p className="text-2xl font-bold text-gray-900">{filteredTrips.length}</p>
              <p className="text-xs text-gray-500">{hasActiveFilters ? 'Filtered' : 'All recorded'} operations</p>
            </div>
            <div className="p-3 bg-red-100 rounded-lg">
              <FileText className="h-6 w-6 text-red-600" />
            </div>
          </div>
        </div>
        
        <div className="glass-card rounded-xl p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Client Revenue</p>
              <p className="text-2xl font-bold text-green-600">
                {formatCurrency(filteredTrips
                  .filter(trip => (trip.status || '').toUpperCase() !== 'CANCELLED')
                  .reduce((sum, trip) => sum + (trip.client_freight || 0), 0))}
              </p>
              <p className="text-xs text-gray-500">Amount charged to clients (excl. cancelled)</p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
          </div>
        </div>
        
        <div className="glass-card rounded-xl p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Company Profit</p>
              <p className="text-2xl font-bold text-red-600">
                {formatCurrency(filteredTrips
                  .filter(trip => (trip.status || '').toUpperCase() !== 'CANCELLED')
                  .reduce((sum, trip) => sum + (trip.gross_profit || 0), 0))}
              </p>
              <p className="text-xs text-gray-500">Client freight - Vendor freight (excl. cancelled)</p>
            </div>
            <div className="p-3 bg-red-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-red-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Add Trip Modal */}
      {showAddForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl w-full max-w-4xl max-h-[90vh] overflow-hidden">
            
            {/* Modal Header */}
            <div className="bg-red-600 px-6 py-4 text-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Plus className="h-6 w-6" />
                  <h2 className="text-xl font-semibold">Add New Operation</h2>
                </div>
                <button
                  onClick={() => setShowAddForm(false)}
                  className="p-1 hover:bg-red-700 rounded transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            </div>

            {/* Modal Content */}
            <div className="p-6 overflow-y-auto max-h-[calc(90vh-80px)]">
              <form onSubmit={handleSubmit} className="space-y-6">
                
                {/* Basic Information */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                    <FileText className="h-5 w-5 text-red-600" />
                    Basic Information
                  </h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Date *</label>
                      <input
                        type="date"
                        name="date"
                        value={formData.date}
                        onChange={handleInputChange}
                        required
                        className="input-field"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Reference No</label>
                      <input
                        type="text"
                        name="reference_no"
                        value={formData.reference_no}
                        onChange={handleInputChange}
                        placeholder="Auto-generated if empty"
                        className="input-field"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Vehicle *</label>
                      <select
                        name="vehicle_id"
                        value={formData.vehicle_id}
                        onChange={handleInputChange}
                        required
                        className="input-field"
                      >
                        <option value="">Select Vehicle</option>
                        {vehicles.map(vehicle => (
                          <option key={vehicle.id} value={vehicle.id}>
                            {vehicle.vehicle_no} - {vehicle.vehicle_type}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>

                {/* Trip Details */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                    <MapPin className="h-5 w-5 text-red-600" />
                    Trip Details
                  </h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Category/Product *</label>
                      <select
                        name="category_product"
                        value={showCustomProduct ? 'Custom' : formData.category_product}
                        onChange={(e) => {
                          if (e.target.value === 'Custom') {
                            setShowCustomProduct(true);
                            setFormData({ ...formData, category_product: '' });
                          } else {
                            setShowCustomProduct(false);
                            setFormData({ ...formData, category_product: e.target.value });
                          }
                        }}
                        required={!showCustomProduct}
                        className="input-field"
                      >
                        <option value="">Select Product</option>
                        {commonProducts.map((product) => (
                          <option key={product} value={product}>{product}</option>
                        ))}
                        <option value="Custom">Custom (Enter Manually)</option>
                      </select>
                      
                      {showCustomProduct && (
                        <input
                          type="text"
                          name="category_product"
                          value={formData.category_product}
                          onChange={handleInputChange}
                          required
                          placeholder="Enter custom product name"
                          className="input-field mt-2"
                        />
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Total Tonnage *</label>
                      <input
                        type="number"
                        step="0.01"
                        name="total_tonnage"
                        value={formData.total_tonnage}
                        onChange={handleInputChange}
                        required
                        placeholder="Total weight in tons"
                        className="input-field"
                      />
                      <p className="text-xs text-gray-500 mt-1">Total cargo weight for this trip</p>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Destination *</label>
                      <input
                        type="text"
                        name="destination_location"
                        value={formData.destination_location}
                        onChange={handleInputChange}
                        required
                        placeholder="Destination"
                        className="input-field"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Source Location</label>
                      <input
                        type="text"
                        name="source_location"
                        value={formData.source_location}
                        onChange={handleInputChange}
                        placeholder="Origin"
                        className="input-field"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Driver/Operator</label>
                      <input
                        type="text"
                        name="driver_operator"
                        value={formData.driver_operator}
                        onChange={handleInputChange}
                        placeholder="Driver or operator name"
                        className="input-field"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Vendor/Client (Legacy)</label>
                    <input
                      type="text"
                      name="vendor_client"
                      value={formData.vendor_client}
                      onChange={handleInputChange}
                      placeholder="Optional legacy field"
                      className="input-field"
                    />
                  </div>
                </div>

                {/* SMART SYSTEM: Client and Vendor Selection */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                    <DollarSign className="h-5 w-5 text-red-600" />
                    SMART System: Client & Vendor
                  </h3>
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                    <p className="text-sm text-blue-800">
                      <strong>🚀 One-Time Entry:</strong> Select client and vendor to automatically create receivable and payable records.
                    </p>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Client (Who Pays Us) *</label>
                      <div className="flex gap-2">
                        <select
                          name="client_id"
                          value={formData.client_id}
                          onChange={handleInputChange}
                          required
                          className="input-field flex-1"
                        >
                          <option value="">Select Client</option>
                          {clients.map(client => (
                            <option key={client.id} value={client.id}>
                              {client.name} {client.client_code ? `(${client.client_code})` : ''}
                            </option>
                          ))}
                        </select>
                        <button
                          type="button"
                          onClick={() => setShowAddClient(true)}
                          className="px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm"
                          title="Add New Client"
                        >
                          + Add
                        </button>
                      </div>
                      <p className="text-xs text-gray-500 mt-1">Receivable will be auto-created</p>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Vendor (Who We Pay) *</label>
                      <div className="flex gap-2">
                        <select
                          name="vendor_id"
                          value={formData.vendor_id}
                          onChange={handleInputChange}
                          required
                          className="input-field flex-1"
                        >
                          <option value="">Select Vendor</option>
                          {vendors.map(vendor => (
                            <option key={vendor.id} value={vendor.id}>
                              {vendor.name} {vendor.vendor_code ? `(${vendor.vendor_code})` : ''}
                            </option>
                          ))}
                        </select>
                        <button
                          type="button"
                          onClick={() => setShowAddVendor(true)}
                          className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
                          title="Add New Vendor"
                        >
                          + Add
                        </button>
                      </div>
                      <p className="text-xs text-gray-500 mt-1">Payable will be auto-created</p>
                    </div>
                  </div>
                </div>

                {/* SMART Freight Calculation */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                    <Calculator className="h-5 w-5 text-red-600" />
                    SMART Freight Calculation
                  </h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <label className="flex items-center p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50">
                      <input
                        type="radio"
                        name="freight_mode"
                        value="total"
                        checked={formData.freight_mode === 'total'}
                        onChange={handleInputChange}
                        className="mr-3"
                      />
                      <div>
                        <span className="font-medium text-gray-900">Total Amount</span>
                        <p className="text-sm text-gray-600">Manual entry</p>
                      </div>
                    </label>
                    
                    <label className="flex items-center p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50">
                      <input
                        type="radio"
                        name="freight_mode"
                        value="per_ton"
                        checked={formData.freight_mode === 'per_ton'}
                        onChange={handleInputChange}
                        className="mr-3"
                      />
                      <div>
                        <span className="font-medium text-gray-900">Per Ton Calculation</span>
                        <p className="text-sm text-gray-600">Auto-calculated</p>
                      </div>
                    </label>
                  </div>

                  {formData.freight_mode === 'per_ton' && (
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="mb-4">
                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                          <p className="text-sm text-blue-800">
                            <strong>💡 Per-Ton Mode:</strong> Enter tonnage and client rate per ton. Client freight will be auto-calculated. 
                            Vendor freight remains manual (lump sum deal).
                          </p>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Tonnage for Rate Calculation *</label>
                          <input
                            type="number"
                            step="0.01"
                            name="tonnage"
                            value={formData.tonnage}
                            onChange={handleInputChange}
                            required={formData.freight_mode === 'per_ton'}
                            placeholder="Tonnage for client billing"
                            className="input-field"
                          />
                          <p className="text-xs text-gray-500 mt-1">May differ from total tonnage</p>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Client Rate per Ton (PKR) *</label>
                          <input
                            type="number"
                            step="0.01"
                            name="rate_per_ton"
                            value={formData.rate_per_ton}
                            onChange={handleInputChange}
                            required={formData.freight_mode === 'per_ton'}
                            placeholder="Rate charged to client"
                            className="input-field"
                          />
                          <p className="text-xs text-gray-500 mt-1">Per ton rate for client</p>
                        </div>
                      </div>

                      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                          <span className="text-sm font-medium text-gray-600">Auto-Calculated Client Freight:</span>
                          <div className="text-lg font-bold text-green-700">
                            {formData.tonnage && formData.rate_per_ton 
                              ? formatCurrency(parseFloat(formData.tonnage) * parseFloat(formData.rate_per_ton))
                              : 'PKR 0'
                            }
                          </div>
                          <p className="text-xs text-gray-500">
                            {formData.tonnage && formData.rate_per_ton 
                              ? `${formData.tonnage} tons × ${formatCurrency(formData.rate_per_ton)}/ton`
                              : 'Enter tonnage and rate'
                            }
                          </p>
                        </div>
                        
                        <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                          <span className="text-sm font-medium text-gray-600">Vendor Freight (Manual):</span>
                          <div className="text-lg font-bold text-red-700">
                            {formData.vendor_freight ? formatCurrency(formData.vendor_freight) : 'Enter below'}
                          </div>
                          <p className="text-xs text-gray-500">Lump sum deal with vendor</p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* SMART Financial Details */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                    <DollarSign className="h-5 w-5 text-red-600" />
                    SMART Financial Details
                  </h3>
                  
                  {/* Core Freight Amounts */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Vendor Freight (PKR) *
                        {formData.freight_mode === 'per_ton' && (
                          <span className="text-blue-600 text-xs ml-1">(Lump Sum Deal)</span>
                        )}
                      </label>
                      <input
                        type="number"
                        step="0.01"
                        name="vendor_freight"
                        value={formData.vendor_freight}
                        onChange={handleInputChange}
                        required
                        placeholder={formData.freight_mode === 'per_ton' 
                          ? "Lump sum amount for vendor (e.g., 180,000)" 
                          : "Amount to pay vendor (e.g., 30,000)"
                        }
                        className="input-field"
                      />
                      <p className="text-xs text-gray-500 mt-1">
                        {formData.freight_mode === 'per_ton' 
                          ? "Fixed lump sum deal with vendor" 
                          : "Amount company pays to vendor"
                        }
                      </p>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Client Freight (PKR) *
                        {formData.freight_mode === 'per_ton' && (
                          <span className="text-green-600 text-xs ml-1">(Auto-calculated)</span>
                        )}
                      </label>
                      <input
                        type="number"
                        step="0.01"
                        name="client_freight"
                        value={formData.client_freight}
                        onChange={handleInputChange}
                        required
                        readOnly={formData.freight_mode === 'per_ton'}
                        placeholder={formData.freight_mode === 'per_ton' 
                          ? "Auto-calculated from tonnage × rate" 
                          : "Amount to charge client (e.g., 40,000)"
                        }
                        className={`input-field ${
                          formData.freight_mode === 'per_ton' 
                            ? 'bg-gray-100 cursor-not-allowed' 
                            : ''
                        }`}
                      />
                      <p className="text-xs text-gray-500 mt-1">
                        {formData.freight_mode === 'per_ton' 
                          ? "Calculated from tonnage × client rate per ton" 
                          : "Amount client pays to company"
                        }
                      </p>
                    </div>
                  </div>

                  {/* Additional Costs */}
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Local + Shifting Charges</label>
                      <input
                        type="number"
                        step="0.01"
                        name="local_shifting_charges"
                        value={formData.local_shifting_charges}
                        onChange={handleInputChange}
                        placeholder="0.00"
                        className="input-field"
                      />
                      <p className="text-xs text-gray-500 mt-1">Added to vendor freight</p>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Advance Paid</label>
                      <input
                        type="number"
                        step="0.01"
                        name="advance_paid"
                        value={formData.advance_paid}
                        onChange={handleInputChange}
                        placeholder="0.00"
                        className="input-field"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Fuel Cost</label>
                      <input
                        type="number"
                        step="0.01"
                        name="fuel_cost"
                        value={formData.fuel_cost}
                        onChange={handleInputChange}
                        placeholder="0.00"
                        className="input-field"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Munshiyana & Bank Charges</label>
                      <input
                        type="number"
                        step="0.01"
                        name="munshiyana_bank_charges"
                        value={formData.munshiyana_bank_charges}
                        onChange={handleInputChange}
                        placeholder="0.00"
                        className="input-field"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-1 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Other Expenses</label>
                      <input
                        type="number"
                        step="0.01"
                        name="other_expenses"
                        value={formData.other_expenses}
                        onChange={handleInputChange}
                        placeholder="0.00"
                        className="input-field"
                      />
                    </div>
                  </div>

                  {/* SMART Profit Display */}
                  <div className="bg-gradient-to-r from-green-50 to-red-50 border border-gray-200 rounded-lg p-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="text-center">
                        <span className="block text-sm font-medium text-gray-600">Gross Profit</span>
                        <span className="text-lg font-bold text-green-600">
                          {formatCurrency(calculateGrossProfit())}
                        </span>
                        <p className="text-xs text-gray-500">Client - (Vendor + Local/Shifting)</p>
                      </div>
                      <div className="text-center">
                        <span className="block text-sm font-medium text-gray-600">Net Profit</span>
                        <span className="text-lg font-bold text-red-600">
                          {formatCurrency(calculateNetProfit())}
                        </span>
                        <p className="text-xs text-gray-500">After all expenses</p>
                      </div>
                      <div className="text-center">
                        <span className="block text-sm font-medium text-gray-600">Profit Margin</span>
                        <span className="text-lg font-bold text-blue-600">
                          {calculateProfitMargin().toFixed(2)}%
                        </span>
                        <p className="text-xs text-gray-500">Net profit / Client freight</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Notes */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Notes</label>
                  <textarea
                    name="notes"
                    value={formData.notes}
                    onChange={handleInputChange}
                    rows="3"
                    placeholder="Add any additional notes..."
                    className="input-field resize-none"
                  />
                </div>

                {/* Action Buttons */}
                <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
                  <button
                    type="button"
                    onClick={() => setShowAddForm(false)}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={submitting}
                    className="btn-primary"
                  >
                    {submitting ? 'Adding...' : 'Add Operation'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Operations Table */}
      <div className="glass-card rounded-xl overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">Operations Records</h3>
            <div className="flex items-center gap-3">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <input
                  type="text"
                  placeholder="Search operations..."
                  className="pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-red-500 focus:border-transparent"
                />
              </div>
              <button className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                <Filter className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
        
        {filteredTrips.length === 0 ? (
          <div className="p-12 text-center">
            <div className="w-16 h-16 mx-auto mb-4 bg-red-100 rounded-full flex items-center justify-center">
              <FileText className="h-8 w-8 text-red-600" />
            </div>
            <h4 className="text-lg font-semibold text-gray-900 mb-2">
              {hasActiveFilters ? 'No trips match your filters' : 'No operations found'}
            </h4>
            <p className="text-gray-600 mb-4">
              {hasActiveFilters ? 'Try adjusting your filter criteria' : 'Get started by adding your first operation'}
            </p>
            {hasActiveFilters ? (
              <button
                onClick={clearFilters}
                className="btn-secondary"
              >
                Clear Filters
              </button>
            ) : (
              <button
                onClick={() => setShowAddForm(true)}
                className="btn-primary"
              >
                Add Your First Operation
              </button>
            )}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reference</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tonnage</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Route</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Client → Vendor</th>
                  {/* DIRECTOR'S IRON WALL: Hide freight from Supervisor */}
                  {user?.role !== 'supervisor' && (
                    <>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Client Freight</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vendor Freight</th>
                    </>
                  )}
                  {/* DIRECTOR'S IRON WALL: Profit columns ONLY for Admin */}
                  {user?.role === 'admin' && (
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Profit</th>
                  )}
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredTrips.map((trip, index) => (
                  <tr key={trip.id || index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {new Date(trip.date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                        {trip.reference_no}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {trip.category_product}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      <div className="text-center">
                        <div className="font-semibold text-blue-600">
                          {trip.total_tonnage ? `${trip.total_tonnage} tons` : 'N/A'}
                        </div>
                        {trip.freight_mode === 'per_ton' && trip.tonnage && (
                          <div className="text-xs text-gray-500">
                            Rate: {trip.tonnage} tons
                          </div>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      <div className="flex items-center">
                        <MapPin className="h-4 w-4 text-gray-400 mr-1" />
                        {trip.source_location || 'N/A'} → {trip.destination_location}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="space-y-1">
                        <div className="text-green-600 font-medium">
                          {trip.client_name || 'N/A'}
                        </div>
                        <div className="text-red-600 text-xs">
                          → {trip.vendor_name || 'N/A'}
                        </div>
                      </div>
                    </td>
                    {/* DIRECTOR'S IRON WALL: Hide freight from Supervisor */}
                    {user?.role !== 'supervisor' && (
                      <>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-green-600">
                          {formatCurrency(trip.client_freight || 0)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-red-600">
                          {formatCurrency(trip.vendor_freight || 0)}
                        </td>
                      </>
                    )}
                    {/* DIRECTOR'S IRON WALL: Profit column ONLY for Admin */}
                    {user?.role === 'admin' && (
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold">
                        <div className="space-y-1">
                          <div className={`${(trip.gross_profit || 0) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            {formatCurrency(trip.gross_profit || 0)}
                          </div>
                          <div className="text-xs text-gray-500">
                            {((trip.gross_profit || 0) / (trip.client_freight || 1) * 100).toFixed(1)}%
                          </div>
                        </div>
                      </td>
                    )}
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="space-y-1">
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          (trip.status === 'COMPLETED' || trip.status === 'completed' || trip.status === 'LOCKED' || trip.status === 'locked')
                            ? 'bg-green-100 text-green-800'
                            : (trip.status === 'CANCELLED' || trip.status === 'cancelled')
                            ? 'bg-red-100 text-red-800'
                            : (trip.status === 'ACTIVE' || trip.status === 'active')
                            ? 'bg-blue-100 text-blue-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {(trip.status === 'COMPLETED' || trip.status === 'completed') ? '✅ Completed' :
                           (trip.status === 'LOCKED' || trip.status === 'locked') ? '🔒 Locked' :
                           (trip.status === 'CANCELLED' || trip.status === 'cancelled') ? '❌ Cancelled' :
                           (trip.status === 'ACTIVE' || trip.status === 'active') ? '🚛 Active' :
                           '📝 Draft'}
                        </span>
                        <div className="text-xs text-gray-500">
                          R: {trip.receivable_created ? '✅' : '❌'} | P: {trip.payable_created ? '✅' : '❌'}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex items-center space-x-2">
                        {/* View Details Button */}
                        <button 
                          onClick={() => handleViewDetails(trip)}
                          className="p-2 rounded-lg text-blue-600 hover:bg-blue-50 hover:text-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200"
                          title="View Details"
                        >
                          <Eye className="h-5 w-5" />
                        </button>
                        
                        {/* Complete Trip Button - for DRAFT or ACTIVE status */}
                        {(trip.status === 'DRAFT' || trip.status === 'draft' || trip.status === 'ACTIVE' || trip.status === 'active') && (
                          <button 
                            onClick={() => handleCompleteTrip(trip)}
                            className="p-2 rounded-lg text-green-600 hover:bg-green-50 hover:text-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 transition-all duration-200"
                            title="Mark as Completed"
                          >
                            <CheckCircle className="h-5 w-5" />
                          </button>
                        )}
                        
                        {/* Cancel Trip Button - for DRAFT or ACTIVE status */}
                        {(trip.status === 'DRAFT' || trip.status === 'draft' || trip.status === 'ACTIVE' || trip.status === 'active') && (
                          <button 
                            onClick={() => handleCancelTripModal(trip)}
                            className="p-2 rounded-lg text-red-600 hover:bg-red-50 hover:text-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all duration-200"
                            title="Cancel Trip"
                          >
                            <XCircle className="h-5 w-5" />
                          </button>
                        )}
                        
                        {/* Status Indicator for Completed/Locked/Cancelled */}
                        {(trip.status === 'COMPLETED' || trip.status === 'completed' || trip.status === 'LOCKED' || trip.status === 'locked' || trip.status === 'CANCELLED' || trip.status === 'cancelled') && (
                          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                            {(trip.status === 'CANCELLED' || trip.status === 'cancelled') ? '❌ Cancelled' : '✅ Completed'}
                          </span>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Add Client Modal */}
      {showAddClient && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl w-full max-w-md">
            <div className="bg-green-600 px-6 py-4 text-white rounded-t-xl">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">Add New Client</h2>
                <button
                  onClick={() => setShowAddClient(false)}
                  className="p-1 hover:bg-green-700 rounded transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            </div>
            
            <div className="p-6">
              <form onSubmit={handleClientSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Client Name *</label>
                  <input
                    type="text"
                    value={clientFormData.name}
                    onChange={(e) => setClientFormData(prev => ({ ...prev, name: e.target.value }))}
                    required
                    placeholder="Enter client name"
                    className="input-field"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Client Code</label>
                  <input
                    type="text"
                    value={clientFormData.client_code}
                    onChange={(e) => setClientFormData(prev => ({ ...prev, client_code: e.target.value }))}
                    placeholder="Optional client code"
                    className="input-field"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Contact Person</label>
                    <input
                      type="text"
                      value={clientFormData.contact_person}
                      onChange={(e) => setClientFormData(prev => ({ ...prev, contact_person: e.target.value }))}
                      placeholder="Contact person name"
                      className="input-field"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                    <input
                      type="tel"
                      value={clientFormData.phone}
                      onChange={(e) => setClientFormData(prev => ({ ...prev, phone: e.target.value }))}
                      placeholder="Phone number"
                      className="input-field"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    type="email"
                    value={clientFormData.email}
                    onChange={(e) => setClientFormData(prev => ({ ...prev, email: e.target.value }))}
                    placeholder="Email address"
                    className="input-field"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                  <textarea
                    value={clientFormData.address}
                    onChange={(e) => setClientFormData(prev => ({ ...prev, address: e.target.value }))}
                    placeholder="Client address"
                    rows="2"
                    className="input-field resize-none"
                  />
                </div>

                <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
                  <button
                    type="button"
                    onClick={() => setShowAddClient(false)}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="btn-primary bg-green-600 hover:bg-green-700"
                  >
                    Add Client
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Add Vendor Modal */}
      {showAddVendor && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl w-full max-w-md">
            <div className="bg-blue-600 px-6 py-4 text-white rounded-t-xl">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">Add New Vendor</h2>
                <button
                  onClick={() => setShowAddVendor(false)}
                  className="p-1 hover:bg-blue-700 rounded transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            </div>
            
            <div className="p-6">
              <form onSubmit={handleVendorSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Vendor Name *</label>
                  <input
                    type="text"
                    value={vendorFormData.name}
                    onChange={(e) => setVendorFormData(prev => ({ ...prev, name: e.target.value }))}
                    required
                    placeholder="Enter vendor name"
                    className="input-field"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Vendor Code</label>
                  <input
                    type="text"
                    value={vendorFormData.vendor_code}
                    onChange={(e) => setVendorFormData(prev => ({ ...prev, vendor_code: e.target.value }))}
                    placeholder="Optional vendor code"
                    className="input-field"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Contact Person</label>
                    <input
                      type="text"
                      value={vendorFormData.contact_person}
                      onChange={(e) => setVendorFormData(prev => ({ ...prev, contact_person: e.target.value }))}
                      placeholder="Contact person name"
                      className="input-field"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                    <input
                      type="tel"
                      value={vendorFormData.phone}
                      onChange={(e) => setVendorFormData(prev => ({ ...prev, phone: e.target.value }))}
                      placeholder="Phone number"
                      className="input-field"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    type="email"
                    value={vendorFormData.email}
                    onChange={(e) => setVendorFormData(prev => ({ ...prev, email: e.target.value }))}
                    placeholder="Email address"
                    className="input-field"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                  <textarea
                    value={vendorFormData.address}
                    onChange={(e) => setVendorFormData(prev => ({ ...prev, address: e.target.value }))}
                    placeholder="Vendor address"
                    rows="2"
                    className="input-field resize-none"
                  />
                </div>

                <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
                  <button
                    type="button"
                    onClick={() => setShowAddVendor(false)}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="btn-primary bg-blue-600 hover:bg-blue-700"
                  >
                    Add Vendor
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Trip Details Modal */}
      {showDetailsModal && selectedTripDetails && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-semibold text-gray-900">Trip Details</h2>
              <button
                onClick={() => {
                  setShowDetailsModal(false);
                  setSelectedTripDetails(null);
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            <div className="space-y-6">
              {/* Status Banner */}
              <div className={`p-4 rounded-lg ${
                (selectedTripDetails.status === 'COMPLETED' || selectedTripDetails.status === 'completed' || selectedTripDetails.status === 'LOCKED' || selectedTripDetails.status === 'locked')
                  ? 'bg-green-50 border border-green-200'
                  : (selectedTripDetails.status === 'CANCELLED' || selectedTripDetails.status === 'cancelled')
                  ? 'bg-red-50 border border-red-200'
                  : (selectedTripDetails.status === 'ACTIVE' || selectedTripDetails.status === 'active')
                  ? 'bg-blue-50 border border-blue-200'
                  : 'bg-yellow-50 border border-yellow-200'
              }`}>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {selectedTripDetails.reference_no}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {selectedTripDetails.category_product} - {selectedTripDetails.total_tonnage} tons
                    </p>
                  </div>
                  <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                    (selectedTripDetails.status === 'COMPLETED' || selectedTripDetails.status === 'completed' || selectedTripDetails.status === 'LOCKED' || selectedTripDetails.status === 'locked')
                      ? 'bg-green-100 text-green-800'
                      : (selectedTripDetails.status === 'CANCELLED' || selectedTripDetails.status === 'cancelled')
                      ? 'bg-red-100 text-red-800'
                      : (selectedTripDetails.status === 'ACTIVE' || selectedTripDetails.status === 'active')
                      ? 'bg-blue-100 text-blue-800'
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {(selectedTripDetails.status || 'DRAFT').toUpperCase()}
                  </span>
                </div>
              </div>

              {/* Route Information */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center">
                  <MapPin className="h-4 w-4 mr-2" />
                  Route Information
                </h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-gray-500">Source</p>
                    <p className="text-sm font-medium text-gray-900">{selectedTripDetails.source_location || 'N/A'}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Destination</p>
                    <p className="text-sm font-medium text-gray-900">{selectedTripDetails.destination_location}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Driver/Operator</p>
                    <p className="text-sm font-medium text-gray-900">{selectedTripDetails.driver_operator || 'N/A'}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Vehicle</p>
                    <p className="text-sm font-medium text-gray-900">{selectedTripDetails.vehicle_number || 'N/A'}</p>
                  </div>
                </div>
              </div>

              {/* Financial Information */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center">
                  <DollarSign className="h-4 w-4 mr-2" />
                  Financial Details
                </h3>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <p className="text-xs text-gray-500">Client</p>
                    <p className="text-sm font-medium text-green-600">{selectedTripDetails.client_name}</p>
                    <p className="text-lg font-bold text-green-600 mt-1">{formatCurrency(selectedTripDetails.client_freight)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Vendor</p>
                    <p className="text-sm font-medium text-red-600">{selectedTripDetails.vendor_name}</p>
                    <p className="text-lg font-bold text-red-600 mt-1">{formatCurrency(selectedTripDetails.vendor_freight)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Gross Profit</p>
                    <p className={`text-lg font-bold mt-1 ${selectedTripDetails.gross_profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {formatCurrency(selectedTripDetails.gross_profit)}
                    </p>
                    <p className="text-xs text-gray-500">
                      {((selectedTripDetails.gross_profit / selectedTripDetails.client_freight) * 100).toFixed(1)}% margin
                    </p>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex justify-end space-x-3 pt-4 border-t">
                {((selectedTripDetails.status || '').toUpperCase() === 'DRAFT' || (selectedTripDetails.status || '').toUpperCase() === 'ACTIVE') && (
                  <>
                    <button
                      onClick={() => {
                        setShowDetailsModal(false);
                        handleCompleteTrip(selectedTripDetails);
                      }}
                      className="btn-primary flex items-center bg-green-600 hover:bg-green-700"
                    >
                      <CheckCircle className="h-4 w-4 mr-2" />
                      Mark as Completed
                    </button>
                    <button
                      onClick={() => {
                        setShowDetailsModal(false);
                        handleCancelTripModal(selectedTripDetails);
                      }}
                      className="btn-secondary flex items-center text-red-600 hover:bg-red-50"
                    >
                      <XCircle className="h-4 w-4 mr-2" />
                      Cancel Trip
                    </button>
                  </>
                )}
                <button
                  onClick={() => {
                    setShowDetailsModal(false);
                    setSelectedTripDetails(null);
                  }}
                  className="btn-secondary"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Cancel Trip Modal */}
      {showCancelModal && selectedTripToCancel && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                <AlertTriangle className="h-6 w-6 text-red-600 mr-2" />
                Cancel Trip
              </h2>
              <button
                onClick={() => {
                  setShowCancelModal(false);
                  setSelectedTripToCancel(null);
                  setCancelReason('');
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            <div className="space-y-4">
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-sm text-red-800">
                  <strong>Warning:</strong> Cancelling this trip will:
                </p>
                <ul className="mt-2 text-sm text-red-700 list-disc list-inside space-y-1">
                  <li>Mark the trip as CANCELLED</li>
                  <li>Reverse the receivable (Client: {selectedTripToCancel.client_name})</li>
                  <li>Reverse the payable (Vendor: {selectedTripToCancel.vendor_name})</li>
                  <li>This action cannot be undone</li>
                </ul>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Cancellation Reason *
                </label>
                <textarea
                  value={cancelReason}
                  onChange={(e) => setCancelReason(e.target.value)}
                  placeholder="Please provide a reason for cancellation..."
                  rows="4"
                  className="input-field resize-none"
                  required
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4 border-t">
                <button
                  onClick={() => {
                    setShowCancelModal(false);
                    setSelectedTripToCancel(null);
                    setCancelReason('');
                  }}
                  className="btn-secondary"
                >
                  Keep Trip
                </button>
                <button
                  onClick={handleCancelTrip}
                  className="btn-primary bg-red-600 hover:bg-red-700 flex items-center"
                >
                  <XCircle className="h-4 w-4 mr-2" />
                  Cancel Trip
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FleetLogs;