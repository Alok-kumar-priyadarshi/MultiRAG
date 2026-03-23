import { useState } from "react";
import { sendMessage } from "../services/api";

export default function useChat() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const session_id = "session-" + Date.now();

  const now = new Date().toLocaleTimeString();

//   const send = async ({ query, url, file }) => {
//     setLoading(true);

//     setMessages((prev) => [
//       ...prev,
//       { role: "user", content: query }
//     ]);

//     try {
//       const data = await sendMessage({ query, url, file, session_id });

//       setMessages((prev) => [
//         ...prev,
//         {
//           role: "assistant",
//           content: data.answer || "No response from server",
//           sources: data.sources || [],
//           time:now
//         }
//       ]);
//     } catch (err) {
//       console.error(err);
//     }

//     setLoading(false);
//   };

    const send = async ({ query, url, file }) => {
    if (!query?.trim() && !url && !file) return;

    setLoading(true);

    const now = new Date().toLocaleTimeString();

    // 🟢 Add user message
    setMessages((prev) => [
        ...prev,
        { role: "user", content: query, time: now }
    ]);

    // 🟡 Add EMPTY assistant message
    let assistantIndex;

    setMessages((prev) => {
        assistantIndex = prev.length + 1;
        return [
        ...prev,
        { role: "assistant", content: "", sources: [], time: now }
        ];
    });

    try {
        const data = await sendMessage({ query, url, file, session_id });

        const fullText = data?.answer || "No response from server";

        // 🔥 STREAMING EFFECT
        let i = 0;

        const interval = setInterval(() => {
        i++;

        setMessages((prev) => {
            const updated = [...prev];

            updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            content: fullText.slice(0, i),
            sources: data.sources || []
            };

            return updated;
        });

        if (i >= fullText.length) {
            clearInterval(interval);
        }
        }, 10); // speed (lower = faster)

    } catch (err) {
        console.error(err);
    }

    setLoading(false);
    };
  return { messages, send, loading };
}