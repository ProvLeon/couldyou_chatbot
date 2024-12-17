"use client";
import { useEffect, useRef, useState } from "react";
import { IoSend } from "react-icons/io5"; // Import send icon

interface ChatInputProps {
  onSendMessage: (message: string) => void;
}

export const ChatInput = ({ onSendMessage }: ChatInputProps) => {
  const [message, setMessage] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-grow textarea
  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "inherit";
      const computed = window.getComputedStyle(textarea);
      const height =
        parseInt(computed.getPropertyValue("border-top-width"), 10) +
        parseInt(computed.getPropertyValue("border-bottom-width"), 10) +
        textarea.scrollHeight;

      textarea.style.height = `${Math.min(height, 200)}px`; // Max height of 200px
    }
  };

  useEffect(() => {
    adjustTextareaHeight();
  }, [message]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message.trim());
      setMessage("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex gap-2 p-4 border-t bg-white sticky bottom-0"
    >
      <div className="flex-1 relative">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message... (Shift + Enter for new line)"
          className="w-full px-4 py-2 pr-12 rounded-2xl border border-gray-200
                     focus:outline-none focus:ring-2 focus:ring-purple-400
                     focus:border-transparent resize-none min-h-[44px] max-h-[200px]
                     scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100"
          rows={1}
        />
        <button
          type="submit"
          className="absolute right-2 bottom-1.5 p-2 text-purple-600
                     hover:text-purple-700 transition-colors duration-200
                     disabled:text-gray-400"
          disabled={!message.trim()}
        >
          <IoSend className="w-5 h-5" />
        </button>
      </div>
    </form>
  );
};
