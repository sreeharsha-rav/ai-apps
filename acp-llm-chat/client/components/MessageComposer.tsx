import { Button } from "@/components/ui/button";
import { AutosizeTextarea } from "@/components/ui/autosize-textarea";
import { Send, Loader } from "lucide-react";

interface MessageComposerProps {
    inputValue: string;
    setInputValue: (value: string) => void;
    onSend: () => void;
    isGenerating: boolean;
}

export function MessageComposer({
    inputValue,
    setInputValue,
    onSend,
    isGenerating
}: MessageComposerProps) {
    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            onSend();
        }
    };

    return (
        <div className="flex-none p-4 bg-background border-t border-border/50">
            <div className="max-w-3xl mx-auto">
                <div className="relative flex items-end group bg-muted/50 border border-border/50 rounded-2xl focus-within:ring-1 focus-within:ring-primary/20 focus-within:border-primary/20 transition-all shadow-sm">
                    <AutosizeTextarea
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Ask anything..."
                        className="w-full resize-none border-0 bg-transparent py-4 pl-4 pr-14 focus-visible:ring-0 focus-visible:ring-offset-0 text-base max-h-[200px]"
                        minRows={1}
                        maxRows={8}
                        disabled={isGenerating}
                    />
                    <Button
                        onClick={() => onSend()}
                        size="icon"
                        disabled={!inputValue.trim() || isGenerating}
                        className="absolute right-2 bottom-2 h-9 w-9 rounded-xl transition-all hover:scale-105 active:scale-95 bg-primary hover:bg-primary/90 mb-0.5"
                    >
                        {isGenerating ? (
                            <Loader className="h-4 w-4 animate-spin" />
                        ) : (
                            <Send className="h-4 w-4" />
                        )}
                    </Button>
                </div>
                <p className="text-[10px] text-center text-muted-foreground mt-3 font-medium tracking-wide opacity-70">
                    AI can make mistakes. Check important info.
                </p>
            </div>
        </div>
    );
}
