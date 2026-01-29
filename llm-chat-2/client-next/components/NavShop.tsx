"use client"

import { ShoppingCart } from "lucide-react"
import {
    SidebarGroup,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar"
import Link from "next/link"
import { useShopStore } from "@/stores/ShopStore"
import { Badge } from "@/components/ui/badge"

export function NavShop() {
    const cart = useShopStore((state) => state.cart);
    const cartCount = cart.reduce((total, item) => total + item.quantity, 0);

    return (
        <SidebarGroup>
            <SidebarGroupLabel>Platform</SidebarGroupLabel>
            <SidebarMenu>
                <SidebarMenuItem>
                    <SidebarMenuButton asChild tooltip="Shop">
                        <Link href="/shop" className="flex items-center justify-between w-full">
                            <div className="flex items-center gap-2">
                                <ShoppingCart className="size-4" />
                                <span>Shop</span>
                            </div>
                            {cartCount > 0 && (
                                <Badge variant="default" className="ml-auto flex h-5 w-5 items-center justify-center rounded-full p-0 text-[10px] bg-primary text-primary-foreground">
                                    {cartCount}
                                </Badge>
                            )}
                        </Link>
                    </SidebarMenuButton>
                </SidebarMenuItem>
            </SidebarMenu>
        </SidebarGroup>
    )
}

