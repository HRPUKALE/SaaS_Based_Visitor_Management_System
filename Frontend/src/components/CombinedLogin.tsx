import React, { useState } from 'react';
import { apiService, TokenResponse } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const CombinedLogin: React.FC = () => {
  const [email, setEmail] = useState('');
  const [otp, setOtp] = useState('');
  const [step, setStep] = useState<'email' | 'otp'>('email');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [role, setRole] = useState<'admin' | 'user'>('user');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSendOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    console.log(`🔍 Sending OTP for role: ${role}, email: ${email}`);
    
    try {
      if (role === 'admin') {
        console.log('📤 Calling admin login API...');
        await apiService.adminLogin(email);
        console.log('✅ Admin login API call successful');
      } else {
        console.log('📤 Calling user login API...');
        await apiService.userLogin(email);
        console.log('✅ User login API call successful');
      }
      setStep('otp');
    } catch (err: any) {
      console.error('❌ Login API error:', err);
      setError(err.message || 'Failed to send OTP');
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    console.log(`🔍 Verifying OTP for role: ${role}, email: ${email}, OTP: ${otp}`);
    
    try {
      let response: TokenResponse;
      let targetRoute: string;
      
      if (role === 'admin') {
        console.log('📤 Calling admin verify OTP API...');
        response = await apiService.adminVerifyOTP(email, otp);
        console.log('✅ Admin verify OTP successful');
        targetRoute = '/admin/dashboard';
      } else {
        console.log('📤 Calling user verify OTP API...');
        response = await apiService.userVerifyOTP(email, otp);
        console.log('✅ User verify OTP successful');
        targetRoute = '/user/dashboard';
      }
      
      console.log('🔐 Logging in user:', response.user);
      console.log('🎯 User role from backend:', response.user.role);
      console.log('🎯 Frontend selected role:', role);
      
      // First set the authentication state
      login(response);
      
      // Then navigate to the appropriate dashboard
      console.log(`🚀 Navigating to: ${targetRoute}`);
      navigate(targetRoute);
      
    } catch (err: any) {
      console.error('❌ OTP verification error:', err);
      setError(err.message || 'Invalid OTP');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setStep('email');
    setOtp('');
    setError('');
  };

  const handleRoleChange = (newRole: 'admin' | 'user') => {
    console.log(`🔄 Role changed from ${role} to ${newRole}`);
    setRole(newRole);
    setEmail('');
    setOtp('');
    setError('');
    setStep('email');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-xl shadow-2xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Sign In
            </h1>
            <p className="text-gray-600">
              Access your account
            </p>
          </div>

          {/* Role Toggle */}
          <div className="mb-6">
            <div className="text-center mb-2">
              <span className="text-sm font-medium text-gray-700">Select Role:</span>
            </div>
            <div className="flex bg-gray-100 rounded-lg p-1">
              <button
                type="button"
                onClick={() => handleRoleChange('user')}
                className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                  role === 'user'
                    ? 'bg-white text-blue-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                👤 User
              </button>
              <button
                type="button"
                onClick={() => handleRoleChange('admin')}
                className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                  role === 'admin'
                    ? 'bg-white text-blue-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                🔧 Admin
              </button>
            </div>
            <div className="mt-2 text-center">
              <span className="text-xs text-gray-500">
                Currently selected: <span className="font-medium text-blue-600">{role === 'user' ? 'User' : 'Admin'}</span>
              </span>
            </div>
          </div>

          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {step === 'email' ? (
            <form onSubmit={handleSendOTP} className="space-y-6">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  id="email"
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-3 px-4 rounded-lg transition duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                {loading ? 'Sending OTP...' : 'Send OTP'}
              </button>
            </form>
          ) : (
            <form onSubmit={handleVerifyOTP} className="space-y-6">
              <div>
                <label htmlFor="otp" className="block text-sm font-medium text-gray-700 mb-2">
                  One-Time Password
                </label>
                <input
                  type="text"
                  id="otp"
                  required
                  maxLength={6}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200 text-center text-2xl tracking-widest"
                  placeholder="000000"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
                />
                <p className="mt-2 text-sm text-gray-500 text-center">
                  OTP sent to {email}
                </p>
              </div>
              
              <div className="flex space-x-3">
                <button
                  type="button"
                  onClick={handleBack}
                  className="flex-1 py-3 px-4 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-200"
                >
                  Back
                </button>
                <button
                  type="submit"
                  disabled={loading || otp.length !== 6}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-3 px-4 rounded-lg transition duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  {loading ? 'Verifying...' : 'Sign In'}
                </button>
              </div>
            </form>
          )}

          <div className="mt-8 p-4 bg-gray-50 rounded-lg">
            <h3 className="text-sm font-medium text-gray-900 mb-2">Demo Credentials:</h3>
            <div className="text-sm text-gray-600 space-y-1">
              <p>Company Admin: admin@techcorp.com</p>
              <p>User: john@techcorp.com</p>
              <p>Password: OTP will be sent to email</p>
            </div>
          </div>

          <div className="mt-6 text-center">
            <p className="text-xs text-gray-500">
              Superadmin? <a href="/super-admin-login" className="text-blue-600 hover:text-blue-700">Login here</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CombinedLogin; 