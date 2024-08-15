import { useState, useCallback } from 'react';
import { useTranslation } from './useTranslation';

/**
 * Represents a chat message.
 */
interface Message {
  id: number;
  text: string;
  isUser: boolean;
}

/**
 * Custom hook for managing chat functionality.
 *
 * @param selectedLanguage - The selected language for translation.
 * @returns An object containing the chat messages, translation status, and submit handler.
 */
export const useChat = (selectedLanguage: string) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTranslating, setIsTranslating] = useState<boolean>(false);
  const { translateText } = useTranslation();

  const addMessage = useCallback((text: string, isUser: boolean) => {
    const newMessage: Message = { id: Date.now(), text, isUser };
    setMessages(prev => [...prev, newMessage]);
  }, []);

  const handleSubmit = useCallback(async (inputValue: string) => {
    if (inputValue.trim() && !isTranslating) {
      setIsTranslating(true);
      addMessage(inputValue, true);

      try {
        console.log("Translating:", inputValue, selectedLanguage);
        const translatedText = await translateText(inputValue, selectedLanguage);
        addMessage(translatedText, false);
      } catch (error) {
        console.error("Translation error:", error);
        // Optionally add an error message to the chat
      } finally {
        setIsTranslating(false);
      }
    }
  }, [selectedLanguage, isTranslating, addMessage, translateText]);

  return { messages, isTranslating, handleSubmit };
};