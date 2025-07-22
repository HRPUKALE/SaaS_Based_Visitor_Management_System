import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import SuperadminLogin from './components/SuperadminLogin';
import SuperadminDashboard from './components/SuperadminDashboard';
import CombinedLogin from './components/CombinedLogin';
import AdminDashboard from './components/AdminDashboard';
import AppointmentSystem from './components/AppointmentSystem';
import ManualBooking from './components/ManualBooking';
import TalkToVira from './components/TalkToVira';
import HomePage from './components/HomePage';

// Protected Route Component
const ProtectedRoute: React.FC<{ 
  children: React.ReactNode; 
  allowedRoles: string[];
  redirectTo: string;
}> = ({ children, allowedRoles, redirectTo }) => {
  const { isAuthenticated, userRole } = useAuth();

  console.log('🔒 ProtectedRoute: isAuthenticated:', isAuthenticated, 'userRole:', userRole, 'allowedRoles:', allowedRoles);

  if (!isAuthenticated) {
    console.log('🔒 ProtectedRoute: Not authenticated, redirecting to:', redirectTo);
    return <Navigate to={redirectTo} replace />;
  }

  if (!allowedRoles.includes(userRole || '')) {
    console.log('🔒 ProtectedRoute: Role not allowed, redirecting to /');
    return <Navigate to="/" replace />;
  }

  console.log('🔒 ProtectedRoute: Access granted');
  return <>{children}</>;
};

// Main App component with routing
const AppContent: React.FC = () => {
  const { isAuthenticated, userRole } = useAuth();

  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<CombinedLogin />} />
      <Route path="/super-admin-login" element={<SuperadminLogin />} />

      {/* Protected Routes */}
      <Route 
        path="/superadmin/dashboard" 
        element={
          <ProtectedRoute 
            allowedRoles={['superadmin']} 
            redirectTo="/super-admin-login"
          >
            <SuperadminDashboard />
          </ProtectedRoute>
        } 
      />
      
      <Route 
        path="/admin/dashboard" 
        element={
          <ProtectedRoute 
            allowedRoles={['admin']} 
            redirectTo="/login"
          >
            <AdminDashboard />
          </ProtectedRoute>
        } 
      />
      
      <Route 
        path="/user/dashboard" 
        element={
          <ProtectedRoute 
            allowedRoles={['user']} 
            redirectTo="/login"
          >
            <AppointmentSystem />
          </ProtectedRoute>
        } 
      />

      {/* User Appointment Routes */}
      <Route 
        path="/user/manual-booking" 
        element={
          <ProtectedRoute 
            allowedRoles={['user']} 
            redirectTo="/login"
          >
            <ManualBooking />
          </ProtectedRoute>
        } 
      />

      <Route 
        path="/user/talk-to-vira" 
        element={
          <ProtectedRoute 
            allowedRoles={['user']} 
            redirectTo="/login"
          >
            <TalkToVira />
          </ProtectedRoute>
        } 
      />

      {/* Redirect authenticated users to their dashboard */}
      <Route 
        path="*" 
        element={
          isAuthenticated ? (
            <Navigate 
              to={
                userRole === 'superadmin' ? '/superadmin/dashboard' :
                userRole === 'admin' ? '/admin/dashboard' :
                userRole === 'user' ? '/user/dashboard' : '/'
              } 
              replace 
            />
          ) : (
            <Navigate to="/" replace />
          )
        } 
      />
    </Routes>
  );
};

// Main App component
function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;