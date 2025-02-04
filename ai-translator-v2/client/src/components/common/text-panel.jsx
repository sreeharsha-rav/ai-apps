import PropTypes from "prop-types";
import { Volume2, Copy } from "lucide-react";
import { ttsAtom } from "../../store/atoms";
import { useAtomValue } from "jotai";
import { memo, useCallback } from "react";

const TextPanel = memo(
  ({ isReadOnly, placeholder, text, setText, language }) => {
    const ttsState = useAtomValue(ttsAtom);

    const handleTextChange = useCallback(
      (e) => {
        setText(e.target.value);
      },
      [setText],
    );

    const handleSpeakText = useCallback(() => {
      console.log(`Speaking text: ${text} in ${language.name}`);
    }, [text, language]);

    const handleCopyText = useCallback(() => {
      if (!text) return;
      console.log(`Copying text: ${text}`);
      navigator.clipboard.writeText(text);
    }, [text]);

    return (
      <div className="flex flex-col relative w-full h-full p-2">
        <textarea
          className="w-full h-32 bg-transparent border-0 resize-none focus:outline-none text-3xl text-base-500"
          readOnly={isReadOnly}
          placeholder={placeholder}
          value={text}
          onChange={handleTextChange}
        />

        {/* Text-to-speech button on the bottom left */}
        {text && (
          <>
            <div className="absolute bottom-2 left-2">
              <button
                onClick={handleSpeakText}
                className={`btn btn-ghost btn-xs btn-circle ${ttsState.isPlaying ? "text-primary" : "text-base-500"}`}
                title={ttsState.isPlaying ? "Stop speaking" : "Speak text"}
              >
                <Volume2 size={16} />
              </button>
            </div>
            <div className="absolute bottom-2 right-2">
              <button
                onClick={handleCopyText}
                className="btn btn-ghost btn-xs btn-circle text-base-500"
                title="Copy text"
              >
                <Copy size={16} />
              </button>
            </div>
          </>
        )}
      </div>
    );
  },
);

TextPanel.propTypes = {
  isReadOnly: PropTypes.bool,
  placeholder: PropTypes.string,
  text: PropTypes.string.isRequired,
  setText: PropTypes.func.isRequired,
  language: PropTypes.object.isRequired,
};

TextPanel.displayName = "TextPanel";

export default TextPanel;
