import { Outlet, useLocation } from "react-router";
import { AppSidebar } from "@/components/sidebar/app-sidebar";
import { Separator } from "@/components/ui/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { ThemeToggle } from "@/components/theme/theme-toggle";

interface PathIndicatorProps {
  path: string;
}

function PathIndicator({ path }: PathIndicatorProps) {
  return (
    <div className="text-sm text-muted-foreground">Current Path: {path}</div>
  );
}

function MainContent() {
  const location = useLocation();
  return (
    <div className="flex flex-col gap-4">
      <PathIndicator path={location.pathname} />
      <Outlet />
    </div>
  );
}

function AppHeader() {
  return (
    <header className="flex h-16 shrink-0 items-center gap-2">
      <div className="flex items-center gap-2 px-4">
        <SidebarTrigger className="-ml-1" />
        <Separator orientation="vertical" className="mr-2 h-4" />
      </div>
      <div className="flex-1" />
      <div className="px-4">
        <ThemeToggle />
      </div>
    </header>
  );
}

function AppMain() {
  return (
    <main className="p-4">
      <MainContent />
    </main>
  );
}

export function RootLayout() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <AppHeader />
        <AppMain />
      </SidebarInset>
    </SidebarProvider>
  );
}
