import { TextField } from "@/subframe/components/TextField";

const styles = {
    chat_input_wrapper: "flex h-16 w-full flex-none items-center gap-2 overflow-hidden rounded-full bg-neutral-100 pt-3 pr-4 pb-3 pl-4",
    text_field: "h-auto grow shrink-0 basis-0",
};

/**
 * Represents the props for the ChatInput component.
 */
interface ChatInputProps {
    value: string;
    onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
    onSubmit: () => void;
    isDisabled: boolean;
  }

/**
 * ChatInput component.
 * 
 * @component
 * @param {Object} props - The component props.
 * @param {string} props.value - The value of the input field.
 * @param {Function} props.onChange - The function to handle input field changes.
 * @param {Function} props.onSubmit - The function to handle form submission.
 * @param {boolean} props.isDisabled - Whether the input field is disabled.
 * @returns {JSX.Element} The rendered ChatInput component.
 */
const ChatInput: React.FC<ChatInputProps> = ({ value, onChange, onSubmit, isDisabled }) => {
    const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
      if (event.key === 'Enter' && !event.shiftKey && !isDisabled) {
        event.preventDefault();
        onSubmit();
      }
    };

    return (
        <div className={styles.chat_input_wrapper}>
            <TextField
              className={styles.text_field}
              variant="filled"
              label=""
              helpText=""
              iconRight="FeatherCornerDownLeft"
            >
              <TextField.Input
                placeholder="Chat to translate..."
                value={value}
                onChange={onChange}
                onKeyDown={handleKeyDown}
                disabled={isDisabled}
              />
            </TextField>
        </div>
    );
};

export default ChatInput;