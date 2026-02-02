"use client";

import { useState } from "react";
import Link from "next/link";
import { MoreHorizontal, Trash2, Search } from "lucide-react";

import { useGetChats, useDeleteChat } from "@/hooks/use-chat";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export default function HistoryPage() {
    const { data: chats, isLoading } = useGetChats();
    const deleteChatMutation = useDeleteChat();
    const [searchQuery, setSearchQuery] = useState("");

    // Sort chats by date descending
    const sortedChats = chats
        ? [...chats].sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
        : [];

    // Filter based on search query
    const filteredChats = sortedChats.filter((chat) =>
        chat.title.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="flex flex-col h-full p-6 gap-6">
            <div className="flex flex-col gap-2">
                <h1 className="text-2xl font-bold tracking-tight">Chat History</h1>
                <p className="text-muted-foreground">
                    View and manage your past conversations.
                </p>
            </div>

            <div className="relative">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                    type="search"
                    placeholder="Search history..."
                    className="pl-8 w-full md:w-[300px]"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
            </div>

            {isLoading ? (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {Array.from({ length: 9 }).map((_, i) => (
                        <Card key={i} className="h-[100px]">
                            <CardHeader>
                                <Skeleton className="h-5 w-3/4 mb-2" />
                                <Skeleton className="h-4 w-1/4" />
                            </CardHeader>
                        </Card>
                    ))}
                </div>
            ) : filteredChats.length === 0 ? (
                <div className="flex flex-1 items-center justify-center text-muted-foreground">
                    <p>No chats found.</p>
                </div>
            ) : (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {filteredChats.map((chat) => (
                        <Card key={chat.id} className="group relative hover:shadow-md transition-shadow">
                            <Link href={`/c/${chat.id}`} className="absolute inset-0 z-0" prefetch={false}>
                                <span className="sr-only">View chat</span>
                            </Link>
                            <CardHeader className="relative z-10 flex flex-row items-start justify-between space-y-0 pb-2">
                                <div className="space-y-1 pr-6 max-w-full">
                                    <CardTitle className="text-base font-medium leading-none truncate w-full">
                                        {chat.title}
                                    </CardTitle>
                                    <CardDescription className="text-xs">
                                        {new Date(chat.updatedAt).toLocaleDateString()}
                                    </CardDescription>
                                </div>
                                <DropdownMenu>
                                    <DropdownMenuTrigger asChild>
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            className="h-8 w-8 -mr-2 -mt-2 opacity-0 group-hover:opacity-100 transition-opacity"
                                        >
                                            <MoreHorizontal className="h-4 w-4" />
                                            <span className="sr-only">Actions</span>
                                        </Button>
                                    </DropdownMenuTrigger>
                                    <DropdownMenuContent align="end">
                                        <DropdownMenuItem
                                            className="text-destructive focus:text-destructive"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                deleteChatMutation.mutate(chat.id);
                                            }}
                                        >
                                            <Trash2 className="mr-2 h-4 w-4" />
                                            Delete
                                        </DropdownMenuItem>
                                    </DropdownMenuContent>
                                </DropdownMenu>
                            </CardHeader>
                        </Card>
                    ))}
                </div>
            )}
        </div>
    );
}
