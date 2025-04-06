import { create } from "zustand";
import { nanoid } from "nanoid";

export interface ChatItem {
  id: string;
  title: string;
  url: string;
  createdAt: Date;
  updatedAt: Date;
}

interface ChatStore {
  chats: ChatItem[];
  addChat: (title: string) => ChatItem;
  updateChat: (id: string, title: string) => void;
  deleteChat: (id: string) => void;
  getChatById: (id: string) => ChatItem | undefined;
}

export const useChatStore = create<ChatStore>((set, get) => ({
  chats: [
    {
      id: "1",
      title: "New Chat",
      url: "/chat/new",
      createdAt: new Date(),
      updatedAt: new Date(),
    },
    {
      id: "2",
      title: "Previous Chat 1",
      url: "/chat/2",
      createdAt: new Date(),
      updatedAt: new Date(),
    },
    {
      id: "3",
      title: "Previous Chat 2",
      url: "/chat/3",
      createdAt: new Date(),
      updatedAt: new Date(),
    },
  ],

  addChat: (title: string) => {
    const newChat = {
      id: nanoid(),
      title,
      url: `/chat/${nanoid()}`,
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    set((state) => ({
      chats: [newChat, ...state.chats],
    }));
    return newChat;
  },

  updateChat: (id: string, title: string) =>
    set((state) => ({
      chats: state.chats.map((chat) =>
        chat.id === id ? { ...chat, title, updatedAt: new Date() } : chat
      ),
    })),

  deleteChat: (id: string) =>
    set((state) => ({
      chats: state.chats.filter((chat) => chat.id !== id),
    })),

  getChatById: (id: string) => get().chats.find((chat) => chat.id === id),
}));
