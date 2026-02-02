import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { ChatItem, Item } from "@/stores/ChatStore";
import { toast } from "sonner";
import { v4 as uuidv4 } from "uuid";

// --- Types ---
interface ServerItem {
    id: string;
    data: any;
    timestamp: string;
}

interface ServerChat {
    id: string;
    title: string;
    items: ServerItem[];
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
        items: chat.items.map((item) => {
            // Best effort content normalization
            let content = "";
            const rawContent = item.data?.content;

            if (typeof rawContent === "string") {
                content = rawContent;
            } else if (Array.isArray(rawContent)) {
                // Handle new structure: [{type: 'input_text', text: '...'}, {type: 'output_text', text: '...'}]
                content = rawContent
                    .map(c => c.text || c.content || "")
                    .join("");
            }

            return {
                id: item.id,
                data: {
                    ...item.data,
                    content: content,
                    role: item.data?.role || "assistant"
                },
                timestamp: new Date(item.timestamp),
            };
        }),
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
        items: [],
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
            const userItem: Item = {
                id: uuidv4(),
                data: {
                    role: "user",
                    content,
                },
                timestamp: new Date(),
            };

            const assistantItemId = uuidv4();
            const assistantItem: Item = {
                id: assistantItemId,
                data: {
                    role: "assistant",
                    content: "",
                },
                timestamp: new Date(),
            };

            // 1. Optimistic Update: Add User Message & Empty Assistant Message
            queryClient.setQueryData(["chats"], (old: ChatItem[] = []) => {
                return old.map((chat) => {
                    if (chat.id === chatId) {
                        return {
                            ...chat,
                            items: [...chat.items, userItem, assistantItem],
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
                            const rawData = dataLine[1].trim();

                            try {
                                const jsonData = JSON.parse(rawData);

                                // 1. Handle Text Deltas
                                if (eventType === "response.output_text.delta") {
                                    // The server sends us a constructed message object in 'data' for this event
                                    // conforming to: { type: "message", role: "assistant", content: [{ type: "output_text", text: "..." }] }
                                    const deltaText = jsonData.content?.[0]?.text || "";

                                    if (deltaText) {
                                        assistantContent += deltaText;

                                        // Incremental Content Update
                                        queryClient.setQueryData(["chats"], (old: ChatItem[] = []) => {
                                            return old.map((chat) => {
                                                if (chat.id === chatId) {
                                                    return {
                                                        ...chat,
                                                        items: chat.items.map((item) =>
                                                            item.id === assistantItemId
                                                                ? { ...item, data: { ...item.data, content: assistantContent } }
                                                                : item
                                                        ),
                                                    };
                                                }
                                                return chat;
                                            });
                                        });
                                    }
                                }

                                // 2. Handle Item Done (Server confirms item persistence and gives real ID)
                                else if (eventType === "response.output_item.done") {
                                    const doneItem = jsonData.item;
                                    if (doneItem && doneItem.type === "message" && doneItem.id) {
                                        // Replace optimistic ID with real server ID
                                        queryClient.setQueryData(["chats"], (old: ChatItem[] = []) => {
                                            return old.map((chat) => {
                                                if (chat.id === chatId) {
                                                    return {
                                                        ...chat,
                                                        items: chat.items.map((item) =>
                                                            item.id === assistantItemId
                                                                ? { ...item, id: doneItem.id } // Update ID
                                                                : item
                                                        ),
                                                    };
                                                }
                                                return chat;
                                            });
                                        });
                                    }
                                }

                            } catch (e) {
                                console.warn("Failed to parse SSE data JSON:", e, rawData);
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
                                items: chat.items.map((item) =>
                                    item.id === assistantItemId
                                        ? { ...item, data: { ...item.data, content: `🚨 ${error.message || "Error"}` } }
                                        : item
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
