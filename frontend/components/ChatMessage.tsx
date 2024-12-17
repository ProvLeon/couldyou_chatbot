"use client";
// import { useState } from 'react';

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { motion } from "framer-motion";

interface ChatMessageProps {
  message: string;
  isUser: boolean;
}

export const ChatMessage = ({ message, isUser }: ChatMessageProps) => {
  // Process and format the message content
  const formatMessage = (content: string) => {
    // Format the message with proper markdown
    return content
      // Format headers
      .replace(/###\s*(.*?)(?:\n|$)/g, "\n## $1\n")
      // Format bullet points
      .replace(/•\s*(.*?)(?:\n|$)/g, "* $1\n")
      // Format links
      .replace(/(?<![\[!])\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>')
      // Add spacing between sections
      .replace(/\n\n/g, "\n\n\n")
      // Format important information
      .replace(/(!important:.*?(?:\n|$))/gi, "> $1\n")
      // Clean up extra spaces
      .trim();
  };

  const messageClasses = `
    max-w-[85%] rounded-2xl px-6 py-4 shadow-md
    ${
    isUser
      ? "bg-purple-600 text-white ml-auto"
      : "bg-white border border-gray-100 mr-auto"
  }
  `;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="mb-6"
    >
      <div className={messageClasses}>
        {isUser
          ? <p className="text-sm leading-relaxed">{message}</p>
          : (
            <div className="prose prose-sm dark:prose-invert max-w-none">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeRaw]}
                components={{
                  h2: ({ children }) => (
                    <div className="mt-6 mb-3">
                      <h2 className="text-xl font-semibold text-purple-600 border-b border-purple-100 pb-2">
                        {children}
                      </h2>
                    </div>
                  ),
                  p: ({ children }) => (
                    <p className="text-gray-700 leading-relaxed mb-4">
                      {children}
                    </p>
                  ),
                  ul: ({ children }) => (
                    <div className="bg-gray-50 rounded-lg p-4 my-4">
                      <ul className="space-y-3">
                        {children}
                      </ul>
                    </div>
                  ),
                  li: ({ children }) => (
                    <li className="flex items-start space-x-3">
                      <span className="text-purple-500 mt-1">•</span>
                      <span className="text-gray-700 flex-1">{children}</span>
                    </li>
                  ),
                  strong: ({ children }) => (
                    <strong className="font-semibold text-purple-600 bg-purple-50 px-1.5 py-0.5 rounded">
                      {children}
                    </strong>
                  ),
                  a: ({ children, href }) => (
                    <a
                      href={href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-purple-600 hover:text-purple-700 underline decoration-2
                             decoration-purple-200 hover:decoration-purple-500 transition-all"
                    >
                      {children}
                    </a>
                  ),
                  blockquote: ({ children }) => (
                    <div className="my-4">
                      <blockquote className="border-l-4 border-purple-300 bg-purple-50 pl-4 py-3
                                         rounded-r-lg italic text-gray-700">
                        {children}
                      </blockquote>
                    </div>
                  ),
                }}
              >
                {formatMessage(message)}
              </ReactMarkdown>
            </div>
          )}
      </div>
    </motion.div>
  );
};
