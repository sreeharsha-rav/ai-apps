"use client";

import * as React from "react";
import TextareaAutosize, {
    TextareaAutosizeProps,
} from "react-textarea-autosize";
import { cn } from "@/lib/utils";

export const AutosizeTextarea = React.forwardRef<
    HTMLTextAreaElement,
    TextareaAutosizeProps
>(({ className, ...props }, ref) => {
    return (
        <TextareaAutosize
            className={cn(
                "flex w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 resize-none",
                className
            )}
            ref={ref}
            {...props}
        />
    );
});

AutosizeTextarea.displayName = "AutosizeTextarea";
