"use client";
// frontend/components/ChatWindow.tsx
import { useCallback, useEffect, useRef } from "react";
import { useChat } from "@/context/ChatContext";
import { v4 as uuidv4 } from "uuid";
// import { LanguageSelector } from "./LanguageSelector";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { TypingIndicator } from "./TypingIndicator";

// interface ChatError extends Error {
//   status?: number;
//   code?: string;
// }
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL ||
  "http://localhost:5000";

export const ChatWindow = () => {
  const { state, dispatch } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [state.messages]);

  const handleSendMessage = useCallback(async (text: string) => {
    dispatch({
      type: "ADD_MESSAGE",
      payload: {
        id: uuidv4(),
        text,
        isUser: true,
        timestamp: new Date(),
      },
    });

    dispatch({ type: "SET_TYPING", payload: true });

    try {
      const response = await fetch(`${BACKEND_URL}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text, language: state.language }),
        credentials: "include", // Include this if using cookies
        mode: "cors", // Explicitly set CORS mode
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      dispatch({
        type: "ADD_MESSAGE",
        payload: {
          id: uuidv4(),
          text: data.response.text,
          isUser: false,
          timestamp: new Date(),
        },
      });
    } catch (error: unknown) {
      let errorMessage = "Failed to send message. Please try again.";

      if (error instanceof Error) {
        errorMessage = `${errorMessage} ${error.message}`;
      } else if (typeof error === "string") {
        errorMessage = `${errorMessage} ${error}`;
      }

      dispatch({
        type: "SET_ERROR",
        payload: errorMessage,
      });
    } finally {
      dispatch({ type: "SET_TYPING", payload: false });
    }
  }, [dispatch, state.language]);

  return (
    <div className="chat-window">
      <div className="flex flex-col h-[700px] w-full max-w-3xl mx-auto bg-white rounded-xl shadow-xl">
        <div className="flex items-center justify-between p-4 border-b dark:border-gray-700">
          <div className="flex items-center space-x-3">
            <div className="w-3 h-3 bg-purple-500 rounded-full animate-pulse" />
            <h2 className="text-xl font-semibold text-purple-500">
              CouldYou? Cup Health Assistant
            </h2>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {state.messages.map((message, index) => (
            <div
              key={message.id}
              className="message-animation"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <ChatMessage
                message={message.text}
                isUser={message.isUser}
              />
            </div>
          ))}
          {state.isTyping && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>

        <ChatInput onSendMessage={handleSendMessage} />
      </div>
    </div>
  );
};
