export interface Conversation {
  id: string;
  title: string;
  created_at: Date;
  updated_at: Date;
}

export interface Message {
  id: string;
  conversation_id: string;
  content: string;
  role: "user" | "assistant";
  created_at: Date;
  updated_at: Date;
}

export interface sidebarNavItem {
  title: string;
  url: string;
  icon: LucideIcon;
}
