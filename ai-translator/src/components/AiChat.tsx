"use client";

import { useCallback, useState } from "react";
import { TranslationInput, TranslationOutput } from "./Translation";
import LanguageSelector from "./LanguageSelector";
import ChatInput from "./ChatInput";

const styles = {
  chat_window_wrapper: "flex-grow overflow-y-auto pb-4 space-y-4 mx-auto w-full max-w-[576px]",
  chat_input_wrapper: "flex flex-col items-start gap-4 bg-white pt-2 px-2 pb-6 sticky bottom-0 w-full",
};

interface Message {
  id: number;
  text: string;
  isUser: boolean;
}

const AiChat: React.FC = () => {
  const [inputValue, setInputValue] = useState<string>('');
  const [selectedLanguage, setSelectedLanguage] = useState<string>("French");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTranslating, setIsTranslating] = useState<boolean>(false);

  const handleInputChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  }, []);


  const handleLanguageChange = useCallback((language: string) => {
    setSelectedLanguage(language);
    console.log("Selected language:", language);
  }, []);

  const translateText = useCallback(async (text: string, language: string): Promise<string> => {
    try {
      const response = await fetch('/api/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, targetLanguage: language }),
      });

      if (!response.ok) {
        throw new Error('Translation request failed');
      }

      const data = await response.json();
      return data.translatedText;
    } catch (error) {
      console.error('Translation error:', error);
      throw error;
    }
  }, []);

  const handleSubmit = useCallback(async () => {
    if (inputValue.trim() && !isTranslating) {
      setIsTranslating(true);
      const userMessage: Message = { id: Date.now(), text: inputValue, isUser: true };
      setMessages(prev => [...prev, userMessage]);
      setInputValue('');

      try {
        console.log("Translating:", inputValue, selectedLanguage);
        const translatedText = await translateText(inputValue, selectedLanguage);
        const aiMessage: Message = { id: Date.now() + 1, text: translatedText, isUser: false };
        setMessages(prev => [...prev, aiMessage]);
      } catch (error) {
        console.error("Translation error:", error);
        // Optionally add an error message to the chat
      } finally {
        setIsTranslating(false);
      }
    }
  }, [inputValue, selectedLanguage, isTranslating, translateText]);

  return (
    <>
      <ul className={styles.chat_window_wrapper}>
      {messages.map((message) => (
          message.isUser ? (
            <TranslationInput key={message.id} text={message.text} />
          ) : (
            <TranslationOutput key={message.id} text={message.text} />
          )
        ))}
      </ul>
      <div className={styles.chat_input_wrapper}>
        <LanguageSelector
          selectedLanguage={selectedLanguage}
          onLanguageChange={handleLanguageChange}
        />
        <ChatInput
          value={inputValue}
          onChange={handleInputChange}
          onSubmit={handleSubmit}
          isDisabled={isTranslating}
        />
      </div>
    </>
  );
}

export default AiChat;