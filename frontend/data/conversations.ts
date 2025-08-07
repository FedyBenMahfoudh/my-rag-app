import { Conversation } from "@/types";

export const mockConversations: Conversation[] = [
  {
    id: "1",
    title: "Project Discussion",
    created_at: new Date("2024-08-01T10:00:00Z"),
    updated_at: new Date("2024-08-01T12:00:00Z"),
  },
  {
    id: "2",
    title: "AI Research",
    created_at: new Date("2024-08-02T09:30:00Z"),
    updated_at: new Date("2024-08-02T10:15:00Z"),
  },
  {
    id: "3",
    title: "General Chat",
    created_at: new Date("2024-08-03T14:20:00Z"),
    updated_at: new Date("2024-08-03T15:00:00Z"),
  },
];
