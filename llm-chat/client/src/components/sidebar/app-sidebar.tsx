import { Sparkles } from "lucide-react";
import { NavUser } from "@/components/sidebar/nav-user";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { ChatListContainer, NewChatButton } from "@/components/chat";
import { SearchButton } from "@/components/sidebar/search-button";

const USER_DATA = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
};

function SidebarLogo() {
  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <SidebarMenuButton size="lg" asChild>
          <a href="#">
            <div className="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center rounded-lg">
              <Sparkles className="size-4" />
            </div>
            <div className="grid flex-1 text-left text-sm leading-tight">
              <span className="truncate font-medium">LLM Chat</span>
            </div>
          </a>
        </SidebarMenuButton>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}

function SidebarContentWrapper() {
  return (
    <SidebarContent>
      <ChatListContainer />
    </SidebarContent>
  );
}

function SidebarHeaderWrapper() {
  return (
    <SidebarHeader>
      <SidebarLogo />
      <SearchButton />
      <NewChatButton />
    </SidebarHeader>
  );
}

function SidebarFooterWrapper() {
  return (
    <SidebarFooter>
      <NavUser user={USER_DATA.user} />
    </SidebarFooter>
  );
}

export function AppSidebar() {
  return (
    <Sidebar variant="inset">
      <SidebarHeaderWrapper />
      <SidebarContentWrapper />
      <SidebarFooterWrapper />
    </Sidebar>
  );
}
