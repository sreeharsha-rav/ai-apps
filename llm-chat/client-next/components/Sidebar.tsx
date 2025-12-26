import { Sparkles } from "lucide-react";
import { SidebarUser } from "@/components/SidebarUser";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { ChatList, NewChatButton } from "@/components/Chat";
import { SearchChatButton } from "@/components/SearchChat";

export const SidebarActions = () => {
  return (
    <div className="mt-4 space-y-2">
      <NewChatButton />
      <SearchChatButton />
    </div>
  );
};

const SidebarLogo = () => {
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

export const SidebarComponent = () => {
    const USER_DATA = {
        user: {
            name: "shadcn",
            email: "m@example.com",
            avatar: "/avatars/shadcn.jpg",
        },
    };

    return (
        <Sidebar variant="inset">
            <SidebarHeader>
                <SidebarLogo />
                <SearchChatButton />
                <NewChatButton />
            </SidebarHeader>
            {/* TODO: implement Chat History Here 
            <SidebarContent>
                <ChatList />
            </SidebarContent> */}
            <SidebarFooter>
                <SidebarUser user={USER_DATA.user} />
            </SidebarFooter>
        </Sidebar>
    );
}
