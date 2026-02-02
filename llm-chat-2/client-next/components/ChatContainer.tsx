"use client";

import React, { useRef, useEffect, useState } from "react";
import { useVirtualizer } from "@tanstack/react-virtual";
import { useSendMessage, useGetChats } from "@/hooks/use-chat";
import { Message, ChatItem } from "@/stores/ChatStore";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, User, Bot, Loader, MessageSquare } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";
import { cn } from "@/lib/utils";
import { format } from "date-fns";
import { useRouter } from "next/navigation";
import { ChatSkeleton } from "./ChatSkeleton";
import { ChatMessage } from "./ChatMessage";
import { AutosizeTextarea } from "@/components/ui/autosize-textarea";

interface ChatContainerProps {
    chatId: string;
}

export function ChatContainer({ chatId }: ChatContainerProps) {
    const { data: chats, isLoading } = useGetChats();
    const sendMessageMutation = useSendMessage();
    const [inputValue, setInputValue] = useState("");
    const parentRef = useRef<HTMLDivElement>(null);
    const router = useRouter();

    const chat = chats?.find((c: ChatItem) => c.id === chatId);
    const messages = chat?.messages || [];
    const isGenerating = sendMessageMutation.isPending;

    const rowVirtualizer = useVirtualizer({
        count: messages.length,
        getScrollElement: () => parentRef.current,
        estimateSize: () => 80,
        overscan: 5,
    });

    // Auto-scroll to bottom on new messages
    useEffect(() => {
        if (messages.length > 0) {
            rowVirtualizer.scrollToIndex(messages.length - 1, { align: 'end', behavior: 'smooth' });
        }
    }, [messages.length, rowVirtualizer]);

    const handleSend = async (e?: React.FormEvent) => {
        if (e) e.preventDefault();
        if (!inputValue.trim() || sendMessageMutation.isPending) return;

        const content = inputValue;
        setInputValue("");

        try {
            await sendMessageMutation.mutateAsync({ chatId, content });
        } catch (error) {
            console.error("Failed to send message:", error);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    if (isLoading) {
        return <ChatSkeleton />;
    }

    if (!chat) {
        return (
            <div className="flex flex-col items-center justify-center h-full gap-4">
                <div className="bg-muted p-4 rounded-full">
                    <Bot className="h-8 w-8 text-muted-foreground" />
                </div>
                <h2 className="text-xl font-semibold">Chat not found</h2>
                <p className="text-muted-foreground">The chat you are looking for does not exist or has been deleted.</p>
                <Button variant="outline" onClick={() => router.push("/")}>
                    Go Home
                </Button>
            </div>
        );
    }

    return (
        <div className="flex flex-col h-[calc(100svh-4rem)] md:h-[calc(100svh-4.5rem)] w-full bg-background">
            {/* Thread Title Bar */}
            <header className="flex-none flex items-center justify-between px-6 py-3 border-b border-border/50 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 z-20">
                <div className="flex items-center gap-3 min-w-0">
                    <div className="bg-primary/10 p-2 rounded-lg">
                        <MessageSquare className="h-4 w-4 text-primary" />
                    </div>
                    <div className="flex flex-col min-w-0">
                        <h1 className="text-sm font-semibold truncate">
                            {chat.title || "Untitled Chat"}
                        </h1>
                        <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-medium">
                            {messages.length} Messages • {chat.total_tokens || 0} Tokens
                        </p>
                    </div>
                </div>
            </header>

            {/* Messages Area */}
            <div
                ref={parentRef}
                className="flex-1 min-h-0 overflow-y-auto scroll-smooth"
            >
                <div
                    style={{
                        height: `${rowVirtualizer.getTotalSize()}px`,
                        width: '100%',
                        position: 'relative',
                    }}
                    className="max-w-3xl mx-auto py-6 px-4"
                >
                    {rowVirtualizer.getVirtualItems().map((virtualItem) => {
                        const message = messages[virtualItem.index];
                        const isLast = virtualItem.index === messages.length - 1;
                        const showLoader = isLast && isGenerating && message.role === "assistant" && !message.content;

                        return (
                            <div
                                key={virtualItem.key}
                                data-index={virtualItem.index}
                                ref={rowVirtualizer.measureElement}
                                style={{
                                    position: 'absolute',
                                    top: 0,
                                    left: 0,
                                    width: '100%',
                                    transform: `translateY(${virtualItem.start}px)`,
                                }}
                            >
                                <ChatMessage
                                    message={showLoader ? { ...message, content: "" } : message}
                                    isLoader={showLoader}
                                />
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Standard Input Area */}
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
                            disabled={sendMessageMutation.isPending}
                        />
                        <Button
                            onClick={() => handleSend()}
                            size="icon"
                            disabled={!inputValue.trim() || sendMessageMutation.isPending}
                            className="absolute right-2 bottom-2 h-9 w-9 rounded-xl transition-all hover:scale-105 active:scale-95 bg-primary hover:bg-primary/90 mb-0.5"
                        >
                            {sendMessageMutation.isPending ? (
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
        </div>
    );
}

