
import { useState } from "react";
import { Send } from "lucide-react";
import FileUpload from "./FileUpload";
import UrlInput from "./UrlInput";

export default function InputBar({ onSend }) {
  const [query, setQuery] = useState("");
  const [url, setUrl] = useState("");
  const [file, setFile] = useState(null);

  const handleSubmit = () => {
    if (!query?.trim() && !url && !file) return;

    onSend({ query, url, file });

    setQuery("");
    setUrl("");
    setFile(null);
  };

  return (
    <div className="bg-[#111827] border-t border-gray-700 p-4">

      {/* Main Input */}
      <div className="flex items-center gap-2 bg-[#1e293b] rounded-xl px-3 py-2 border border-gray-600">

        <input
        className="flex-1 bg-transparent outline-none text-sm text-white placeholder-gray-400"
        placeholder="Ask anything..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
            }
        }}
        />

        <button
          onClick={handleSubmit}
          className="bg-blue-600 hover:bg-blue-700 p-2 rounded-lg"
        >
          <Send size={16} />
        </button>
      </div>

      {/* Secondary controls */}
      <div className="flex items-center justify-between mt-2 gap-2">

        <UrlInput url={url} setUrl={setUrl} />

        <FileUpload file={file} setFile={setFile} />

      </div>
    </div>
  );
}