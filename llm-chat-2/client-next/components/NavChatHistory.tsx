"use client"

import {
    Folder,
    Forward,
    MoreHorizontal,
    Trash2,
    MessageSquare,
} from "lucide-react"

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
    SidebarGroup,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuAction,
    SidebarMenuButton,
    SidebarMenuItem,
    useSidebar,
} from "@/components/ui/sidebar"
import { Skeleton } from "@/components/ui/skeleton"
import Link from "next/link"
import { useRouter, useParams } from "next/navigation"
import { useGetChats, useDeleteChat } from "@/hooks/use-chat"
import { useMemo } from "react"

export function NavChatHistory() {
    const { isMobile } = useSidebar()
    // We'll hydrate the store or assume it's available. 
    // Using getRecentChats needs to be reactive.
    // Ideally, we just select all chats and slice them, or the store has a specific selector.
    // The logic 'getRecentChats' is a function, not a state selector, so we might need to wrap it or select 'chats' and sort manually.

    const { data: chats, isLoading } = useGetChats();
    const deleteChatMutation = useDeleteChat();

    // Derived state from query data
    const recentChats = useMemo(() => {
        if (!chats) return [];
        return [...chats]
            .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
            .slice(0, 5);
    }, [chats]);

    const router = useRouter();
    const params = useParams();
    const activeChatId = params?.chatId as string;

    const handleDelete = (id: string) => {
        deleteChatMutation.mutate(id, {
            onSuccess: () => {
                // Only redirect if the deleted chat is the one we are currently viewing
                if (activeChatId === id) {
                    router.push("/");
                }
            }
        });
    };

    return (
        <SidebarGroup className="group-data-[collapsible=icon]:hidden">
            <SidebarGroupLabel>Recent Chats</SidebarGroupLabel>
            <SidebarMenu>
                {isLoading ? (
                    Array.from({ length: 5 }).map((_, i) => (
                        <SidebarMenuItem key={i} className="px-2 py-1">
                            <div className="flex items-center gap-2 w-full">
                                <Skeleton className="h-4 w-4 rounded-sm" />
                                <Skeleton className="h-4 flex-1 rounded-sm" />
                            </div>
                        </SidebarMenuItem>
                    ))
                ) : (
                    recentChats.map((item) => (
                        <SidebarMenuItem key={item.id}>
                            <SidebarMenuButton asChild>
                                <Link href={`/c/${item.id}`}>
                                    <MessageSquare className="text-muted-foreground" />
                                    <span>{item.title}</span>
                                </Link>
                            </SidebarMenuButton>
                            <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                    <SidebarMenuAction showOnHover>
                                        <MoreHorizontal />
                                        <span className="sr-only">More</span>
                                    </SidebarMenuAction>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent
                                    className="w-48 rounded-lg"
                                    side={isMobile ? "bottom" : "right"}
                                    align={isMobile ? "end" : "start"}
                                >
                                    <DropdownMenuItem onClick={() => { /* View Logic */ }}>
                                        <Folder className="text-muted-foreground" />
                                        <span>View Chat</span>
                                    </DropdownMenuItem>
                                    <DropdownMenuItem>
                                        <Forward className="text-muted-foreground" />
                                        <span>Share Chat</span>
                                    </DropdownMenuItem>
                                    <DropdownMenuSeparator />
                                    <DropdownMenuItem onClick={() => handleDelete(item.id)}>
                                        <Trash2 className="text-muted-foreground" />
                                        <span>Delete Chat</span>
                                    </DropdownMenuItem>
                                </DropdownMenuContent>
                            </DropdownMenu>
                        </SidebarMenuItem>
                    )))}
                <SidebarMenuItem>
                    <SidebarMenuButton asChild className="text-sidebar-foreground/70">
                        <Link href="/history">
                            <MoreHorizontal className="text-sidebar-foreground/70" />
                            <span>View All History</span>
                        </Link>
                    </SidebarMenuButton>
                </SidebarMenuItem>
            </SidebarMenu>
        </SidebarGroup>
    )
}
