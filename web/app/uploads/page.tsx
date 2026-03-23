"use client";

import { useState } from "react";
import { Card } from "@/components/card";
import { api } from "@/lib/api";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string>("");

  const onUpload = async () => {
    if (!file) return;
    try {
      const result = await api.upload(file);
      setMessage(`Uploaded ${result.filename} (${result.row_count} rows). Thresholds and breaches recomputed.`);
    } catch (err) {
      setMessage(String(err));
    }
  };

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Upload Daily CSV</h1>
      <Card>
        <div className="space-y-3">
          <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
          <button className="rounded bg-sky-700 px-4 py-2 text-white" onClick={onUpload}>
            Upload
          </button>
          <p className="text-sm text-slate-600">{message}</p>
        </div>
      </Card>
    </div>
  );
}
