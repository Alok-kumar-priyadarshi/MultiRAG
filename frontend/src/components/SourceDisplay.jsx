import { useState } from "react";

export default function SourceDisplay({ sources }) {
  const [open, setOpen] = useState(false);

  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-2 text-xs text-gray-600">
      <button
        onClick={() => setOpen(!open)}
        className="text-blue-500 underline"
      >
        {open ? "Hide Sources" : "Show Sources"}
      </button>

      {open && (
        <div className="mt-2 space-y-2">
          {sources.map((s, i) => (
            <div
              key={i}
              className="p-2 bg-gray-100 rounded border text-xs"
            >
              {s}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}