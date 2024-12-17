// frontend/app/page.tsx
import { ChatWindow } from "@/components/ChatWindow";
import { ChatProvider } from "@/context/ChatContext";

export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <header className="text-center mb-8">
          <h1 className="text-3xl font-bold text-purple-600 mb-2">
            CouldYou? Cup
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Get answers to your questions about CouldYou? Cup or anything
            related to menstrual health.
          </p>
        </header>
        <ChatProvider>
          <ChatWindow />
        </ChatProvider>
      </div>
    </main>
  );
}
