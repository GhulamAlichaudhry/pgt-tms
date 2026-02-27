import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Layout from './components/Layout';
import Login from './pages/Login';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import Dashboard from './pages/Dashboard';
import FleetLogs from './pages/FleetLogs';
import StaffPayroll from './pages/StaffPayroll';
import StaffAdvanceLedger from './pages/StaffAdvanceLedger';
import SupervisorMobileForm from './pages/SupervisorMobileForm';
import FinancialLedgers from './pages/FinancialLedgers';
import Expenses from './pages/Expenses';
import Payables from './pages/Payables';
import Receivables from './pages/Receivables';
import ReceivableAging from './pages/ReceivableAging';
import DailyCashFlow from './pages/DailyCashFlow';
import VendorReports from './pages/VendorReports';
import ClientReports from './pages/ClientReports';
import Settings from './pages/Settings';

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }
  
  return user ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
            }}
          />
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/reset-password" element={<ResetPassword />} />
            <Route path="/" element={
              <ProtectedRoute>
                <Layout>
                  <Dashboard />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <Layout>
                  <Dashboard />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/fleet-logs" element={
              <ProtectedRoute>
                <Layout>
                  <FleetLogs />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/staff-payroll" element={
              <ProtectedRoute>
                <Layout>
                  <StaffPayroll />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/staff-advance-ledger/:staffId" element={
              <ProtectedRoute>
                <Layout>
                  <StaffAdvanceLedger />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/supervisor-mobile" element={
              <ProtectedRoute>
                <SupervisorMobileForm />
              </ProtectedRoute>
            } />
            <Route path="/financial-ledgers" element={
              <ProtectedRoute>
                <Layout>
                  <FinancialLedgers />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/expenses" element={
              <ProtectedRoute>
                <Layout>
                  <Expenses />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/payables" element={
              <ProtectedRoute>
                <Layout>
                  <Payables />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/receivables" element={
              <ProtectedRoute>
                <Layout>
                  <Receivables />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/receivable-aging" element={
              <ProtectedRoute>
                <Layout>
                  <ReceivableAging />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/daily-cash-flow" element={
              <ProtectedRoute>
                <Layout>
                  <DailyCashFlow />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/vendor-reports" element={
              <ProtectedRoute>
                <Layout>
                  <VendorReports />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/client-reports" element={
              <ProtectedRoute>
                <Layout>
                  <ClientReports />
                </Layout>
              </ProtectedRoute>
            } />
            <Route path="/settings" element={
              <ProtectedRoute>
                <Layout>
                  <Settings />
                </Layout>
              </ProtectedRoute>
            } />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;