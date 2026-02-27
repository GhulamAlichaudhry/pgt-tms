import React, { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { 
  Plus, 
  Download, 
  Filter,
  DollarSign,
  TrendingUp,
  TrendingDown,
  Calendar,
  FileText,
  X
} from 'lucide-react';

const Expenses = () => {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  
  // Filter states
  const [filterStartDate, setFilterStartDate] = useState('');
  const [filterEndDate, setFilterEndDate] = useState('');
  const [filterCategory, setFilterCategory] = useState('');
  const [filterType, setFilterType] = useState(''); // 'received' or 'paid'
  
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    entry_type: 'expense', // 'expense' or 'cash_received'
    account_title: '',
    particulars: '',
    amount_received: '',
    amount_paid: ''
  });

  // Expense categories matching your Excel
  const expenseCategories = [
    'Guest & Mess Expenses',
    'Printing & Stationary',
    'Courier Charges',
    'Utility Bills',
    'Rent',
    'Salaries',
    'Fuel & Transport',
    'Maintenance & Repairs',
    'Communication',
    'Other Expenses'
  ];

  useEffect(() => {
    fetchExpenses();
  }, []);

  const fetchExpenses = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/office-expenses/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setExpenses(response.data || []);
    } catch (error) {
      console.error('Error fetching expenses:', error);
      if (error.response?.status === 404) {
        // Endpoint doesn't exist yet, use empty array
        setExpenses([]);
      } else {
        toast.error('Failed to fetch expenses');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!formData.date || !formData.account_title || !formData.particulars) {
      toast.error('Please fill in all required fields');
      return;
    }

    if (formData.entry_type === 'cash_received' && !formData.amount_received) {
      toast.error('Please enter amount received');
      return;
    }

    if (formData.entry_type === 'expense' && !formData.amount_paid) {
      toast.error('Please enter amount paid');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      
      const expenseData = {
        date: formData.date,
        entry_type: formData.entry_type,
        account_title: formData.account_title,
        particulars: formData.particulars,
        amount_received: formData.amount_received ? parseFloat(formData.amount_received) : 0,
        amount_paid: formData.amount_paid ? parseFloat(formData.amount_paid) : 0
      };

      await axios.post('/office-expenses/', expenseData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      toast.success('Entry added successfully!');
      setShowAddForm(false);
      resetForm();
      fetchExpenses();
    } catch (error) {
      console.error('Error adding entry:', error);
      toast.error(error.response?.data?.detail || 'Failed to add entry');
    }
  };

  const resetForm = () => {
    setFormData({
      date: new Date().toISOString().split('T')[0],
      entry_type: 'expense',
      account_title: '',
      particulars: '',
      amount_received: '',
      amount_paid: ''
    });
  };

  const handleDownloadExcel = async () => {
    try {
      const token = localStorage.getItem('token');
      
      // Build query parameters for filters
      const params = new URLSearchParams();
      if (filterStartDate) params.append('start_date', filterStartDate);
      if (filterEndDate) params.append('end_date', filterEndDate);
      if (filterCategory) params.append('category', filterCategory);
      if (filterType) params.append('type', filterType);
      
      const response = await axios.get(`/office-expenses/download?${params.toString()}`, {
        headers: { 'Authorization': `Bearer ${token}` },
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Office_Expenses_${new Date().toISOString().split('T')[0]}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast.success('Excel file downloaded successfully!');
    } catch (error) {
      console.error('Error downloading Excel:', error);
      toast.error('Failed to download Excel file');
    }
  };

  // Calculate running balance
  const calculateBalance = () => {
    let balance = 0;
    return filteredExpenses.map(expense => {
      balance += (expense.amount_received || 0) - (expense.amount_paid || 0);
      return { ...expense, balance };
    });
  };

  // Apply filters
  const filteredExpenses = expenses.filter(expense => {
    if (filterStartDate && expense.date < filterStartDate) return false;
    if (filterEndDate && expense.date > filterEndDate) return false;
    if (filterCategory && expense.account_title !== filterCategory) return false;
    if (filterType === 'received' && expense.amount_received === 0) return false;
    if (filterType === 'paid' && expense.amount_paid === 0) return false;
    return true;
  });

  const expensesWithBalance = calculateBalance();

  // Calculate totals
  const totalReceived = filteredExpenses.reduce((sum, exp) => sum + (exp.amount_received || 0), 0);
  const totalPaid = filteredExpenses.reduce((sum, exp) => sum + (exp.amount_paid || 0), 0);
  const currentBalance = totalReceived - totalPaid;

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
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Office Expenses</h1>
          <p className="text-sm text-gray-500 mt-1">Track office expenses and cash flow</p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="btn-secondary flex items-center"
          >
            <Filter className="h-4 w-4 mr-2" />
            Filters
          </button>
          <button
            onClick={handleDownloadExcel}
            className="btn-secondary flex items-center"
          >
            <Download className="h-4 w-4 mr-2" />
            Download Excel
          </button>
          <button
            onClick={() => setShowAddForm(true)}
            className="btn-primary flex items-center"
          >
            <Plus className="h-4 w-4 mr-2" />
            Add Entry
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card rounded-xl p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Received</p>
              <p className="text-2xl font-bold text-green-600 mt-1">
                PKR {totalReceived.toLocaleString()}
              </p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Paid</p>
              <p className="text-2xl font-bold text-red-600 mt-1">
                PKR {totalPaid.toLocaleString()}
              </p>
            </div>
            <div className="p-3 bg-red-100 rounded-lg">
              <TrendingDown className="h-6 w-6 text-red-600" />
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Current Balance</p>
              <p className={`text-2xl font-bold mt-1 ${currentBalance >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                PKR {currentBalance.toLocaleString()}
              </p>
            </div>
            <div className={`p-3 rounded-lg ${currentBalance >= 0 ? 'bg-green-100' : 'bg-red-100'}`}>
              <DollarSign className={`h-6 w-6 ${currentBalance >= 0 ? 'text-green-600' : 'text-red-600'}`} />
            </div>
          </div>
        </div>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <div className="glass-card rounded-xl p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Filters</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
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
              <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
              <select
                value={filterCategory}
                onChange={(e) => setFilterCategory(e.target.value)}
                className="input-field"
              >
                <option value="">All Categories</option>
                {expenseCategories.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
                <option value="Cash Received">Cash Received</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="input-field"
              >
                <option value="">All Types</option>
                <option value="received">Cash Received</option>
                <option value="paid">Expenses Paid</option>
              </select>
            </div>
          </div>
          <div className="flex justify-end mt-4">
            <button
              onClick={() => {
                setFilterStartDate('');
                setFilterEndDate('');
                setFilterCategory('');
                setFilterType('');
              }}
              className="btn-secondary"
            >
              Clear Filters
            </button>
          </div>
        </div>
      )}

      {/* Expenses Table */}
      <div className="glass-card rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Sr#
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acc. Title
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Particulars/Descriptions
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount Rcvd
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount Paid
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Balance
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {expensesWithBalance.length === 0 ? (
                <tr>
                  <td colSpan="7" className="px-6 py-12 text-center">
                    <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">No expense entries found</p>
                    <p className="text-sm text-gray-400 mt-1">Add your first entry to get started</p>
                  </td>
                </tr>
              ) : (
                expensesWithBalance.map((expense, index) => (
                  <tr key={expense.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {index + 1}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {new Date(expense.date).toLocaleDateString('en-GB')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {expense.account_title}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {expense.particulars}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right">
                      {expense.amount_received > 0 ? (
                        <span className="text-green-600 font-medium">
                          {expense.amount_received.toLocaleString()}
                        </span>
                      ) : (
                        <span className="text-gray-400">-</span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right">
                      {expense.amount_paid > 0 ? (
                        <span className="text-red-600 font-medium">
                          {expense.amount_paid.toLocaleString()}
                        </span>
                      ) : (
                        <span className="text-gray-400">-</span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right">
                      <span className={`font-semibold ${expense.balance >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {expense.balance.toLocaleString()}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add Entry Modal */}
      {showAddForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl w-full max-w-2xl overflow-hidden">
            {/* Modal Header */}
            <div className="bg-red-600 px-6 py-4 text-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Plus className="h-6 w-6" />
                  <h2 className="text-xl font-semibold">Add Expense Entry</h2>
                </div>
                <button
                  onClick={() => {
                    setShowAddForm(false);
                    resetForm();
                  }}
                  className="p-1 hover:bg-red-700 rounded transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            </div>

            {/* Modal Content */}
            <div className="p-6">
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                    <label className="block text-sm font-medium text-gray-700 mb-1">Entry Type *</label>
                    <select
                      name="entry_type"
                      value={formData.entry_type}
                      onChange={handleInputChange}
                      required
                      className="input-field"
                    >
                      <option value="expense">Expense Paid</option>
                      <option value="cash_received">Cash Received</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Account Title *</label>
                  {formData.entry_type === 'cash_received' ? (
                    <input
                      type="text"
                      name="account_title"
                      value={formData.account_title}
                      onChange={handleInputChange}
                      required
                      placeholder="e.g., Cash Received"
                      className="input-field"
                    />
                  ) : (
                    <select
                      name="account_title"
                      value={formData.account_title}
                      onChange={handleInputChange}
                      required
                      className="input-field"
                    >
                      <option value="">Select Category</option>
                      {expenseCategories.map(cat => (
                        <option key={cat} value={cat}>{cat}</option>
                      ))}
                    </select>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Particulars/Description *</label>
                  <textarea
                    name="particulars"
                    value={formData.particulars}
                    onChange={handleInputChange}
                    required
                    rows="3"
                    placeholder="Enter detailed description..."
                    className="input-field"
                  />
                </div>

                {formData.entry_type === 'cash_received' ? (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Amount Received (PKR) *</label>
                    <input
                      type="number"
                      step="0.01"
                      name="amount_received"
                      value={formData.amount_received}
                      onChange={handleInputChange}
                      required
                      placeholder="0.00"
                      className="input-field"
                    />
                  </div>
                ) : (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Amount Paid (PKR) *</label>
                    <input
                      type="number"
                      step="0.01"
                      name="amount_paid"
                      value={formData.amount_paid}
                      onChange={handleInputChange}
                      required
                      placeholder="0.00"
                      className="input-field"
                    />
                  </div>
                )}

                <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
                  <button
                    type="button"
                    onClick={() => {
                      setShowAddForm(false);
                      resetForm();
                    }}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn-primary">
                    Add Entry
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

export default Expenses;
