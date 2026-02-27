import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { 
  Plus, 
  Search, 
  Download,
  TrendingUp,
  TrendingDown,
  DollarSign,
  Calendar,
  ArrowUpCircle,
  ArrowDownCircle,
  X,
  Eye
} from 'lucide-react';

const DailyCashFlow = () => {
  const [cashFlows, setCashFlows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('');
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [submitting, setSubmitting] = useState(false);
  const [summary, setSummary] = useState({
    total_income: 0,
    total_outgoing: 0,
    total_net: 0,
    days: 0
  });
  const [dateRange, setDateRange] = useState({
    start: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    end: new Date().toISOString().split('T')[0]
  });

  const { register, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      date: new Date().toISOString().split('T')[0],
      type: '',
      description: '',
      amount: '',
      category: '',
      reference: ''
    }
  });

  const cashFlowTypes = [
    { value: 'inflow', label: 'Cash Inflow', icon: ArrowUpCircle, color: 'text-green-600' },
    { value: 'outflow', label: 'Cash Outflow', icon: ArrowDownCircle, color: 'text-red-600' }
  ];

  const categories = [
    'Trip Revenue',
    'Fuel Payment',
    'Maintenance',
    'Office Expenses',
    'Vendor Payment',
    'Client Payment',
    'Salary Payment',
    'Insurance',
    'Other'
  ];

  useEffect(() => {
    fetchCashFlows();
  }, [dateRange]);

  const fetchCashFlows = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      
      // Use the new daily-cash-flow endpoint with date range
      const response = await axios.get(
        `/daily-cash-flow?start_date=${dateRange.start}&end_date=${dateRange.end}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      // Transform data for display
      const cashFlowData = response.data.cash_flows.map(flow => ({
        date: flow.date,
        income: flow.daily_income,
        outgoing: flow.daily_outgoing,
        net: flow.daily_net
      }));
      
      setCashFlows(cashFlowData);
      setSummary(response.data.summary);
    } catch (error) {
      console.error('Error fetching cash flows:', error);
      if (error.response?.status === 401) {
        toast.error('Please login again');
        window.location.href = '/login';
      } else {
        toast.error('Failed to fetch cash flows');
      }
    } finally {
      setLoading(false);
    }
  };

  const setToday = () => {
    const today = new Date().toISOString().split('T')[0];
    setDateRange({ start: today, end: today });
  };

  const setThisWeek = () => {
    const today = new Date();
    const weekStart = new Date(today.setDate(today.getDate() - today.getDay()));
    setDateRange({
      start: weekStart.toISOString().split('T')[0],
      end: new Date().toISOString().split('T')[0]
    });
  };

  const setThisMonth = () => {
    const today = new Date();
    const monthStart = new Date(today.getFullYear(), today.getMonth(), 1);
    setDateRange({
      start: monthStart.toISOString().split('T')[0],
      end: new Date().toISOString().split('T')[0]
    });
  };

  const onSubmit = async (data) => {
    if (submitting) return;
    
    setSubmitting(true);
    try {
      // For now, we'll just show success message
      // In a real implementation, you'd save to a cash_flows table
      toast.success('Cash flow entry added successfully!');
      reset();
      setShowAddForm(false);
      fetchCashFlows();
    } catch (error) {
      console.error('Error adding cash flow:', error);
      toast.error('Failed to add cash flow entry');
    } finally {
      setSubmitting(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-PK', {
      style: 'currency',
      currency: 'PKR',
      minimumFractionDigits: 0,
    }).format(amount || 0);
  };

  const getTypeIcon = (type) => {
    const typeData = cashFlowTypes.find(t => t.value === type);
    if (typeData) {
      const Icon = typeData.icon;
      return <Icon className={`h-4 w-4 ${typeData.color}`} />;
    }
    return <DollarSign className="h-4 w-4 text-gray-600" />;
  };

  const filteredCashFlows = cashFlows.filter(flow => {
    const matchesSearch = 
      flow.date?.toLowerCase().includes(searchTerm.toLowerCase());
    
    return matchesSearch;
  });

  // Use summary from API
  const dailyInflow = summary.total_income || 0;
  const dailyOutflow = summary.total_outgoing || 0;
  const netCashFlow = summary.total_net || 0;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Daily Cash Flow</h1>
        <div className="flex items-center space-x-3">
          <button
            onClick={setToday}
            className="btn-secondary text-sm"
          >
            Today
          </button>
          <button
            onClick={setThisWeek}
            className="btn-secondary text-sm"
          >
            This Week
          </button>
          <button
            onClick={setThisMonth}
            className="btn-secondary text-sm"
          >
            This Month
          </button>
          <input
            type="date"
            value={dateRange.start}
            onChange={(e) => setDateRange({...dateRange, start: e.target.value})}
            className="input-field"
            placeholder="Start Date"
          />
          <span className="text-gray-500">to</span>
          <input
            type="date"
            value={dateRange.end}
            onChange={(e) => setDateRange({...dateRange, end: e.target.value})}
            className="input-field"
            placeholder="End Date"
          />
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '1px solid rgba(34, 197, 94, 0.2)'
        }}>
          <div className="flex items-center">
            <TrendingUp className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Income</p>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(dailyInflow)}</p>
              <p className="text-xs text-gray-500 mt-1">{summary.days} days</p>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '1px solid rgba(239, 68, 68, 0.2)'
        }}>
          <div className="flex items-center">
            <TrendingDown className="h-8 w-8 text-red-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Outgoing</p>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(dailyOutflow)}</p>
              <p className="text-xs text-gray-500 mt-1">{summary.days} days</p>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6" style={{
          background: `linear-gradient(135deg, rgba(${netCashFlow >= 0 ? '34, 197, 94' : '239, 68, 68'}, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)`,
          border: `1px solid rgba(${netCashFlow >= 0 ? '34, 197, 94' : '239, 68, 68'}, 0.2)`
        }}>
          <div className="flex items-center">
            <DollarSign className={`h-8 w-8 ${netCashFlow >= 0 ? 'text-green-600' : 'text-red-600'}`} />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Net Cash Flow</p>
              <p className={`text-2xl font-bold ${netCashFlow >= 0 ? 'text-green-900' : 'text-red-900'}`}>
                {formatCurrency(netCashFlow)}
              </p>
              <p className="text-xs text-gray-500 mt-1">{summary.days} days</p>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '1px solid rgba(59, 130, 246, 0.2)'
        }}>
          <div className="flex items-center">
            <Calendar className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Days</p>
              <p className="text-2xl font-bold text-gray-900">{summary.days}</p>
              <p className="text-xs text-gray-500 mt-1">Avg: {formatCurrency(netCashFlow / (summary.days || 1))}/day</p>
            </div>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="glass-card rounded-xl p-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <input
              type="text"
              placeholder="Search by date..."
              className="input-field pl-10"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <button className="btn-secondary flex items-center">
            <Download className="h-5 w-5 mr-2" />
            Export
          </button>
        </div>
      </div>

      {/* Cash Flow List */}
      <div className="glass-card rounded-xl overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">
            Daily Cash Flow Breakdown ({dateRange.start} to {dateRange.end})
          </h3>
        </div>
        
        {filteredCashFlows.length === 0 ? (
          <div className="p-8 text-center">
            <DollarSign className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">No cash flow data for this date range</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Income</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Outgoing</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Net</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredCashFlows.map((flow, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {new Date(flow.date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium text-green-600">
                      {formatCurrency(flow.income)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium text-red-600">
                      {formatCurrency(flow.outgoing)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-semibold">
                      <span className={flow.net >= 0 ? 'text-green-600' : 'text-red-600'}>
                        {formatCurrency(flow.net)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
              <tfoot className="bg-gray-50">
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">
                    TOTAL
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-bold text-green-600">
                    {formatCurrency(dailyInflow)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-bold text-red-600">
                    {formatCurrency(dailyOutflow)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-bold">
                    <span className={netCashFlow >= 0 ? 'text-green-600' : 'text-red-600'}>
                      {formatCurrency(netCashFlow)}
                    </span>
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default DailyCashFlow;