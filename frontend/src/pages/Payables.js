import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { 
  Plus, 
  Search, 
  Download,
  CreditCard,
  DollarSign,
  Calendar,
  Building2,
  AlertTriangle,
  CheckCircle,
  Clock,
  X,
  Eye,
  Send,
  Check,
  XCircle,
  ArrowRight,
  Banknote,
  CreditCard as CreditCardIcon,
  Smartphone,
  FileText,
  MoreVertical,
  Bell
} from 'lucide-react';

const Payables = () => {
  const location = useLocation();
  const [payables, setPayables] = useState([]);
  const [vendors, setVendors] = useState([]);
  const [paymentRequests, setPaymentRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [showRequestsModal, setShowRequestsModal] = useState(false);
  const [selectedPayable, setSelectedPayable] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [filterVendor, setFilterVendor] = useState(location.state?.vendorId?.toString() || '');
  const [submitting, setSubmitting] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [selectedPayableDetails, setSelectedPayableDetails] = useState(null);

  const { register, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      due_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      vendor_id: '',
      invoice_number: '',
      description: '',
      amount: '',
      status: 'pending'
    }
  });

  const { register: registerPayment, handleSubmit: handlePaymentSubmit, reset: resetPayment, watch, formState: { errors: paymentErrors } } = useForm({
    defaultValues: {
      payment_type: 'full',
      requested_amount: '',
      payment_channel: 'bank_transfer',
      request_reason: '',
      urgency_level: 'normal'
    }
  });

  const paymentType = watch('payment_type');

  const payableStatuses = [
    { value: 'pending', label: 'Pending', color: 'text-yellow-600', bg: 'bg-yellow-100' },
    { value: 'approved', label: 'Approved', color: 'text-blue-600', bg: 'bg-blue-100' },
    { value: 'paid', label: 'Paid', color: 'text-green-600', bg: 'bg-green-100' },
    { value: 'partially_paid', label: 'Partially Paid', color: 'text-orange-600', bg: 'bg-orange-100' },
    { value: 'overdue', label: 'Overdue', color: 'text-red-600', bg: 'bg-red-100' }
  ];

  const paymentChannels = [
    { value: 'bank_transfer', label: 'Bank Transfer', icon: Building2 },
    { value: 'cash', label: 'Cash', icon: Banknote },
    { value: 'cheque', label: 'Cheque', icon: FileText },
    { value: 'online_transfer', label: 'Online Transfer', icon: CreditCardIcon },
    { value: 'mobile_banking', label: 'Mobile Banking', icon: Smartphone }
  ];

  const urgencyLevels = [
    { value: 'low', label: 'Low', color: 'text-green-600' },
    { value: 'normal', label: 'Normal', color: 'text-blue-600' },
    { value: 'high', label: 'High', color: 'text-orange-600' },
    { value: 'urgent', label: 'Urgent', color: 'text-red-600' }
  ];

  useEffect(() => {
    fetchPayables();
    fetchVendors();
    fetchPaymentRequests();
  }, []);

  const fetchPayables = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8002/payables/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setPayables(response.data);
    } catch (error) {
      console.error('Error fetching payables:', error);
      if (error.response?.status === 401) {
        toast.error('Please login again');
        window.location.href = '/login';
      } else {
        toast.error('Failed to fetch payables');
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchVendors = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8002/vendors/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setVendors(response.data);
    } catch (error) {
      console.error('Error fetching vendors:', error);
    }
  };

  const fetchPaymentRequests = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8002/payment-requests/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setPaymentRequests(response.data);
    } catch (error) {
      console.error('Error fetching payment requests:', error);
    }
  };

  const onSubmit = async (data) => {
    if (submitting) return;
    
    setSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      
      if (!data.vendor_id || !data.invoice_number || !data.description || !data.amount) {
        toast.error('Please fill in all required fields');
        setSubmitting(false);
        return;
      }
      
      const payableData = {
        due_date: new Date(data.due_date).toISOString(),
        vendor_id: parseInt(data.vendor_id),
        invoice_number: data.invoice_number.trim(),
        description: data.description.trim(),
        amount: parseFloat(data.amount),
        status: data.status || 'pending'
      };

      const response = await axios.post('http://localhost:8002/payables/', payableData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      toast.success('Payable added successfully!');
      reset();
      setShowAddForm(false);
      fetchPayables();
    } catch (error) {
      console.error('Error adding payable:', error);
      
      if (error.response?.status === 401) {
        toast.error('Please login again');
        window.location.href = '/login';
      } else if (error.response?.status === 422) {
        toast.error('Validation error: Please check your input data');
      } else if (error.response?.data?.detail) {
        if (Array.isArray(error.response.data.detail)) {
          const errorMessages = error.response.data.detail.map(err => err.msg).join(', ');
          toast.error(`Validation errors: ${errorMessages}`);
        } else {
          toast.error(`Error: ${error.response.data.detail}`);
        }
      } else {
        toast.error('Failed to add payable. Please try again.');
      }
    } finally {
      setSubmitting(false);
    }
  };

  const onPaymentSubmit = async (data) => {
    if (submitting) return;
    
    setSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      
      const paymentData = {
        payable_id: selectedPayable.id,
        payment_type: data.payment_type,
        requested_amount: data.payment_type === 'full' ? selectedPayable.amount : parseFloat(data.requested_amount),
        payment_channel: data.payment_channel,
        request_reason: data.request_reason,
        urgency_level: data.urgency_level
      };

      await axios.post('http://localhost:8002/payment-requests/', paymentData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      toast.success('Payment request submitted successfully!');
      resetPayment();
      setShowPaymentModal(false);
      setSelectedPayable(null);
      fetchPaymentRequests();
    } catch (error) {
      console.error('Error submitting payment request:', error);
      
      if (error.response?.status === 401) {
        toast.error('Please login again');
        window.location.href = '/login';
      } else {
        toast.error('Failed to submit payment request. Please try again.');
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handlePaymentAction = (payable) => {
    setSelectedPayable(payable);
    setShowPaymentModal(true);
    resetPayment({
      payment_type: 'full',
      requested_amount: payable.amount,
      payment_channel: 'bank_transfer',
      request_reason: '',
      urgency_level: 'normal'
    });
  };

  const handleViewDetails = (payable) => {
    setSelectedPayableDetails(payable);
    setShowDetailsModal(true);
  };

  const handleSendReminder = async (payable) => {
    try {
      const token = localStorage.getItem('token');
      // Create a notification for the vendor
      await axios.post('http://localhost:8002/notifications/', {
        user_id: payable.vendor?.id,
        title: 'Payment Reminder',
        message: `Payment reminder for Invoice ${payable.invoice_number}. Amount: ${formatCurrency(payable.outstanding_amount || payable.amount)}. Due date: ${new Date(payable.due_date).toLocaleDateString()}`,
        type: 'payment_reminder',
        priority: 'high'
      }, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      toast.success(`Reminder sent to ${payable.vendor?.name}`);
    } catch (error) {
      console.error('Error sending reminder:', error);
      toast.error('Failed to send reminder');
    }
  };

  const approvePaymentRequest = async (requestId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(`http://localhost:8002/payment-requests/${requestId}`, 
        { status: 'approved' },
        { headers: { 'Authorization': `Bearer ${token}` } }
      );
      
      toast.success('Payment request approved!');
      fetchPaymentRequests();
      fetchPayables();
    } catch (error) {
      console.error('Error approving payment request:', error);
      toast.error('Failed to approve payment request');
    }
  };

  const rejectPaymentRequest = async (requestId, reason) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(`http://localhost:8002/payment-requests/${requestId}`, 
        { status: 'rejected', rejection_reason: reason },
        { headers: { 'Authorization': `Bearer ${token}` } }
      );
      
      toast.success('Payment request rejected');
      fetchPaymentRequests();
    } catch (error) {
      console.error('Error rejecting payment request:', error);
      toast.error('Failed to reject payment request');
    }
  };

  const markPaymentPaid = async (requestId, paymentRef, notes) => {
    console.log('Marking payment as paid:', { requestId, paymentRef, notes });
    try {
      const token = localStorage.getItem('token');
      console.log('Token:', token ? 'exists' : 'missing');
      
      const response = await axios.put(`http://localhost:8002/payment-requests/${requestId}`, 
        { 
          status: 'paid', 
          payment_reference: paymentRef,
          payment_notes: notes
        },
        { headers: { 'Authorization': `Bearer ${token}` } }
      );
      
      console.log('Payment marked as paid response:', response.data);
      toast.success('Payment marked as paid!');
      fetchPaymentRequests();
      fetchPayables();
    } catch (error) {
      console.error('Error marking payment as paid:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);
      toast.error(`Failed to mark payment as paid: ${error.response?.data?.detail || error.message}`);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-PK', {
      style: 'currency',
      currency: 'PKR',
      minimumFractionDigits: 0,
    }).format(amount || 0);
  };

  const getStatusBadge = (status) => {
    const statusData = payableStatuses.find(s => s.value === status);
    if (!statusData) return null;
    
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusData.bg} ${statusData.color}`}>
        {statusData.label}
      </span>
    );
  };

  const getUrgencyBadge = (urgency) => {
    const urgencyData = urgencyLevels.find(u => u.value === urgency);
    if (!urgencyData) return null;
    
    return (
      <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${urgencyData.color}`}>
        {urgencyData.label}
      </span>
    );
  };

  const filteredPayables = payables.filter(payable => {
    const matchesSearch = 
      payable.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      payable.invoice_number?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      payable.vendor?.name?.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = !filterStatus || payable.status === filterStatus;
    const matchesVendor = !filterVendor || payable.vendor_id?.toString() === filterVendor;
    
    return matchesSearch && matchesStatus && matchesVendor;
  });

  // Calculate summary statistics from ALL payables (not filtered)
  const totalPayables = payables.reduce((sum, payable) => sum + (payable.outstanding_amount || 0), 0);
  const pendingPayables = payables.filter(p => p.status === 'pending');
  const overduePayables = payables.filter(p => p.status === 'overdue' || (p.status === 'pending' && new Date(p.due_date) < new Date()));
  const pendingRequests = paymentRequests.filter(r => r.status === 'pending');

  // Download functions
  const downloadPayablesPDF = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/reports/payables-pdf', {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `payables_report_${new Date().toISOString().split('T')[0]}.pdf`);
      
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('Payables PDF report downloaded successfully!');
    } catch (error) {
      console.error('Error downloading payables PDF:', error);
      toast.error('Failed to download payables report');
    }
  };

  const downloadPayablesExcel = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/reports/payables-excel', {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `payables_export_${new Date().toISOString().split('T')[0]}.xlsx`);
      
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('Payables Excel export downloaded successfully!');
    } catch (error) {
      console.error('Error downloading payables Excel:', error);
      toast.error('Failed to export payables data');
    }
  };

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
        <h1 className="text-2xl font-bold text-gray-900">Accounts Payable</h1>
        <div className="flex space-x-3">
          <button
            onClick={downloadPayablesPDF}
            className="btn-secondary flex items-center"
            title="Download Payables PDF Report"
          >
            <Download className="h-5 w-5 mr-2" />
            PDF Report
          </button>
          <button
            onClick={downloadPayablesExcel}
            className="btn-secondary flex items-center"
            title="Export Payables to Excel"
          >
            <Download className="h-5 w-5 mr-2" />
            Excel Export
          </button>
          <button
            onClick={() => setShowRequestsModal(true)}
            className="btn-secondary flex items-center"
          >
            <Clock className="h-5 w-5 mr-2" />
            Payment Requests ({pendingRequests.length})
          </button>
          <button
            onClick={() => setShowAddForm(true)}
            className="btn-primary flex items-center"
          >
            <Plus className="h-5 w-5 mr-2" />
            Add Payable
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '1px solid rgba(239, 68, 68, 0.2)'
        }}>
          <div className="flex items-center">
            <DollarSign className="h-8 w-8 text-red-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Payables</p>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(totalPayables)}</p>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(251, 146, 60, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '1px solid rgba(251, 146, 60, 0.2)'
        }}>
          <div className="flex items-center">
            <Clock className="h-8 w-8 text-orange-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Pending</p>
              <p className="text-2xl font-bold text-gray-900">{pendingPayables.length}</p>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '1px solid rgba(239, 68, 68, 0.2)'
        }}>
          <div className="flex items-center">
            <AlertTriangle className="h-8 w-8 text-red-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Overdue</p>
              <p className="text-2xl font-bold text-gray-900">{overduePayables.length}</p>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '1px solid rgba(34, 197, 94, 0.2)'
        }}>
          <div className="flex items-center">
            <Send className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Payment Requests</p>
              <p className="text-2xl font-bold text-gray-900">{pendingRequests.length}</p>
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
              placeholder="Search by description, invoice number, or vendor..."
              className="input-field pl-10"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <select
            value={filterVendor}
            onChange={(e) => setFilterVendor(e.target.value)}
            className="input-field"
          >
            <option value="">All Vendors</option>
            {vendors.map(vendor => (
              <option key={vendor.id} value={vendor.id}>
                {vendor.name}
              </option>
            ))}
          </select>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="input-field"
          >
            <option value="">All Status</option>
            {payableStatuses.map(status => (
              <option key={status.value} value={status.value}>
                {status.label}
              </option>
            ))}
          </select>
          <button className="btn-secondary flex items-center">
            <Download className="h-5 w-5 mr-2" />
            Export
          </button>
        </div>
      </div>

      {/* Payables List */}
      <div className="glass-card rounded-xl overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Payable Records</h3>
        </div>
        
        {filteredPayables.length === 0 ? (
          <div className="p-8 text-center">
            <CreditCard className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">No payables found</p>
            <button
              onClick={() => setShowAddForm(true)}
              className="mt-4 btn-primary"
            >
              Add Your First Payable
            </button>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vendor</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice #</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Description</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Due Date</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredPayables.map((payable) => (
                  <tr key={payable.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex items-center">
                        <Building2 className="h-4 w-4 text-gray-400 mr-2" />
                        {payable.vendor?.name || 'Unknown Vendor'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {payable.invoice_number}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {payable.description}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {formatCurrency(payable.amount)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {new Date(payable.due_date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {getStatusBadge(payable.status)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex items-center space-x-2">
                        {/* View Details Button */}
                        <button 
                          onClick={() => handleViewDetails(payable)}
                          className="p-2 rounded-lg text-blue-600 hover:bg-blue-50 hover:text-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200"
                          title="View Details"
                        >
                          <Eye className="h-5 w-5" />
                        </button>
                        
                        {/* Request Payment Button - for pending, approved, overdue */}
                        {(payable.status === 'pending' || payable.status === 'approved' || payable.status === 'overdue') && (
                          <button 
                            onClick={() => handlePaymentAction(payable)}
                            className="p-2 rounded-lg text-green-600 hover:bg-green-50 hover:text-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 transition-all duration-200"
                            title="Request Payment"
                          >
                            <Send className="h-5 w-5" />
                          </button>
                        )}
                        
                        {/* Send Reminder Button - for overdue or past due date */}
                        {(payable.status === 'overdue' || (payable.status === 'pending' && new Date(payable.due_date) < new Date())) && (
                          <button 
                            onClick={() => handleSendReminder(payable)}
                            className="p-2 rounded-lg text-orange-600 hover:bg-orange-50 hover:text-orange-700 focus:outline-none focus:ring-2 focus:ring-orange-500 transition-all duration-200"
                            title="Send Reminder"
                          >
                            <Bell className="h-5 w-5" />
                          </button>
                        )}
                        
                        {/* Paid Status Indicator */}
                        {payable.status === 'paid' && (
                          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            <CheckCircle className="h-4 w-4 mr-1" />
                            Paid
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
      {/* Add Payable Form Modal */}
      {showAddForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Add New Payable</h2>
              <button
                onClick={() => setShowAddForm(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Vendor *</label>
                  <select
                    {...register('vendor_id', { required: 'Vendor is required' })}
                    className="input-field"
                  >
                    <option value="">Select Vendor</option>
                    {vendors.map(vendor => (
                      <option key={vendor.id} value={vendor.id}>
                        {vendor.name}
                      </option>
                    ))}
                  </select>
                  {errors.vendor_id && <p className="text-red-500 text-sm mt-1">{errors.vendor_id.message}</p>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Invoice Number *</label>
                  <input
                    type="text"
                    {...register('invoice_number', { required: 'Invoice number is required' })}
                    className="input-field"
                    placeholder="INV-001"
                  />
                  {errors.invoice_number && <p className="text-red-500 text-sm mt-1">{errors.invoice_number.message}</p>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Amount (PKR) *</label>
                  <input
                    type="number"
                    step="0.01"
                    {...register('amount', { required: 'Amount is required', min: 0.01 })}
                    className="input-field"
                    placeholder="0.00"
                  />
                  {errors.amount && <p className="text-red-500 text-sm mt-1">{errors.amount.message}</p>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Due Date *</label>
                  <input
                    type="date"
                    {...register('due_date', { required: 'Due date is required' })}
                    className="input-field"
                  />
                  {errors.due_date && <p className="text-red-500 text-sm mt-1">{errors.due_date.message}</p>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                  <select
                    {...register('status')}
                    className="input-field"
                  >
                    {payableStatuses.map(status => (
                      <option key={status.value} value={status.value}>
                        {status.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description *</label>
                <textarea
                  {...register('description', { required: 'Description is required' })}
                  className="input-field"
                  rows="3"
                  placeholder="Description of goods/services..."
                />
                {errors.description && <p className="text-red-500 text-sm mt-1">{errors.description.message}</p>}
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowAddForm(false)}
                  className="btn-secondary"
                  disabled={submitting}
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="btn-primary"
                  disabled={submitting}
                >
                  {submitting ? 'Adding...' : 'Add Payable'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Payment Request Modal */}
      {showPaymentModal && selectedPayable && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Request Payment</h2>
              <button
                onClick={() => {
                  setShowPaymentModal(false);
                  setSelectedPayable(null);
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            {/* Payable Details */}
            <div className="bg-gray-50 rounded-lg p-4 mb-6">
              <h3 className="font-medium text-gray-900 mb-2">Payable Details</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Vendor:</span>
                  <span className="ml-2 font-medium">{selectedPayable.vendor?.name}</span>
                </div>
                <div>
                  <span className="text-gray-600">Invoice:</span>
                  <span className="ml-2 font-medium">{selectedPayable.invoice_number}</span>
                </div>
                <div>
                  <span className="text-gray-600">Total Amount:</span>
                  <span className="ml-2 font-medium">{formatCurrency(selectedPayable.amount)}</span>
                </div>
                <div>
                  <span className="text-gray-600">Due Date:</span>
                  <span className="ml-2 font-medium">{new Date(selectedPayable.due_date).toLocaleDateString()}</span>
                </div>
              </div>
            </div>

            <form onSubmit={handlePaymentSubmit(onPaymentSubmit)} className="space-y-4">
              {/* Payment Type */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">Payment Type *</label>
                <div className="grid grid-cols-2 gap-4">
                  <label className="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                    <input
                      type="radio"
                      {...registerPayment('payment_type')}
                      value="full"
                      className="mr-3"
                    />
                    <div>
                      <div className="font-medium">Full Payment</div>
                      <div className="text-sm text-gray-600">{formatCurrency(selectedPayable.amount)}</div>
                    </div>
                  </label>
                  <label className="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                    <input
                      type="radio"
                      {...registerPayment('payment_type')}
                      value="partial"
                      className="mr-3"
                    />
                    <div>
                      <div className="font-medium">Partial Payment</div>
                      <div className="text-sm text-gray-600">Specify amount</div>
                    </div>
                  </label>
                </div>
              </div>

              {/* Partial Amount */}
              {paymentType === 'partial' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Payment Amount (PKR) *</label>
                  <input
                    type="number"
                    step="0.01"
                    {...registerPayment('requested_amount', { 
                      required: paymentType === 'partial' ? 'Amount is required for partial payment' : false,
                      min: { value: 0.01, message: 'Amount must be greater than 0' },
                      max: { value: selectedPayable.amount, message: 'Amount cannot exceed total payable' }
                    })}
                    className="input-field"
                    placeholder="0.00"
                    max={selectedPayable.amount}
                  />
                  {paymentErrors.requested_amount && <p className="text-red-500 text-sm mt-1">{paymentErrors.requested_amount.message}</p>}
                  {paymentType === 'partial' && (
                    <p className="text-sm text-gray-600 mt-1">
                      Remaining: {formatCurrency(selectedPayable.amount - (parseFloat(watch('requested_amount')) || 0))}
                    </p>
                  )}
                </div>
              )}

              {/* Payment Channel */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">Payment Channel *</label>
                <div className="grid grid-cols-2 gap-3">
                  {paymentChannels.map(channel => {
                    const IconComponent = channel.icon;
                    return (
                      <label key={channel.value} className="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                        <input
                          type="radio"
                          {...registerPayment('payment_channel')}
                          value={channel.value}
                          className="mr-3"
                        />
                        <IconComponent className="h-5 w-5 mr-2 text-gray-600" />
                        <span className="text-sm">{channel.label}</span>
                      </label>
                    );
                  })}
                </div>
              </div>

              {/* Urgency Level */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Urgency Level</label>
                <select
                  {...registerPayment('urgency_level')}
                  className="input-field"
                >
                  {urgencyLevels.map(level => (
                    <option key={level.value} value={level.value}>
                      {level.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Request Reason */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Request Reason</label>
                <textarea
                  {...registerPayment('request_reason')}
                  className="input-field"
                  rows="3"
                  placeholder="Reason for payment request (optional)..."
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowPaymentModal(false);
                    setSelectedPayable(null);
                  }}
                  className="btn-secondary"
                  disabled={submitting}
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="btn-primary"
                  disabled={submitting}
                >
                  {submitting ? 'Submitting...' : 'Submit Request'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Payable Details Modal */}
      {showDetailsModal && selectedPayableDetails && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl p-6 w-full max-w-3xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-semibold text-gray-900">Payable Details</h2>
              <button
                onClick={() => {
                  setShowDetailsModal(false);
                  setSelectedPayableDetails(null);
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            <div className="space-y-6">
              {/* Status Banner */}
              <div className={`p-4 rounded-lg ${
                selectedPayableDetails.status === 'paid' ? 'bg-green-50 border border-green-200' :
                selectedPayableDetails.status === 'overdue' ? 'bg-red-50 border border-red-200' :
                selectedPayableDetails.status === 'approved' ? 'bg-blue-50 border border-blue-200' :
                'bg-yellow-50 border border-yellow-200'
              }`}>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      Invoice #{selectedPayableDetails.invoice_number}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {selectedPayableDetails.description}
                    </p>
                  </div>
                  {getStatusBadge(selectedPayableDetails.status)}
                </div>
              </div>

              {/* Vendor Information */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center">
                  <Building2 className="h-4 w-4 mr-2" />
                  Vendor Information
                </h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-gray-500">Vendor Name</p>
                    <p className="text-sm font-medium text-gray-900">{selectedPayableDetails.vendor?.name || 'N/A'}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Contact</p>
                    <p className="text-sm font-medium text-gray-900">{selectedPayableDetails.vendor?.contact_person || 'N/A'}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Phone</p>
                    <p className="text-sm font-medium text-gray-900">{selectedPayableDetails.vendor?.phone || 'N/A'}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Email</p>
                    <p className="text-sm font-medium text-gray-900">{selectedPayableDetails.vendor?.email || 'N/A'}</p>
                  </div>
                </div>
              </div>

              {/* Financial Information */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center">
                  <DollarSign className="h-4 w-4 mr-2" />
                  Financial Details
                </h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-gray-500">Total Amount</p>
                    <p className="text-lg font-bold text-gray-900">{formatCurrency(selectedPayableDetails.amount)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Outstanding Amount</p>
                    <p className="text-lg font-bold text-red-600">
                      {formatCurrency(selectedPayableDetails.outstanding_amount || selectedPayableDetails.amount)}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Due Date</p>
                    <p className="text-sm font-medium text-gray-900 flex items-center">
                      <Calendar className="h-4 w-4 mr-1 text-gray-400" />
                      {new Date(selectedPayableDetails.due_date).toLocaleDateString('en-US', { 
                        year: 'numeric', 
                        month: 'long', 
                        day: 'numeric' 
                      })}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Days Until Due</p>
                    <p className={`text-sm font-medium ${
                      Math.ceil((new Date(selectedPayableDetails.due_date) - new Date()) / (1000 * 60 * 60 * 24)) < 0 
                        ? 'text-red-600' 
                        : 'text-gray-900'
                    }`}>
                      {Math.ceil((new Date(selectedPayableDetails.due_date) - new Date()) / (1000 * 60 * 60 * 24))} days
                      {Math.ceil((new Date(selectedPayableDetails.due_date) - new Date()) / (1000 * 60 * 60 * 24)) < 0 && ' (Overdue)'}
                    </p>
                  </div>
                </div>
              </div>

              {/* Timestamps */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center">
                  <Clock className="h-4 w-4 mr-2" />
                  Timeline
                </h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-gray-500">Created At</p>
                    <p className="text-sm font-medium text-gray-900">
                      {selectedPayableDetails.created_at 
                        ? new Date(selectedPayableDetails.created_at).toLocaleString()
                        : 'N/A'}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Last Updated</p>
                    <p className="text-sm font-medium text-gray-900">
                      {selectedPayableDetails.updated_at 
                        ? new Date(selectedPayableDetails.updated_at).toLocaleString()
                        : 'N/A'}
                    </p>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex justify-end space-x-3 pt-4 border-t">
                {(selectedPayableDetails.status === 'pending' || selectedPayableDetails.status === 'approved' || selectedPayableDetails.status === 'overdue') && (
                  <>
                    <button
                      onClick={() => {
                        setShowDetailsModal(false);
                        handlePaymentAction(selectedPayableDetails);
                      }}
                      className="btn-primary flex items-center"
                    >
                      <Send className="h-4 w-4 mr-2" />
                      Request Payment
                    </button>
                    {(selectedPayableDetails.status === 'overdue' || new Date(selectedPayableDetails.due_date) < new Date()) && (
                      <button
                        onClick={() => {
                          handleSendReminder(selectedPayableDetails);
                          setShowDetailsModal(false);
                        }}
                        className="btn-secondary flex items-center"
                      >
                        <Bell className="h-4 w-4 mr-2" />
                        Send Reminder
                      </button>
                    )}
                  </>
                )}
                <button
                  onClick={() => {
                    setShowDetailsModal(false);
                    setSelectedPayableDetails(null);
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

      {/* Payment Requests Modal */}
      {showRequestsModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl p-6 w-full max-w-6xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Payment Requests</h2>
              <button
                onClick={() => setShowRequestsModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            {paymentRequests.length === 0 ? (
              <div className="p-8 text-center">
                <Send className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">No payment requests found</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200 text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vendor</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Channel</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Urgency</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {paymentRequests.map((request) => (
                      <tr key={request.id} className="hover:bg-gray-50">
                        <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                          {request.vendor?.name}
                        </td>
                        <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                          {request.payable?.invoice_number}
                        </td>
                        <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                          <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${
                            request.payment_type === 'full' ? 'bg-green-100 text-green-800' : 'bg-orange-100 text-orange-800'
                          }`}>
                            {request.payment_type === 'full' ? 'Full' : 'Partial'}
                          </span>
                        </td>
                        <td className="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {formatCurrency(request.requested_amount)}
                        </td>
                        <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                          {paymentChannels.find(c => c.value === request.payment_channel)?.label}
                        </td>
                        <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                          {getUrgencyBadge(request.urgency_level)}
                        </td>
                        <td className="px-4 py-4 whitespace-nowrap">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            request.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                            request.status === 'approved' ? 'bg-blue-100 text-blue-800' :
                            request.status === 'paid' ? 'bg-green-100 text-green-800' :
                            'bg-red-100 text-red-800'
                          }`}>
                            {request.status.charAt(0).toUpperCase() + request.status.slice(1)}
                          </span>
                        </td>
                        <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                          <div className="flex space-x-2">
                            {request.status === 'pending' && (
                              <>
                                <button 
                                  onClick={() => approvePaymentRequest(request.id)}
                                  className="text-green-600 hover:text-green-800"
                                  title="Approve"
                                >
                                  <Check className="h-4 w-4" />
                                </button>
                                <button 
                                  onClick={() => rejectPaymentRequest(request.id, 'Rejected by admin')}
                                  className="text-red-600 hover:text-red-800"
                                  title="Reject"
                                >
                                  <XCircle className="h-4 w-4" />
                                </button>
                              </>
                            )}
                            {request.status === 'approved' && (
                              <button 
                                onClick={() => markPaymentPaid(request.id, 'PAID-' + Date.now(), 'Payment completed')}
                                className="text-blue-600 hover:text-blue-800"
                                title="Mark as Paid"
                              >
                                <ArrowRight className="h-4 w-4" />
                              </button>
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
        </div>
      )}
    </div>
  );
};

export default Payables;