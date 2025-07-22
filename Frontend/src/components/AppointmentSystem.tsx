import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const AppointmentSystem: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleManualBooking = () => {
    navigate('/user/manual-booking');
  };

  const handleTalkToVira = () => {
    navigate('/user/talk-to-vira');
  };

  const handleLogout = () => {
    logout();
    navigate('/user-login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">KANISHKA</div>
                <div className="text-sm font-semibold text-green-600">SOFTWARE</div>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 transition duration-200"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Welcome to Our Appointment System
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Book your visit with ease using our intuitive booking system. Choose your preferred method below.
          </p>
        </div>

        {/* Booking Options */}
        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {/* Manual Booking Card */}
          <div className="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition duration-300">
            <div className="text-center">
              {/* Icon */}
              <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>

              {/* Title */}
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Manual Booking</h2>
              
              {/* Description */}
              <p className="text-gray-600 mb-6">
                Fill out a traditional form at your own pace
              </p>

              {/* Features */}
              <div className="space-y-3 mb-8">
                <div className="flex items-center text-sm text-gray-700">
                  <div className="w-5 h-5 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                    <svg className="w-3 h-3 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                    </svg>
                  </div>
                  Select department and employee
                </div>
                <div className="flex items-center text-sm text-gray-700">
                  <div className="w-5 h-5 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                    <svg className="w-3 h-3 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
                    </svg>
                  </div>
                  Automatic date selection (today)
                </div>
                <div className="flex items-center text-sm text-gray-700">
                  <div className="w-5 h-5 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                    <svg className="w-3 h-3 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                    </svg>
                  </div>
                  Pick available time slots
                </div>
              </div>

              {/* Button */}
              <button
                onClick={handleManualBooking}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-lg transition duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Book Manually
              </button>
            </div>
          </div>

          {/* Talk to Vira Card */}
          <div className="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition duration-300">
            <div className="text-center">
              {/* Icon */}
              <div className="w-16 h-16 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>

              {/* Title */}
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Talk to Vira</h2>
              
              {/* Description */}
              <p className="text-gray-600 mb-6">
                Book your appointment using voice commands
              </p>

              {/* Features */}
              <div className="space-y-3 mb-8">
                <div className="flex items-center text-sm text-gray-700">
                  <div className="w-5 h-5 bg-green-100 rounded-full flex items-center justify-center mr-3">
                    <svg className="w-3 h-3 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd" />
                    </svg>
                  </div>
                  Speak naturally to our AI assistant
                </div>
                <div className="flex items-center text-sm text-gray-700">
                  <div className="w-5 h-5 bg-green-100 rounded-full flex items-center justify-center mr-3">
                    <svg className="w-3 h-3 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  Get instant confirmation
                </div>
                <div className="flex items-center text-sm text-gray-700">
                  <div className="w-5 h-5 bg-green-100 rounded-full flex items-center justify-center mr-3">
                    <svg className="w-3 h-3 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  Hands-free accessibility
                </div>
              </div>

              {/* Button */}
              <button
                onClick={handleTalkToVira}
                className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-6 rounded-lg transition duration-200 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
              >
                Talk to Vira
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-white border-t border-gray-200 py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center text-sm text-gray-600">
            Powered by Kanishka Software PVT LTD • AI-Enhanced Appointment Booking
          </div>
        </div>
      </div>
    </div>
  );
};

export default AppointmentSystem; 