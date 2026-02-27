import React, { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { 
  AlertTriangle,
  Clock,
  DollarSign,
  TrendingUp,
  Send,
  Download,
  Printer,
  Building2,
  Calendar,
  Phone,
  Mail
} from 'lucide-react';

const ReceivableAging = () => {
  const [agingData, setAgingData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedClients, setSelectedClients] = useState([]);

  useEffect(() => {
    fetchAgingData();
  }, []);

  const fetchAgingData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/clients/aging-analysis', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setAgingData(response.data);
    } catch (error) {
      console.error('Error fetching aging data:', error);
      toast.error('Failed to fetch receivable aging data');
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

  const calculateTotals = () => {
    return agingData.reduce((acc, client) => {
      acc.current += client.aging['0-30'] || 0;
      acc.days30 += client.aging['31-60'] || 0;
      acc.days60 += client.aging['61-90'] || 0;
      acc.days90Plus += client.aging['90+'] || 0;
      acc.total += client.outstanding_balance || 0;
      return acc;
    }, { current: 0, days30: 0, days60: 0, days90Plus: 0, total: 0 });
  };

  const totals = calculateTotals();

  const handleSelectClient = (clientId) => {
    setSelectedClients(prev => 
      prev.includes(clientId) 
        ? prev.filter(id => id !== clientId)
        : [...prev, clientId]
    );
  };

  const handleSelectAll = () => {
    if (selectedClients.length === agingData.length) {
      setSelectedClients([]);
    } else {
      setSelectedClients(agingData.map(c => c.client_id));
    }
  };

  const sendReminders = () => {
    if (selectedClients.length === 0) {
      toast.error('Please select at least one client');
      return;
    }

    const selectedData = agingData.filter(c => selectedClients.includes(c.client_id));
    const overdueClients = selectedData.filter(c => c.total_overdue > 0);

    if (overdueClients.length === 0) {
      toast.error('Selected clients have no overdue amounts');
      return;
    }

    // Generate reminder summary
    let reminderText = '=== PAYMENT REMINDER ===\n\n';
    reminderText += 'PGT INTERNATIONAL (PRIVATE) LIMITED\n';
    reminderText += 'Excellence in Transportation & Logistics\n\n';
    reminderText += `Date: ${new Date().toLocaleDateString('en-PK')}\n\n`;
    reminderText += 'OVERDUE RECEIVABLES SUMMARY:\n\n';

    overdueClients.forEach(client => {
      reminderText += `Client: ${client.client_name}\n`;
      reminderText += `Total Outstanding: ${formatCurrency(client.outstanding_balance)}\n`;
      reminderText += `Overdue Amount: ${formatCurrency(client.total_overdue)}\n`;
      reminderText += `  31-60 Days: ${formatCurrency(client.aging['31-60'])}\n`;
      reminderText += `  61-90 Days: ${formatCurrency(client.aging['61-90'])}\n`;
      reminderText += `  90+ Days: ${formatCurrency(client.aging['90+'])}\n`;
      if (client.contact_person) reminderText += `Contact: ${client.contact_person}\n`;
      if (client.phone) reminderText += `Phone: ${client.phone}\n`;
      reminderText += '\n';
    });

    reminderText += 'Please arrange payment at your earliest convenience.\n';
    reminderText += 'For queries, contact: +92-42-35291747\n';

    // Copy to clipboard
    navigator.clipboard.writeText(reminderText);
    toast.success(`Reminder summary copied for ${overdueClients.length} client(s)!`);
  };

  const printAgingReport = () => {
    const printWindow = window.open('', '', 'height=800,width=1000');
    
    printWindow.document.write(`
      <html>
      <head>
        <title>Receivable Aging Report</title>
        <style>
          body { font-family: Arial; padding: 20px; }
          .header { text-align: center; margin-bottom: 30px; border-bottom: 3px solid #dc2626; padding-bottom: 20px; }
          .company-name { font-size: 24px; font-weight: bold; color: #dc2626; }
          .report-title { font-size: 18px; font-weight: bold; margin: 20px 0; }
          table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 11px; }
          th { background: #dc2626; color: white; padding: 10px 8px; text-align: left; }
          td { padding: 8px; border-bottom: 1px solid #e5e7eb; }
          .total-row { font-weight: bold; background: #fef2f2; }
          .overdue { color: #dc2626; font-weight: bold; }
          .current { color: #059669; }
        </style>
      </head>
      <body>
        <div class="header">
          <div class="company-name">PGT INTERNATIONAL (PRIVATE) LIMITED</div>
          <div>Receivable Aging Report</div>
          <div>As of ${new Date().toLocaleDateString('en-PK', { day: '2-digit', month: 'long', year: 'numeric' })}</div>
        </div>
        
        <table>
          <thead>
            <tr>
              <th>Client Name</th>
              <th style="text-align: right">Current (0-30)</th>
              <th style="text-align: right">31-60 Days</th>
              <th style="text-align: right">61-90 Days</th>
              <th style="text-align: right">90+ Days</th>
              <th style="text-align: right">Total Outstanding</th>
              <th>Contact</th>
            </tr>
          </thead>
          <tbody>
            ${agingData.map(client => `
              <tr>
                <td>${client.client_name}</td>
                <td style="text-align: right" class="current">${formatCurrency(client.aging['0-30'])}</td>
                <td style="text-align: right">${formatCurrency(client.aging['31-60'])}</td>
                <td style="text-align: right" class="overdue">${formatCurrency(client.aging['61-90'])}</td>
                <td style="text-align: right" class="overdue">${formatCurrency(client.aging['90+'])}</td>
                <td style="text-align: right"><strong>${formatCurrency(client.outstanding_balance)}</strong></td>
                <td>${client.phone || 'N/A'}</td>
              </tr>
            `).join('')}
            <tr class="total-row">
              <td>TOTAL</td>
              <td style="text-align: right">${formatCurrency(totals.current)}</td>
              <td style="text-align: right">${formatCurrency(totals.days30)}</td>
              <td style="text-align: right">${formatCurrency(totals.days60)}</td>
              <td style="text-align: right">${formatCurrency(totals.days90Plus)}</td>
              <td style="text-align: right">${formatCurrency(totals.total)}</td>
              <td></td>
            </tr>
          </tbody>
        </table>
        
        <div style="margin-top: 40px; font-size: 10px; color: #6b7280;">
          Generated: ${new Date().toLocaleString('en-PK')} | PGT International (Private) Limited
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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Receivable Aging Analysis</h1>
          <p className="text-sm text-gray-600 mt-1">Track overdue payments and collection priorities</p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={sendReminders}
            disabled={selectedClients.length === 0}
            className="btn-secondary flex items-center"
          >
            <Send className="h-5 w-5 mr-2" />
            Send Reminders ({selectedClients.length})
          </button>
          <button
            onClick={printAgingReport}
            className="btn-primary flex items-center"
          >
            <Printer className="h-5 w-5 mr-2" />
            Print Report
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div className="glass-card rounded-xl p-4" style={{
          background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '2px solid rgba(34, 197, 94, 0.3)'
        }}>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600">Current (0-30)</p>
              <p className="text-lg font-bold text-green-600">{formatCurrency(totals.current)}</p>
            </div>
            <Clock className="h-8 w-8 text-green-600" />
          </div>
        </div>

        <div className="glass-card rounded-xl p-4" style={{
          background: 'linear-gradient(135deg, rgba(251, 146, 60, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '2px solid rgba(251, 146, 60, 0.3)'
        }}>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600">31-60 Days</p>
              <p className="text-lg font-bold text-orange-600">{formatCurrency(totals.days30)}</p>
            </div>
            <AlertTriangle className="h-8 w-8 text-orange-600" />
          </div>
        </div>

        <div className="glass-card rounded-xl p-4" style={{
          background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '2px solid rgba(239, 68, 68, 0.3)'
        }}>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600">61-90 Days</p>
              <p className="text-lg font-bold text-red-600">{formatCurrency(totals.days60)}</p>
            </div>
            <AlertTriangle className="h-8 w-8 text-red-600" />
          </div>
        </div>

        <div className="glass-card rounded-xl p-4" style={{
          background: 'linear-gradient(135deg, rgba(220, 38, 38, 0.15) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '3px solid rgba(220, 38, 38, 0.5)'
        }}>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600">90+ Days (CRITICAL)</p>
              <p className="text-lg font-bold text-red-700">{formatCurrency(totals.days90Plus)}</p>
            </div>
            <AlertTriangle className="h-8 w-8 text-red-700 animate-pulse" />
          </div>
        </div>

        <div className="glass-card rounded-xl p-4" style={{
          background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '2px solid rgba(59, 130, 246, 0.3)'
        }}>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600">Total Outstanding</p>
              <p className="text-lg font-bold text-blue-600">{formatCurrency(totals.total)}</p>
            </div>
            <DollarSign className="h-8 w-8 text-blue-600" />
          </div>
        </div>
      </div>

      {/* Aging Table */}
      <div className="glass-card rounded-xl overflow-hidden">
        <div className="bg-gradient-to-r from-red-600 to-red-700 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <TrendingUp className="h-6 w-6 text-white" />
              <h2 className="text-xl font-bold text-white">Client Aging Breakdown</h2>
            </div>
            <button
              onClick={handleSelectAll}
              className="text-white text-sm hover:underline"
            >
              {selectedClients.length === agingData.length ? 'Deselect All' : 'Select All'}
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-4 text-left">
                  <input
                    type="checkbox"
                    checked={selectedClients.length === agingData.length}
                    onChange={handleSelectAll}
                    className="rounded border-gray-300"
                  />
                </th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase">Client Name</th>
                <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase">Current (0-30)</th>
                <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase">31-60 Days</th>
                <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase">61-90 Days</th>
                <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase">90+ Days</th>
                <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase">Total Outstanding</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase">Contact</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {agingData.map((client, index) => (
                <tr 
                  key={client.client_id} 
                  className={`${index % 2 === 0 ? 'bg-white' : 'bg-gray-50'} ${
                    client.aging['90+'] > 0 ? 'border-l-4 border-red-600' : ''
                  }`}
                >
                  <td className="px-6 py-4">
                    <input
                      type="checkbox"
                      checked={selectedClients.includes(client.client_id)}
                      onChange={() => handleSelectClient(client.client_id)}
                      className="rounded border-gray-300"
                    />
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <Building2 className="h-5 w-5 text-gray-400 mr-2" />
                      <div>
                        <div className="text-sm font-medium text-gray-900">{client.client_name}</div>
                        {client.contact_person && (
                          <div className="text-xs text-gray-500">{client.contact_person}</div>
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-green-600 font-medium">
                    {formatCurrency(client.aging['0-30'])}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-orange-600 font-medium">
                    {formatCurrency(client.aging['31-60'])}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-red-600 font-semibold">
                    {formatCurrency(client.aging['61-90'])}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-red-700 font-bold">
                    {client.aging['90+'] > 0 && (
                      <div className="flex items-center justify-end space-x-1">
                        <AlertTriangle className="h-4 w-4" />
                        <span>{formatCurrency(client.aging['90+'])}</span>
                      </div>
                    )}
                    {client.aging['90+'] === 0 && '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-bold text-gray-900">
                    {formatCurrency(client.outstanding_balance)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    <div className="space-y-1">
                      {client.phone && (
                        <div className="flex items-center text-xs">
                          <Phone className="h-3 w-3 mr-1" />
                          {client.phone}
                        </div>
                      )}
                      {client.email && (
                        <div className="flex items-center text-xs">
                          <Mail className="h-3 w-3 mr-1" />
                          {client.email}
                        </div>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
            <tfoot className="bg-red-50">
              <tr className="font-bold">
                <td className="px-6 py-4"></td>
                <td className="px-6 py-4 text-sm text-gray-900">TOTAL</td>
                <td className="px-6 py-4 text-right text-sm text-green-600">{formatCurrency(totals.current)}</td>
                <td className="px-6 py-4 text-right text-sm text-orange-600">{formatCurrency(totals.days30)}</td>
                <td className="px-6 py-4 text-right text-sm text-red-600">{formatCurrency(totals.days60)}</td>
                <td className="px-6 py-4 text-right text-sm text-red-700">{formatCurrency(totals.days90Plus)}</td>
                <td className="px-6 py-4 text-right text-sm text-gray-900">{formatCurrency(totals.total)}</td>
                <td className="px-6 py-4"></td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>

      {/* Priority Alert */}
      {totals.days90Plus > 0 && (
        <div className="glass-card rounded-xl p-6" style={{
          background: 'linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(255, 255, 255, 0.95) 100%)',
          border: '3px solid rgba(220, 38, 38, 0.5)'
        }}>
          <div className="flex items-start space-x-4">
            <AlertTriangle className="h-8 w-8 text-red-600 flex-shrink-0 animate-pulse" />
            <div>
              <h3 className="text-lg font-bold text-red-600 mb-2">CRITICAL: 90+ Days Overdue</h3>
              <p className="text-sm text-gray-700 mb-3">
                You have <span className="font-bold text-red-600">{formatCurrency(totals.days90Plus)}</span> in receivables 
                that are over 90 days old. Immediate action required to collect these amounts.
              </p>
              <p className="text-xs text-gray-600">
                Recommendation: Contact these clients immediately and consider legal action if necessary.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReceivableAging;
