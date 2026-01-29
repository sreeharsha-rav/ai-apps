import { create } from "zustand";
import { v4 as uuidv4 } from "uuid";
import { toast } from "sonner";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  total_tokens?: number;
}

export interface ChatItem {
  id: string;
  title: string;
  messages: Message[];
  total_tokens: number;
  createdAt: Date;
  updatedAt: Date;
}

interface ChatStore {
  chats: ChatItem[];
  setChats: (chats: ChatItem[]) => void;
  updateChat: (id: string, title: string) => void;
  getChatById: (id: string) => ChatItem | undefined;
  isLoading: boolean;
}

export const useChatStore = create<ChatStore>((set, get) => ({
  chats: [],
  isLoading: false,

  setChats: (chats: ChatItem[]) => set({ chats }),

  // NOTE: Server state is now managed by TanStack Query.
  // These are kept here only if client-side imperative updates are absolutely necessary
  // or for specific UI state legacy support.
  updateChat: (id: string, title: string) => {
    set((state) => ({
      chats: state.chats.map((chat) =>
        chat.id === id ? { ...chat, title, updatedAt: new Date() } : chat
      ),
    }));
  },

  getChatById: (id: string) => {
    return get().chats.find((chat) => chat.id === id);
  },
}));
