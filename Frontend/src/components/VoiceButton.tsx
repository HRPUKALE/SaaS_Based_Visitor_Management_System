import React from 'react';
import { Mic, MicOff, Volume2, VolumeX } from 'lucide-react';

interface VoiceButtonProps {
  isListening: boolean;
  isSpeaking: boolean;
  onStartListening: () => void;
  onStopListening: () => void;
  onStopSpeaking: () => void;
  isSupported: boolean;
}

export const VoiceButton: React.FC<VoiceButtonProps> = ({
  isListening,
  isSpeaking,
  onStartListening,
  onStopListening,
  onStopSpeaking,
  isSupported
}) => {
  if (!isSupported) {
    return (
      <div className="text-sm text-gray-500 text-center p-2">
        Voice features not supported in this browser
      </div>
    );
  }

  return (
    <div className="flex items-center gap-3">
      {/* Microphone Button */}
      <button
        onClick={isListening ? onStopListening : onStartListening}
        disabled={isSpeaking}
        className={`
          relative p-4 rounded-full transition-all duration-300 transform hover:scale-105
          ${isListening 
            ? 'bg-red-500 hover:bg-red-600 shadow-lg shadow-red-500/30' 
            : 'bg-blue-500 hover:bg-blue-600 shadow-lg shadow-blue-500/30'
          }
          ${isSpeaking ? 'opacity-50 cursor-not-allowed' : ''}
          disabled:transform-none
        `}
      >
        {isListening ? (
          <MicOff className="w-6 h-6 text-white" />
        ) : (
          <Mic className="w-6 h-6 text-white" />
        )}
        
        {/* Pulse animation when listening */}
        {isListening && (
          <div className="absolute inset-0 rounded-full bg-red-500 animate-ping opacity-75"></div>
        )}
      </button>

      {/* Speaker Button */}
      {isSpeaking && (
        <button
          onClick={onStopSpeaking}
          className="p-3 rounded-full bg-green-500 hover:bg-green-600 transition-all duration-300 transform hover:scale-105 shadow-lg shadow-green-500/30"
        >
          <Volume2 className="w-5 h-5 text-white" />
        </button>
      )}

      {/* Status Text */}
      <div className="text-sm font-medium">
        {isListening && (
          <span className="text-red-500 flex items-center gap-2">
            <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
            Listening...
          </span>
        )}
        {isSpeaking && (
          <span className="text-green-500 flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            Speaking...
          </span>
        )}
        {!isListening && !isSpeaking && (
          <span className="text-gray-500">Tap to speak</span>
        )}
      </div>
    </div>
  );
};