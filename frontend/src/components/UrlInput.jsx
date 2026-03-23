import { Link } from "lucide-react";

export default function UrlInput({ url, setUrl }) {
  return (
    <div className="flex items-center gap-2 bg-[#1e293b] px-3 py-2 rounded-lg border border-gray-600 flex-1">

      <Link size={14} />

      <input
        className="flex-1 bg-transparent outline-none text-sm text-gray-100 placeholder-gray-400"
        placeholder="Paste URL..."
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
    </div>
  );
}