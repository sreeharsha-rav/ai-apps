"use client";

import React, { useState } from "react";
import { useSendMessage, useGetChats } from "@/hooks/use-chat";
import { ChatItem } from "@/stores/ChatStore";
import { useCanvasStore } from "@/stores/CanvasStore";
import { Button } from "@/components/ui/button";
import { Bot } from "lucide-react";
import { useRouter } from "next/navigation";
import { ChatSkeleton } from "./ChatSkeleton";
import { ChatHeader } from "./ChatHeader";
import { MessageList } from "./MessageList";
import { MessageComposer } from "./MessageComposer";
import { Canvas } from "./Canvas";

interface ChatContainerProps {
    chatId: string;
}

export function ChatContainer({ chatId }: ChatContainerProps) {
    const { data: chats, isLoading } = useGetChats();
    const sendMessageMutation = useSendMessage();
    const [inputValue, setInputValue] = useState("");
    const router = useRouter();

    // Canvas UI State
    const { isOpen: isCanvasOpen, toggle: toggleCanvas, setIsOpen: setCanvasOpen } = useCanvasStore();

    const chat = chats?.find((c: ChatItem) => c.id === chatId);
    const items = chat?.items || [];
    const isGenerating = sendMessageMutation.isPending;

    // Get Canvas content from chat object
    const canvasContent = chat?.canvas?.content || null;

    const handleSend = async () => {
        if (!inputValue.trim() || sendMessageMutation.isPending) return;

        const content = inputValue;
        setInputValue("");

        try {
            await sendMessageMutation.mutateAsync({ chatId, content });
        } catch (error) {
            console.error("Failed to send message:", error);
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
        <div className="flex flex-row h-[calc(100svh-4rem)] md:h-[calc(100svh-4.5rem)] w-full bg-background overflow-hidden relative">
            {/* Main Chat Area */}
            <div className="flex flex-col flex-1 min-w-0 h-full transition-all duration-300">

                <ChatHeader
                    title={chat.title}
                    messageCount={items.length}
                    tokenCount={chat.total_tokens}
                    isCanvasOpen={isCanvasOpen}
                    onToggleCanvas={toggleCanvas}
                />

                <MessageList
                    items={items}
                    isGenerating={isGenerating}
                />

                <MessageComposer
                    inputValue={inputValue}
                    setInputValue={setInputValue}
                    onSend={handleSend}
                    isGenerating={isGenerating}
                />
            </div>

            {/* Canvas Sidebar */}
            <Canvas
                isOpen={isCanvasOpen}
                onClose={() => setCanvasOpen(false)}
                content={canvasContent}
            />
        </div>
    );
}
