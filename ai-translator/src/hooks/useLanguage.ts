import { useState, useCallback } from 'react';

/**
 * Custom hook for managing language selection.
 * 
 * @param initialLanguage - The initial language to be selected. Defaults to "French".
 * @returns An object containing the selected language and a function to handle language changes.
 */
export const useLanguage = (initialLanguage: string = "French") => {
  const [selectedLanguage, setSelectedLanguage] = useState<string>(initialLanguage);

  const handleLanguageChange = useCallback((language: string) => {
    setSelectedLanguage(language);
    console.log("Selected language:", language);
  }, []);

  return { selectedLanguage, handleLanguageChange };
};