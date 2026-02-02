import { NextResponse } from "next/server";
import chatsMock from "@/lib/chats-mock.json";

export async function GET() {
    // Simulate a network delay
    await new Promise((resolve) => setTimeout(resolve, 500));

    // Generate a stress test chat with 100 messages
    const stressMessages = [];
    for (let i = 1; i <= 100; i++) {
        const isUser = i % 2 !== 0;
        stressMessages.push({
            id: `stress_m${i}`,
            role: isUser ? "user" : "assistant",
            content: isUser
                ? `Message #${i}: Testing scroll performance with some **bold** text and [links](https://google.com).`
                : `Reply #${i}: This is an automated response for the stress test. It contains some \`inline code\` and a list:\n\n- Item ${i}\n- Efficiency check\n- UI smooth?`,
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

    return NextResponse.json([...chatsMock, stressChat]);
}
