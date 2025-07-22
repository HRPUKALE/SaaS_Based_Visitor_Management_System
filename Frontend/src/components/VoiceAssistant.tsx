import React, { useState, useEffect, useRef, forwardRef, useImperativeHandle } from 'react';
import { Send, RotateCcw } from 'lucide-react';
import { ChatMessage } from './ChatMessage';
import { VoiceButton } from './VoiceButton';
import { AppointmentSummary } from './AppointmentSummary';
import { useSpeechRecognition } from '../hooks/useSpeechRecognition';
import { useSpeechSynthesis } from '../hooks/useSpeechSynthesis';
import { GeminiService } from '../services/geminiService';
import { ChatMessage as ChatMessageType, AppointmentState, AppointmentBooking } from '../types';
import { useAuth } from '../context/AuthContext';
import { apiService, AppointmentCreateRequest } from '../services/api';

export interface VoiceAssistantRef {
  stopAllAudio: () => void;
}

const VoiceAssistant = forwardRef<VoiceAssistantRef>((props, ref) => {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [inputText, setInputText] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [appointmentState, setAppointmentState] = useState<AppointmentState>({
    employee_name: null,
    department: null,
    reason: null,
    appointment_time: null,
    visitor_name: null,
    email: null,
    phone: null,
    appointment_date: new Date().toISOString().split('T')[0] // YYYY-MM-DD format
  });
  const [booking, setBooking] = useState<AppointmentBooking | null>(null);
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { logout, user } = useAuth();
  
  const {
    isListening,
    transcript,
    startListening,
    stopListening,
    resetTranscript,
    isSupported: speechRecognitionSupported
  } = useSpeechRecognition();
  
  const {
    speak,
    isSpeaking,
    stop: stopSpeaking,
    isSupported: speechSynthesisSupported
  } = useSpeechSynthesis();

  // Expose methods to parent component
  useImperativeHandle(ref, () => ({
    stopAllAudio: () => {
      if (speechSynthesisSupported) {
        stopSpeaking();
      }
      if (isListening) {
        stopListening();
      }
    }
  }), [speechSynthesisSupported, stopSpeaking, isListening, stopListening]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle speech recognition transcript
  useEffect(() => {
    if (transcript && !isListening) {
      setInputText(transcript);
      resetTranscript();
    }
  }, [transcript, isListening, resetTranscript]);

  // Initial greeting
  useEffect(() => {
    const initialMessage: ChatMessageType = {
      role: 'assistant',
      content: 'Hello! I\'m your AI appointment assistant for Kanishka Software. I can help you book an appointment with any of our team members. You can either type or speak to me. Who would you like to meet with?',
      timestamp: new Date()
    };
    setMessages([initialMessage]);
    
    // Speak the initial greeting
    if (speechSynthesisSupported) {
      setTimeout(() => speak(initialMessage.content), 1000);
    }
  }, [speak, speechSynthesisSupported]);

  // Cleanup effect - Stop speech synthesis when component unmounts
  useEffect(() => {
    return () => {
      // Stop any ongoing speech synthesis when component unmounts
      if (speechSynthesisSupported && isSpeaking) {
        stopSpeaking();
      }
      // Also stop listening if active
      if (isListening) {
        stopListening();
      }
    };
  }, [speechSynthesisSupported, isSpeaking, stopSpeaking, isListening, stopListening]);

  // Helper function to clean text for voice output
  const cleanTextForVoice = (text: string): string => {
    return text
      // Remove all emojis using comprehensive regex
      .replace(/[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F1E0}-\u{1F1FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]/gu, '')
      // Remove specific emoji patterns that might be missed
      .replace(/[📧📱📋👤🕐👋📅✅🤖]/g, '')
      // Remove email and phone lines from summaries
      .replace(/Email:.*$/gm, '')
      .replace(/Phone:.*$/gm, '')
      // Remove verification messages
      .replace(/You can verify.*$/gm, '')
      // Clean up extra whitespace
      .replace(/\s+/g, ' ')
      .trim();
  };

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isProcessing) return;

    console.log('📨 Sending message:', content);

    const userMessage: ChatMessageType = {
      role: 'user',
      content: content.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsProcessing(true);

    try {
      console.log('🤖 Processing with Gemini service...');
      const result = await GeminiService.processConversation(
        [...messages, userMessage],
        appointmentState
      );

      console.log('📋 Gemini service result:', result);

      const assistantMessage: ChatMessageType = {
        role: 'assistant',
        content: result.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
      setAppointmentState(result.updatedState);

      // Check if we have a final booking
      if (result.finalBooking) {
        console.log('🎉 Final booking received, showing confirmation card...');
        setBooking(result.finalBooking);
      }

      // Enhanced voice feedback with emoji removal
      if (speechSynthesisSupported && !isSpeaking) {
        const voiceText = cleanTextForVoice(result.response);
        if (voiceText.trim()) {
          speak(voiceText);
        }
      }
      
    } catch (error) {
      console.error('❌ Error processing message:', error);
      const errorMessage: ChatMessageType = {
        role: 'assistant',
        content: 'I apologize, but I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleEditBooking = (updatedBooking: AppointmentBooking) => {
    setBooking(updatedBooking);
    
    // Update the appointment state as well
    setAppointmentState({
      employee_name: updatedBooking.employee_name,
      department: updatedBooking.department,
      reason: updatedBooking.reason,
      appointment_time: updatedBooking.appointment_time,
      visitor_name: updatedBooking.visitor_name,
      email: updatedBooking.email,
      phone: updatedBooking.phone,
      appointment_date: updatedBooking.appointment_date
    });

    // Add a message about the update
    const updateMessage: ChatMessageType = {
      role: 'assistant',
      content: 'Your appointment details have been updated successfully!',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, updateMessage]);
  };

  const handleReset = () => {
    setMessages([]);
    setAppointmentState({
      employee_name: null,
      department: null,
      reason: null,
      appointment_time: null,
      visitor_name: null,
      email: null,
      phone: null,
      appointment_date: new Date().toISOString().split('T')[0] // YYYY-MM-DD format
    });
    setBooking(null);
    setInputText('');
    stopSpeaking();
    
    // Re-add initial greeting
    const initialMessage: ChatMessageType = {
      role: 'assistant',
      content: 'Hello! I\'m your AI appointment assistant for Kanishka Software. I can help you book an appointment with any of our team members. You can either type or speak to me. Who would you like to meet with?',
      timestamp: new Date()
    };
    setMessages([initialMessage]);
    
    if (speechSynthesisSupported) {
      setTimeout(() => speak(initialMessage.content), 500);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(inputText);
    }
  };

  // Save appointment to backend
  const saveAppointment = async (data: AppointmentBooking) => {
    console.log('🔍 Starting appointment save process...');
    console.log('👤 Current user:', user);
    console.log('📋 Appointment data:', data);
    
    if (!user) {
      const errorMsg = "You must be logged in to book an appointment.";
      console.error('❌ No user found:', errorMsg);
      setSaveError(errorMsg);
      setSaving(false);
      return;
    }
    
    if (!user.company_id) {
      const errorMsg = "User account is missing company ID. Please contact your administrator.";
      console.error('❌ No company_id found:', errorMsg);
      setSaveError(errorMsg);
      setSaving(false);
      return;
    }
    
    setSaving(true);
    setSaveError(null);
    
    try {
      // Convert to API format
      const appointmentData: AppointmentCreateRequest = {
        employee_name: data.employee_name,
        department: data.department,
        reason: data.reason || undefined,
        appointment_date: data.appointment_date,
        appointment_time: data.appointment_time,
        visitor_name: data.visitor_name,
        visitor_email: data.email,
        visitor_phone: data.phone || undefined,
        booking_method: 'voice'
      };

      console.log('📤 Sending appointment data to API:', appointmentData);
      const createdAppointment = await apiService.createAppointment(appointmentData);
      console.log('✅ Appointment created successfully:', createdAppointment);
      
      // Show success message
      const successMessage: ChatMessageType = {
        role: 'assistant',
        content: 'Your appointment has been successfully saved to our system!',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, successMessage]);
      
    } catch (err: any) {
      console.error('❌ Error saving appointment:', err);
      const errorMsg = err.message || 'Failed to save appointment. Please try again.';
      setSaveError(errorMsg);
      
      // Show error message in chat
      const errorMessage: ChatMessageType = {
        role: 'assistant',
        content: `Sorry, I couldn't save your appointment: ${errorMsg}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setSaving(false);
    }
  };

  // Close modal and return to chat
  const handleCloseSummary = () => {
    setBooking(null);
    setSaveError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                Voice Assistant
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">
                Logged in as: {user?.email}
              </span>
              <button
                onClick={logout}
                className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Chat Interface */}
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full p-4">
        {/* Debug Info - Remove this in production */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
          <div className="text-sm text-yellow-800">
            <strong>Debug Info:</strong> User: {user?.email || 'Not logged in'} | 
            Company ID: {user?.company_id || 'None'} | 
            Role: {user?.role || 'None'}
            {(!user || !user.company_id) && (
              <div className="mt-2 text-red-600">
                ⚠️ Authentication issue detected. Please log out and log back in.
              </div>
            )}
          </div>
        </div>
        
        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto mb-4 space-y-4">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Section */}
        <div className="bg-white rounded-lg shadow-lg p-4">
          <div className="flex items-center space-x-2">
            <div className="flex-1 relative">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message or use voice..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isProcessing}
              />
            </div>
            
            <VoiceButton
              isListening={isListening}
              isSpeaking={isSpeaking}
              onStartListening={startListening}
              onStopListening={stopListening}
              onStopSpeaking={stopSpeaking}
              isSupported={speechRecognitionSupported}
            />
            
            <button
              onClick={() => handleSendMessage(inputText)}
              disabled={!inputText.trim() || isProcessing}
              className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send size={20} />
            </button>
            
            <button
              onClick={handleReset}
              className="p-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
              title="Reset conversation"
            >
              <RotateCcw size={20} />
            </button>
          </div>
        </div>
      </div>

      {/* Booking Summary Modal */}
      {booking && (
        <>
          {saving && (
            <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
              <div className="bg-white p-6 rounded-xl shadow-xl text-center">
                <div className="mb-2 text-lg font-semibold">Saving appointment...</div>
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto" />
              </div>
            </div>
          )}
          {saveError && (
            <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
              <div className="bg-white p-6 rounded-xl shadow-xl text-center">
                <div className="mb-2 text-lg font-semibold text-red-600">{saveError}</div>
                <button className="mt-2 px-4 py-2 bg-blue-600 text-white rounded" onClick={handleCloseSummary}>Close</button>
              </div>
            </div>
          )}
          <AppointmentSummary
            booking={booking}
            onClose={handleCloseSummary}
            onEdit={handleEditBooking}
            onSave={saveAppointment}
            isSaving={saving}
          />
        </>
      )}
    </div>
  );
});

export default VoiceAssistant; 