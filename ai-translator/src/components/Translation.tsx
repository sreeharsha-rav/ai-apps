const styles = {
  input_wrapper: "flex ms-auto gap-x-2 sm:gap-x-4",
  input_container: "grow text-end space-y-3",
  input_card: "inline-block bg-neutral-200 rounded-2xl p-4 shadow-sm",
  input_text: "text-sm text-gray-800",
  input_avatar: "shrink-0 inline-flex items-center justify-center size-[38px] rounded-full bg-gray-600",
  input_avatarText: "text-sm font-medium text-white leading-none",

  output_wrapper: "max-w-lg flex gap-x-2 sm:gap-x-4 me-11",
  output_avatar: "shrink-0 inline-flex items-center justify-center size-[38px] rounded-full bg-blue-600",
  output_avatarText: "text-sm font-medium text-white leading-none",
  output_card: "bg-blue-200 rounded-2xl p-4 space-y-3",
  output_text: "text-sm text-blue-800",
};

/**
 * Represents the props for the TranslationInput component.
 */
interface TranslationInputProps {
    text: string;
}

/**
 * TranslationInput component
 * 
 * This component is responsible for rendering the input text provided by the user.
 * It displays the text inside a styled card and includes an avatar with the letter "G".
 * 
 * @param {TranslationInputProps} props - The props for the component.
 * @param {string} props.text - The input text to be displayed.
 * 
 * @returns {JSX.Element} The rendered TranslationInput component.
 */
const TranslationInput: React.FC<TranslationInputProps> = ({ text }) => {
  return (
    <li className={styles.input_wrapper}>
      <div className={styles.input_container}>
        <div className={styles.input_card}>
          <p className={styles.input_text}>
            {text}
          </p>
        </div>
      </div>
      <span className={styles.input_avatar}>
        <span className={styles.input_avatarText}>G</span>
      </span>
    </li>
  );
};

/**
 * Represents the props for the TranslationOutput component.
 */
interface TranslationOutputProps {
    text: string;
}

/**
 * TranslationOutput component
 * 
 * This component is responsible for rendering the translated text provided by the AI.
 * It displays the text inside a styled card and includes an avatar with the text "AI".
 * 
 * @param {TranslationOutputProps} props - The props for the component.
 * @param {string} props.text - The translated text to be displayed.
 * 
 * @returns {JSX.Element} The rendered TranslationOutput component.
 */
const TranslationOutput: React.FC<TranslationOutputProps> = ({ text }) => {
  return (
    <li className={styles.output_wrapper}>
      <span className={styles.output_avatar}>
        <span className={styles.output_avatarText}>AI</span>
    </span>
      <div className={styles.output_card}>
        <p className={styles.output_text}>
          {text}
        </p>
      </div>
    </li>
  );
};

export { TranslationInput, TranslationOutput };