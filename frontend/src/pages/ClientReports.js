import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import toast from 'react-hot-toast';
import { 
  Search, 
  Download,
  Building2,
  DollarSign,
  TrendingUp,
  MapPin,
  FileText,
  BarChart3,
  Eye,
  Package,
  Users,
  BookOpen,
  Truck,
  CreditCard
} from 'lucide-react';

const ClientReports = () => {
  const navigate = useNavigate();
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedClient, setSelectedClient] = useState('');
  const [dateRange, setDateRange] = useState({
    start: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0],
    end: new Date().toISOString().split('T')[0]
  });

  useEffect(() => {
    fetchReportData();
  }, [dateRange]);

  const fetchReportData = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const params = new URLSearchParams();
      if (dateRange.start) params.append('start_date', dateRange.start);
      if (dateRange.end) params.append('end_date', dateRange.end);
      if (selectedClient) params.append('client_id', selectedClient);
      
      const response = await axios.get(`/api/reports/client-performance?${params}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      setReportData(response.data);
    } catch (error) {
      console.error('Error fetching report data:', error);
      if (error.response?.status === 401) {
        toast.error('Please login again');
        window.location.href = '/login';
      } else {
        toast.error('Failed to fetch client report data');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    setExporting(true);
    try {
      const token = localStorage.getItem('token');
      const params = new URLSearchParams();
      if (dateRange.start) params.append('start_date', dateRange.start);
      if (dateRange.end) params.append('end_date', dateRange.end);
      if (selectedClient) params.append('client_id', selectedClient);
      
      const response = await axios.get(`/api/reports/client-performance-excel?${params}`, {
        headers: { 'Authorization': `Bearer ${token}` },
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `client_performance_report_${new Date().toISOString().split('T')[0]}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('Report exported successfully!');
    } catch (error) {
      console.error('Error exporting report:', error);
      toast.error('Failed to export report');
    } finally {
      setExporting(false);
    }
  };

  const viewLedger = (clientId) => {
    navigate('/financial-ledgers', { state: { tab: 'clients', clientId } });
  };

  const viewTrips = (clientId) => {
    navigate('/fleet-logs', { state: { clientId } });
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-PK', {
      style: 'currency',
      currency: 'PKR',
      minimumFractionDigits: 0,
    }).format(amount || 0);
  };

  const filteredClients = reportData?.clients.filter(client => {
    const matchesSearch = client.client_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         client.client_code?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesClient = !selectedClient || client.client_id.toString() === selectedClient;
    return matchesSearch && matchesClient;
  }) || [];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600"></div>
      </div>
    );
  }

  const summary = reportData?.summary || {};

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Client Reports</h1>
        <button 
          onClick={handleExport}
          disabled={exporting}
          className="btn-primary flex items-center"
        >
          <Download className="h-5 w-5 mr-2" />
          {exporting ? 'Exporting...' : 'Export Report'}
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '1px solid rgba(59, 130, 246, 0.2)'
        }}>
          <div className="flex items-center">
            <Building2 className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Clients</p>
              <p className="text-2xl font-bold text-gray-900">{summary.total_clients || 0}</p>
              <p className="text-xs text-gray-500 mt-1">{summary.active_clients || 0} active</p>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '1px solid rgba(34, 197, 94, 0.2)'
        }}>
          <div className="flex items-center">
            <DollarSign className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Receivables</p>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(summary.total_receivables)}</p>
              <p className="text-xs text-gray-500 mt-1">Amount owed to us</p>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '1px solid rgba(59, 130, 246, 0.2)'
        }}>
          <div className="flex items-center">
            <TrendingUp className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Collected</p>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(summary.total_collected)}</p>
              <p className="text-xs text-gray-500 mt-1">Payments received</p>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(251, 146, 60, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '1px solid rgba(251, 146, 60, 0.2)'
        }}>
          <div className="flex items-center">
            <BarChart3 className="h-8 w-8 text-orange-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Outstanding</p>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(summary.total_outstanding)}</p>
              <p className="text-xs text-gray-500 mt-1">Pending collection</p>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="glass-card rounded-xl p-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <input
              type="text"
              placeholder="Search clients..."
              className="input-field pl-10"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <select
            value={selectedClient}
            onChange={(e) => {
              setSelectedClient(e.target.value);
              fetchReportData();
            }}
            className="input-field"
          >
            <option value="">All Clients</option>
            {reportData?.clients.map(client => (
              <option key={client.client_id} value={client.client_id}>
                {client.client_name}
              </option>
            ))}
          </select>

          <input
            type="date"
            value={dateRange.start}
            onChange={(e) => setDateRange({...dateRange, start: e.target.value})}
            className="input-field"
          />

          <input
            type="date"
            value={dateRange.end}
            onChange={(e) => setDateRange({...dateRange, end: e.target.value})}
            className="input-field"
          />
        </div>
      </div>

      {/* Top Clients */}
      <div className="glass-card rounded-xl p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Clients by Revenue</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {filteredClients
            .sort((a, b) => b.total_receivables - a.total_receivables)
            .slice(0, 3)
            .map((client, index) => (
              <div key={client.client_id} className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900 truncate">{client.client_name}</h4>
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    index === 0 ? 'bg-yellow-100 text-yellow-800' :
                    index === 1 ? 'bg-gray-100 text-gray-800' :
                    'bg-orange-100 text-orange-800'
                  }`}>
                    #{index + 1}
                  </span>
                </div>
                <div className="space-y-1 text-sm text-gray-600">
                  <div className="flex justify-between">
                    <span>Receivables:</span>
                    <span className="font-medium">{formatCurrency(client.total_receivables)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Trips:</span>
                    <span className="font-medium">{client.total_trips}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Outstanding:</span>
                    <span className="font-medium text-orange-600">{formatCurrency(client.outstanding_amount)}</span>
                  </div>
                </div>
              </div>
            ))}
        </div>
      </div>

      {/* Client Performance Table */}
      <div className="glass-card rounded-xl overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Client Performance Details</h3>
        </div>
        
        {filteredClients.length === 0 ? (
          <div className="p-8 text-center">
            <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">No clients found</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Client</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total Trips</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total Receivables</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Collected</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Outstanding</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Destinations</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">This Month</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Last Trip</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredClients.map((client) => (
                  <tr key={client.client_id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex items-center">
                        <Building2 className="h-4 w-4 text-gray-400 mr-2" />
                        <div>
                          <div className="font-medium">{client.client_name}</div>
                          <div className="text-gray-500">{client.client_code}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex items-center">
                        <FileText className="h-4 w-4 text-blue-500 mr-1" />
                        {client.total_trips}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {formatCurrency(client.total_receivables)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">
                      {formatCurrency(client.total_collected)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span className={`font-medium ${
                        client.outstanding_amount > 0 ? 'text-orange-600' : 'text-gray-900'
                      }`}>
                        {formatCurrency(client.outstanding_amount)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex items-center">
                        <MapPin className="h-4 w-4 text-green-500 mr-1" />
                        {client.destinations?.length || 0}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div>
                        <div className="font-medium">{client.this_month_trips} trips</div>
                        <div className="text-gray-500">{formatCurrency(client.this_month_receivables)}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div>
                        <div className="font-medium">{client.last_trip_date ? new Date(client.last_trip_date).toLocaleDateString() : 'N/A'}</div>
                        <div className="text-gray-500">{client.last_trip_reference || '-'}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex space-x-2">
                        <button 
                          onClick={() => viewLedger(client.client_id)}
                          className="text-blue-600 hover:text-blue-800"
                          title="View Ledger"
                        >
                          <BookOpen className="h-4 w-4" />
                        </button>
                        <button 
                          onClick={() => viewTrips(client.client_id)}
                          className="text-green-600 hover:text-green-800"
                          title="View Trips"
                        >
                          <Truck className="h-4 w-4" />
                        </button>
                        <button 
                          onClick={() => navigate('/receivables', { state: { clientId: client.client_id } })}
                          className="text-orange-600 hover:text-orange-800"
                          title="View Receivables"
                        >
                          <CreditCard className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default ClientReports;
