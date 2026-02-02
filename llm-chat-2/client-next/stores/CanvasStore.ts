import { create } from "zustand";

interface CanvasStore {
    isOpen: boolean;
    setIsOpen: (isOpen: boolean) => void;
    toggle: () => void;
    // Content can be added here later, or we can just track the active message ID
    activeContent: string | null;
    setActiveContent: (content: string | null) => void;
}

export const useCanvasStore = create<CanvasStore>((set) => ({
    isOpen: false,
    setIsOpen: (isOpen: boolean) => set({ isOpen }),
    toggle: () => set((state) => ({ isOpen: !state.isOpen })),
    activeContent: null,
    setActiveContent: (content: string | null) => set({ activeContent: content }),
}));
