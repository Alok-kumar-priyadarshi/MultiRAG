import { useState } from "react";
import ChatBox from "./components/ChatBox";
import InputBar from "./components/InputBar";
import useChat from "./hooks/useChat";
import { resetChat } from "./services/api";
import TypingIndicator from "./components/TypingIndicator";

export default function App() {
  const { messages, send, loading } = useChat();


  return (
    <div className="h-screen flex flex-col bg-gray-900">

      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 bg-gray-800 shadow">
        <h1 className="text-lg font-semibold">RAG Assistant</h1>

        <div className="flex gap-2">

          <button
            onClick={async () => { await resetChat(); window.location.reload(); }}
            className="bg-red-500 text-white px-3 py-1 rounded"
          >
            Reset
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-hidden">
        <ChatBox messages={messages} />
      </div>

      {loading && (
        <TypingIndicator />
      )}

      <InputBar onSend={send} />
    </div>
  );
}