import { useAtom } from "jotai";
import { sourceLanguageAtom, targetLanguageAtom } from "../store/atoms";
import { useCallback } from "react";
import { ArrowLeftRight } from "lucide-react";
import languages from "../data/languages";

const LanguageSelector = () => {
  const [sourceLanguage, setSourceLanguage] = useAtom(sourceLanguageAtom);
  const [targetLanguage, setTargetLanguage] = useAtom(targetLanguageAtom);

  const handleSwapLanguages = useCallback(() => {
    const tempLang = sourceLanguage;
    setSourceLanguage(targetLanguage);
    setTargetLanguage(tempLang);
  }, [sourceLanguage, targetLanguage, setSourceLanguage, setTargetLanguage]);

  return (
    <div className="flex items-center justify-center gap-2 px-4 mb-4">
      <div className="dropdown">
        <button
          className="btn"
          popovertarget="source-language-dropdown"
          style={{ anchorName: `--anchor-source-language` }}
        >
          {sourceLanguage.name}
        </button>
        <ul
          className="dropdown dropdown-top dropdown-center menu w-52 bg-base-100 shadow-sm max-h-60 overflow-y-auto"
          popover="auto"
          id="source-language-dropdown"
          style={{ positionAnchor: `--anchor-source-language` }}
        >
          {languages.map((lang) => (
            <li key={lang.code}>
              <a onClick={() => setSourceLanguage(lang)}>{lang.name}</a>
            </li>
          ))}
        </ul>
      </div>

      <button
        onClick={handleSwapLanguages}
        className="btn btn-circle btn-soft btn-xs"
      >
        <ArrowLeftRight size={16} />
      </button>

      <div className="dropdown">
        <button
          className="btn"
          popovertarget="target-language-dropdown"
          style={{ anchorName: `--anchor-target-language` }}
        >
          {targetLanguage.name}
        </button>
        <ul
          className="dropdown dropdown-top dropdown-center menu w-52 bg-base-100 shadow-sm max-h-60 overflow-y-auto"
          popover="auto"
          id="target-language-dropdown"
          style={{ positionAnchor: `--anchor-target-language` }}
        >
          {languages.map((lang) => (
            <li key={lang.code}>
              <a onClick={() => setTargetLanguage(lang)}>{lang.name}</a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

LanguageSelector.displayName = "LanguageSelector";

export default LanguageSelector;
