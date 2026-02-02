"use client"

import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { useCreateChat, useGetChats } from "@/hooks/use-chat";

export const NewChatButton = () => {
  const mutation = useCreateChat();
  const router = useRouter();

  const handleNewChat = () => {
    mutation.mutate(undefined, {
      onSuccess: (newChat) => {
        router.push(`/c/${newChat.id}`);
      }
    });
  };

  return (
    <Button
      variant="default"
      size="sm"
      className="w-full gap-2 justify-center bg-primary text-primary-foreground hover:bg-primary/90"
      onClick={() => handleNewChat()}
    >
      <Plus size={14} strokeWidth={2} />
      <span>New Chat</span>
    </Button>
  );
};


export const ChatList = () => {
  const { data: chats } = useGetChats();

  if (!chats) return null;

  return (
    <div>
      {chats.map((chat) => (
        <div key={chat.id}>{chat.title}</div>
      ))}
    </div>
  );
};
