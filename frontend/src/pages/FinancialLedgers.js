import React, { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { 
  Plus, 
  Search, 
  Building2, 
  DollarSign,
  TrendingUp,
  FileText,
  X,
  Download,
  Filter,
  Calendar,
  Users,
  Truck
} from 'lucide-react';

const FinancialLedgers = () => {
  // Tab state
  const [activeTab, setActiveTab] = useState('vendors'); // 'vendors' or 'clients'
  
  // Data states
  const [vendors, setVendors] = useState([]);
  const [clients, setClients] = useState([]);
  const [selectedEntity, setSelectedEntity] = useState(null);
  const [ledgerData, setLedgerData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Filter states
  const [showFilters, setShowFilters] = useState(false);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [filterApplied, setFilterApplied] = useState(false);

  useEffect(() => {
    fetchVendors();
    fetchClients();
  }, []);

  useEffect(() => {
    if (selectedEntity) {
      fetchLedger();
    }
  }, [selectedEntity, activeTab, filterApplied]);

  const fetchVendors = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/vendors/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setVendors(response.data);
      if (response.data.length > 0 && !selectedEntity && activeTab === 'vendors') {
        setSelectedEntity(response.data[0]);
      }
    } catch (error) {
      console.error('Error fetching vendors:', error);
      toast.error('Failed to fetch vendors');
    } finally {
      setLoading(false);
    }
  };

  const fetchClients = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/clients/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setClients(response.data);
    } catch (error) {
      console.error('Error fetching clients:', error);
      toast.error('Failed to fetch clients');
    }
  };

  const fetchLedger = async () => {
    if (!selectedEntity) return;
    
    try {
      const token = localStorage.getItem('token');
      const endpoint = activeTab === 'vendors' 
        ? `/api/ledgers/vendor/${selectedEntity.id}`
        : `/api/ledgers/client/${selectedEntity.id}`;
      
      const params = {};
      if (startDate) params.start_date = startDate;
      if (endDate) params.end_date = endDate;
      
      const response = await axios.get(endpoint, {
        headers: { 'Authorization': `Bearer ${token}` },
        params
      });
      
      setLedgerData(response.data);
    } catch (error) {
      console.error('Error fetching ledger:', error);
      toast.error('Failed to fetch ledger data');
    }
  };

  const downloadExcel = async () => {
    if (!selectedEntity) return;
    
    try {
      const token = localStorage.getItem('token');
      const endpoint = activeTab === 'vendors'
        ? `/reports/vendor-ledger-excel/${selectedEntity.id}`
        : `/reports/client-ledger-excel/${selectedEntity.id}`;
      
      const params = {};
      if (startDate) params.start_date = startDate;
      if (endDate) params.end_date = endDate;
      
      const response = await axios.get(endpoint, {
        headers: { 'Authorization': `Bearer ${token}` },
        params,
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      const entityName = activeTab === 'vendors' ? selectedEntity.name : selectedEntity.name;
      link.setAttribute('download', `${activeTab}_ledger_${entityName.replace(/\s+/g, '_')}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('Ledger downloaded successfully!');
    } catch (error) {
      console.error('Error downloading ledger:', error);
      toast.error('Failed to download ledger');
    }
  };

  const applyFilters = () => {
    setFilterApplied(!filterApplied);
    setShowFilters(false);
    toast.success('Filters applied');
  };

  const clearFilters = () => {
    setStartDate('');
    setEndDate('');
    setFilterApplied(!filterApplied);
    toast.success('Filters cleared');
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-PK', {
      style: 'currency',
      currency: 'PKR',
      minimumFractionDigits: 0,
    }).format(amount || 0);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'paid': return 'bg-green-100 text-green-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'partial': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const currentList = activeTab === 'vendors' ? vendors : clients;
  const filteredList = currentList.filter(entity =>
    entity.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    entity.contact_person?.toLowerCase().includes(searchTerm.toLowerCase())
  );

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
        <h1 className="text-2xl font-bold text-gray-900">Financial Ledgers</h1>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`btn-secondary flex items-center ${filterApplied ? 'bg-blue-100 border-blue-300' : ''}`}
          >
            <Filter className="h-5 w-5 mr-2" />
            Filters {filterApplied && '✓'}
          </button>
          {selectedEntity && ledgerData && (
            <button
              onClick={downloadExcel}
              className="btn-primary flex items-center"
            >
              <Download className="h-5 w-5 mr-2" />
              Download Excel
            </button>
          )}
        </div>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <div className="glass-card rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <Calendar className="h-5 w-5 mr-2 text-red-600" />
              Date Range Filter
            </h3>
            <button
              onClick={() => setShowFilters(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="input-field"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="input-field"
              />
            </div>
            
            <div className="flex items-end space-x-2">
              <button
                onClick={applyFilters}
                className="btn-primary flex-1"
              >
                Apply Filters
              </button>
              <button
                onClick={clearFilters}
                className="btn-secondary"
              >
                Clear
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Tab Switcher */}
      <div className="glass-card rounded-xl">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            <button
              onClick={() => {
                setActiveTab('vendors');
                setSelectedEntity(vendors[0] || null);
                setLedgerData(null);
              }}
              className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'vendors'
                  ? 'border-red-600 text-red-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center">
                <Truck className="h-5 w-5 mr-2" />
                Vendor Ledgers
                <span className="ml-2 px-2 py-1 text-xs rounded-full bg-gray-100">
                  {vendors.length}
                </span>
              </div>
            </button>
            
            <button
              onClick={() => {
                setActiveTab('clients');
                setSelectedEntity(clients[0] || null);
                setLedgerData(null);
              }}
              className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'clients'
                  ? 'border-red-600 text-red-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center">
                <Users className="h-5 w-5 mr-2" />
                Client Ledgers
                <span className="ml-2 px-2 py-1 text-xs rounded-full bg-gray-100">
                  {clients.length}
                </span>
              </div>
            </button>
          </nav>
        </div>
      </div>

      {/* Summary Cards */}
      {ledgerData && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="glass-card rounded-xl p-6">
            <div className="flex items-center">
              <TrendingUp className="h-8 w-8 text-green-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Debit</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(ledgerData.summary.total_debit)}
                </p>
              </div>
            </div>
          </div>

          <div className="glass-card rounded-xl p-6">
            <div className="flex items-center">
              <DollarSign className="h-8 w-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Credit</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(ledgerData.summary.total_credit)}
                </p>
              </div>
            </div>
          </div>

          <div className="glass-card rounded-xl p-6">
            <div className="flex items-center">
              <Building2 className="h-8 w-8 text-orange-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Balance</p>
                <p className={`text-2xl font-bold ${ledgerData.summary.balance > 0 ? 'text-red-600' : 'text-green-600'}`}>
                  {formatCurrency(ledgerData.summary.balance)}
                </p>
              </div>
            </div>
          </div>

          <div className="glass-card rounded-xl p-6">
            <div className="flex items-center">
              <FileText className="h-8 w-8 text-purple-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Trips</p>
                <p className="text-2xl font-bold text-gray-900">
                  {ledgerData.summary.trip_count}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Entity List */}
        <div className="lg:col-span-1">
          <div className="glass-card rounded-xl">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">
                {activeTab === 'vendors' ? 'Vendors' : 'Clients'}
              </h3>
              <div className="mt-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                  <input
                    type="text"
                    placeholder={`Search ${activeTab}...`}
                    className="input-field pl-10"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>
            </div>
            
            <div className="max-h-96 overflow-y-auto">
              {filteredList.map((entity) => (
                <div
                  key={entity.id}
                  onClick={() => setSelectedEntity(entity)}
                  className={`p-4 border-b border-gray-100 cursor-pointer hover:bg-gray-50 ${
                    selectedEntity?.id === entity.id ? 'bg-blue-50 border-blue-200' : ''
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-gray-900">{entity.name}</h4>
                      <p className="text-sm text-gray-500">
                        {activeTab === 'vendors' ? entity.vendor_code : entity.client_code}
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-gray-600">
                        {entity.contact_person || 'N/A'}
                      </div>
                      <div className="text-xs text-gray-400">{entity.phone || 'No phone'}</div>
                    </div>
                  </div>
                </div>
              ))}
              
              {filteredList.length === 0 && (
                <div className="p-8 text-center text-gray-500">
                  <Building2 className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                  <p>No {activeTab} found</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Ledger Entries */}
        <div className="lg:col-span-2">
          <div className="glass-card rounded-xl">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {selectedEntity ? `${selectedEntity.name} - Ledger` : `Select a ${activeTab === 'vendors' ? 'Vendor' : 'Client'}`}
                  </h3>
                  {ledgerData && (
                    <div className="mt-2 text-sm text-gray-600">
                      Balance: <span className={`font-medium ${ledgerData.summary.balance > 0 ? 'text-red-600' : 'text-green-600'}`}>
                        {formatCurrency(ledgerData.summary.balance)}
                      </span>
                      {filterApplied && (startDate || endDate) && (
                        <span className="ml-3 text-blue-600">
                          📅 Filtered: {startDate || 'Start'} to {endDate || 'End'}
                        </span>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
            
            {selectedEntity && ledgerData ? (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200 text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Description</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Trip Ref</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Debit</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Credit</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Balance</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {ledgerData.entries.map((entry, index) => (
                      <tr key={index} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {new Date(entry.date).toLocaleDateString()}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">
                          <div>
                            {entry.description}
                            {entry.trip_details && (
                              <div className="text-xs text-gray-500 mt-1">
                                {entry.trip_details.from} → {entry.trip_details.to}
                                {entry.trip_details.tonnage && ` | ${entry.trip_details.tonnage} tons`}
                              </div>
                            )}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-blue-600">
                          {entry.trip_reference || '-'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600 font-medium">
                          {entry.debit > 0 ? formatCurrency(entry.debit) : '-'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">
                          {entry.credit > 0 ? formatCurrency(entry.credit) : '-'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {formatCurrency(entry.balance)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(entry.status)}`}>
                            {entry.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                
                {ledgerData.entries.length === 0 && (
                  <div className="p-8 text-center text-gray-500">
                    <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                    <p>No ledger entries found</p>
                    {filterApplied && (
                      <button
                        onClick={clearFilters}
                        className="mt-4 btn-secondary"
                      >
                        Clear Filters
                      </button>
                    )}
                  </div>
                )}
              </div>
            ) : (
              <div className="p-8 text-center text-gray-500">
                <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>Select a {activeTab === 'vendors' ? 'vendor' : 'client'} to view ledger entries</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FinancialLedgers;
