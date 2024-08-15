import { useCallback } from 'react';

/**
 * Custom hook for translation functionality.
 * @returns An object containing the `translateText` function.
 */
export const useTranslation = () => {
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

  return { translateText };
};