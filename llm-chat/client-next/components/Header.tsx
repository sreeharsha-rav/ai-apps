import { Separator } from "@/components/ui/separator";
import { SidebarTrigger } from '@/components/ui/sidebar';
import { ThemeToggle } from "@/components/ThemeToggle";

export const Header = () => {
  return (
    <header className="flex h-16 shrink-0 items-center gap-2">
      <div className="flex items-center gap-2 px-4">
        <SidebarTrigger />
        <Separator orientation="vertical" className="mr-2 h-4" />
      </div>
      <div className="flex-1" />
      <div className="px-4">
        <ThemeToggle />
      </div>
    </header>
  );
}
