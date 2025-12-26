import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { cn } from "@/lib/utils";
import { NavLink } from "react-router";

interface NavItem {
  title: string;
  url: string;
  isActive?: boolean;
  items?: {
    title: string;
    url: string;
    isActive?: boolean;
  }[];
}

export function NavMain({ items }: { items: NavItem[] }) {
  return (
    <>
      {items.map((item) => (
        <SidebarGroup key={item.title}>
          <SidebarGroupLabel>{item.title}</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {item.items?.map((subItem) => (
                <SidebarMenuItem key={subItem.title}>
                  <SidebarMenuButton
                    asChild
                    isActive={subItem.isActive}
                    className={cn(subItem.isActive ? "font-bold" : "")}
                  >
                    <NavLink
                      to={subItem.url}
                      className={({ isActive }: { isActive: boolean }) =>
                        cn(
                          "flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-sm hover:bg-accent hover:text-accent-foreground",
                          isActive &&
                            "bg-accent text-accent-foreground font-medium"
                        )
                      }
                    >
                      <span className="truncate" title={subItem.title}>
                        {subItem.title}
                      </span>
                      {/* TODO: Implement edit and delete 
                      <div className="absolute right-2 flex items-center gap-0.5">
                        <button
                          onClick={(e) => {
                            e.preventDefault();
                            // Handle edit
                          }}
                          className="p-1 hover:bg-accent rounded-md"
                        >
                          <Pencil className="size-4 text-muted-foreground hover:text-accent-foreground" />
                        </button>
                        <button
                          onClick={(e) => {
                            e.preventDefault();
                            // Handle delete
                          }}
                          className="p-1 hover:bg-accent rounded-md"
                        >
                          <Trash2 className="size-4 text-muted-foreground hover:text-destructive" />
                        </button>
                      </div> */}
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      ))}
    </>
  );
}
