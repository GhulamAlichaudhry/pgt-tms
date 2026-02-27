import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import toast from 'react-hot-toast';
import { 
  TrendingUp, 
  DollarSign, 
  Truck, 
  Users, 
  Calendar,
  AlertTriangle,
  Plus,
  FileText,
  BarChart3
} from 'lucide-react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard = () => {
  const navigate = useNavigate();
  const [financialData, setFinancialData] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showReceivablesModal, setShowReceivablesModal] = useState(false);
  const [showPayablesModal, setShowPayablesModal] = useState(false);
  const [receivablesDetails, setReceivablesDetails] = useState(null);
  const [payablesDetails, setPayablesDetails] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      // Fetch financial summary and chart data in parallel
      const [financialResponse, chartResponse] = await Promise.all([
        axios.get('/dashboard/financial-summary', { headers }),
        axios.get('/dashboard/chart-data', { headers })
      ]);

      setFinancialData(financialResponse.data);
      setChartData(chartResponse.data);
      setError(null);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setError('Failed to load dashboard data');
      
      // Use fallback data if API fails
      setFinancialData({
        total_receivables: 4928445,
        total_payables: 2500000,
        cash_bank_balance: 1500000,
        total_income: 987000,
        total_expenses: 400000,
        net_profit: 587000,
        profit_margin: 59.5,
        daily_income: 45000,
        daily_outgoing: 32000,
        daily_net: 13000,
        monthly_profit: 587000,
        monthly_revenue: 987000,
        monthly_expenses: 400000,
        monthly_growth: 12.5,
        active_vehicles: 3,
        total_trips: 156,
        monthly_trips: 15,
        top_clients: [],
        top_vendors: [],
        alerts: []
      });
      
      setChartData({
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        revenue: [450000, 520000, 480000, 600000, 580000, 650000],
        expenses: [300000, 350000, 320000, 400000, 380000, 400000],
        profit: [150000, 170000, 160000, 200000, 200000, 250000]
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchReceivablesDetails = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };
      const response = await axios.get('/dashboard/receivables-details', { headers });
      setReceivablesDetails(response.data);
      setShowReceivablesModal(true);
    } catch (error) {
      console.error('Error fetching receivables details:', error);
    }
  };

  const fetchPayablesDetails = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };
      const response = await axios.get('/dashboard/payables-details', { headers });
      setPayablesDetails(response.data);
      setShowPayablesModal(true);
    } catch (error) {
      console.error('Error fetching payables details:', error);
    }
  };

  const downloadFinancialSummaryPDF = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/reports/financial-summary-pdf', {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        responseType: 'blob'
      });
      
      // Create blob link to download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `financial_summary_${new Date().toISOString().split('T')[0]}.pdf`);
      
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('Financial summary downloaded successfully!');
    } catch (error) {
      console.error('Error downloading financial summary:', error);
      toast.error('Failed to download financial summary');
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-PK', {
      style: 'currency',
      currency: 'PKR',
      minimumFractionDigits: 0,
    }).format(amount);
  };

  // Generate chart data from live API data
  const getFreightTrendData = () => {
    if (!chartData) return { labels: [], datasets: [] };
    
    return {
      labels: chartData.labels,
      datasets: [
        {
          label: 'Monthly Revenue',
          data: chartData.revenue,
          borderColor: '#dc2626',
          backgroundColor: 'rgba(220, 38, 38, 0.1)',
          tension: 0.4,
          fill: true,
        },
      ],
    };
  };

  const getRevenueExpenseData = () => {
    if (!financialData) return { labels: [], datasets: [] };
    
    return {
      labels: ['Revenue', 'Expenses', 'Profit'],
      datasets: [
        {
          label: 'This Month (PKR)',
          data: [
            financialData.monthly_revenue,
            financialData.monthly_expenses,
            financialData.monthly_profit
          ],
          backgroundColor: [
            'rgba(34, 197, 94, 0.8)',
            'rgba(239, 68, 68, 0.8)',
            'rgba(59, 130, 246, 0.8)',
          ],
          borderColor: [
            'rgb(34, 197, 94)',
            'rgb(239, 68, 68)',
            'rgb(59, 130, 246)',
          ],
          borderWidth: 2,
        },
      ],
    };
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return 'PKR ' + value.toLocaleString();
          }
        }
      },
    },
  };

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center', 
        height: '16rem' 
      }}>
        <div style={{
          width: '3rem',
          height: '3rem',
          border: '3px solid #f3f4f6',
          borderTop: '3px solid #dc2626',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite'
        }}></div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ 
        display: 'flex', 
        flexDirection: 'column',
        alignItems: 'center', 
        justifyContent: 'center', 
        height: '16rem',
        gap: '1rem'
      }}>
        <AlertTriangle style={{ height: '3rem', width: '3rem', color: '#dc2626' }} />
        <div style={{ textAlign: 'center' }}>
          <h3 style={{ color: '#dc2626', marginBottom: '0.5rem' }}>Dashboard Error</h3>
          <p style={{ color: '#6b7280' }}>{error}</p>
          <button 
            onClick={fetchDashboardData}
            style={{
              marginTop: '1rem',
              padding: '0.5rem 1rem',
              backgroundColor: '#dc2626',
              color: 'white',
              border: 'none',
              borderRadius: '0.375rem',
              cursor: 'pointer'
            }}
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#111827' }}>
          Dashboard Overview
        </h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <button
            onClick={downloadFinancialSummaryPDF}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '0.5rem 1rem',
              backgroundColor: '#dc2626',
              color: 'white',
              border: 'none',
              borderRadius: '0.375rem',
              fontSize: '0.875rem',
              cursor: 'pointer'
            }}
            title="Download Financial Summary"
          >
            <FileText style={{ height: '1rem', width: '1rem' }} />
            Download Report
          </button>
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            fontSize: '0.875rem', 
            color: '#6b7280',
            gap: '0.25rem'
          }}>
            <Calendar style={{ height: '1rem', width: '1rem' }} />
            {new Date().toLocaleDateString('en-US', { 
              weekday: 'long', 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            })}
          </div>
        </div>
      </div>

      {/* Smart Cards */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
        gap: '1.5rem' 
      }}>
        {/* Net Profit */}
        <div className="glass-card" style={{
          background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          borderRadius: '0.75rem',
          padding: '1.5rem',
          border: '1px solid rgba(34, 197, 94, 0.2)',
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <p style={{ fontSize: '0.875rem', fontWeight: '500', color: '#6b7280' }}>
                Net Profit
              </p>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#059669' }}>
                {formatCurrency(financialData?.net_profit || 0)}
              </p>
            </div>
            <div style={{
              padding: '0.75rem',
              backgroundColor: 'rgba(34, 197, 94, 0.1)',
              borderRadius: '50%'
            }}>
              <TrendingUp style={{ height: '1.5rem', width: '1.5rem', color: '#059669' }} />
            </div>
          </div>
          <div style={{ marginTop: '1rem', display: 'flex', alignItems: 'center', fontSize: '0.875rem' }}>
            <span style={{ color: '#059669', fontWeight: '500' }}>
              {financialData?.profit_margin ? `${financialData.profit_margin.toFixed(1)}%` : '0%'} margin
            </span>
            <span style={{ color: '#6b7280', marginLeft: '0.25rem' }}>
              | {financialData?.monthly_growth ? `${financialData.monthly_growth > 0 ? '+' : ''}${financialData.monthly_growth.toFixed(1)}%` : '0%'} growth
            </span>
          </div>
        </div>

        {/* Total Receivables */}
        <div 
          className="glass-card" 
          onClick={() => navigate('/receivables')}
          style={{
            background: 'linear-gradient(135deg, rgba(251, 146, 60, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
            borderRadius: '0.75rem',
            padding: '1.5rem',
            border: '1px solid rgba(251, 146, 60, 0.2)',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
            cursor: 'pointer',
            transition: 'all 0.3s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-4px)';
            e.currentTarget.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.15)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1)';
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <p style={{ fontSize: '0.875rem', fontWeight: '500', color: '#6b7280' }}>
                Total Receivables
              </p>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#ea580c' }}>
                {formatCurrency(financialData?.total_receivables || 0)}
              </p>
            </div>
            <div style={{
              padding: '0.75rem',
              backgroundColor: 'rgba(251, 146, 60, 0.1)',
              borderRadius: '50%'
            }}>
              <DollarSign style={{ height: '1.5rem', width: '1.5rem', color: '#ea580c' }} />
            </div>
          </div>
          <div style={{ marginTop: '1rem', display: 'flex', alignItems: 'center', fontSize: '0.875rem' }}>
            <span style={{ color: '#6b7280' }}>
              Outstanding from clients
            </span>
          </div>
        </div>

        {/* Total Payables */}
        <div 
          className="glass-card" 
          onClick={() => navigate('/payables')}
          style={{
            background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
            borderRadius: '0.75rem',
            padding: '1.5rem',
            border: '1px solid rgba(239, 68, 68, 0.2)',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
            cursor: 'pointer',
            transition: 'all 0.3s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-4px)';
            e.currentTarget.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.15)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1)';
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <p style={{ fontSize: '0.875rem', fontWeight: '500', color: '#6b7280' }}>
                Total Payables
              </p>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#dc2626' }}>
                {formatCurrency(financialData?.total_payables || 0)}
              </p>
            </div>
            <div style={{
              padding: '0.75rem',
              backgroundColor: 'rgba(239, 68, 68, 0.1)',
              borderRadius: '50%'
            }}>
              <DollarSign style={{ height: '1.5rem', width: '1.5rem', color: '#dc2626' }} />
            </div>
          </div>
          <div style={{ marginTop: '1rem', display: 'flex', alignItems: 'center', fontSize: '0.875rem' }}>
            <span style={{ color: '#6b7280' }}>
              Outstanding to vendors
            </span>
          </div>
        </div>

        {/* Active Fleet */}
        <div className="glass-card" 
          onClick={() => navigate('/fleet-logs')}
          style={{
            background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
            borderRadius: '0.75rem',
            padding: '1.5rem',
            border: '1px solid rgba(59, 130, 246, 0.2)',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
            cursor: 'pointer',
            transition: 'all 0.3s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-4px)';
            e.currentTarget.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.15)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1)';
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <p style={{ fontSize: '0.875rem', fontWeight: '500', color: '#6b7280' }}>
                Active Fleet
              </p>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#2563eb' }}>
                {financialData?.active_vehicles || 0}
              </p>
            </div>
            <div style={{
              padding: '0.75rem',
              backgroundColor: 'rgba(59, 130, 246, 0.1)',
              borderRadius: '50%'
            }}>
              <Truck style={{ height: '1.5rem', width: '1.5rem', color: '#2563eb' }} />
            </div>
          </div>
          <div style={{ marginTop: '1rem', display: 'flex', alignItems: 'center', fontSize: '0.875rem' }}>
            <span style={{ color: '#6b7280' }}>
              {financialData?.monthly_trips || 0} trips this month
            </span>
          </div>
        </div>

        {/* Daily Cash Flow */}
        <div className="glass-card" 
          onClick={() => navigate('/daily-cash-flow')}
          style={{
          background: 'linear-gradient(135deg, rgba(147, 51, 234, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%)',
          borderRadius: '0.75rem',
          padding: '1.5rem',
          border: '1px solid rgba(147, 51, 234, 0.2)',
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          transform: 'translateY(0)'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'translateY(-4px)';
          e.currentTarget.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.15)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1)';
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <p style={{ fontSize: '0.875rem', fontWeight: '500', color: '#6b7280' }}>
                Today's Cash Flow
              </p>
              <p style={{ 
                fontSize: '1.5rem', 
                fontWeight: 'bold', 
                color: (financialData?.daily_net || 0) >= 0 ? '#059669' : '#dc2626'
              }}>
                {formatCurrency(financialData?.daily_net || 0)}
              </p>
            </div>
            <div style={{
              padding: '0.75rem',
              backgroundColor: 'rgba(147, 51, 234, 0.1)',
              borderRadius: '50%'
            }}>
              <DollarSign style={{ height: '1.5rem', width: '1.5rem', color: '#9333ea' }} />
            </div>
          </div>
          <div style={{ marginTop: '1rem', display: 'flex', alignItems: 'center', fontSize: '0.875rem' }}>
            <span style={{ color: '#6b7280' }}>
              In: {formatCurrency(financialData?.daily_income || 0)} | Out: {formatCurrency(financialData?.daily_outgoing || 0)}
            </span>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', 
        gap: '1.5rem' 
      }}>
        {/* Revenue Trend Chart */}
        <div className="glass-card" style={{
          borderRadius: '0.75rem',
          padding: '1.5rem',
          background: 'rgba(255, 255, 255, 0.9)',
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
        }}>
          <h3 style={{ 
            fontSize: '1.125rem', 
            fontWeight: '600', 
            color: '#111827', 
            marginBottom: '1rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <BarChart3 style={{ height: '1.25rem', width: '1.25rem', color: '#dc2626' }} />
            Revenue Trend (6 Months)
          </h3>
          <Line data={getFreightTrendData()} options={chartOptions} />
        </div>

        {/* Revenue vs Expense Chart */}
        <div className="glass-card" style={{
          borderRadius: '0.75rem',
          padding: '1.5rem',
          background: 'rgba(255, 255, 255, 0.9)',
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
        }}>
          <h3 style={{ 
            fontSize: '1.125rem', 
            fontWeight: '600', 
            color: '#111827', 
            marginBottom: '1rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <BarChart3 style={{ height: '1.25rem', width: '1.25rem', color: '#dc2626' }} />
            This Month's Performance
          </h3>
          <Bar data={getRevenueExpenseData()} options={chartOptions} />
        </div>
      </div>

      {/* Financial Alerts */}
      {financialData?.alerts && financialData.alerts.length > 0 && (
        <div className="glass-card" style={{
          borderRadius: '0.75rem',
          padding: '1.5rem',
          background: 'rgba(255, 255, 255, 0.9)',
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
        }}>
          <h3 style={{ 
            fontSize: '1.125rem', 
            fontWeight: '600', 
            color: '#111827', 
            marginBottom: '1rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <AlertTriangle style={{ height: '1.25rem', width: '1.25rem', color: '#dc2626' }} />
            Financial Alerts
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {financialData.alerts.map((alert, index) => (
              <div 
                key={index}
                style={{
                  padding: '0.75rem',
                  borderRadius: '0.5rem',
                  backgroundColor: alert.type === 'error' ? 'rgba(239, 68, 68, 0.1)' : 
                                   alert.type === 'warning' ? 'rgba(251, 146, 60, 0.1)' : 
                                   'rgba(59, 130, 246, 0.1)',
                  border: `1px solid ${alert.type === 'error' ? 'rgba(239, 68, 68, 0.2)' : 
                                      alert.type === 'warning' ? 'rgba(251, 146, 60, 0.2)' : 
                                      'rgba(59, 130, 246, 0.2)'}`,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem'
                }}
              >
                <AlertTriangle style={{ 
                  height: '1rem', 
                  width: '1rem', 
                  color: alert.type === 'error' ? '#dc2626' : 
                         alert.type === 'warning' ? '#d97706' : 
                         '#2563eb'
                }} />
                <div>
                  <div style={{ fontWeight: '500', fontSize: '0.875rem' }}>{alert.title}</div>
                  <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>{alert.message}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="glass-card" style={{
        borderRadius: '0.75rem',
        padding: '1.5rem',
        background: 'rgba(255, 255, 255, 0.9)',
        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
      }}>
        <h3 style={{ 
          fontSize: '1.125rem', 
          fontWeight: '600', 
          color: '#111827', 
          marginBottom: '1rem' 
        }}>
          Quick Actions
        </h3>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
          gap: '1rem' 
        }}>
          <button 
            onClick={() => navigate('/fleet-logs')}
            className="btn-primary" style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-start',
            padding: '1rem',
            borderRadius: '0.5rem',
            backgroundColor: '#dc2626',
            color: 'white',
            border: 'none',
            cursor: 'pointer',
            textAlign: 'left'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <Plus style={{ height: '1.25rem', width: '1.25rem' }} />
              <span style={{ fontWeight: '500' }}>Add New Trip</span>
            </div>
            <div style={{ fontSize: '0.875rem', opacity: 0.9 }}>
              Log a new transport entry with Excel-style form
            </div>
          </button>
          
          <button 
            onClick={() => navigate('/payroll')}
            className="btn-secondary" style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-start',
            padding: '1rem',
            borderRadius: '0.5rem',
            backgroundColor: '#f3f4f6',
            color: '#374151',
            border: 'none',
            cursor: 'pointer',
            textAlign: 'left'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <Users style={{ height: '1.25rem', width: '1.25rem' }} />
              <span style={{ fontWeight: '500' }}>Process Payroll</span>
            </div>
            <div style={{ fontSize: '0.875rem', opacity: 0.75 }}>
              Generate monthly payroll with advance deductions
            </div>
          </button>
          
          <button 
            onClick={() => navigate('/receivables')}
            className="btn-secondary" style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-start',
            padding: '1rem',
            borderRadius: '0.5rem',
            backgroundColor: '#f3f4f6',
            color: '#374151',
            border: 'none',
            cursor: 'pointer',
            textAlign: 'left'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <FileText style={{ height: '1.25rem', width: '1.25rem' }} />
              <span style={{ fontWeight: '500' }}>Generate Report</span>
            </div>
            <div style={{ fontSize: '0.875rem', opacity: 0.75 }}>
              Export financial reports and trip summaries
            </div>
          </button>
        </div>
      </div>

      {/* Receivables Details Modal */}
      {showReceivablesModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '0.75rem',
            padding: '2rem',
            maxWidth: '600px',
            width: '90%',
            maxHeight: '80vh',
            overflow: 'auto',
            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#111827' }}>
                Receivables Details
              </h3>
              <button
                onClick={() => setShowReceivablesModal(false)}
                style={{
                  padding: '0.5rem',
                  backgroundColor: '#f3f4f6',
                  border: 'none',
                  borderRadius: '0.375rem',
                  cursor: 'pointer'
                }}
              >
                ✕
              </button>
            </div>
            
            {receivablesDetails && (
              <>
                <div style={{ marginBottom: '1.5rem', padding: '1rem', backgroundColor: '#f9fafb', borderRadius: '0.5rem' }}>
                  <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>Total Receivables</p>
                  <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#ea580c' }}>
                    {formatCurrency(receivablesDetails.total_receivables)}
                  </p>
                  {receivablesDetails.message ? (
                    <p style={{ fontSize: '0.875rem', color: '#6b7280', fontStyle: 'italic' }}>
                      {receivablesDetails.message}
                    </p>
                  ) : (
                    <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                      {receivablesDetails.count} clients with outstanding balances
                    </p>
                  )}
                </div>
                
                {receivablesDetails.details.length > 0 ? (
                  <div style={{ maxHeight: '300px', overflow: 'auto' }}>
                    {receivablesDetails.details.map((receivable, index) => (
                      <div key={receivable.id} style={{
                        padding: '1rem',
                        borderBottom: index < receivablesDetails.details.length - 1 ? '1px solid #e5e7eb' : 'none',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center'
                      }}>
                        <div>
                          <p style={{ fontWeight: '500', color: '#111827' }}>{receivable.client_name}</p>
                          <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                            Invoice: {receivable.invoice_number}
                          </p>
                          <p style={{ fontSize: '0.75rem', color: '#6b7280' }}>
                            Due: {new Date(receivable.due_date).toLocaleDateString()}
                          </p>
                        </div>
                        <div style={{ textAlign: 'right' }}>
                          <p style={{ fontWeight: '600', color: '#ea580c' }}>
                            {formatCurrency(receivable.remaining_amount)}
                          </p>
                          <p style={{ fontSize: '0.75rem', color: '#6b7280' }}>
                            {receivable.status}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div style={{ 
                    textAlign: 'center', 
                    padding: '2rem', 
                    color: '#6b7280',
                    backgroundColor: '#f9fafb',
                    borderRadius: '0.5rem'
                  }}>
                    <p>Client receivables will be available when client management is implemented.</p>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      )}

      {/* Payables Details Modal */}
      {showPayablesModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '0.75rem',
            padding: '2rem',
            maxWidth: '600px',
            width: '90%',
            maxHeight: '80vh',
            overflow: 'auto',
            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#111827' }}>
                Payables Details
              </h3>
              <button
                onClick={() => setShowPayablesModal(false)}
                style={{
                  padding: '0.5rem',
                  backgroundColor: '#f3f4f6',
                  border: 'none',
                  borderRadius: '0.375rem',
                  cursor: 'pointer'
                }}
              >
                ✕
              </button>
            </div>
            
            {payablesDetails && (
              <>
                <div style={{ marginBottom: '1.5rem', padding: '1rem', backgroundColor: '#fef2f2', borderRadius: '0.5rem' }}>
                  <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>Total Payables</p>
                  <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#dc2626' }}>
                    {formatCurrency(payablesDetails.total_payables)}
                  </p>
                  <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                    {payablesDetails.count} vendors to pay
                  </p>
                </div>
                
                <div style={{ maxHeight: '300px', overflow: 'auto' }}>
                  {payablesDetails.details.map((payable, index) => (
                    <div key={payable.id} style={{
                      padding: '1rem',
                      borderBottom: index < payablesDetails.details.length - 1 ? '1px solid #e5e7eb' : 'none',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }}>
                      <div>
                        <p style={{ fontWeight: '500', color: '#111827' }}>{payable.vendor_name}</p>
                        <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                          Invoice: {payable.invoice_number}
                        </p>
                        <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                          {payable.vendor_contact} • {payable.vendor_phone}
                        </p>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <p style={{ fontWeight: '600', color: '#dc2626' }}>
                          {formatCurrency(payable.amount)}
                        </p>
                        <p style={{ fontSize: '0.75rem', color: '#6b7280' }}>
                          {payable.status}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;