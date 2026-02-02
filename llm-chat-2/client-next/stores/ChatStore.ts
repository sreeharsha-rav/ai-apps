import { create } from "zustand";

export interface Item {
  id: string;
  data: any;
  timestamp: Date;
}

export interface ChatItem {
  id: string;
  title: string;
  items: Item[];
  canvas: { content: string; language: string } | null;
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
  activeCopiedId: string | null;
  setActiveCopiedId: (id: string | null) => void;
}

export const useChatStore = create<ChatStore>((set, get) => ({
  chats: [],
  isLoading: false,
  activeCopiedId: null,

  setActiveCopiedId: (id: string | null) => set({ activeCopiedId: id }),

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
