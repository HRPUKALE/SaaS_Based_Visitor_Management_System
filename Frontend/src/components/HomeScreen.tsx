import React from 'react';
import Logo from './Logo';

interface HomeScreenProps {
  onManualBooking: () => void;
  onTalkToVira: () => void;
}

const HomeScreen: React.FC<HomeScreenProps> = ({ onManualBooking, onTalkToVira }: HomeScreenProps) => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-blue-50 py-8 px-2">
      <Logo className="mb-6" />
      <h1 className="text-4xl font-bold text-center mb-2">Welcome to Our Appointment System</h1>
      <p className="text-center text-gray-600 mb-6 max-w-xl">
        Book your visit with ease using our intuitive booking system. Choose your preferred method below.
      </p>
      <div className="flex flex-col md:flex-row gap-8 mb-8">
        {/* Manual Booking Card */}
        <div className="bg-white rounded-xl shadow-lg p-8 flex-1 max-w-md flex flex-col items-center">
          <div className="bg-blue-100 rounded-full p-4 mb-4">
            <span className="text-3xl text-blue-600">
              <i className="fas fa-clipboard-list"></i>
            </span>
          </div>
          <h2 className="text-xl font-semibold mb-2">Manual Booking</h2>
          <p className="text-center text-gray-500 mb-4">Fill out a traditional form at your own pace</p>
          <ul className="text-gray-500 text-sm mb-6 space-y-1">
            <li>👤 Select department and employee</li>
            <li>📅 Automatic date selection (today)</li>
            <li>⏰ Pick available time slots</li>
          </ul>
          <button
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg shadow"
            onClick={onManualBooking}
          >
            Book Manually
          </button>
        </div>
        {/* Talk to Vira Card */}
        <div className="bg-white rounded-xl shadow-lg p-8 flex-1 max-w-md flex flex-col items-center">
          <div className="bg-green-100 rounded-full p-4 mb-4">
            <span className="text-3xl text-green-600">
              <i className="fas fa-microphone"></i>
            </span>
          </div>
          <h2 className="text-xl font-semibold mb-2">Talk to Vira</h2>
          <p className="text-center text-gray-500 mb-4">Book your appointment using voice commands</p>
          <ul className="text-gray-500 text-sm mb-6 space-y-1">
            <li>💬 Speak naturally to our AI assistant</li>
            <li>✅ Get instant confirmation</li>
            <li>♿ Hands-free accessibility</li>
          </ul>
          <button
            className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-6 rounded-lg shadow"
            onClick={onTalkToVira}
          >
            Talk to Vira
          </button>
        </div>
      </div>
      <p className="text-center text-gray-400 text-sm mt-8">
        Powered by <span className="text-blue-700 font-semibold">Kanishka Software PVT LTD</span> • AI-Enhanced Appointment Booking
      </p>
    </div>
  );
};

export default HomeScreen; 