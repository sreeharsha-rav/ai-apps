import { SearchButton } from "./search-button";
import { NewChatButton } from "@/components/chat/new-chat-button";

export function ActionButtons() {
  return (
    <div className="mt-4 space-y-2">
      <SearchButton />
      <NewChatButton />
    </div>
  );
}
