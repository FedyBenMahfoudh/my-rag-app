import { DashboardSidebar } from "@/components/dashboard-sidebar";
import MaxWidthWrapper from "@/components/max-width-wrapper";
import React from "react";
import { mockConversations } from "../../data/conversations";
import { UserSidebar } from "@/components/sidebar";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { Separator } from "@/components/ui/separator";
import { ModeToggle } from "@/components/mode-toggle";
import DashboardHeader from "@/components/dashboard-header";
import { createClient } from "@/lib/server";
import { redirect } from "next/navigation";
import { getCurrentUser } from "@/actions/user";

const layout = async ({ children }: { children: React.ReactNode }) => {
  const user = await getCurrentUser();
  if (!user) {
    redirect("/auth/login");
  }
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <DashboardHeader />
        <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
          <main className="bg-background max-h-[calc(100vh-4rem)]">{children}</main>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
};

export default layout;
