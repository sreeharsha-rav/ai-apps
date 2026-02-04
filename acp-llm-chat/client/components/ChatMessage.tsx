"use client";

import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";
import rehypeRaw from "rehype-raw";
import rehypeSanitize from "rehype-sanitize";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Item } from "@/stores/ChatStore";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Bot, User, Copy, Check } from "lucide-react";
import { cn } from "@/lib/utils";
import { format } from "date-fns";
import { useChatStore } from "@/stores/ChatStore";
import { Loader } from "@/components/prompt-kit/loader";

interface ChatMessageProps {
    item: Item;
    isLoader?: boolean;
}

const ImageRenderer = ({ src, alt }: React.ImgHTMLAttributes<HTMLImageElement>) => {
    const [hasError, setHasError] = React.useState(false);

    if (hasError) {
        return (
            <div className="block my-4 p-4 border border-dashed border-border rounded-xl bg-muted/50 text-center">
                <p className="text-xs text-muted-foreground italic">
                    Image failed to load: {alt || "Untitled"}
                </p>
            </div>
        );
    }

    return (
        <span className="block my-4 rounded-xl overflow-hidden border border-border/20 shadow-md bg-muted/20 relative min-h-[100px] flex items-center justify-center">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            {/* FUTURE: Use Next Image, optimize loading of images */}
            <img
                src={src}
                alt={alt}
                className="max-w-full h-auto block"
                onError={() => setHasError(true)}
                loading="lazy"
            />
        </span>
    );
};

const StaticComponents = {
    p: ({ children }: any) => <div className="mb-2 last:mb-0 leading-relaxed font-normal">{children}</div>,
    hr: () => <hr className="my-4 border-border/50" />,
    ul: ({ children }: any) => <ul className="list-disc ml-6 mb-2 space-y-1">{children}</ul>,
    ol: ({ children }: any) => <ol className="list-decimal ml-6 mb-2 space-y-1">{children}</ol>,
    li: ({ children }: any) => <li className="mb-0.5">{children}</li>,
    h1: ({ children }: any) => <h1 className="text-xl font-bold mt-4 mb-2">{children}</h1>,
    h2: ({ children }: any) => <h2 className="text-lg font-bold mt-3 mb-2">{children}</h2>,
    h3: ({ children }: any) => <h3 className="text-md font-bold mt-2 mb-1">{children}</h3>,
    blockquote: ({ children }: any) => (
        <blockquote className="border-l-4 border-primary/30 pl-4 py-1 italic my-2 bg-muted/20 rounded-r">
            {children}
        </blockquote>
    ),
    table: ({ children }: any) => (
        <div className="my-4 overflow-x-auto rounded-lg border border-border/20 shadow-sm">
            <table className="w-full text-left border-collapse">{children}</table>
        </div>
    ),
    thead: ({ children }: any) => <thead className="bg-muted/50">{children}</thead>,
    th: ({ children }: any) => (
        <th className="px-4 py-2 border-b border-border/20 font-bold text-sm">{children}</th>
    ),
    td: ({ children }: any) => (
        <td className="px-4 py-2 border-b border-border/10 text-sm">{children}</td>
    ),
    a: ({ href, children }: any) => (
        <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary hover:underline underline-offset-4"
        >
            {children}
        </a>
    ),
    img: ImageRenderer as any,
};

export function ChatMessage({ item, isLoader }: ChatMessageProps) {
    const isAssistant = item.data.role === "assistant";
    const { activeCopiedId, setActiveCopiedId } = useChatStore();

    let content = "";
    // Best effort content extraction
    if (typeof item.data.content === "string") {
        content = item.data.content;
    } else if (Array.isArray(item.data.content)) {
        content = item.data.content
            .map((c: any) => c.text || c.content || "")
            .join("");
    } else if (item.data.text) {
        content = item.data.text;
    } else if (item.data.type == "message" && Array.isArray(item.data.content)) {
        content = item.data.content[0]?.text || "";
    }

    const handleCopy = React.useCallback((text: string, id: string) => {
        navigator.clipboard.writeText(text);
        setActiveCopiedId(id);
        setTimeout(() => {
            setActiveCopiedId(null);
        }, 2000);
    }, [setActiveCopiedId]);

    const components = React.useMemo(() => ({
        ...StaticComponents,
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
            const codeContent = String(children).replace(/\n$/, "");
            const codeId = `${item.id}-code-${match[1]}`;
            const isCopied = activeCopiedId === codeId;

            return (
                <div className="rounded-xl overflow-hidden my-4 border border-[#333333] shadow-xl group/code">
                    <div className="flex items-center justify-between px-4 py-2 bg-[#252526] text-[11px] uppercase tracking-wider font-semibold text-[#858585] border-b border-[#333333]">
                        <span>{match[1]}</span>
                        <button
                            onClick={() => handleCopy(codeContent, codeId)}
                            className="flex items-center gap-1.5 hover:text-white transition-colors"
                        >
                            {isCopied ? (
                                <Check className="h-3 w-3 text-green-500" />
                            ) : (
                                <Copy className="h-3 w-3" />
                            )}
                            <span className="normal-case">{isCopied ? "Copied" : "Copy"}</span>
                        </button>
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
                        {codeContent}
                    </SyntaxHighlighter>
                </div>
            );
        },
    }), [handleCopy, activeCopiedId, item.id]);

    return (
        <div className={cn(
            "flex w-full gap-3 py-2 group/message",
            isAssistant ? "justify-start" : "justify-end"
        )}>
            {isAssistant && (
                <Avatar className="h-8 w-8 border border-border/30 shrink-0 mt-1">
                    <AvatarImage src="/bot-avatar.png" />
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
                    "px-4 py-2.5 rounded-2xl text-[14px] leading-relaxed relative",
                    isAssistant
                        ? "bg-muted/40 rounded-tl-none border border-border/10"
                        : "bg-primary text-primary-foreground rounded-tr-none shadow-sm",
                    isLoader && "animate-pulse"
                )}>
                    <div className="max-w-none break-words overflow-hidden antialiased">
                        {content && (
                            <ReactMarkdown
                                remarkPlugins={[remarkGfm, remarkBreaks]}
                                rehypePlugins={[rehypeRaw, rehypeSanitize]}
                                components={components}
                            >
                                {content}
                            </ReactMarkdown>
                        )}

                        {(isLoader || (item.metadata?.status && item.metadata.status !== "streaming" && item.metadata.status !== "completed")) && (
                            <div className={cn("flex flex-col gap-2", content && "mt-4 pt-2 border-t border-border/10")}>
                                <div className="flex items-center gap-3">
                                    <Loader
                                        variant="text-shimmer"
                                        className="text-xs"
                                        text={item.metadata?.statusMessage || "Thinking..."}
                                    />
                                </div>
                                {item.metadata?.reasoning && (
                                    <div className="text-xs text-muted-foreground/80 bg-background/50 p-3 rounded-lg border border-border/20 font-mono mt-1 overflow-x-auto whitespace-pre-wrap leading-relaxed max-h-[300px] overflow-y-auto">
                                        {item.metadata.reasoning}
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>
                <div className="flex items-center gap-2 px-1">
                    <button
                        onClick={() => handleCopy(content, item.id)}
                        className={cn(
                            "flex items-center gap-1 px-1.5 py-0.5 rounded-md transition-all",
                            "hover:bg-muted opacity-0 group-hover/message:opacity-100",
                            activeCopiedId === item.id && "opacity-100 text-green-500 hover:text-green-600"
                        )}
                        title="Copy message"
                    >
                        {activeCopiedId === item.id ? (
                            <Check className="h-3 w-3" />
                        ) : (
                            <Copy className="h-3 w-3" />
                        )}
                        <span className="text-[10px] font-medium">
                            {activeCopiedId === item.id ? "Copied" : "Copy"}
                        </span>
                    </button>
                    <span className="text-[10px] text-muted-foreground font-medium">
                        {format(new Date(item.timestamp), "h:mm a")}
                    </span>
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
