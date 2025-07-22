import { useState, useCallback } from 'react';

interface SpeechSynthesisHook {
  speak: (text: string) => void;
  isSpeaking: boolean;
  stop: () => void;
  isSupported: boolean;
}

export const useSpeechSynthesis = (): SpeechSynthesisHook => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const isSupported = 'speechSynthesis' in window;

  const speak = useCallback((text: string) => {
    if (!isSupported) return;

    // Stop any ongoing speech
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.3;
    utterance.pitch = 1;
    utterance.volume = 0.8;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  }, [isSupported]);

  const stop = useCallback(() => {
    if (isSupported) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  }, [isSupported]);

  return {
    speak,
    isSpeaking,
    stop,
    isSupported
  };
};