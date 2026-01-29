import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

export function ChatSkeleton() {
    return (
        <div className="flex-1 flex flex-col bg-background relative overflow-hidden h-[calc(100svh-4rem)] md:h-[calc(100svh-4.5rem)] min-h-0">
            {/* Thread Title Bar Skeleton */}
            <header className="flex items-center justify-between px-6 py-3 border-b border-border/50 bg-background/80 backdrop-blur-md sticky top-0 z-20">
                <div className="flex items-center gap-3 min-w-0 w-full max-w-sm">
                    <Skeleton className="h-8 w-8 rounded-lg shrink-0" />
                    <div className="flex flex-col gap-2 flex-1">
                        <Skeleton className="h-4 w-1/3" />
                        <Skeleton className="h-3 w-1/4" />
                    </div>
                </div>
            </header>

            {/* Messages Area Skeleton */}
            <div className="flex-1 min-h-0 relative">
                <div className="h-full overflow-y-auto py-8 px-4 pb-40">
                    <div className="max-w-3xl mx-auto space-y-8">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className={cn(
                                "flex w-full gap-3",
                                i % 2 === 0 ? "justify-end" : "justify-start"
                            )}>
                                {i % 2 !== 0 && <Skeleton className="h-8 w-8 rounded-full shrink-0 mt-1" />}
                                <div className={cn(
                                    "flex flex-col gap-2 max-w-[80%]",
                                    i % 2 === 0 && "items-end"
                                )}>
                                    <Skeleton className={cn(
                                        "h-20 rounded-2xl",
                                        i % 2 === 0 ? "w-64 rounded-tr-none" : "w-80 rounded-tl-none"
                                    )} />
                                    <Skeleton className="h-3 w-16" />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Floating Input Area Skeleton */}
            <div className="absolute bottom-0 left-0 right-0 z-30 pointer-events-none">
                <div className="bg-gradient-to-t from-background via-background/80 to-transparent pt-20 pb-8 px-4">
                    <div className="max-w-3xl mx-auto pointer-events-auto">
                        <div className="relative flex items-center">
                            <Skeleton className="h-16 w-full rounded-2xl shadow-2xl" />
                            <Skeleton className="absolute right-3 h-12 w-12 rounded-xl" />
                        </div>
                        <div className="flex justify-center mt-4">
                            <Skeleton className="h-3 w-40" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
