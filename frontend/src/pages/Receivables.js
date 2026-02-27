import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { 
  Plus, 
  Search, 
  Download,
  DollarSign,
  Calendar,
  Building2,
  AlertTriangle,
  CheckCircle,
  Clock,
  X,
  Eye,
  CreditCard,
  Banknote,
  Smartphone,
  FileText,
  TrendingUp,
  Bell,
  Send,
  Mail,
  Printer
} from 'lucide-react';

const Receivables = () => {
  const location = useLocation();
  const [receivables, setReceivables] = useState([]);
  const [clients, setClients] = useState([]);
  const [collections, setCollections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showCollectionModal, setShowCollectionModal] = useState(false);
  const [selectedReceivable, setSelectedReceivable] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [filterClient, setFilterClient] = useState(location.state?.clientId?.toString() || '');
  const [submitting, setSubmitting] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [selectedReceivableDetails, setSelectedReceivableDetails] = useState(null);

  const { register, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: {
      due_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      client_id: '',
      invoice_number: '',
      description: '',
      total_amount: '',
      payment_terms: 30
    }
  });

  const { register: registerCollection, handleSubmit: handleCollectionSubmit, reset: resetCollection, formState: { errors: collectionErrors } } = useForm({
    defaultValues: {
      collection_amount: '',
      collection_date: new Date().toISOString().split('T')[0],
      collection_channel: 'bank_transfer',
      reference_number: '',
      notes: ''
    }
  });

  const receivableStatuses = [
    { value: 'pending', label: 'Pending', color: 'text-yellow-600', bg: 'bg-yellow-100' },
    { value: 'partially_paid', label: 'Partially Paid', color: 'text-orange-600', bg: 'bg-orange-100' },
    { value: 'paid', label: 'Paid', color: 'text-green-600', bg: 'bg-green-100' },
    { value: 'overdue', label: 'Overdue', color: 'text-red-600', bg: 'bg-red-100' },
    { value: 'cancelled', label: 'Cancelled', color: 'text-gray-600', bg: 'bg-gray-100' }
  ];

  const collectionChannels = [
    { value: 'bank_transfer', label: 'Bank Transfer', icon: Building2 },
    { value: 'cash', label: 'Cash', icon: Banknote },
    { value: 'cheque', label: 'Cheque', icon: FileText },
    { value: 'online_transfer', label: 'Online Transfer', icon: CreditCard },
    { value: 'mobile_banking', label: 'Mobile Banking', icon: Smartphone },
    { value: 'credit_card', label: 'Credit Card', icon: CreditCard }
  ];

  useEffect(() => {
    fetchReceivables();
    fetchClients();
  }, []);

  const fetchReceivables = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8002/receivables/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setReceivables(response.data);
    } catch (error) {
      console.error('Error fetching receivables:', error);
      if (error.response?.status === 401) {
        toast.error('Please login again');
        window.location.href = '/login';
      } else {
        toast.error('Failed to fetch receivables');
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchClients = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8002/clients/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setClients(response.data);
    } catch (error) {
      console.error('Error fetching clients:', error);
    }
  };

  const onSubmit = async (data) => {
    if (submitting) return;
    
    setSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      
      const receivableData = {
        client_id: parseInt(data.client_id),
        invoice_number: data.invoice_number.trim(),
        description: data.description.trim(),
        total_amount: parseFloat(data.total_amount),
        invoice_date: new Date().toISOString(),
        due_date: new Date(data.due_date).toISOString(),
        payment_terms: parseInt(data.payment_terms)
      };

      await axios.post('http://localhost:8002/receivables/', receivableData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      toast.success('Receivable created successfully!');
      reset();
      setShowAddForm(false);
      fetchReceivables();
    } catch (error) {
      console.error('Error creating receivable:', error);
      
      if (error.response?.status === 401) {
        toast.error('Please login again');
        window.location.href = '/login';
      } else {
        toast.error('Failed to create receivable. Please try again.');
      }
    } finally {
      setSubmitting(false);
    }
  };

  const onCollectionSubmit = async (data) => {
    if (submitting) return;
    
    setSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      
      const collectionData = {
        receivable_id: selectedReceivable.id,
        collection_amount: parseFloat(data.collection_amount),
        collection_date: new Date(data.collection_date).toISOString(),
        collection_channel: data.collection_channel,
        reference_number: data.reference_number,
        notes: data.notes
      };

      await axios.post('http://localhost:8002/collections/', collectionData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      toast.success('Payment collected successfully!');
      resetCollection();
      setShowCollectionModal(false);
      setSelectedReceivable(null);
      fetchReceivables();
    } catch (error) {
      console.error('Error collecting payment:', error);
      
      if (error.response?.status === 401) {
        toast.error('Please login again');
        window.location.href = '/login';
      } else {
        toast.error('Failed to collect payment. Please try again.');
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleCollectPayment = (receivable) => {
    setSelectedReceivable(receivable);
    setShowCollectionModal(true);
    resetCollection({
      collection_amount: receivable.remaining_amount,
      collection_date: new Date().toISOString().split('T')[0],
      collection_channel: 'bank_transfer',
      reference_number: '',
      notes: ''
    });
  };

  const handleViewDetails = (receivable) => {
    setSelectedReceivableDetails(receivable);
    setShowDetailsModal(true);
  };

  const handleSendReminder = async (receivable) => {
    try {
      const token = localStorage.getItem('token');
      // Create a notification for the client
      await axios.post('http://localhost:8002/notifications/', {
        user_id: receivable.client?.id,
        title: 'Payment Reminder',
        message: `Payment reminder for Invoice ${receivable.invoice_number}. Amount due: ${formatCurrency(receivable.remaining_amount)}. Due date: ${new Date(receivable.due_date).toLocaleDateString()}`,
        type: 'payment_reminder',
        priority: 'high'
      }, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      toast.success(`Reminder sent to ${receivable.client?.name}`);
    } catch (error) {
      console.error('Error sending reminder:', error);
      toast.error('Failed to send reminder');
    }
  };

  // ============================================
  // INVOICE HANDLERS
  // ============================================

  const handleGenerateInvoice = async (receivable) => {
    if (!receivable.trip_id) {
      toast.error('No trip associated with this receivable');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      toast.loading('Generating invoice...', { id: 'generate-invoice' });
      
      const response = await axios.post(
        `http://localhost:8002/invoices/generate-from-trip/${receivable.trip_id}`,
        null,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      );
      
      toast.success('Invoice generated successfully!', { id: 'generate-invoice' });
      fetchReceivables(); // Refresh to show updated status
    } catch (error) {
      console.error('Error generating invoice:', error);
      toast.error(error.response?.data?.detail || 'Failed to generate invoice', { id: 'generate-invoice' });
    }
  };

  const handleViewInvoice = async (receivable) => {
    try {
      const token = localStorage.getItem('token');
      toast.loading('Loading invoice...', { id: 'view-invoice' });
      
      const response = await axios.get(
        `http://localhost:8002/invoices/${receivable.id}/pdf`,
        {
          headers: { 'Authorization': `Bearer ${token}` },
          responseType: 'blob'
        }
      );
      
      // Create blob URL and open in new tab
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      window.open(url, '_blank');
      
      toast.success('Invoice opened', { id: 'view-invoice' });
    } catch (error) {
      console.error('Error viewing invoice:', error);
      toast.error('Failed to load invoice', { id: 'view-invoice' });
    }
  };

  const handleEmailInvoice = async (receivable) => {
    if (!receivable.client?.email) {
      toast.error('Client email not found');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      toast.loading('Sending invoice...', { id: 'email-invoice' });
      
      await axios.post(
        `http://localhost:8002/invoices/${receivable.id}/email`,
        null,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      );
      
      toast.success(`Invoice emailed to ${receivable.client.email}`, { id: 'email-invoice' });
      fetchReceivables(); // Refresh to show updated status
    } catch (error) {
      console.error('Error emailing invoice:', error);
      toast.error(error.response?.data?.detail || 'Failed to email invoice', { id: 'email-invoice' });
    }
  };

  const handleDownloadInvoice = async (receivable) => {
    try {
      const token = localStorage.getItem('token');
      toast.loading('Downloading invoice...', { id: 'download-invoice' });
      
      const response = await axios.get(
        `http://localhost:8002/invoices/${receivable.id}/pdf`,
        {
          headers: { 'Authorization': `Bearer ${token}` },
          responseType: 'blob'
        }
      );
      
      // Create download link
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${receivable.invoice_number}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      toast.success('Invoice downloaded', { id: 'download-invoice' });
    } catch (error) {
      console.error('Error downloading invoice:', error);
      toast.error('Failed to download invoice', { id: 'download-invoice' });
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
    const statusData = receivableStatuses.find(s => s.value === status);
    if (!statusData) return null;
    
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusData.bg} ${statusData.color}`}>
        {statusData.label}
      </span>
    );
  };

  const getDaysOverdue = (dueDate) => {
    const today = new Date();
    const due = new Date(dueDate);
    const diffTime = today - due;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays > 0 ? diffDays : 0;
  };

  const filteredReceivables = receivables.filter(receivable => {
    const matchesSearch = 
      receivable.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      receivable.invoice_number?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      receivable.client?.name?.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = !filterStatus || receivable.status === filterStatus;
    const matchesClient = !filterClient || receivable.client_id?.toString() === filterClient;
    
    return matchesSearch && matchesStatus && matchesClient;
  });

  // Calculate summary statistics
  const totalReceivables = filteredReceivables.reduce((sum, receivable) => sum + (receivable.remaining_amount || 0), 0);
  const pendingReceivables = receivables.filter(r => r.status === 'pending');
  const overdueReceivables = receivables.filter(r => r.status === 'overdue' || getDaysOverdue(r.due_date) > 0);

  // Download functions
  const downloadReceivablesPDF = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/reports/receivables-pdf', {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `receivables_report_${new Date().toISOString().split('T')[0]}.pdf`);
      
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('Receivables PDF report downloaded successfully!');
    } catch (error) {
      console.error('Error downloading receivables PDF:', error);
      toast.error('Failed to download receivables report');
    }
  };

  const downloadReceivablesExcel = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/reports/receivables-excel', {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `receivables_export_${new Date().toISOString().split('T')[0]}.xlsx`);
      
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('Receivables Excel export downloaded successfully!');
    } catch (error) {
      console.error('Error downloading receivables Excel:', error);
      toast.error('Failed to export receivables data');
    }
  };

  const paidThisMonth = receivables.filter(r => {
    const paidDate = new Date(r.last_payment_date);
    const now = new Date();
    return r.last_payment_date && paidDate.getMonth() === now.getMonth() && paidDate.getFullYear() === now.getFullYear();
  });

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
        <h1 className="text-2xl font-bold text-gray-900">Accounts Receivable</h1>
        <div className="flex space-x-3">
          <button
            onClick={downloadReceivablesPDF}
            className="btn-secondary flex items-center"
            title="Download Receivables PDF Report"
          >
            <Download className="h-5 w-5 mr-2" />
            PDF Report
          </button>
          <button
            onClick={downloadReceivablesExcel}
            className="btn-secondary flex items-center"
            title="Export Receivables to Excel"
          >
            <Download className="h-5 w-5 mr-2" />
            Excel Export
          </button>
          <button
            onClick={() => setShowAddForm(true)}
            className="btn-primary flex items-center"
          >
            <Plus className="h-5 w-5 mr-2" />
            Add Receivable
          </button>
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
              <p className="text-sm font-medium text-gray-600">Total Receivables</p>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(totalReceivables)}</p>
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
              <p className="text-2xl font-bold text-gray-900">{pendingReceivables.length}</p>
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
              <p className="text-2xl font-bold text-gray-900">{overdueReceivables.length}</p>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '1px solid rgba(34, 197, 94, 0.2)'
        }}>
          <div className="flex items-center">
            <CheckCircle className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Collected This Month</p>
              <p className="text-2xl font-bold text-gray-900">{paidThisMonth.length}</p>
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
              placeholder="Search by description, invoice number, or client..."
              className="input-field pl-10"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <select
            value={filterClient}
            onChange={(e) => setFilterClient(e.target.value)}
            className="input-field"
          >
            <option value="">All Clients</option>
            {clients.map(client => (
              <option key={client.id} value={client.id}>
                {client.name}
              </option>
            ))}
          </select>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="input-field"
          >
            <option value="">All Status</option>
            {receivableStatuses.map(status => (
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

      {/* Receivables List */}
      <div className="glass-card rounded-xl overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Receivable Records</h3>
        </div>
        
        {filteredReceivables.length === 0 ? (
          <div className="p-8 text-center">
            <TrendingUp className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">No receivables found</p>
            <button
              onClick={() => setShowAddForm(true)}
              className="mt-4 btn-primary"
            >
              Add Your First Receivable
            </button>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Client</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice #</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Description</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total Amount</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Paid</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Remaining</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Due Date</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredReceivables.map((receivable) => (
                  <tr key={receivable.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex items-center">
                        <Building2 className="h-4 w-4 text-gray-400 mr-2" />
                        {receivable.client?.name || 'Unknown Client'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {receivable.invoice_number}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {receivable.description}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {formatCurrency(receivable.total_amount)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">
                      {formatCurrency(receivable.paid_amount)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600 font-medium">
                      {formatCurrency(receivable.remaining_amount)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div>
                        {new Date(receivable.due_date).toLocaleDateString()}
                        {getDaysOverdue(receivable.due_date) > 0 && (
                          <div className="text-xs text-red-600">
                            {getDaysOverdue(receivable.due_date)} days overdue
                          </div>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {getStatusBadge(receivable.status)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex items-center space-x-2">
                        {/* View Details Button */}
                        <button 
                          onClick={() => handleViewDetails(receivable)}
                          className="p-2 rounded-lg text-blue-600 hover:bg-blue-50 hover:text-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200"
                          title="View Details"
                        >
                          <Eye className="h-5 w-5" />
                        </button>
                        
                        {/* Invoice Buttons */}
                        {receivable.trip_id && (
                          <>
                            {/* Generate/View Invoice Button */}
                            <button 
                              onClick={() => handleViewInvoice(receivable)}
                              className="p-2 rounded-lg text-purple-600 hover:bg-purple-50 hover:text-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all duration-200"
                              title="View Invoice PDF"
                            >
                              <FileText className="h-5 w-5" />
                            </button>
                            
                            {/* Download Invoice Button */}
                            <button 
                              onClick={() => handleDownloadInvoice(receivable)}
                              className="p-2 rounded-lg text-indigo-600 hover:bg-indigo-50 hover:text-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all duration-200"
                              title="Download Invoice"
                            >
                              <Download className="h-5 w-5" />
                            </button>
                            
                            {/* Email Invoice Button */}
                            {receivable.client?.email && (
                              <button 
                                onClick={() => handleEmailInvoice(receivable)}
                                className="p-2 rounded-lg text-cyan-600 hover:bg-cyan-50 hover:text-cyan-700 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all duration-200"
                                title="Email Invoice to Client"
                              >
                                <Mail className="h-5 w-5" />
                              </button>
                            )}
                          </>
                        )}
                        
                        {/* Collect Payment Button - for pending, partially_paid, overdue */}
                        {receivable.remaining_amount > 0 && (
                          <button 
                            onClick={() => handleCollectPayment(receivable)}
                            className="p-2 rounded-lg text-green-600 hover:bg-green-50 hover:text-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 transition-all duration-200"
                            title="Collect Payment"
                          >
                            <DollarSign className="h-5 w-5" />
                          </button>
                        )}
                        
                        {/* Send Reminder Button - for overdue or past due date */}
                        {(receivable.status === 'overdue' || getDaysOverdue(receivable.due_date) > 0) && (
                          <button 
                            onClick={() => handleSendReminder(receivable)}
                            className="p-2 rounded-lg text-orange-600 hover:bg-orange-50 hover:text-orange-700 focus:outline-none focus:ring-2 focus:ring-orange-500 transition-all duration-200"
                            title="Send Reminder"
                          >
                            <Bell className="h-5 w-5" />
                          </button>
                        )}
                        
                        {/* Paid Status Indicator */}
                        {receivable.status === 'paid' && receivable.remaining_amount === 0 && (
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

      {/* Receivable Details Modal */}
      {showDetailsModal && selectedReceivableDetails && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl p-6 w-full max-w-3xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-semibold text-gray-900">Receivable Details</h2>
              <button
                onClick={() => {
                  setShowDetailsModal(false);
                  setSelectedReceivableDetails(null);
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            <div className="space-y-6">
              {/* Status Banner */}
              <div className={`p-4 rounded-lg ${
                selectedReceivableDetails.status === 'paid' ? 'bg-green-50 border border-green-200' :
                selectedReceivableDetails.status === 'overdue' ? 'bg-red-50 border border-red-200' :
                selectedReceivableDetails.status === 'partially_paid' ? 'bg-orange-50 border border-orange-200' :
                'bg-yellow-50 border border-yellow-200'
              }`}>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      Invoice #{selectedReceivableDetails.invoice_number}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {selectedReceivableDetails.description}
                    </p>
                  </div>
                  {getStatusBadge(selectedReceivableDetails.status)}
                </div>
              </div>

              {/* Client Information */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center">
                  <Building2 className="h-4 w-4 mr-2" />
                  Client Information
                </h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-gray-500">Client Name</p>
                    <p className="text-sm font-medium text-gray-900">{selectedReceivableDetails.client?.name || 'N/A'}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Contact</p>
                    <p className="text-sm font-medium text-gray-900">{selectedReceivableDetails.client?.contact_person || 'N/A'}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Phone</p>
                    <p className="text-sm font-medium text-gray-900">{selectedReceivableDetails.client?.phone || 'N/A'}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Email</p>
                    <p className="text-sm font-medium text-gray-900">{selectedReceivableDetails.client?.email || 'N/A'}</p>
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
                    <p className="text-lg font-bold text-gray-900">{formatCurrency(selectedReceivableDetails.total_amount)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Paid Amount</p>
                    <p className="text-lg font-bold text-green-600">
                      {formatCurrency(selectedReceivableDetails.paid_amount || 0)}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Remaining Amount</p>
                    <p className="text-lg font-bold text-red-600">
                      {formatCurrency(selectedReceivableDetails.remaining_amount || selectedReceivableDetails.total_amount)}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Payment Terms</p>
                    <p className="text-sm font-medium text-gray-900">
                      {selectedReceivableDetails.payment_terms || 30} days
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Invoice Date</p>
                    <p className="text-sm font-medium text-gray-900 flex items-center">
                      <Calendar className="h-4 w-4 mr-1 text-gray-400" />
                      {new Date(selectedReceivableDetails.invoice_date).toLocaleDateString('en-US', { 
                        year: 'numeric', 
                        month: 'long', 
                        day: 'numeric' 
                      })}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Due Date</p>
                    <p className="text-sm font-medium text-gray-900 flex items-center">
                      <Calendar className="h-4 w-4 mr-1 text-gray-400" />
                      {new Date(selectedReceivableDetails.due_date).toLocaleDateString('en-US', { 
                        year: 'numeric', 
                        month: 'long', 
                        day: 'numeric' 
                      })}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Days Until Due</p>
                    <p className={`text-sm font-medium ${
                      Math.ceil((new Date(selectedReceivableDetails.due_date) - new Date()) / (1000 * 60 * 60 * 24)) < 0 
                        ? 'text-red-600' 
                        : 'text-gray-900'
                    }`}>
                      {Math.ceil((new Date(selectedReceivableDetails.due_date) - new Date()) / (1000 * 60 * 60 * 24))} days
                      {Math.ceil((new Date(selectedReceivableDetails.due_date) - new Date()) / (1000 * 60 * 60 * 24)) < 0 && ' (Overdue)'}
                    </p>
                  </div>
                  {selectedReceivableDetails.last_payment_date && (
                    <div>
                      <p className="text-xs text-gray-500">Last Payment</p>
                      <p className="text-sm font-medium text-gray-900">
                        {new Date(selectedReceivableDetails.last_payment_date).toLocaleDateString()}
                      </p>
                    </div>
                  )}
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
                      {selectedReceivableDetails.created_at 
                        ? new Date(selectedReceivableDetails.created_at).toLocaleString()
                        : 'N/A'}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Last Updated</p>
                    <p className="text-sm font-medium text-gray-900">
                      {selectedReceivableDetails.updated_at 
                        ? new Date(selectedReceivableDetails.updated_at).toLocaleString()
                        : 'N/A'}
                    </p>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex justify-end space-x-3 pt-4 border-t">
                {selectedReceivableDetails.remaining_amount > 0 && (
                  <>
                    <button
                      onClick={() => {
                        setShowDetailsModal(false);
                        handleCollectPayment(selectedReceivableDetails);
                      }}
                      className="btn-primary flex items-center"
                    >
                      <DollarSign className="h-4 w-4 mr-2" />
                      Collect Payment
                    </button>
                    {(selectedReceivableDetails.status === 'overdue' || getDaysOverdue(selectedReceivableDetails.due_date) > 0) && (
                      <button
                        onClick={() => {
                          handleSendReminder(selectedReceivableDetails);
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
                    setSelectedReceivableDetails(null);
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

      {/* Add Receivable Form Modal */}
      {showAddForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Add New Receivable</h2>
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
                  <label className="block text-sm font-medium text-gray-700 mb-1">Client *</label>
                  <select
                    {...register('client_id', { required: 'Client is required' })}
                    className="input-field"
                  >
                    <option value="">Select Client</option>
                    {clients.map(client => (
                      <option key={client.id} value={client.id}>
                        {client.name}
                      </option>
                    ))}
                  </select>
                  {errors.client_id && <p className="text-red-500 text-sm mt-1">{errors.client_id.message}</p>}
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
                    {...register('total_amount', { required: 'Amount is required', min: 0.01 })}
                    className="input-field"
                    placeholder="0.00"
                  />
                  {errors.total_amount && <p className="text-red-500 text-sm mt-1">{errors.total_amount.message}</p>}
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
                  <label className="block text-sm font-medium text-gray-700 mb-1">Payment Terms (Days)</label>
                  <input
                    type="number"
                    {...register('payment_terms')}
                    className="input-field"
                    placeholder="30"
                  />
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
                  {submitting ? 'Creating...' : 'Create Receivable'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Collection Modal */}
      {showCollectionModal && selectedReceivable && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Collect Payment</h2>
              <button
                onClick={() => {
                  setShowCollectionModal(false);
                  setSelectedReceivable(null);
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            {/* Receivable Details */}
            <div className="bg-gray-50 rounded-lg p-4 mb-6">
              <h3 className="font-medium text-gray-900 mb-2">Receivable Details</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Client:</span>
                  <span className="ml-2 font-medium">{selectedReceivable.client?.name}</span>
                </div>
                <div>
                  <span className="text-gray-600">Invoice:</span>
                  <span className="ml-2 font-medium">{selectedReceivable.invoice_number}</span>
                </div>
                <div>
                  <span className="text-gray-600">Total Amount:</span>
                  <span className="ml-2 font-medium">{formatCurrency(selectedReceivable.total_amount)}</span>
                </div>
                <div>
                  <span className="text-gray-600">Remaining:</span>
                  <span className="ml-2 font-medium text-red-600">{formatCurrency(selectedReceivable.remaining_amount)}</span>
                </div>
              </div>
            </div>

            <form onSubmit={handleCollectionSubmit(onCollectionSubmit)} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Collection Amount (PKR) *</label>
                  <input
                    type="number"
                    step="0.01"
                    {...registerCollection('collection_amount', { 
                      required: 'Collection amount is required',
                      min: { value: 0.01, message: 'Amount must be greater than 0' },
                      max: { value: selectedReceivable.remaining_amount, message: 'Amount cannot exceed remaining balance' }
                    })}
                    className="input-field"
                    placeholder="0.00"
                    max={selectedReceivable.remaining_amount}
                  />
                  {collectionErrors.collection_amount && <p className="text-red-500 text-sm mt-1">{collectionErrors.collection_amount.message}</p>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Collection Date *</label>
                  <input
                    type="date"
                    {...registerCollection('collection_date', { required: 'Collection date is required' })}
                    className="input-field"
                  />
                  {collectionErrors.collection_date && <p className="text-red-500 text-sm mt-1">{collectionErrors.collection_date.message}</p>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Collection Channel *</label>
                  <select
                    {...registerCollection('collection_channel')}
                    className="input-field"
                  >
                    {collectionChannels.map(channel => (
                      <option key={channel.value} value={channel.value}>
                        {channel.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Reference Number</label>
                  <input
                    type="text"
                    {...registerCollection('reference_number')}
                    className="input-field"
                    placeholder="Bank ref, cheque number, etc."
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Notes</label>
                <textarea
                  {...registerCollection('notes')}
                  className="input-field"
                  rows="3"
                  placeholder="Additional notes about the collection..."
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowCollectionModal(false);
                    setSelectedReceivable(null);
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
                  {submitting ? 'Collecting...' : 'Collect Payment'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Receivables;