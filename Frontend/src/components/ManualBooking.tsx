import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ManualBookingForm from './ManualBookingForm';
import { AppointmentSummary } from './AppointmentSummary';
import { AppointmentBooking } from '../types';

const ManualBooking: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [booking, setBooking] = useState<AppointmentBooking | null>(null);

  const handleBook = (bookingData: AppointmentBooking) => {
    // Here you would typically send the booking data to your backend
    console.log('Booking data:', bookingData);
    setBooking(bookingData);
  };

  const handleBack = () => {
    navigate('/user/dashboard');
  };

  const handleLogout = () => {
    logout();
    navigate('/user-login');
  };

  const handleCloseSummary = () => {
    setBooking(null);
    navigate('/user/dashboard');
  };

  const handleEditBooking = (updatedBooking: AppointmentBooking) => {
    setBooking(updatedBooking);
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
      <div className="flex justify-center items-center py-8">
        <ManualBookingForm onBook={handleBook} onBack={handleBack} />
      </div>

      {/* Booking Summary Modal */}
      {booking && (
        <AppointmentSummary
          booking={booking}
          onClose={handleCloseSummary}
          onEdit={handleEditBooking}
        />
      )}
    </div>
  );
};

export default ManualBooking; 