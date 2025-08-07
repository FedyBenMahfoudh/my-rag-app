"use client";

import { ChevronRight, type LucideIcon } from "lucide-react";

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/components/ui/sidebar";
import { sidebarNavItem } from "@/types";
import { Icons } from "./icons";

export function NavMain({ items }: { items: sidebarNavItem[] }) {
  const iconMap = {
    filePenLine: Icons.filePenLine,
    search: Icons.search,
    // add other icons as needed
  };

  return (
    <SidebarGroup>
      <SidebarGroupLabel> Features </SidebarGroupLabel>
      <SidebarMenu>
        {items.map((item) => {
          const Icon = iconMap[item.icon as keyof typeof iconMap];
          return (
            <SidebarMenuItem key={item.title}>
              <SidebarMenuButton tooltip={item.title}>
                {item.icon && <Icon />}
                <span>{item.title}</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
          );
        })}
      </SidebarMenu>
    </SidebarGroup>
  );
}
