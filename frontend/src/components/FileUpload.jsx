// import { Upload } from "lucide-react";

// export default function FileUpload({ setFile }) {
//   return (
//     <label className="flex items-center gap-2 cursor-pointer text-sm">
//       <Upload size={16} />
//       Upload PDF
//       <input
//         type="file"
//         hidden
//         onChange={(e) => setFile(e.target.files[0])}
//       />
//     </label>
//   );
// }

import { Upload, X } from "lucide-react";

export default function FileUpload({ file, setFile }) {
  return (
    <div className="flex items-center gap-2 text-sm">

      {/* Upload Button */}
      <label className="flex items-center gap-2 cursor-pointer bg-[#1e293b] px-3 py-2 rounded-lg border border-gray-600 hover:bg-[#334155] transition">
        <Upload size={16} />
        Upload PDF
        <input
          type="file"
          hidden
          onChange={(e) => setFile(e.target.files[0])}
        />
      </label>

      {/* Show file name */}
      {file && (
        <div className="flex items-center gap-2 bg-[#0f172a] px-2 py-1 rounded border border-gray-700">
          <span className="truncate max-w-120px">{file.name}</span>

          {/* Remove button */}
          <button onClick={() => setFile(null)}>
            <X size={14} />
          </button>
        </div>
      )}
    </div>
  );
}

