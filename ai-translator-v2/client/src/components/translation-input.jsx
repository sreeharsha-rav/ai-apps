/* eslint-disable react-hooks/exhaustive-deps */
import TextPanel from "./common/text-panel";
import { useAtom, useAtomValue } from "jotai";
import {
  sourceTextAtom,
  sourceLanguageAtom,
  translateActionAtom,
} from "../store/atoms";
import debounce from "lodash/debounce";
import { useCallback } from "react";
import { useEffect } from "react";

const TranslationInput = () => {
  const [sourceText, setSourceText] = useAtom(sourceTextAtom);
  const sourceLanguage = useAtomValue(sourceLanguageAtom);
  const [, translateAction] = useAtom(translateActionAtom);

  const debouncedTranslate = useCallback(
    debounce(() => {
      console.log("Translating...");
      translateAction();
    }, 500),
    [translateAction],
  );

  useEffect(() => {
    if (sourceText.trim() === "") return;

    debouncedTranslate();

    return () => {
      console.log("Cancelling translation...");
      debouncedTranslate.cancel();
    };
  }, [sourceText, debouncedTranslate]);

  return (
    <TextPanel
      isReadOnly={false}
      placeholder="Enter text to translate..."
      text={sourceText}
      setText={setSourceText}
      language={sourceLanguage}
    />
  );
};

export default TranslationInput;
