"use client";

import { ChatMessage } from "@/components/chat-message";
import { ChatInput } from "@/components/chat-panel";
import { Icons } from "@/components/icons";
import { Separator } from "@/components/ui/separator";
import { Icon } from "lucide-react";
import { useState, useRef, useEffect } from "react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
}

const mockConversations: Conversation[] = [
  {
    id: "1",
    title: "React Best Practices",
    messages: [
      {
        id: "1",
        role: "user",
        content: "What are the best practices for React development?",
        timestamp: new Date("2024-01-15T10:00:00"),
      },
      {
        id: "2",
        role: "assistant",
        content:
          "<think>lorem ipsum</think>Here are some key React best practices:\n\n1. **Use Functional Components**: Prefer functional components with hooks over class components\n2. **Component Composition**: Break down complex components into smaller, reusable pieces\n3. **Props Validation**: Use TypeScript or PropTypes for type checking\n4. **State Management**: Keep state as close to where it's used as possible\n5. **Performance**: Use React.memo, useMemo, and useCallback when needed\n6. **Error Boundaries**: Implement error boundaries to gracefully handle errors\n7. **Testing**: Write unit tests for your components",
        timestamp: new Date("2024-01-15T10:00:30"),
      },
      {
        id: "1",
        role: "user",
        content: "What are the best practices for React development?",
        timestamp: new Date("2024-01-15T10:00:00"),
      },
      {
        id: "2",
        role: "assistant",
        content: `Here are some key React best practices:

1. **Use Functional Components**: Prefer functional components with hooks over class components  
2. **Component Composition**: Break down complex components into smaller, reusable pieces  
3. **Props Validation**: Use TypeScript or PropTypes for type checking  
4. **State Management**: Keep state as close to where it's used as possible  
5. **Performance**: Use React.memo, useMemo, and useCallback when needed  
6. **Error Boundaries**: Implement error boundaries to gracefully handle errors  
7. **Testing**: Write unit tests for your components

Here's an example of a functional component with hooks:

\`\`\`tsx
import { useState, useCallback } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  const increment = useCallback(() => {
    setCount((prev) => prev + 1);
  }, []);

  return (
    <button onClick={increment}>
      Count: {count}
    </button>
  );
}
\`\`\`
`,
        timestamp: new Date("2024-01-15T10:00:30"),
      },
      {
        id: "2",
        role: "assistant",
        content:
          "Here are some key React best practices:\n\n1. **Use Functional Components**: Prefer functional components with hooks over class components\n2. **Component Composition**: Break down complex components into smaller, reusable pieces\n3. **Props Validation**: Use TypeScript or PropTypes for type checking\n4. **State Management**: Keep state as close to where it's used as possible\n5. **Performance**: Use React.memo, useMemo, and useCallback when needed\n6. **Error Boundaries**: Implement error boundaries to gracefully handle errors\n7. **Testing**: Write unit tests for your components",
        timestamp: new Date("2024-01-15T10:00:30"),
      },
    ],
    createdAt: new Date("2024-01-15T10:00:00"),
  },
];

export default function ChatUI() {
  const [conversations, setConversations] =
    useState<Conversation[]>(mockConversations);
  const [activeConversationId, setActiveConversationId] = useState<string>("1");
  const [inputMessage, setInputMessage] = useState("");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const activeConversation = conversations.find(
    (conv) => conv.id === activeConversationId
  );

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [activeConversation?.messages]);

  const adjustTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        200
      )}px`;
    }
  };

  useEffect(() => {
    adjustTextareaHeight();
  }, [inputMessage]);

  const handleSendMessage = () => {
    if (!inputMessage.trim() || !activeConversation) return;

    const newUserMessage: Message = {
      id: Date.now().toString() + "-user",
      role: "user",
      content: inputMessage.trim(),
      timestamp: new Date(),
    };

    const newAssistantMessage: Message = {
      id: Date.now().toString() + "-assistant",
      role: "assistant",
      content: `I received your message: "${inputMessage.trim()}". This is a mock response from the assistant. In a real implementation, this would be connected to an AI service.`,
      timestamp: new Date(),
    };

    setConversations((prev) =>
      prev.map((conv) =>
        conv.id === activeConversationId
          ? {
              ...conv,
              messages: [...conv.messages, newUserMessage, newAssistantMessage],
            }
          : conv
      )
    );

    setInputMessage("");
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const createNewConversation = () => {
    const newConversation: Conversation = {
      id: Date.now().toString(),
      title: "New Conversation",
      messages: [],
      createdAt: new Date(),
    };

    setConversations((prev) => [newConversation, ...prev]);
    setActiveConversationId(newConversation.id);
    setIsSidebarOpen(false);
  };

  const formatTime = (date: Date) => {
    return new Intl.DateTimeFormat("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  };

  return (
    <div className="flex-1 flex flex-col min-w-0 h-[89vh]">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-full mx-auto space-y-6">
          {activeConversation?.messages.length === 0 ? (
            <div className="text-center text-gray-500 mt-20 flex flex-col items-center">
              <Icons.messageCircle size={50} className="text-blue-600" />
              <h2 className="text-2xl font-medium mb-2">
                Start a conversation
              </h2>
              <p>Type a message below to get started.</p>
            </div>
          ) : (
            activeConversation?.messages.map((message, index) => (
              //   <div
              //     key={message.id}
              //     className={`flex ${
              //       message.role === "user" ? "justify-end" : "justify-start"
              //     }`}
              //   >
              //     <div
              //       className={`max-w-[80%] rounded-lg px-4 py-3 ${
              //         message.role === "user"
              //           ? "bg-blue-600 text-white ml-auto"
              //           : "bg-accent border text-white"
              //       }`}
              //     >
              //       <div className="whitespace-pre-wrap break-words">
              //         {message.content}
              //       </div>
              //       <div
              //         className={`text-xs mt-2 ${
              //           message.role === "user"
              //             ? "text-blue-100"
              //             : "text-gray-500"
              //         }`}
              //       >
              //         {formatTime(message.timestamp)}
              //       </div>
              //     </div>
              //   </div>
              <div key={index}>
                <ChatMessage message={message} />
                {index < activeConversation?.messages.length - 1 && (
                  <Separator className="my-4 md:my-8" />
                )}
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <ChatInput
        onSendMessage={handleSendMessage}
        isLoading={false}
        placeholder="Message ChatGPT..."
      />
    </div>
  );
}
