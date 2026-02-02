import React from "react";
import { Button } from "@/components/ui/button";
import { X } from "lucide-react";
import { cn } from "@/lib/utils";

interface CanvasProps {
    isOpen: boolean;
    onClose: () => void;
    content: string | null;
}

export function Canvas({ isOpen, onClose, content }: CanvasProps) {
    if (!isOpen) return null;

    return (
        <div className={cn(
            "flex flex-col h-full border-l border-border/50 bg-background transition-all duration-300 ease-in-out",
            isOpen ? "w-1/2 min-w-[400px]" : "w-0 overflow-hidden opacity-0"
        )}>
            <div className="flex items-center justify-between px-4 py-3 border-b border-border/50">
                <h2 className="text-sm font-semibold">Canvas</h2>
                <Button variant="ghost" size="icon" className="h-8 w-8" onClick={onClose}>
                    <X className="h-4 w-4" />
                </Button>
            </div>
            <div className="flex-1 p-4 overflow-y-auto">
                {content ? (
                    <div className="prose dark:prose-invert max-w-none">
                        {content}
                    </div>
                ) : (
                    <div className="flex items-center justify-center h-full text-muted-foreground text-sm">
                        Canvas is empty
                    </div>
                )}
            </div>
        </div>
    );
}
