import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { 
  ArrowLeft, 
  Printer, 
  Download,
  TrendingDown,
  TrendingUp,
  Calendar,
  User,
  Briefcase,
  DollarSign,
  AlertCircle,
  FileText
} from 'lucide-react';

const StaffAdvanceLedger = () => {
  const { staffId } = useParams();
  const navigate = useNavigate();
  const [ledgerData, setLedgerData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLedgerData();
  }, [staffId]);

  const fetchLedgerData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`/staff/${staffId}/advance-ledger`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setLedgerData(response.data);
    } catch (error) {
      console.error('Error fetching ledger:', error);
      toast.error('Failed to fetch advance ledger');
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-PK', {
      style: 'currency',
      currency: 'PKR',
      minimumFractionDigits: 0,
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-PK', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  };

  const printStatement = () => {
    const printWindow = window.open('', '', 'height=800,width=1000');
    const staff = ledgerData.staff;
    const summary = ledgerData.advance_summary;
    const entries = ledgerData.ledger_entries;

    printWindow.document.write(`
      <html>
      <head>
        <title>Staff Advance Statement - ${staff.name}</title>
        <style>
          @media print {
            @page { margin: 0.5in; }
          }
          body {
            font-family: 'Arial', sans-serif;
            padding: 20px;
            color: #1f2937;
          }
          .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 3px solid #dc2626;
            padding-bottom: 20px;
          }
          .company-name {
            font-size: 28px;
            font-weight: bold;
            color: #dc2626;
            margin-bottom: 5px;
          }
          .company-tagline {
            font-size: 12px;
            color: #6b7280;
            font-style: italic;
            margin-bottom: 10px;
          }
          .company-details {
            font-size: 11px;
            color: #374151;
          }
          .statement-title {
            font-size: 20px;
            font-weight: bold;
            color: #374151;
            margin: 20px 0;
            text-align: center;
          }
          .employee-info {
            background: #f9fafb;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #dc2626;
          }
          .info-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 13px;
          }
          .info-label {
            font-weight: 600;
            color: #6b7280;
          }
          .info-value {
            color: #1f2937;
          }
          table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 12px;
          }
          th {
            background: #dc2626;
            color: white;
            padding: 12px 8px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 11px;
          }
          td {
            padding: 10px 8px;
            border-bottom: 1px solid #e5e7eb;
          }
          tr:hover {
            background: #f9fafb;
          }
          .debit {
            color: #dc2626;
            font-weight: 600;
          }
          .credit {
            color: #059669;
            font-weight: 600;
          }
          .balance {
            font-weight: 700;
            color: #1f2937;
          }
          .summary-box {
            background: #fef2f2;
            border: 2px solid #dc2626;
            padding: 20px;
            border-radius: 8px;
            margin: 30px 0;
          }
          .summary-title {
            font-size: 16px;
            font-weight: bold;
            color: #dc2626;
            margin-bottom: 15px;
          }
          .summary-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 14px;
          }
          .summary-label {
            font-weight: 600;
          }
          .summary-value {
            font-weight: 700;
            color: #dc2626;
          }
          .signature-section {
            margin-top: 60px;
            display: flex;
            justify-content: space-between;
          }
          .signature-box {
            text-align: center;
          }
          .signature-line {
            border-top: 2px solid #374151;
            width: 200px;
            margin: 40px auto 10px;
          }
          .signature-label {
            font-size: 12px;
            color: #6b7280;
            font-weight: 600;
          }
          .footer {
            margin-top: 40px;
            text-align: center;
            font-size: 10px;
            color: #9ca3af;
            border-top: 1px solid #e5e7eb;
            padding-top: 15px;
          }
          .watermark {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-45deg);
            font-size: 120px;
            color: rgba(220, 38, 38, 0.05);
            font-weight: bold;
            z-index: -1;
            pointer-events: none;
          }
        </style>
      </head>
      <body>
        <div class="watermark">PGT INTERNATIONAL</div>
        
        <div class="header">
          <div class="company-name">PGT INTERNATIONAL (PRIVATE) LIMITED</div>
          <div class="company-tagline">Excellence in Transportation & Logistics</div>
          <div class="company-details">
            Office # 1, 1st Floor, Haji Yousuf Plaza, Opposite Pak Arab Fertilizer, Multan Road, Lahore<br>
            Phone: +92-42-35291747 | Email: info@pgtinternational.com | Web: www.pgtinternational.com
          </div>
        </div>

        <div class="statement-title">STAFF ADVANCE STATEMENT</div>

        <div class="employee-info">
          <div class="info-row">
            <span class="info-label">Employee Name:</span>
            <span class="info-value">${staff.name}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Employee ID:</span>
            <span class="info-value">${staff.employee_id}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Position:</span>
            <span class="info-value">${staff.position}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Gross Salary:</span>
            <span class="info-value">${formatCurrency(staff.gross_salary)}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Statement Date:</span>
            <span class="info-value">${new Date().toLocaleDateString('en-PK', { day: '2-digit', month: 'long', year: 'numeric' })}</span>
          </div>
        </div>

        <table>
          <thead>
            <tr>
              <th style="width: 15%">Date</th>
              <th style="width: 35%">Description</th>
              <th style="width: 15%; text-align: right">Debit (Advance)</th>
              <th style="width: 15%; text-align: right">Credit (Recovery)</th>
              <th style="width: 20%; text-align: right">Running Balance</th>
            </tr>
          </thead>
          <tbody>
            ${entries.map(entry => `
              <tr>
                <td>${formatDate(entry.date)}</td>
                <td>${entry.description}</td>
                <td style="text-align: right" class="${entry.amount > 0 ? 'debit' : ''}">
                  ${entry.amount > 0 ? formatCurrency(entry.amount) : '-'}
                </td>
                <td style="text-align: right" class="${entry.amount < 0 ? 'credit' : ''}">
                  ${entry.amount < 0 ? formatCurrency(Math.abs(entry.amount)) : '-'}
                </td>
                <td style="text-align: right" class="balance">
                  ${formatCurrency(entry.balance_after)}
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>

        <div class="summary-box">
          <div class="summary-title">ADVANCE SUMMARY</div>
          <div class="summary-row">
            <span class="summary-label">Current Outstanding Balance:</span>
            <span class="summary-value">${formatCurrency(summary.current_balance)}</span>
          </div>
          <div class="summary-row">
            <span class="summary-label">Monthly Recovery Amount:</span>
            <span class="summary-value">${formatCurrency(summary.monthly_deduction)}</span>
          </div>
          ${summary.months_to_clear ? `
            <div class="summary-row">
              <span class="summary-label">Estimated Months to Clear:</span>
              <span class="summary-value">${summary.months_to_clear} months</span>
            </div>
          ` : ''}
          ${summary.expected_clear_date ? `
            <div class="summary-row">
              <span class="summary-label">Expected Clear Date:</span>
              <span class="summary-value">${formatDate(summary.expected_clear_date)}</span>
            </div>
          ` : ''}
        </div>

        <div class="signature-section">
          <div class="signature-box">
            <div class="signature-line"></div>
            <div class="signature-label">Employee Signature</div>
          </div>
          <div class="signature-box">
            <div class="signature-line"></div>
            <div class="signature-label">Director's Signature</div>
          </div>
        </div>

        <div class="footer">
          This is a computer-generated statement. For any discrepancies, please contact the Accounts Department.<br>
          Generated on ${new Date().toLocaleString('en-PK')} | PGT International (Private) Limited
        </div>
      </body>
      </html>
    `);
    
    printWindow.document.close();
    printWindow.focus();
    setTimeout(() => {
      printWindow.print();
    }, 250);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600"></div>
      </div>
    );
  }

  if (!ledgerData) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600">No ledger data found</p>
      </div>
    );
  }

  const { staff, advance_summary, ledger_entries } = ledgerData;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => navigate('/staff-payroll')}
            className="btn-secondary flex items-center"
          >
            <ArrowLeft className="h-5 w-5 mr-2" />
            Back to Staff
          </button>
          <h1 className="text-2xl font-bold text-gray-900">Staff Advance Ledger</h1>
        </div>
        <button
          onClick={printStatement}
          className="btn-primary flex items-center"
        >
          <Printer className="h-5 w-5 mr-2" />
          Print Statement
        </button>
      </div>

      {/* Employee Info Card */}
      <div className="glass-card rounded-xl p-6" style={{
        background: 'linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
        border: '2px solid rgba(220, 38, 38, 0.3)'
      }}>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="flex items-start space-x-3">
            <User className="h-6 w-6 text-red-600 mt-1" />
            <div>
              <p className="text-sm text-gray-600">Employee Name</p>
              <p className="text-lg font-semibold text-gray-900">{staff.name}</p>
              <p className="text-sm text-gray-500">ID: {staff.employee_id}</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <Briefcase className="h-6 w-6 text-red-600 mt-1" />
            <div>
              <p className="text-sm text-gray-600">Position</p>
              <p className="text-lg font-semibold text-gray-900">{staff.position}</p>
              <p className="text-sm text-gray-500">Gross: {formatCurrency(staff.gross_salary)}</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <DollarSign className="h-6 w-6 text-red-600 mt-1" />
            <div>
              <p className="text-sm text-gray-600">Monthly Recovery</p>
              <p className="text-lg font-semibold text-gray-900">{formatCurrency(advance_summary.monthly_deduction)}</p>
              {advance_summary.months_to_clear && (
                <p className="text-sm text-gray-500">{advance_summary.months_to_clear} months remaining</p>
              )}
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <Calendar className="h-6 w-6 text-red-600 mt-1" />
            <div>
              <p className="text-sm text-gray-600">Expected Clear Date</p>
              <p className="text-lg font-semibold text-gray-900">
                {advance_summary.expected_clear_date ? formatDate(advance_summary.expected_clear_date) : 'N/A'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Current Balance Alert */}
      {advance_summary.current_balance > 0 && (
        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '2px solid rgba(239, 68, 68, 0.3)'
        }}>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <AlertCircle className="h-8 w-8 text-red-600" />
              <div>
                <p className="text-sm font-medium text-gray-600">Current Outstanding Balance</p>
                <p className="text-3xl font-bold text-red-600">{formatCurrency(advance_summary.current_balance)}</p>
              </div>
            </div>
            {advance_summary.advance_given_date && (
              <div className="text-right">
                <p className="text-sm text-gray-600">Advance Given</p>
                <p className="text-sm font-medium text-gray-900">{formatDate(advance_summary.advance_given_date)}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Bank Statement Style Ledger */}
      <div className="glass-card rounded-xl overflow-hidden">
        <div className="bg-gradient-to-r from-red-600 to-red-700 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <FileText className="h-6 w-6 text-white" />
              <h2 className="text-xl font-bold text-white">Transaction History</h2>
            </div>
            <p className="text-white text-sm">Total Entries: {ledger_entries.length}</p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                  Description
                </th>
                <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">
                  Debit (Advance Given)
                </th>
                <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">
                  Credit (Recovery)
                </th>
                <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">
                  Running Balance
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {ledger_entries.map((entry, index) => (
                <tr key={entry.id} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatDate(entry.date)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    <div>
                      <p className="font-medium">{entry.description}</p>
                      {entry.created_by && (
                        <p className="text-xs text-gray-500">By: {entry.created_by}</p>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                    {entry.amount > 0 ? (
                      <span className="font-semibold text-red-600">
                        {formatCurrency(entry.amount)}
                      </span>
                    ) : (
                      <span className="text-gray-400">-</span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                    {entry.amount < 0 ? (
                      <span className="font-semibold text-green-600">
                        {formatCurrency(Math.abs(entry.amount))}
                      </span>
                    ) : (
                      <span className="text-gray-400">-</span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                    <span className="font-bold text-gray-900">
                      {formatCurrency(entry.balance_after)}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default StaffAdvanceLedger;
