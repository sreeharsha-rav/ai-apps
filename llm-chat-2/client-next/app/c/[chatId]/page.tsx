import { ChatContainer } from "@/components/ChatContainer";

interface ChatPageProps {
    params: Promise<{
        chatId: string;
    }>;
}

export default async function ChatPage(props: ChatPageProps) {
    const params = await props.params;

    return <ChatContainer chatId={params.chatId} />;
}

