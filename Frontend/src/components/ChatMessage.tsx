import React from 'react';
import { User, Bot } from 'lucide-react';
import { ChatMessage as ChatMessageType } from '../types';

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  
  return (
    <div className={`flex gap-3 mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-600 rounded-full flex items-center justify-center shadow-lg">
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}
      
      <div className={`
        max-w-[80%] p-4 rounded-2xl shadow-lg
        ${isUser 
          ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-br-md' 
          : 'bg-white border border-gray-200 text-gray-800 rounded-bl-md'
        }
      `}>
        <div className="whitespace-pre-wrap text-sm leading-relaxed">
          {message.content}
        </div>
        <div className={`text-xs mt-2 opacity-70 ${isUser ? 'text-blue-100' : 'text-gray-500'}`}>
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
      
      {isUser && (
        <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center shadow-lg">
          <User className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  );
};