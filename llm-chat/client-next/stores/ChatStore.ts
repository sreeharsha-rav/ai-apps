import { create } from "zustand";
import { v4 as uuidv4 } from "uuid";

export interface ChatItem {
  id: string;
  title: string;
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
  chats: [],

  addChat: (title: string) => {
    const newChat = {
      id: "chat_" + uuidv4(),
      title,
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    set((state) => ({
      chats: [newChat, ...state.chats],
    }));
    return newChat;
  },

  updateChat: (id: string, title: string) => {
    set((state) => ({
      chats: state.chats.map((Chat) =>
        Chat.id === id ? { ...Chat, title, updatedAt: new Date() } : Chat
      ),
    }));
  },

  deleteChat: (id: string) => {
    set((state) => ({
      chats: state.chats.filter((Chat) => Chat.id !== id),
    }));
  },

  getChatById: (id: string) => {
    return get().chats.find((Chat) => Chat.id === id);
  },
}));
