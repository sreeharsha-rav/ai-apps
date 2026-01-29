"use client";

import { useState } from "react";
import { Sparkles, Send } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useCreateChat, useSendMessage } from "@/hooks/use-chat";
import { useRouter } from "next/navigation";
import { cn } from "@/lib/utils";

export default function Home() {
  const [inputValue, setInputValue] = useState("");
  const createChatMutation = useCreateChat();
  const sendMessageMutation = useSendMessage();
  const router = useRouter();

  const handleStartChat = async () => {
    if (!inputValue.trim()) return;

    try {
      // 1. Create the chat first
      const newChat = await createChatMutation.mutateAsync();

      // 2. Send the initial message (fire and forget, optimistic updates handle the UI)
      sendMessageMutation.mutate({ chatId: newChat.id, content: inputValue });

      // 3. Redirect to the new chat
      router.push(`/c/${newChat.id}`);
    } catch (error) {
      console.error("Failed to start chat:", error);
      // Error handling is managed by the mutation hooks (toasts)
    }
  };

  return (
    <main className="flex flex-col items-center justify-center h-full px-4">
      <div className="max-w-2xl w-full flex flex-col items-center space-y-8">
        <div className="flex flex-col items-center space-y-4 text-center">
          <div className="p-4 rounded-3xl bg-primary/10 transition-transform hover:scale-110 duration-500">
            <Sparkles className="size-12 text-primary" />
          </div>
          <h1 className="text-4xl font-bold tracking-tight">How can I help you today?</h1>
          <p className="text-muted-foreground text-lg">
            Start a new conversation to get personalized assistance.
          </p>
        </div>

        <div className="w-full relative group">
          <div className="absolute -inset-1 bg-gradient-to-r from-primary/30 to-primary/10 rounded-2xl blur opacity-30 group-focus-within:opacity-100 transition duration-1000"></div>
          <div className="relative flex items-center bg-card border rounded-2xl p-2 shadow-2xl focus-within:ring-2 ring-primary/20 transition-all">
            <Input
              placeholder="Message AI Assistant..."
              className="border-none focus-visible:ring-0 focus-visible:ring-offset-0 bg-transparent text-lg py-7 px-4 h-auto"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleStartChat();
              }}
              disabled={createChatMutation.isPending}
            />
            <Button
              size="icon"
              className={cn(
                "rounded-xl transition-all",
                inputValue.trim() ? "bg-primary scale-100 shadow-lg" : "bg-muted text-muted-foreground scale-90"
              )}
              disabled={!inputValue.trim() || createChatMutation.isPending}
              onClick={handleStartChat}
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* <div className="grid grid-cols-2 md:grid-cols-4 gap-3 w-full max-w-lg">
          {["Order Status", "Return Policy", "Product Search", "Support"].map((label) => (
            <Button
              key={label}
              variant="outline"
              className="rounded-xl py-6 h-auto text-xs hover:bg-primary/5 hover:border-primary/50 transition-colors"
              onClick={() => {
                setInputValue(`Tell me about ${label.toLowerCase()}`);
              }}
            >
              // TODO: handle setInputValue and state change to actual view and mutate sync
              {label}
            </Button>
          ))}
        </div> */}
      </div>
    </main>
  );
}

