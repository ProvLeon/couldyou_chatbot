"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { motion } from "framer-motion";
import { IoMdCopy } from "react-icons/io";
import { MdDone } from "react-icons/md";
import { format } from "date-fns";
import { FaRobot, FaUser } from "react-icons/fa"; // Import user and bot icons

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp?: Date;
  avatar?: string;
  username?: string;
}

export const ChatMessage = ({
  message,
  isUser,
  timestamp = new Date(),
  username = isUser ? "You" : "Assistant",
}: ChatMessageProps) => {
  const [isCopied, setIsCopied] = useState(false);

  // Copy message to clipboard
  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(message);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy text: ", err);
    }
  };

  const formatMessage = (content: string) => {
    return content
      .replace(/###\s*(.*?)(?:\n|$)/g, "\n## $1\n")
      .replace(/•\s*(.*?)(?:\n|$)/g, "* $1\n")
      .replace(/(?<![\[!])\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>')
      .replace(/\n\n/g, "\n\n\n")
      .replace(/(!important:.*?(?:\n|$))/gi, "> $1\n")
      .replace(
        /`{3}(\w+)?\n([\s\S]*?)\n`{3}/g,
        '<pre><code class="language-$1">$2</code></pre>',
      )
      .trim();
  };

  const messageClasses = `
    max-w-[90%] sm:max-w-[85%] rounded-2xl px-4 sm:px-6 py-3 sm:py-4 shadow-md
    ${
    isUser
      ? "bg-purple-600 text-white ml-auto rounded-tr-none"
      : "bg-white border border-gray-100 mr-auto rounded-tl-none"
  }
  `;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="mb-6 relative group"
    >
      {/* Message Header with Avatar and Timestamp */}
      <div
        className={`flex items-center gap-2 mb-2 ${
          isUser ? "justify-end" : "justify-start"
        }`}
      >
        <div
          className={`w-6 h-6 rounded-full flex items-center justify-center
                  ${isUser ? "bg-purple-100" : "bg-gray-100"}`}
        >
          {isUser
            ? <FaUser className="w-3 h-3 text-purple-600" />
            : <FaRobot className="w-3 h-3 text-gray-600" />}
        </div>
        <span className="text-xs text-gray-500">{username}</span>
        <span className="text-xs text-gray-400">
          {format(timestamp, "HH:mm")}
        </span>
      </div>

      <div className={messageClasses}>
        {/* Copy Button */}
        <button
          onClick={copyToClipboard}
          className={`
            absolute top-2 right-2 opacity-0 group-hover:opacity-100
            transition-opacity duration-200 p-2 rounded-full
            ${
            isUser
              ? "bg-purple-700 hover:bg-purple-800"
              : "bg-gray-100 hover:bg-gray-200"
          }
          `}
          title="Copy message"
        >
          {isCopied
            ? (
              <MdDone
                className={`w-4 h-4 ${
                  isUser ? "text-white" : "text-green-600"
                }`}
              />
            )
            : (
              <IoMdCopy
                className={`w-4 h-4 ${isUser ? "text-white" : "text-gray-600"}`}
              />
            )}
        </button>

        {/* Message Content */}
        {isUser
          ? <p className="text-xs md:text-sm leading-relaxed pr-8">{message}</p>
          : (
            <div className="prose prose-sm dark:prose-invert max-w-none">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeRaw]}
                components={{
                  h2: ({ children }) => (
                    <div className="mt-4 mb-2">
                      <h2 className="text-md md:text-lg font-semibold text-purple-600 border-b border-purple-100 pb-2">
                        {children}
                      </h2>
                    </div>
                  ),
                  p: ({ children }) => (
                    <p className="text-gray-700 text-sm md:text-base leading-relaxed mb-3">
                      {children}
                    </p>
                  ),
                  ul: ({ children }) => (
                    <div className="bg-gray-50 rounded-lg p-3 my-3">
                      <ul className="space-y-2">{children}</ul>
                    </div>
                  ),
                  li: ({ children }) => (
                    <li className="flex items-start space-x-2 text-sm">
                      <span className="text-purple-500 mt-1">•</span>
                      <span className="text-gray-700 flex-1">{children}</span>
                    </li>
                  ),
                  code: ({ inline, className, children, ...props }) => (
                    <code
                      className={`${className} ${
                        inline
                          ? "bg-gray-100 rounded px-1 py-0.5"
                          : "block bg-gray-800 text-white p-4 rounded-lg overflow-x-auto"
                      }`}
                      {...props}
                    >
                      {children}
                    </code>
                  ),
                  strong: ({ children }) => (
                    <strong className="text-sm md:text-base font-semibold text-purple-600 bg-purple-50 px-1.5 py-0.5 rounded">
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
