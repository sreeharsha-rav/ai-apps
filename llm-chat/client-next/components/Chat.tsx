import { Plus } from "lucide-react";
import { useChatStore } from "@/stores/ChatStore";
import { Button } from "@/components/ui/button";

export const NewChatButton = () => {
  const chatStore = useChatStore();

  const handleNewChat = (title: string) => {
    chatStore.addChat(title);
    // TODO: Navigate to the new chat
  };

  return (
    <Button
      variant="default"
      size="sm"
      className="w-full gap-2 justify-center bg-primary text-primary-foreground hover:bg-primary/90"
      onClick={() => handleNewChat("New Chat")}
    >
      <Plus size={14} strokeWidth={2} />
      <span>New Chat</span>
    </Button>
  );
};

export const ChatList = () => {
  const chats = useChatStore((state) => state.chats);

  return (
    <div>
      {chats.map((chat) => (
        <div key={chat.id}>{chat.title}</div>
      ))}
    </div>
  );
};
