"use client"

import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ShoppingCart, Package, Tag, Plus, Minus, Trash2 } from "lucide-react";
import { useShopStore, Product } from "@/stores/ShopStore";
import Image from "next/image";
import { Separator } from "@/components/ui/separator";

export default function ShopPage() {
    const { products, cart, addToCart, removeFromCart, updateQuantity, getTotal } = useShopStore();

    return (
        <div className="flex flex-col lg:flex-row gap-6 p-6">
            <div className="flex-1 flex flex-col gap-4">
                <header className="flex flex-col gap-1">
                    <h1 className="text-3xl font-bold tracking-tight">Marketplace</h1>
                    <p className="text-muted-foreground">Discover premium products for your lifestyle.</p>
                </header>

                <ScrollArea className="h-[calc(100vh-12rem)] pr-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pb-8">
                        {products.map((product) => (
                            <Card key={product.id} className="overflow-hidden group flex flex-col">
                                <div className="relative h-48 w-full overflow-hidden bg-muted">
                                    {product.image ? (
                                        <img
                                            src={product.image}
                                            alt={product.name}
                                            className="object-cover w-full h-full transition-transform duration-300 group-hover:scale-105"
                                        />
                                    ) : (
                                        <div className="flex items-center justify-center h-full">
                                            <Package className="h-12 w-12 text-muted-foreground/50" />
                                        </div>
                                    )}
                                    <Badge className="absolute top-2 right-2 backdrop-blur-md bg-background/50 text-foreground border-none">
                                        {product.category}
                                    </Badge>
                                </div>
                                <CardHeader className="pb-2">
                                    <div className="flex justify-between items-start">
                                        <CardTitle className="text-xl font-semibold leading-tight">{product.name}</CardTitle>
                                        <span className="text-lg font-bold text-primary">${product.price.toFixed(2)}</span>
                                    </div>
                                    <p className="text-sm text-muted-foreground line-clamp-2 mt-1">
                                        {product.description}
                                    </p>
                                </CardHeader>
                                <CardContent className="pb-2 pt-0 flex-1">
                                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                                        <Tag className="h-3 w-3" />
                                        <span>{product.stock} units available</span>
                                    </div>
                                </CardContent>
                                <CardFooter className="pt-2">
                                    <Button
                                        className="w-full gap-2 transition-all"
                                        onClick={() => addToCart(product)}
                                    >
                                        <Plus className="h-4 w-4" />
                                        Add to Cart
                                    </Button>
                                </CardFooter>
                            </Card>
                        ))}
                    </div>
                </ScrollArea>
            </div>

            {/* Shopping Cart Sidebar for Desktop */}
            <div className="w-full lg:w-80 flex flex-col gap-4">
                <Card className="sticky top-6">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <ShoppingCart className="h-5 w-5" />
                            Your Cart
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="p-0">
                        <ScrollArea className="h-[calc(100vh-25rem)] px-6">
                            {cart.length === 0 ? (
                                <div className="flex flex-col items-center justify-center py-12 text-center text-muted-foreground">
                                    <ShoppingCart className="h-12 w-12 mb-4 opacity-20" />
                                    <p>Your cart is empty.</p>
                                </div>
                            ) : (
                                <div className="space-y-4 py-4">
                                    {cart.map((item) => (
                                        <div key={item.id} className="flex flex-col gap-2">
                                            <div className="flex justify-between items-start gap-2">
                                                <div className="flex-1 min-w-0">
                                                    <p className="text-sm font-medium truncate">{item.name}</p>
                                                    <p className="text-xs text-muted-foreground">${item.price.toFixed(2)}</p>
                                                </div>
                                                <Button
                                                    variant="ghost"
                                                    size="icon"
                                                    className="h-7 w-7 text-muted-foreground hover:text-destructive"
                                                    onClick={() => removeFromCart(item.id)}
                                                >
                                                    <Trash2 className="h-4 w-4" />
                                                </Button>
                                            </div>
                                            <div className="flex items-center justify-between">
                                                <div className="flex items-center border rounded-md">
                                                    <Button
                                                        variant="ghost"
                                                        size="icon"
                                                        className="h-7 w-7 rounded-none"
                                                        onClick={() => updateQuantity(item.id, item.quantity - 1)}
                                                    >
                                                        <Minus className="h-3 w-3" />
                                                    </Button>
                                                    <span className="w-8 text-center text-xs">{item.quantity}</span>
                                                    <Button
                                                        variant="ghost"
                                                        size="icon"
                                                        className="h-7 w-7 rounded-none"
                                                        onClick={() => updateQuantity(item.id, item.quantity + 1)}
                                                    >
                                                        <Plus className="h-3 w-3" />
                                                    </Button>
                                                </div>
                                                <span className="text-sm font-semibold">${(item.price * item.quantity).toFixed(2)}</span>
                                            </div>
                                            <Separator className="mt-2" />
                                        </div>
                                    ))}
                                </div>
                            )}
                        </ScrollArea>
                    </CardContent>
                    <CardFooter className="flex flex-col gap-4 pt-6">
                        <div className="flex justify-between w-full text-lg font-bold">
                            <span>Total</span>
                            <span>${getTotal().toFixed(2)}</span>
                        </div>
                        <Button className="w-full" size="lg" disabled={cart.length === 0}>
                            Checkout
                        </Button>
                    </CardFooter>
                </Card>
            </div>
        </div>
    );
}

