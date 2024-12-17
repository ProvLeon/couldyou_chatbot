// frontend/utils/types.ts
export interface ChatMessage {
  text: string;
  isUser: boolean;
  timestamp: number;
}

export interface ChatSession {
  id: string;
  messages: ChatMessage[];
}
