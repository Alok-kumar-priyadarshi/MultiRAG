import MessageBubble from "./MessageBubble";
import SourceDisplay from "./SourceDisplay";
import { useEffect, useRef } from "react";

export default function ChatBox({ messages }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    const el = bottomRef.current;
    if (!el) return;

    el.scrollIntoView({ behavior: "smooth" });

    const parent = el.parentElement;
    if (parent) {
      parent.scrollTop = parent.scrollHeight;
    }
  }, [messages.length, messages[messages.length - 1]?.content]);

  return (
    <div className="flex-1 h-full overflow-y-auto p-6 space-y-4 bg-[#0f172a]">

      {messages.map((msg, i) => (
        <div key={i}>
          <MessageBubble message={msg} />
          {msg.role !== "user" && (
            <SourceDisplay sources={msg.sources} />
          )}
        </div>
      ))}

      <div ref={bottomRef} />
    </div>
  );
}