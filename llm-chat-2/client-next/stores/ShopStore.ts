import { create } from "zustand";

export interface Product {
    id: string;
    name: string;
    price: number;
    category: string;
    stock: number;
    image?: string;
    description: string;
}

export interface CartItem extends Product {
    quantity: number;
}

interface ShopStore {
    products: Product[];
    cart: CartItem[];
    addToCart: (product: Product) => void;
    removeFromCart: (productId: string) => void;
    updateQuantity: (productId: string, quantity: number) => void;
    clearCart: () => void;
    getTotal: () => number;
}

export const useShopStore = create<ShopStore>((set, get) => ({
    products: [
        {
            id: "PRD-001",
            name: "Premium Wireless Headphones",
            price: 299.99,
            category: "Electronics",
            stock: 15,
            description: "High-quality wireless headphones with noise cancellation.",
            image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80"
        },
        {
            id: "PRD-002",
            name: "Ergonomic Office Chair",
            price: 199.50,
            category: "Furniture",
            stock: 8,
            description: "Comfortable office chair designed for long hours.",
            image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80"
        },
        {
            id: "PRD-003",
            name: "Mechanical Keyboard",
            price: 129.00,
            category: "Peripherals",
            stock: 24,
            description: "Tactile mechanical keyboard with RGB lighting.",
            image: "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=500&q=80"
        },
        {
            id: "PRD-004",
            name: "Smart Watch Series X",
            price: 399.00,
            category: "Wearables",
            stock: 12,
            description: "Advanced health tracking and notifications.",
            image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80"
        },
        {
            id: "PRD-005",
            name: "Leather Messenger Bag",
            price: 89.99,
            category: "Accessories",
            stock: 20,
            description: "Handcrafted leather bag for professionals.",
            image: "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=500&q=80"
        }
    ],
    cart: [],

    addToCart: (product) => {
        const cart = get().cart;
        const existingItem = cart.find((item) => item.id === product.id);

        if (existingItem) {
            set({
                cart: cart.map((item) =>
                    item.id === product.id
                        ? { ...item, quantity: item.quantity + 1 }
                        : item
                ),
            });
        } else {
            set({ cart: [...cart, { ...product, quantity: 1 }] });
        }
    },

    removeFromCart: (productId) => {
        set({
            cart: get().cart.filter((item) => item.id !== productId),
        });
    },

    updateQuantity: (productId, quantity) => {
        if (quantity <= 0) {
            get().removeFromCart(productId);
            return;
        }
        set({
            cart: get().cart.map((item) =>
                item.id === productId ? { ...item, quantity } : item
            ),
        });
    },

    clearCart: () => set({ cart: [] }),

    getTotal: () => {
        return get().cart.reduce(
            (total, item) => total + item.price * item.quantity,
            0
        );
    },
}));
