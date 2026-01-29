"use client";

import { Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";

export const SearchChatButton = () => {
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  return (
    <Button
      variant="outline"
      size="sm"
      className="w-full gap-2 justify-center bg-secondary text-secondary-foreground hover:bg-secondary/90"
      onClick={() => setIsSearchOpen(true)}
    >
      <Search size={14} strokeWidth={2} />
      <span>Search</span>
    </Button>
  );
}
