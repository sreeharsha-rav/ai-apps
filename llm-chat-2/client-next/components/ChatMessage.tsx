"use client";

import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";
import rehypeRaw from "rehype-raw";
import rehypeSanitize from "rehype-sanitize";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Message } from "@/stores/ChatStore";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Bot, User } from "lucide-react";
import { cn } from "@/lib/utils";
import { format } from "date-fns";

interface ChatMessageProps {
    message: Message;
    isLoader?: boolean;
}

export function ChatMessage({ message, isLoader }: ChatMessageProps) {
    const isAssistant = message.role === "assistant";

    return (
        <div className={cn(
            "flex w-full gap-3 py-2",
            isAssistant ? "justify-start" : "justify-end"
        )}>
            {isAssistant && (
                <Avatar className="h-8 w-8 border border-border/30 shrink-0 mt-1">
                    <AvatarImage src="/ai-avatar.png" />
                    <AvatarFallback className="bg-primary/5 text-primary">
                        <Bot className="h-4 w-4" />
                    </AvatarFallback>
                </Avatar>
            )}

            <div className={cn(
                "flex flex-col gap-1.5 max-w-[85%]",
                !isAssistant && "items-end"
            )}>
                <div className={cn(
                    "px-4 py-2.5 rounded-2xl text-[14px] leading-relaxed",
                    isAssistant
                        ? "bg-muted/40 rounded-tl-none border border-border/10"
                        : "bg-primary text-primary-foreground rounded-tr-none shadow-sm",
                    isLoader && "animate-pulse"
                )}>
                    <div className="max-w-none break-words overflow-hidden antialiased">
                        {isLoader ? (
                            <div className="flex items-center gap-1">
                                <span className="flex gap-0.5">
                                    <span className="animate-bounce">.</span>
                                    <span className="animate-bounce delay-100">.</span>
                                    <span className="animate-bounce delay-200">.</span>
                                </span>
                            </div>
                        ) : (
                            <ReactMarkdown
                                remarkPlugins={[remarkGfm, remarkBreaks]}
                                rehypePlugins={[rehypeRaw, rehypeSanitize]}
                                components={{
                                    p: ({ children }) => <p className="mb-2 last:mb-0 leading-relaxed font-normal">{children}</p>,
                                    hr: () => <hr className="my-4 border-border/50" />,
                                    ul: ({ children }) => <ul className="list-disc ml-6 mb-2 space-y-1">{children}</ul>,
                                    ol: ({ children }) => <ol className="list-decimal ml-6 mb-2 space-y-1">{children}</ol>,
                                    li: ({ children }) => <li className="mb-0.5">{children}</li>,
                                    h1: ({ children }) => <h1 className="text-xl font-bold mt-4 mb-2">{children}</h1>,
                                    h2: ({ children }) => <h2 className="text-lg font-bold mt-3 mb-2">{children}</h2>,
                                    h3: ({ children }) => <h3 className="text-md font-bold mt-2 mb-1">{children}</h3>,
                                    blockquote: ({ children }) => (
                                        <blockquote className="border-l-4 border-primary/30 pl-4 py-1 italic my-2 bg-muted/20 rounded-r">
                                            {children}
                                        </blockquote>
                                    ),
                                    code({ className, children, ...props }: any) {
                                        const match = /language-(\w+)/.exec(className || "");
                                        const isInline = !match;
                                        if (isInline) {
                                            return (
                                                <code
                                                    className={cn(
                                                        "bg-muted-foreground/15 px-1.5 py-0.5 rounded text-[12px] font-mono font-medium",
                                                        className
                                                    )}
                                                    {...props}
                                                >
                                                    {children}
                                                </code>
                                            );
                                        }
                                        return (
                                            <div className="rounded-xl overflow-hidden my-4 border border-[#333333] shadow-xl">
                                                <div className="flex items-center justify-between px-4 py-2 bg-[#252526] text-[11px] uppercase tracking-wider font-semibold text-[#858585] border-b border-[#333333]">
                                                    <span>{match[1]}</span>
                                                </div>
                                                <SyntaxHighlighter
                                                    style={vscDarkPlus}
                                                    language={match[1]}
                                                    PreTag="div"
                                                    customStyle={{
                                                        margin: 0,
                                                        padding: "1.25rem",
                                                        fontSize: "13px",
                                                        lineHeight: "1.6",
                                                        backgroundColor: "#1e1e1e",
                                                    }}
                                                >
                                                    {String(children).replace(/\n$/, "")}
                                                </SyntaxHighlighter>
                                            </div>
                                        );
                                    },
                                    table: ({ children }) => (
                                        <div className="my-4 overflow-x-auto rounded-lg border border-border/20 shadow-sm">
                                            <table className="w-full text-left border-collapse">{children}</table>
                                        </div>
                                    ),
                                    thead: ({ children }) => <thead className="bg-muted/50">{children}</thead>,
                                    th: ({ children }) => (
                                        <th className="px-4 py-2 border-b border-border/20 font-bold text-sm">{children}</th>
                                    ),
                                    td: ({ children }) => (
                                        <td className="px-4 py-2 border-b border-border/10 text-sm">{children}</td>
                                    ),
                                    img: ({ src, alt }) => (
                                        <div className="my-4 rounded-xl overflow-hidden border border-border/20 shadow-md">
                                            {/* eslint-disable-next-line @next/next/no-img-element */}
                                            <img src={src} alt={alt} className="max-w-full h-auto" />
                                        </div>
                                    ),
                                    a: ({ href, children }) => (
                                        <a
                                            href={href}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-primary hover:underline underline-offset-4"
                                        >
                                            {children}
                                        </a>
                                    ),
                                }}
                            >
                                {message.content}
                            </ReactMarkdown>
                        )}
                    </div>
                </div>
                <div className="flex items-center gap-2 px-1">
                    <span className="text-[10px] text-muted-foreground font-medium">
                        {format(new Date(message.timestamp), "h:mm a")}
                    </span>
                    {message.total_tokens ? (
                        <span className="text-[10px] text-muted-foreground/50">
                            • {message.total_tokens} tokens
                        </span>
                    ) : null}
                </div>
            </div>

            {!isAssistant && (
                <Avatar className="h-8 w-8 border border-border/30 shrink-0 mt-1">
                    <AvatarFallback className="bg-muted/50 text-muted-foreground text-[10px] font-bold">
                        <User className="h-4 w-4" />
                    </AvatarFallback>
                </Avatar>
            )}
        </div>
    );
}
