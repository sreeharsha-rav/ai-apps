import TextPanel from "./common/text-panel";
import { useAtom, useAtomValue } from "jotai";
import { targetTextAtom, targetLanguageAtom } from "../store/atoms";

const TranslationOutput = () => {
  const [targetText, setTargetText] = useAtom(targetTextAtom);
  const targetLanguage = useAtomValue(targetLanguageAtom);

  return (
    <TextPanel
      isReadOnly={true}
      placeholder=""
      text={targetText}
      setText={setTargetText}
      language={targetLanguage}
    />
  );
};

export default TranslationOutput;
