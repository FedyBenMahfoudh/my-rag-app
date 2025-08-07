import { sidebarNavItem } from "@/types";


export const siteConfig = {
  name: "My RAG",
  description: "A simple RAG application",
  url: "https://my-rag.example.com",
  ogImage: "https://my-rag.example.com/og-image.png",
  links: {
    twitter: "https://twitter.com/my_rag",
    github: "https://github.com/my_rag"
  }
}

export const SidebarNavMain: sidebarNavItem[] = [
  {
    title: "New Chat",
    url: "#",
    icon: "filePenLine", // just a string key
  },
  {
    title: "Search Chats",
    url: "#",
    icon: "search", // just a string key
  },
];
