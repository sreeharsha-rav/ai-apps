import { MessageSquare, PanelRightClose, PanelRightOpen } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface ChatHeaderProps {
    title: string;
    messageCount: number;
    tokenCount: number;
    isCanvasOpen: boolean;
    onToggleCanvas: () => void;
}

export function ChatHeader({
    title,
    messageCount,
    tokenCount,
    isCanvasOpen,
    onToggleCanvas
}: ChatHeaderProps) {
    return (
        <header className="flex-none flex items-center justify-between px-6 py-3 border-b border-border/50 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 z-20">
            <div className="flex items-center gap-3 min-w-0">
                <div className="bg-primary/10 p-2 rounded-lg">
                    <MessageSquare className="h-4 w-4 text-primary" />
                </div>
                <div className="flex flex-col min-w-0">
                    <h1 className="text-sm font-semibold truncate">
                        {title || "Untitled Chat"}
                    </h1>
                    <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-medium">
                        {messageCount} Messages • {tokenCount || 0} Tokens
                    </p>
                </div>
            </div>

            <div className="flex items-center">
                <Button
                    variant="ghost"
                    size="icon"
                    onClick={onToggleCanvas}
                    className={cn("h-8 w-8", isCanvasOpen && "bg-muted text-foreground")}
                    title={isCanvasOpen ? "Close Canvas" : "Open Canvas"}
                >
                    {isCanvasOpen ? <PanelRightClose className="h-4 w-4" /> : <PanelRightOpen className="h-4 w-4" />}
                </Button>
            </div>
        </header>
    );
}
