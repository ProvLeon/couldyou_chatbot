"use client";
// frontend/context/ChatContext.tsx
import { createContext, ReactNode, useContext, useReducer } from "react";

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

interface ChatState {
  messages: Message[];
  isTyping: boolean;
  error: string | null;
  language: string;
}

type ChatAction =
  | { type: "ADD_MESSAGE"; payload: Message }
  | { type: "SET_TYPING"; payload: boolean }
  | { type: "SET_ERROR"; payload: string | null }
  | { type: "SET_LANGUAGE"; payload: string }
  | { type: "CLEAR_CHAT" };

const ChatContext = createContext<
  {
    state: ChatState;
    dispatch: React.Dispatch<ChatAction>;
  } | null
>(null);

const initialState: ChatState = {
  messages: [
    {
      id: "1",
      text:
        "Hello! I'm here to help answer your questions about menstrual health and period poverty. How can I assist you today?",
      isUser: false,
      timestamp: new Date(),
    },
  ],
  isTyping: false,
  error: null,
  language: "en",
};

function chatReducer(state: ChatState, action: ChatAction): ChatState {
  switch (action.type) {
    case "ADD_MESSAGE":
      return {
        ...state,
        messages: [...state.messages, action.payload],
      };
    case "SET_TYPING":
      return {
        ...state,
        isTyping: action.payload,
      };
    case "SET_ERROR":
      return {
        ...state,
        error: action.payload,
      };
    case "SET_LANGUAGE":
      return {
        ...state,
        language: action.payload,
      };
    case "CLEAR_CHAT":
      return {
        ...initialState,
        language: state.language,
      };
    default:
      return state;
  }
}

export function ChatProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  return (
    <ChatContext.Provider value={{ state, dispatch }}>
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error("useChat must be used within a ChatProvider");
  }
  return context;
}
