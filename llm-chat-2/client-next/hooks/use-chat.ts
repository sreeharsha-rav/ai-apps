import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { ChatItem, Message } from "@/stores/ChatStore";
import { toast } from "sonner";
import { v4 as uuidv4 } from "uuid";

// --- Types ---
interface ServerMessage {
    id: string;
    role: "user" | "assistant";
    content: string;
    timestamp: string;
    total_tokens?: number;
}

interface ServerChat {
    id: string;
    title: string;
    messages: ServerMessage[];
    total_tokens: number;
    created_at: string;
    updated_at: string;
}

// --- API Functions ---

const fetchChats = async (): Promise<ChatItem[]> => {
    const response = await fetch("http://localhost:8000/api/chat/history");
    if (!response.ok) throw new Error("Could not fetch history");
    const data: ServerChat[] = await response.json();
    return data.map((chat) => ({
        id: chat.id,
        title: chat.title,
        messages: chat.messages.map((m) => ({
            id: m.id,
            role: m.role,
            content: m.content,
            timestamp: new Date(m.timestamp),
            total_tokens: m.total_tokens
        })),
        total_tokens: chat.total_tokens || 0,
        createdAt: new Date(chat.created_at || chat.updated_at),
        updatedAt: new Date(chat.updated_at)
    }));
};

const createChat = async (): Promise<ChatItem> => {
    const response = await fetch("http://localhost:8000/api/chat/history", { method: "POST" });
    if (!response.ok) throw new Error("Failed to create chat");
    const data: ServerChat = await response.json();
    return {
        id: data.id,
        title: data.title,
        messages: [],
        total_tokens: 0,
        createdAt: new Date(data.created_at),
        updatedAt: new Date(data.updated_at),
    };
};

const deleteChat = async (id: string) => {
    const response = await fetch(`http://localhost:8000/api/chat/history/${id}`, { method: "DELETE" });
    if (!response.ok) throw new Error("Failed to delete chat");
    return id;
};

// --- Hooks ---

export const useGetChats = () => {
    return useQuery({
        queryKey: ["chats"],
        queryFn: fetchChats,
    });
};

export const useGetChat = (id: string) => {
    const { data: chats } = useGetChats();
    return chats?.find((c) => c.id === id);
};

export const useCreateChat = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: createChat,
        onSuccess: (newChat) => {
            queryClient.setQueryData(["chats"], (old: ChatItem[] = []) => [newChat, ...old]);
        },
        onError: () => toast.error("Failed to create chat"),
    });
};

export const useDeleteChat = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: deleteChat,
        onSuccess: (deletedId) => {
            queryClient.setQueryData(["chats"], (old: ChatItem[] = []) =>
                old.filter((chat) => chat.id !== deletedId)
            );
            toast.success("Chat deleted");
        },
        onError: () => toast.error("Failed to delete chat"),
    });
};

export const useSendMessage = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async ({ chatId, content }: { chatId: string, content: string }) => {
            const userMessage: Message = {
                id: uuidv4(),
                role: "user",
                content,
                timestamp: new Date(),
            };

            const assistantMessageId = uuidv4();
            const assistantMessage: Message = {
                id: assistantMessageId,
                role: "assistant",
                content: "",
                timestamp: new Date(),
            };

            // 1. Optimistic Update: Add User Message & Empty Assistant Message
            queryClient.setQueryData(["chats"], (old: ChatItem[] = []) => {
                return old.map((chat) => {
                    if (chat.id === chatId) {
                        return {
                            ...chat,
                            messages: [...chat.messages, userMessage, assistantMessage],
                            updatedAt: new Date(),
                        };
                    }
                    return chat;
                });
            });

            try {
                const response = await fetch("http://localhost:8000/api/chat/stream", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        prompt: content,
                        chat_id: chatId,
                        model: "gpt-5-mini"
                    }),
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({ detail: "Unknown server error" }));
                    throw new Error(errorData.detail || "Failed to connect to AI server");
                }

                const reader = response.body?.getReader();
                if (!reader) throw new Error("No reader available");

                let assistantContent = "";
                let buffer = "";

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    buffer += new TextDecoder().decode(value);
                    const lines = buffer.split("\n\n");
                    buffer = lines.pop() || ""; // Keep incomplete chunk in buffer

                    for (const line of lines) {
                        const eventLine = line.match(/event: (.*)\n/);
                        const dataLine = line.match(/data: (.*)/); // Modified to not match end of line explicitly for more robust parsing

                        if (eventLine && dataLine) {
                            const eventType = eventLine[1].trim();
                            const data = dataLine[1].trim(); // trim() handles potential trailing \n if regex missed it

                            if (eventType === "response.output_text.delta") {
                                assistantContent += data;

                                // Incremental Update
                                queryClient.setQueryData(["chats"], (old: ChatItem[] = []) => {
                                    return old.map((chat) => {
                                        if (chat.id === chatId) {
                                            return {
                                                ...chat,
                                                messages: chat.messages.map((m) =>
                                                    m.id === assistantMessageId
                                                        ? { ...m, content: assistantContent }
                                                        : m
                                                ),
                                            };
                                        }
                                        return chat;
                                    });
                                });
                            } else if (eventType === "error") {
                                toast.error("Stream Error");
                                assistantContent += `\n\n${data}`; // Append error to chat bubble
                                queryClient.setQueryData(["chats"], (old: ChatItem[] = []) => {
                                    return old.map((chat) => {
                                        if (chat.id === chatId) {
                                            return {
                                                ...chat,
                                                messages: chat.messages.map((m) =>
                                                    m.id === assistantMessageId
                                                        ? { ...m, content: assistantContent }
                                                        : m
                                                ),
                                            };
                                        }
                                        return chat;
                                    });
                                });
                            }
                        }
                    }
                }

                // Refetch to invalidate and get fresh tokens/metadata if needed
                queryClient.invalidateQueries({ queryKey: ["chats"] });

            } catch (error: any) {
                console.error("Streaming error:", error);

                // Update assistant message with error
                queryClient.setQueryData(["chats"], (old: ChatItem[] = []) => {
                    return old.map((chat) => {
                        if (chat.id === chatId) {
                            return {
                                ...chat,
                                messages: chat.messages.map((m) =>
                                    m.id === assistantMessageId
                                        ? { ...m, content: `🚨 ${error.message || "Error"}` }
                                        : m
                                ),
                            };
                        }
                        return chat;
                    });
                });
                throw error;
            }
        },
        onError: (error: Error) => {
            toast.error(error.message || "Failed to send message");
        }
    });
};
