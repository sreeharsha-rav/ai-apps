"use client";

import { useCallback, useState } from "react";
import { TranslationInput, TranslationOutput } from "./Translation";
import LanguageSelector from "./LanguageSelector";
import ChatInput from "./ChatInput";
import { useChat } from "@/hooks/useChat";
import { useLanguage } from "@/hooks/useLanguage";

const styles = {
  chat_window_wrapper: "flex-grow overflow-y-auto pb-4 space-y-4 mx-auto w-full max-w-[576px]",
  chat_input_wrapper: "flex flex-col items-start gap-4 bg-white pt-2 px-2 pb-6 sticky bottom-0 w-full",
};

/**
 * AiChat component.
 *
 * This component represents a chat interface for AI translation.
 * It allows users to input messages, select a language, and view translated messages.
 *
 * @returns The AiChat component.
 */
const AiChat: React.FC = () => {
  const [inputValue, setInputValue] = useState<string>('');
  const { selectedLanguage, handleLanguageChange } = useLanguage();
  const { messages, isTranslating, handleSubmit } = useChat(selectedLanguage);

  // Handle input change
  const handleInputChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  }, []);

  // Handle user input submission
  const onSubmit = useCallback(() => {
    handleSubmit(inputValue);
    setInputValue('');
  }, [handleSubmit, inputValue]);

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
          onSubmit={onSubmit}
          isDisabled={isTranslating}
        />
      </div>
    </>
  );
}

export default AiChat;