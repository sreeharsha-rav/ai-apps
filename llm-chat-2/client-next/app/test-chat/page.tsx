"use client";

import React from "react";
import sampleData from "../../sample.json";
import { ChatMessage } from "@/components/ChatMessage";
import { MessageSquare } from "lucide-react";

export default function TestChatPage() {
    const { messages, title, total_tokens } = sampleData;

    return (
        <div className="flex flex-col h-screen w-full bg-background overflow-hidden">
            <header className="flex-none flex items-center justify-between px-6 py-3 border-b border-border/50 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 z-20">
                <div className="flex items-center gap-3 min-w-0">
                    <div className="bg-primary/10 p-2 rounded-lg">
                        <MessageSquare className="h-4 w-4 text-primary" />
                    </div>
                    <div className="flex flex-col min-w-0">
                        <h1 className="text-sm font-semibold truncate">
                            {title} (Preview)
                        </h1>
                        <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-medium">
                            {messages.length} Messages • {total_tokens || 0} Tokens
                        </p>
                    </div>
                </div>
            </header>

            <div className="flex-1 overflow-y-auto">
                <div className="max-w-3xl mx-auto py-6 px-4 space-y-4">
                    {(messages as any[]).map((message: any) => (
                        <ChatMessage
                            key={message.id}
                            message={{
                                ...message,
                                timestamp: new Date(message.timestamp)
                            }}
                        />
                    ))}
                </div>

                {/* Loader Preview */}
                <div className="max-w-3xl mx-auto pb-10 px-4">
                    <ChatMessage
                        message={{
                            id: "loading",
                            role: "assistant",
                            content: "",
                            timestamp: new Date()
                        } as any}
                        isLoader={true}
                    />
                </div>
            </div>

            <div className="flex-none p-4 bg-background border-t border-border/50">
                <div className="max-w-3xl mx-auto text-center py-2">
                    <p className="text-xs text-muted-foreground">This is a test view for Markdown enhancements.</p>
                </div>
            </div>
        </div>
    );
}
