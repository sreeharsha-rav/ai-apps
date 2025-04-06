import { useParams } from "react-router";
import { useChatStore } from "@/stores/chat-store";

export function ChatPage() {
  const { id } = useParams();
  const { getChatById } = useChatStore();
  const chat = id ? getChatById(id) : null;

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 p-4 pt-0">
        <h1 className="text-2xl font-bold">{chat ? chat.title : "New Chat"}</h1>
        <div className="min-h-[100vh] flex-1 rounded-xl bg-muted/50 md:min-h-min">
          {/* Chat content will go here */}
          <p className="text-sm text-muted-foreground">
            This is a simple chat page layout. You can add your chat components
            here. The layout is responsive and will adjust based on the screen
            size.
            <br />
            The active state is now managed by the URL path.
            <br />
          </p>
        </div>
      </div>
    </div>
  );
}
