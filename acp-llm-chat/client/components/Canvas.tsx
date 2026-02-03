import { Button } from "@/components/ui/button";
import { X, ExternalLink, ShoppingBag, Store, ArrowRight, Share2, Tag } from "lucide-react";
import { cn } from "@/lib/utils";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";
import rehypeRaw from "rehype-raw";
import rehypeSanitize from "rehype-sanitize";
import { CanvasItem } from "@/stores/ChatStore";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from "@/components/ui/carousel";
import { ScrollArea } from "@/components/ui/scroll-area";

interface CanvasProps {
    isOpen: boolean;
    onClose: () => void;
    data: { items: CanvasItem[] } | null;
}

const ProductCard = ({ data }: { data: any }) => {
    const p = data || {};
    const media = p.media || [];
    const imageUrl = media.length > 0 ? media[0].url : null;
    const priceInfo = p.price || p.priceRange?.min || p.priceRange?.max;

    let price = "N/A";
    if (priceInfo) {
        if (typeof priceInfo === 'object') {
            const amount = parseFloat(priceInfo.amount);
            const displayAmount = isNaN(amount) ? priceInfo.amount : (amount / 100).toFixed(2);
            price = `${displayAmount} ${priceInfo.currency || ''}`.trim();
        } else if (typeof priceInfo === 'string') {
            price = priceInfo;
        }
    }

    return (
        <div className="group border rounded-xl p-4 bg-card hover:bg-accent/5 transition-colors shadow-sm">
            {imageUrl ? (
                <div className="aspect-[4/3] w-full mb-3 rounded-lg overflow-hidden bg-muted">
                    <img src={imageUrl} alt={p.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                </div>
            ) : (
                <div className="aspect-[4/3] w-full mb-3 rounded-lg bg-muted flex items-center justify-center text-muted-foreground">
                    No Image
                </div>
            )}
            <div className="flex flex-col gap-1">
                <h3 className="font-semibold text-base leading-tight">{p.title || "Unknown Product"}</h3>
                <p className="font-bold text-primary">{price}</p>
                {p.description && <p className="text-sm text-muted-foreground line-clamp-2 mt-1">{p.description}</p>}

                {p.onlineStoreUrl && (
                    <a href={p.onlineStoreUrl} target="_blank" rel="noopener noreferrer" className="flex items-center gap-1 text-xs text-primary mt-2 font-medium hover:underline">
                        View Details <ExternalLink className="h-3 w-3" />
                    </a>
                )}
            </div>
        </div>
    )
}

const ProductDetailView = ({ data }: { data: any }) => {
    // Inference from JSON sample
    const p = data || {};
    const variants = p.variants || [];
    const mainVariant = variants.length > 0 ? variants[0] : {};

    // Media logic: prefer top-level featuredVariantMedia, else mainVariant media, else top level media
    const rawMedia = (p.featuredVariantMedia?.length ? p.featuredVariantMedia : null)
        || (mainVariant.media?.length ? mainVariant.media : null)
        || (p.media?.length ? p.media : []);

    // Deduplicate media by URL
    const uniqueMedia = Array.from(new Map(rawMedia.map((m: any) => [m.url, m])).values());

    // Price
    let price = "N/A";
    const priceObj = mainVariant.price || p.price;
    if (priceObj) {
        const amount = parseFloat(priceObj.amount);
        const displayAmount = isNaN(amount) ? priceObj.amount : (amount / 100).toFixed(2);
        price = `${displayAmount} ${priceObj.currency || ''}`.trim();
    }

    // Shop
    const shop = mainVariant.shop || {};

    // Actions
    const checkoutUrl = mainVariant.checkoutUrl;
    const variantUrl = mainVariant.variantUrl || p.onlineStoreUrl;

    return (
        <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            {/* Header / Title Section */}
            <div className="space-y-2">
                {shop.name && (
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <Store className="h-4 w-4" />
                        <span>{shop.name}</span>
                    </div>
                )}
                <h1 className="text-2xl font-bold leading-tight">{p.title || mainVariant.displayName || "Product Details"}</h1>
                <div className="text-xl font-bold text-primary">{price}</div>
            </div>

            {/* Image Gallery */}
            {uniqueMedia.length > 0 ? (
                <div className="w-full bg-muted/30 rounded-xl overflow-hidden border">
                    <ScrollArea className="w-full whitespace-nowrap rounded-md border p-4">
                        <div className="flex w-full space-x-4">
                            {uniqueMedia.map((m: any, i: number) => (
                                <figure key={i} className="shrink-0">
                                    <div className="overflow-hidden rounded-md">
                                        <img
                                            src={m.url}
                                            alt={m.altText || `Product Image ${i + 1}`}
                                            className="aspect-[4/3] h-64 w-auto object-contain"
                                        />
                                    </div>
                                </figure>
                            ))}
                        </div>
                    </ScrollArea>
                </div>
            ) : (
                <div className="w-full h-64 bg-muted rounded-xl flex items-center justify-center text-muted-foreground">
                    No Images Available
                </div>
            )}

            {/* Actions */}
            <div className="flex flex-col sm:flex-row gap-3">
                {checkoutUrl && (
                    <Button className="flex-1 gap-2" size="lg" asChild>
                        <a href={checkoutUrl} target="_blank" rel="noopener noreferrer">
                            <ShoppingBag className="h-4 w-4" />
                            Buy Now
                        </a>
                    </Button>
                )}
                {variantUrl && (
                    <Button variant="outline" className="flex-1 gap-2" size="lg" asChild>
                        <a href={variantUrl} target="_blank" rel="noopener noreferrer">
                            View in Store
                            <ExternalLink className="h-4 w-4" />
                        </a>
                    </Button>
                )}
            </div>

            {/* USP Badge */}
            {p.uniqueSellingPoint && (
                <div className="bg-primary/5 border border-primary/20 p-4 rounded-lg flex items-start gap-3">
                    <Tag className="h-5 w-5 text-primary shrink-0 mt-0.5" />
                    <p className="text-sm text-primary/90 font-medium">{p.uniqueSellingPoint}</p>
                </div>
            )}

            <Separator />

            {/* Details Tabs */}
            <Tabs defaultValue="overview" className="w-full">
                <TabsList className="w-full justify-start overflow-x-auto">
                    <TabsTrigger value="overview">Overview</TabsTrigger>
                    {(p.topFeatures?.length > 0) && <TabsTrigger value="features">Features</TabsTrigger>}
                    {(p.techSpecs?.length > 0 || p.attributes?.length > 0) && <TabsTrigger value="specs">Specs</TabsTrigger>}
                    {(p.selectedOptions?.length > 0) && <TabsTrigger value="options">Options</TabsTrigger>}
                </TabsList>

                <TabsContent value="overview" className="mt-4 space-y-4">
                    <div className="prose dark:prose-invert max-w-none text-sm leading-relaxed">
                        {p.description || mainVariant.productDescription || "No description available."}
                    </div>
                </TabsContent>

                <TabsContent value="features" className="mt-4">
                    <ul className="grid gap-3">
                        {p.topFeatures?.map((feature: string, idx: number) => (
                            <li key={idx} className="flex gap-2 text-sm">
                                <span className="text-primary">•</span>
                                <span>{feature}</span>
                            </li>
                        ))}
                    </ul>
                </TabsContent>

                <TabsContent value="specs" className="mt-4 space-y-6">
                    {p.techSpecs?.length > 0 && (
                        <div className="space-y-3">
                            <h4 className="font-semibold text-sm">Technical Specifications</h4>
                            <ul className="grid gap-2 text-sm text-muted-foreground">
                                {p.techSpecs.map((spec: string, i: number) => (
                                    <li key={i} className="border-l-2 border-primary/20 pl-3">{spec}</li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {p.attributes?.length > 0 && (
                        <div className="space-y-3">
                            <h4 className="font-semibold text-sm">Attributes</h4>
                            <div className="flex flex-wrap gap-2">
                                {p.attributes.map((attr: any, i: number) => (
                                    <Badge key={i} variant="secondary" className="font-normal">
                                        <span className="font-semibold mr-1">{attr.name}:</span>
                                        {attr.values?.join(", ")}
                                    </Badge>
                                ))}
                            </div>
                        </div>
                    )}
                </TabsContent>

                <TabsContent value="options" className="mt-4">
                    <div className="grid grid-cols-2 gap-4">
                        {p.selectedOptions?.map((opt: any, i: number) => (
                            <div key={i} className="p-3 border rounded-lg">
                                <span className="text-xs text-muted-foreground uppercase font-bold">{opt.name}</span>
                                <div className="font-medium">{opt.value}</div>
                            </div>
                        ))}
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    );
};

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

// ... ProductCard component remains same ...

export function Canvas({ isOpen, onClose, data }: CanvasProps) {
    if (!isOpen) return null;

    const items = data?.items || [];

    // Group items by type
    const productListItems = items.filter(i => i.type === 'product_list');
    const productDetailItems = items.filter(i => i.type === 'product_detail');
    const errorItems = items.filter(i => i.type === 'error');
    const otherItems = items.filter(i => !['product_list', 'product_detail', 'error'].includes(i.type));

    // Determine default tab
    let defaultTab = "general";
    if (productDetailItems.length > 0) defaultTab = "details";
    else if (productListItems.length > 0) defaultTab = "products";
    else if (errorItems.length > 0) defaultTab = "debug";
    else if (otherItems.length > 0) defaultTab = "general";

    const hasAnyItems = items.length > 0;

    return (
        <div className={cn(
            "flex flex-col h-full border-l border-border/50 bg-background transition-all duration-300 ease-in-out z-20 shadow-xl",
            isOpen ? "w-1/2 min-w-[400px]" : "w-0 overflow-hidden opacity-0"
        )}>
            <div className="flex items-center justify-between px-4 py-3 border-b border-border/50 bg-muted/20">
                <h2 className="text-sm font-semibold flex items-center gap-2">
                    Canvas
                    <span className="text-xs font-normal text-muted-foreground bg-muted px-2 py-0.5 rounded-full">
                        {items.length} items
                    </span>
                </h2>
                <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-muted" onClick={onClose}>
                    <X className="h-4 w-4" />
                </Button>
            </div>

            <div className="flex-1 p-6 overflow-y-auto">
                {hasAnyItems ? (
                    <Tabs defaultValue={defaultTab} className="w-full">
                        <TabsList className="mb-4 w-full justify-start overflow-x-auto">
                            {productListItems.length > 0 && <TabsTrigger value="products">Products</TabsTrigger>}
                            {productDetailItems.length > 0 && <TabsTrigger value="details">Details</TabsTrigger>}
                            {otherItems.length > 0 && <TabsTrigger value="general">Content</TabsTrigger>}
                            {errorItems.length > 0 && <TabsTrigger value="debug">Debug</TabsTrigger>}
                        </TabsList>

                        <TabsContent value="products" className="space-y-6">
                            {productListItems.map((item, idx) => (
                                <div key={item.id || idx} className="flex flex-col gap-4">
                                    {Array.isArray(item.content) && item.content.map((prod: any, pIdx: number) => (
                                        <ProductCard key={pIdx} data={prod} />
                                    ))}
                                </div>
                            ))}
                        </TabsContent>

                        <TabsContent value="details" className="space-y-6">
                            {productDetailItems.map((item, idx) => (
                                <div key={item.id || idx}>
                                    <ProductDetailView data={item.content} />
                                </div>
                            ))}
                        </TabsContent>

                        <TabsContent value="general" className="space-y-6">
                            {otherItems.map((item, idx) => {
                                // Backward compatibility
                                if (item.type === 'products' || item.type === 'product' || item.type === 'offer') {
                                    return <ProductCard key={item.id || idx} data={item.content} />;
                                }
                                if (item.type === 'markdown') {
                                    return (
                                        <div key={item.id || idx} className="prose dark:prose-invert max-w-none bg-card p-4 rounded-lg border">
                                            <ReactMarkdown
                                                remarkPlugins={[remarkGfm, remarkBreaks]}
                                                rehypePlugins={[rehypeRaw, rehypeSanitize]}
                                                components={{
                                                    img: ({ node, ...props }: any) => <img {...props} className="rounded-lg border border-border/50" />
                                                }}
                                            >
                                                {item.content as string}
                                            </ReactMarkdown>
                                        </div>
                                    );
                                }
                                return (
                                    <div key={item.id || idx} className="p-4 border border-dashed rounded text-sm text-muted-foreground">
                                        Unknown item type: {item.type}
                                    </div>
                                );
                            })}
                        </TabsContent>

                        <TabsContent value="debug" className="space-y-4">
                            {errorItems.map((item, idx) => (
                                <div key={item.id || idx} className="p-4 bg-destructive/10 border border-destructive/50 rounded-lg text-sm text-destructive">
                                    <h3 className="font-semibold mb-1">Error</h3>
                                    <p>{item.content?.message || "An error occurred"}</p>
                                    {item.content?.traceback && (
                                        <details className="mt-2">
                                            <summary className="cursor-pointer hover:underline text-xs opacity-80">Technical Details</summary>
                                            <pre className="mt-2 p-2 bg-black/5 dark:bg-black/20 rounded text-xs overflow-x-auto whitespace-pre-wrap">
                                                {item.content.traceback}
                                            </pre>
                                        </details>
                                    )}
                                </div>
                            ))}
                        </TabsContent>
                    </Tabs>
                ) : (
                    <div className="flex flex-col items-center justify-center h-full text-muted-foreground gap-2">
                        <div className="p-4 rounded-full bg-muted/50">
                            <span className="text-2xl">🎨</span>
                        </div>
                        <p className="text-sm">Canvas is empty</p>
                    </div>
                )}
            </div>
        </div>
    );
}
