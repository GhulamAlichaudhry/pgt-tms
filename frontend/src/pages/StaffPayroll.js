import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { 
  Plus, 
  Search, 
  Users, 
  DollarSign,
  AlertTriangle,
  CheckCircle,
  Edit,
  Calculator,
  CreditCard,
  TrendingDown,
  Download,
  Printer,
  FileText,
  Eye,
  XCircle
} from 'lucide-react';

const StaffPayroll = () => {
  const navigate = useNavigate();
  const [staff, setStaff] = useState([]);
  const [payrollEntries, setPayrollEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddStaffForm, setShowAddStaffForm] = useState(false);
  const [showPayrollForm, setShowPayrollForm] = useState(false);
  const [showAdvanceForm, setShowAdvanceForm] = useState(false);
  const [showExitWarning, setShowExitWarning] = useState(false);
  const [selectedStaff, setSelectedStaff] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeTab, setActiveTab] = useState('staff'); // 'staff' or 'payroll'

  const { register, handleSubmit, reset, formState: { errors } } = useForm();
  const { register: registerPayroll, handleSubmit: handlePayrollSubmit, reset: resetPayroll, formState: { errors: payrollErrors } } = useForm();
  const { register: registerAdvance, handleSubmit: handleAdvanceSubmit, reset: resetAdvance, formState: { errors: advanceErrors } } = useForm();

  useEffect(() => {
    fetchStaff();
    fetchPayrollEntries();
  }, []);

  const fetchStaff = async () => {
    try {
      const response = await axios.get('/staff/');
      setStaff(response.data);
    } catch (error) {
      console.error('Error fetching staff:', error);
      toast.error('Failed to fetch staff');
    } finally {
      setLoading(false);
    }
  };

  const fetchPayrollEntries = async () => {
    try {
      const response = await axios.get('/payroll/');
      setPayrollEntries(response.data);
    } catch (error) {
      console.error('Error fetching payroll entries:', error);
    }
  };

  const onSubmitStaff = async (data) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post('/staff/', {
        ...data,
        gross_salary: parseFloat(data.gross_salary),
        monthly_deduction: parseFloat(data.monthly_deduction) || 0,
      }, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      toast.success('Staff member added successfully!');
      reset();
      setShowAddStaffForm(false);
      fetchStaff();
    } catch (error) {
      console.error('Error adding staff:', error);
      if (error.response?.status === 401) {
        toast.error('Please login again');
      } else if (error.response?.data?.detail) {
        toast.error(`Error: ${error.response.data.detail}`);
      } else {
        toast.error('Failed to add staff member');
      }
    }
  };

  const onSubmitPayroll = async (data) => {
    try {
      const currentDate = new Date();
      await axios.post('/payroll/', {
        ...data,
        staff_id: parseInt(data.staff_id),
        month: currentDate.getMonth() + 1,
        year: currentDate.getFullYear(),
        gross_salary: parseFloat(data.gross_salary),
        arrears: parseFloat(data.arrears) || 0,
        advance_deduction: parseFloat(data.advance_deduction) || 0,
        other_deductions: parseFloat(data.other_deductions) || 0,
      });
      toast.success('Payroll entry created successfully!');
      resetPayroll();
      setShowPayrollForm(false);
      fetchPayrollEntries();
      fetchStaff(); // Refresh to update advance balances
    } catch (error) {
      console.error('Error creating payroll entry:', error);
      toast.error('Failed to create payroll entry');
    }
  };

  const onSubmitAdvance = async (data) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`/staff/${selectedStaff.id}/advance`, {
        amount: parseFloat(data.amount),
        description: data.description,
        monthly_deduction: parseFloat(data.monthly_deduction) || selectedStaff.monthly_deduction
      }, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      toast.success('Advance given successfully!');
      resetAdvance();
      setShowAdvanceForm(false);
      setSelectedStaff(null);
      fetchStaff();
    } catch (error) {
      console.error('Error giving advance:', error);
      toast.error('Failed to give advance');
    }
  };

  const handleViewLedger = (staffMember) => {
    navigate(`/staff-advance-ledger/${staffMember.id}`);
  };

  const handleGiveAdvance = (staffMember) => {
    setSelectedStaff(staffMember);
    setShowAdvanceForm(true);
  };

  const handleMarkInactive = (staffMember) => {
    if (staffMember.advance_balance > 0) {
      setSelectedStaff(staffMember);
      setShowExitWarning(true);
    } else {
      // Proceed with marking inactive
      toast.success('Staff member can be marked as inactive');
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-PK', {
      style: 'currency',
      currency: 'PKR',
      minimumFractionDigits: 0,
    }).format(amount);
  };

  const downloadPayrollPDF = async (month = null, year = null) => {
    try {
      const currentDate = new Date();
      const targetMonth = month || currentDate.getMonth() + 1;
      const targetYear = year || currentDate.getFullYear();
      
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:8002/reports/staff-payroll-pdf?month=${targetMonth}&year=${targetYear}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        responseType: 'blob'
      });
      
      // Create blob link to download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `staff_payroll_${targetYear}_${targetMonth.toString().padStart(2, '0')}.pdf`);
      
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('Payroll report downloaded successfully!');
    } catch (error) {
      console.error('Error downloading payroll report:', error);
      toast.error('Failed to download payroll report');
    }
  };

  const printPayrollReport = (month = null, year = null) => {
    const currentDate = new Date();
    const targetMonth = month || currentDate.getMonth() + 1;
    const targetYear = year || currentDate.getFullYear();
    
    const token = localStorage.getItem('token');
    const url = `http://localhost:8002/reports/staff-payroll-pdf?month=${targetMonth}&year=${targetYear}`;
    
    const printWindow = window.open(url + `&token=${token}`, '_blank');
    if (printWindow) {
      printWindow.onload = () => {
        printWindow.print();
      };
    } else {
      toast.error('Please allow popups to print the report');
    }
  };

  const filteredStaff = staff.filter(member =>
    member.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    member.employee_id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    member.position?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const currentMonth = new Date().toLocaleDateString('en-US', { month: 'long', year: 'numeric' });

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
        <h1 className="text-2xl font-bold text-gray-900">Staff & Payroll Management</h1>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowAddStaffForm(true)}
            className="btn-secondary flex items-center"
          >
            <Plus className="h-5 w-5 mr-2" />
            Add Staff
          </button>
          <button
            onClick={() => setShowPayrollForm(true)}
            className="btn-primary flex items-center"
          >
            <Calculator className="h-5 w-5 mr-2" />
            Process Payroll
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '1px solid rgba(59, 130, 246, 0.2)'
        }}>
          <div className="flex items-center">
            <Users className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Staff</p>
              <p className="text-2xl font-bold text-gray-900">{staff.length}</p>
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
              <p className="text-sm font-medium text-gray-600">Total Advances</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatCurrency(staff.reduce((sum, member) => sum + (member.advance_balance || 0), 0))}
              </p>
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
              <p className="text-sm font-medium text-gray-600">Monthly Payroll</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatCurrency(staff.reduce((sum, member) => sum + (member.gross_salary || 0), 0))}
              </p>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(251, 146, 60, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '1px solid rgba(251, 146, 60, 0.2)'
        }}>
          <div className="flex items-center">
            <AlertTriangle className="h-8 w-8 text-orange-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">High Advances</p>
              <p className="text-2xl font-bold text-gray-900">
                {staff.filter(member => (member.advance_balance || 0) > 100000).length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="glass-card rounded-xl">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8 px-6">
            <button
              onClick={() => setActiveTab('staff')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'staff'
                  ? 'border-red-500 text-red-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Staff Management
            </button>
            <button
              onClick={() => setActiveTab('payroll')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'payroll'
                  ? 'border-red-500 text-red-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Payroll History
            </button>
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'staff' && (
            <>
              {/* Search */}
              <div className="mb-6">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                  <input
                    type="text"
                    placeholder="Search staff by name, ID, or position..."
                    className="input-field pl-10"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>

              {/* Staff List */}
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Employee</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Position</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Gross Salary</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Advance Balance</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monthly Deduction</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {filteredStaff.map((member) => (
                      <tr key={member.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            {/* Director's Exit Alert: Yellow Warning Icon */}
                            {member.advance_balance > 0 && (
                              <AlertTriangle className="h-5 w-5 text-yellow-500 mr-2" title={`Pending Advance: ${formatCurrency(member.advance_balance)}`} />
                            )}
                            <div>
                              <div className="text-sm font-medium text-gray-900">{member.name}</div>
                              <div className="text-sm text-gray-500">ID: {member.employee_id}</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {member.position}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {formatCurrency(member.gross_salary)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            (member.advance_balance || 0) > 100000
                              ? 'bg-red-100 text-red-800'
                              : (member.advance_balance || 0) > 50000
                              ? 'bg-yellow-100 text-yellow-800'
                              : (member.advance_balance || 0) > 0
                              ? 'bg-orange-100 text-orange-800'
                              : 'bg-green-100 text-green-800'
                          }`}>
                            {formatCurrency(member.advance_balance || 0)}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {formatCurrency(member.monthly_deduction || 0)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            member.is_active
                              ? 'bg-green-100 text-green-800'
                              : 'bg-gray-100 text-gray-800'
                          }`}>
                            {member.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          <div className="flex items-center space-x-2">
                            <button
                              onClick={() => handleViewLedger(member)}
                              className="text-blue-600 hover:text-blue-900"
                              title="View Advance Ledger"
                            >
                              <FileText className="h-5 w-5" />
                            </button>
                            <button
                              onClick={() => handleGiveAdvance(member)}
                              className="text-green-600 hover:text-green-900"
                              title="Give Advance"
                            >
                              <DollarSign className="h-5 w-5" />
                            </button>
                            {member.is_active && (
                              <button
                                onClick={() => handleMarkInactive(member)}
                                className="text-red-600 hover:text-red-900"
                                title="Mark as Resigned"
                              >
                                <XCircle className="h-5 w-5" />
                              </button>
                            )}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          )}

          {activeTab === 'payroll' && (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-medium text-gray-900">Payroll History - {currentMonth}</h3>
                <div className="flex space-x-2">
                  <button
                    onClick={() => downloadPayrollPDF()}
                    className="btn-secondary flex items-center text-sm"
                    title="Download PDF"
                  >
                    <Download className="h-4 w-4 mr-1" />
                    PDF
                  </button>
                  <button
                    onClick={() => printPayrollReport()}
                    className="btn-secondary flex items-center text-sm"
                    title="Print Report"
                  >
                    <Printer className="h-4 w-4 mr-1" />
                    Print
                  </button>
                </div>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Employee</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Gross Salary</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Arrears</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Advance Deduction</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Other Deductions</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Net Payable</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {payrollEntries.map((entry) => (
                      <tr key={entry.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900">{entry.staff?.name}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {formatCurrency(entry.gross_salary)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {formatCurrency(entry.arrears)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {formatCurrency(entry.advance_deduction)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {formatCurrency(entry.other_deductions)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {formatCurrency(entry.net_payable)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            entry.is_paid
                              ? 'bg-green-100 text-green-800'
                              : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            <CheckCircle className="h-3 w-3 mr-1" />
                            {entry.is_paid ? 'Paid' : 'Pending'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Add Staff Modal */}
      {showAddStaffForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Add New Staff Member</h2>
            <form onSubmit={handleSubmit(onSubmitStaff)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Employee ID</label>
                <input
                  type="text"
                  {...register('employee_id', { required: 'Employee ID is required' })}
                  className="input-field"
                  placeholder="e.g., EMP001"
                />
                {errors.employee_id && <p className="text-red-500 text-sm mt-1">{errors.employee_id.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                <input
                  type="text"
                  {...register('name', { required: 'Name is required' })}
                  className="input-field"
                  placeholder="e.g., Muhammad Ali"
                />
                {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Position</label>
                <input
                  type="text"
                  {...register('position', { required: 'Position is required' })}
                  className="input-field"
                  placeholder="e.g., Port Supervisor, Accounts Manager"
                />
                {errors.position && <p className="text-red-500 text-sm mt-1">{errors.position.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Gross Salary (PKR)</label>
                <input
                  type="number"
                  {...register('gross_salary', { required: 'Gross salary is required', min: 0 })}
                  className="input-field"
                  placeholder="50000"
                />
                {errors.gross_salary && <p className="text-red-500 text-sm mt-1">{errors.gross_salary.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Monthly Deduction (PKR)</label>
                <input
                  type="number"
                  {...register('monthly_deduction')}
                  className="input-field"
                  placeholder="0"
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowAddStaffForm(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Add Staff
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Process Payroll Modal */}
      {showPayrollForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Process Payroll - {currentMonth}</h2>
            <form onSubmit={handlePayrollSubmit(onSubmitPayroll)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Select Staff</label>
                <select
                  {...registerPayroll('staff_id', { required: 'Staff selection is required' })}
                  className="input-field"
                >
                  <option value="">Select Staff Member</option>
                  {staff.map(member => (
                    <option key={member.id} value={member.id}>
                      {member.name} - {member.position}
                    </option>
                  ))}
                </select>
                {payrollErrors.staff_id && <p className="text-red-500 text-sm mt-1">{payrollErrors.staff_id.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Gross Salary (PKR)</label>
                <input
                  type="number"
                  {...registerPayroll('gross_salary', { required: 'Gross salary is required', min: 0 })}
                  className="input-field"
                  placeholder="50000"
                />
                {payrollErrors.gross_salary && <p className="text-red-500 text-sm mt-1">{payrollErrors.gross_salary.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Arrears (PKR)</label>
                <input
                  type="number"
                  {...registerPayroll('arrears')}
                  className="input-field"
                  placeholder="0"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Advance Deduction (PKR)</label>
                <input
                  type="number"
                  {...registerPayroll('advance_deduction')}
                  className="input-field"
                  placeholder="0"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Other Deductions (PKR)</label>
                <input
                  type="number"
                  {...registerPayroll('other_deductions')}
                  className="input-field"
                  placeholder="0"
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowPayrollForm(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Process Payroll
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Give Advance Modal */}
      {showAdvanceForm && selectedStaff && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Give Advance - {selectedStaff.name}</h2>
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
              <p className="text-sm text-yellow-800">
                Current Balance: <span className="font-bold">{formatCurrency(selectedStaff.advance_balance || 0)}</span>
              </p>
            </div>
            <form onSubmit={handleAdvanceSubmit(onSubmitAdvance)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Advance Amount (PKR)</label>
                <input
                  type="number"
                  {...registerAdvance('amount', { required: 'Amount is required', min: 1 })}
                  className="input-field"
                  placeholder="e.g., 5000"
                />
                {advanceErrors.amount && <p className="text-red-500 text-sm mt-1">{advanceErrors.amount.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  {...registerAdvance('description', { required: 'Description is required' })}
                  className="input-field"
                  rows="2"
                  placeholder="e.g., Emergency advance, Medical expenses"
                />
                {advanceErrors.description && <p className="text-red-500 text-sm mt-1">{advanceErrors.description.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Monthly Deduction (PKR)</label>
                <input
                  type="number"
                  {...registerAdvance('monthly_deduction')}
                  className="input-field"
                  placeholder={selectedStaff.monthly_deduction || "10000"}
                  defaultValue={selectedStaff.monthly_deduction}
                />
                <p className="text-xs text-gray-500 mt-1">Leave blank to keep current deduction</p>
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowAdvanceForm(false);
                    setSelectedStaff(null);
                    resetAdvance();
                  }}
                  className="btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Give Advance
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Director's Exit Warning Modal */}
      {showExitWarning && selectedStaff && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-xl p-6 w-full max-w-md" style={{
            background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(255, 255, 255, 0.95) 100%)',
            border: '3px solid rgba(239, 68, 68, 0.5)'
          }}>
            <div className="flex items-center space-x-3 mb-4">
              <AlertTriangle className="h-12 w-12 text-red-600" />
              <h2 className="text-xl font-bold text-red-600">Settlement Required!</h2>
            </div>
            
            <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4 mb-4">
              <p className="text-sm text-gray-700 mb-2">
                <span className="font-bold">{selectedStaff.name}</span> has a pending advance balance:
              </p>
              <p className="text-3xl font-bold text-red-600 text-center my-3">
                {formatCurrency(selectedStaff.advance_balance)}
              </p>
              <p className="text-sm text-gray-600 text-center">
                This employee cannot be marked as resigned until the advance is settled.
              </p>
            </div>

            <div className="space-y-2 mb-4">
              <p className="text-sm font-medium text-gray-700">Options:</p>
              <ul className="text-sm text-gray-600 space-y-1 ml-4">
                <li>• Recover the full amount before exit</li>
                <li>• Deduct from final settlement</li>
                <li>• Create a recovery plan</li>
              </ul>
            </div>

            <div className="flex justify-end space-x-3">
              <button
                onClick={() => {
                  setShowExitWarning(false);
                  setSelectedStaff(null);
                }}
                className="btn-secondary"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  handleViewLedger(selectedStaff);
                  setShowExitWarning(false);
                }}
                className="btn-primary"
              >
                View Ledger
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StaffPayroll;