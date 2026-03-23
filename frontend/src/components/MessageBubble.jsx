import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function formatText(text) {
  if (!text || typeof text !== "string") return "";

  return text
    .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")     // bold
    .replace(/\*(.*?)\*/g, "<i>$1</i>")         // italic
    .replace(/^- /gm, "• ")                     // bullet points
    .replace(/\n/g, "<br/>");                  // line breaks
}

export default function MessageBubble({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className="max-w-2xl">

        <div
          className={`px-4 py-3 rounded-2xl text-sm shadow leading-relaxed
          ${isUser
            ? "bg-blue-600 text-white"
            : "bg-[#1e293b] text-gray-100 border border-gray-700"
          }`}
        >
            <div className="markdown">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {message.content}
            </ReactMarkdown>
            </div>
        </div>

        <div className="text-xs text-gray-400 mt-1">
          {message.time}
        </div>
      </div>
    </div>
  );
}