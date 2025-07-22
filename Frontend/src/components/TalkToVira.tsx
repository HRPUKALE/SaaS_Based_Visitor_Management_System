import React, { useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import VoiceAssistant, { VoiceAssistantRef } from './VoiceAssistant';

const TalkToVira: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const voiceAssistantRef = useRef<VoiceAssistantRef>(null);

  const handleBack = () => {
    // Stop any ongoing speech synthesis before navigating
    if (voiceAssistantRef.current?.stopAllAudio) {
      voiceAssistantRef.current.stopAllAudio();
    }
    navigate('/user/dashboard');
  };

  const handleLogout = () => {
    // Stop any ongoing speech synthesis before navigating
    if (voiceAssistantRef.current?.stopAllAudio) {
      voiceAssistantRef.current.stopAllAudio();
    }
    logout();
    navigate('/user-login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <button
                onClick={handleBack}
                className="mr-4 p-2 text-gray-600 hover:text-gray-900"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
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
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Talk to Vira
          </h1>
          <p className="text-gray-600">
            Book your appointment using voice commands with our AI assistant
          </p>
        </div>

        {/* Voice Assistant Component */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <VoiceAssistant ref={voiceAssistantRef} />
        </div>
      </div>
    </div>
  );
};

export default TalkToVira; 