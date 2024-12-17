// frontend/components/TypingIndicator.tsx
export const TypingIndicator = () => {
  return (
    <div className="flex items-center space-x-2 p-4">
      <div className="flex space-x-1">
        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100">
        </div>
        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200">
        </div>
      </div>
      <span className="text-sm text-gray-500">Assistant is typing...</span>
    </div>
  );
};
