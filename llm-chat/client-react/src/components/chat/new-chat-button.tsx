import { Plus } from "lucide-react";
import { useNavigate } from "react-router";
import { useChatStore } from "@/stores/chat-store";
import { Button } from "@/components/ui/button";

export function NewChatButton() {
  const navigate = useNavigate();
  const addChat = useChatStore((state) => state.addChat);

  const handleNewChat = () => {
    const newChat = addChat("New Chat");
    navigate(newChat.url);
  };

  return (
    <Button
      variant="default"
      size="sm"
      className="w-full gap-2 justify-center bg-primary text-primary-foreground hover:bg-primary/90"
      onClick={handleNewChat}
    >
      <Plus size={14} strokeWidth={2} />
      <span>New Chat</span>
    </Button>
  );
}
