import { atom } from "jotai";
import translateText from "../api/translate";

// Create atoms for source and target languages
export const sourceLanguageAtom = atom({ name: "English", code: "en" });
export const targetLanguageAtom = atom({ name: "Hindi", code: "hi" });

// Create atoms for source and target text
export const sourceTextAtom = atom("");
export const targetTextAtom = atom("");

// Create atoms for text translation
export const translateActionAtom = atom(null, async (get, set) => {
  const sourceText = get(sourceTextAtom);
  const sourceLanguageCode = get(sourceLanguageAtom).code;
  const targetLanguageCode = get(targetLanguageAtom).code;

  if (!sourceText) {
    set(targetTextAtom, "");
    return;
  }

  const translation = await translateText(
    sourceText,
    sourceLanguageCode,
    targetLanguageCode,
  );
  set(targetTextAtom, translation);
});

// Create atoms for text-to-speech
export const ttsAtom = atom({ audio: null, isPlaying: false });

// Create atoms for speech-to-text
