import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated, userRole } = useAuth();

  // If user is already authenticated, redirect to their dashboard
  React.useEffect(() => {
    console.log('🏠 HomePage: isAuthenticated:', isAuthenticated, 'userRole:', userRole);
    
    if (isAuthenticated) {
      const targetRoute = userRole === 'superadmin' ? '/superadmin/dashboard' :
                         userRole === 'admin' ? '/admin/dashboard' :
                         userRole === 'user' ? '/user/dashboard' : '/';
      
      console.log('🏠 HomePage: Navigating to:', targetRoute);
      navigate(targetRoute);
    } else {
      // Redirect to combined login page
      console.log('🏠 HomePage: Not authenticated, redirecting to login');
      navigate('/login');
    }
  }, [isAuthenticated, userRole, navigate]);

  // Show loading while redirecting
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading...</p>
      </div>
    </div>
  );
};

export default HomePage; 