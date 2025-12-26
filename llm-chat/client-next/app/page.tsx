"use client";

import {
  SidebarInset,
  SidebarProvider
} from "@/components/ui/sidebar";
import { SidebarComponent } from '@/components/Sidebar';
import { Header } from '@/components/Header';

export default function Home() {
  return (
    <SidebarProvider>
      <SidebarComponent />
      <SidebarInset>
        <Header />
        <main className="p-4">
          <div className="flex flex-col gap-4">
            <p>Welcome to the AI Chat App! Start a new conversation or search your chat history using the sidebar.</p>
          </div>
        </main>
      </SidebarInset>
    </SidebarProvider>
  );
}
