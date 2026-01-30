module.exports = [
"[externals]/next/dist/compiled/next-server/app-route-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-route-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-route-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-route-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[externals]/next/dist/compiled/@opentelemetry/api [external] (next/dist/compiled/@opentelemetry/api, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/@opentelemetry/api", () => require("next/dist/compiled/@opentelemetry/api"));

module.exports = mod;
}),
"[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-unit-async-storage.external.js [external] (next/dist/server/app-render/work-unit-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/work-unit-async-storage.external.js", () => require("next/dist/server/app-render/work-unit-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-async-storage.external.js [external] (next/dist/server/app-render/work-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/work-async-storage.external.js", () => require("next/dist/server/app-render/work-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/shared/lib/no-fallback-error.external.js [external] (next/dist/shared/lib/no-fallback-error.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/shared/lib/no-fallback-error.external.js", () => require("next/dist/shared/lib/no-fallback-error.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/after-task-async-storage.external.js [external] (next/dist/server/app-render/after-task-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/after-task-async-storage.external.js", () => require("next/dist/server/app-render/after-task-async-storage.external.js"));

module.exports = mod;
}),
"[project]/lib/chats-mock.json (json)", ((__turbopack_context__) => {

__turbopack_context__.v([{"id":"chat_mock_1","title":"Order #12345 Support","messages":[{"id":"m1","role":"user","content":"Hi, I'm checking the status of my order #12345.","timestamp":"2024-01-10T10:00:00Z"},{"id":"m2","role":"assistant","content":"Hello! Let me check that for you... \n\nYour order **#12345** is currently **In Transit** and is expected to arrive by **Thursday, Jan 12th**.\n\n### Order Details:\n- **Item:** Premium Wireless Headphones\n- **Status:** Shipped\n- **Carrier:** Fedex","timestamp":"2024-01-10T10:00:15Z"}],"createdAt":"2024-01-10T10:00:00Z","updatedAt":"2024-01-10T10:00:15Z"},{"id":"chat_mock_2","title":"Product Comparison: Keyboards","messages":[{"id":"m3","role":"user","content":"Can you compare the Mechanical Keyboard and the basic Office Keyboard?","timestamp":"2024-01-11T14:20:00Z"},{"id":"m4","role":"assistant","content":"Certainly! Here's a quick comparison:\n\n| Feature | Mechanical Keyboard | Office Keyboard |\n| :--- | :--- | :--- |\n| **Switch Type** | Tactile Blue | Membrane |\n| **Durability** | 50M Clicks | 5M Clicks |\n| **Backlight** | RGB | None |\n| **Price** | $129.00 | $29.00 |\n\nIf you do a lot of typing or gaming, the **Mechanical Keyboard** is highly recommended for its tactile feedback and durability.","timestamp":"2024-01-11T14:20:30Z"}],"createdAt":"2024-01-11T14:20:00Z","updatedAt":"2024-01-11T14:20:30Z"},{"id":"chat_mock_3","title":"Return Policy Inquiry","messages":[{"id":"m5","role":"user","content":"What is your return policy for electronics?","timestamp":"2024-01-12T09:15:00Z"},{"id":"m6","role":"assistant","content":"Our return policy for electronics is as follows:\n\n1. **30-Day Window**: You can return any electronic item within 30 days of purchase.\n2. **Condition**: Items must be in their original packaging with all accessories.\n3. **Restocking Fee**: A 10% restocking fee applies to opened items.\n\nYou can initiate a return through your `Account Settings` or by speaking with our support team.","timestamp":"2024-01-12T09:15:20Z"}],"createdAt":"2024-01-12T09:15:00Z","updatedAt":"2024-01-12T09:15:20Z"}]);}),
"[project]/app/api/chats/route.ts [app-route] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "GET",
    ()=>GET
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$0$2e$10_$40$babel$2b$core$40$7$2e$_c57d9b56c0bd86dac4690a5de51b3a27$2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/.pnpm/next@16.0.10_@babel+core@7._c57d9b56c0bd86dac4690a5de51b3a27/node_modules/next/server.js [app-route] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$chats$2d$mock$2e$json__$28$json$29$__ = __turbopack_context__.i("[project]/lib/chats-mock.json (json)");
;
;
async function GET() {
    // Simulate a network delay
    await new Promise((resolve)=>setTimeout(resolve, 500));
    // Generate a stress test chat with 100 messages
    const stressMessages = [];
    for(let i = 1; i <= 100; i++){
        const isUser = i % 2 !== 0;
        stressMessages.push({
            id: `stress_m${i}`,
            role: isUser ? "user" : "assistant",
            content: isUser ? `Message #${i}: Testing scroll performance with some **bold** text and [links](https://google.com).` : `Reply #${i}: This is an automated response for the stress test. It contains some \`inline code\` and a list:\n\n- Item ${i}\n- Efficiency check\n- UI smooth?`,
            timestamp: new Date(Date.now() - (101 - i) * 60000).toISOString()
        });
    }
    const stressChat = {
        id: "chat_stress_test",
        title: "🚀 Performance Stress Test (100 msgs)",
        messages: stressMessages,
        createdAt: stressMessages[0].timestamp,
        updatedAt: stressMessages[99].timestamp
    };
    return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$16$2e$0$2e$10_$40$babel$2b$core$40$7$2e$_c57d9b56c0bd86dac4690a5de51b3a27$2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json([
        ...__TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$chats$2d$mock$2e$json__$28$json$29$__["default"],
        stressChat
    ]);
}
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__94007bf3._.js.map