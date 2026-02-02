import React, { useRef, useEffect } from "react";
import { useVirtualizer } from "@tanstack/react-virtual";
import { ChatMessage } from "./ChatMessage";
import { Item } from "@/stores/ChatStore";

interface MessageListProps {
    items: Item[];
    isGenerating: boolean;
}

export function MessageList({ items, isGenerating }: MessageListProps) {
    const parentRef = useRef<HTMLDivElement>(null);

    const rowVirtualizer = useVirtualizer({
        count: items.length,
        getScrollElement: () => parentRef.current,
        estimateSize: () => 80,
        overscan: 5,
    });

    // Auto-scroll to bottom on new items
    useEffect(() => {
        if (items.length > 0) {
            rowVirtualizer.scrollToIndex(items.length - 1, { align: 'end', behavior: 'smooth' });
        }
    }, [items.length, rowVirtualizer]);

    return (
        <div
            ref={parentRef}
            className="flex-1 min-h-0 overflow-y-auto scroll-smooth"
        >
            <div
                style={{
                    height: `${rowVirtualizer.getTotalSize()}px`,
                    width: '100%',
                    position: 'relative',
                }}
                className="max-w-3xl mx-auto py-6 px-4"
            >
                {rowVirtualizer.getVirtualItems().map((virtualItem) => {
                    const item = items[virtualItem.index];
                    const isLast = virtualItem.index === items.length - 1;
                    const showLoader = isLast && isGenerating && item.data.role === "assistant" && !item.data.content;

                    // Clean up item for loader state
                    const displayItem = showLoader
                        ? { ...item, data: { ...item.data, content: "" } }
                        : item;

                    return (
                        <div
                            key={virtualItem.key}
                            data-index={virtualItem.index}
                            ref={rowVirtualizer.measureElement}
                            style={{
                                position: 'absolute',
                                top: 0,
                                left: 0,
                                width: '100%',
                                transform: `translateY(${virtualItem.start}px)`,
                            }}
                        >
                            <ChatMessage
                                item={displayItem}
                                isLoader={showLoader}
                            />
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
