import { memo } from "react";
import { useLocation } from "react-router";
import { useChatStore } from "@/stores/chat-store";
import { NavMain } from "@/components/sidebar/nav-main";

interface ChatListProps {
  chats: Array<{ title: string; url: string }>;
  currentPath: string;
}

export const ChatList = memo(function ChatList({
  chats,
  currentPath,
}: ChatListProps) {
  const navItems = [
    {
      title: "Chat",
      url: "/",
      items: chats.map((chat) => ({
        title: chat.title,
        url: chat.url,
        isActive: currentPath === chat.url,
      })),
    },
  ];

  return <NavMain items={navItems} />;
});

export function ChatListContainer() {
  const location = useLocation();
  const chats = useChatStore((state) => state.chats);

  return <ChatList chats={chats} currentPath={location.pathname} />;
}
