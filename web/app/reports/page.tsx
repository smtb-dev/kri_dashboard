"use client";

import { useState } from "react";
import { Card } from "@/components/card";
import { api } from "@/lib/api";

export default function ReportsPage() {
  const [month, setMonth] = useState("2025-12");
  const [pdfId, setPdfId] = useState("");

  const generatePdf = async () => {
    const result = await api.reportPdf(month);
    setPdfId(result.id);
  };

  const excelUrl = `${process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api"}/exports/excel`;

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Reports</h1>
      <Card>
        <div className="flex items-end gap-3">
          <div>
            <p className="mb-1 text-sm">Monthly PDF</p>
            <input className="rounded border px-3 py-2" value={month} onChange={(e) => setMonth(e.target.value)} />
          </div>
          <button className="rounded bg-slate-900 px-4 py-2 text-white" onClick={generatePdf}>
            Generate
          </button>
          {pdfId ? (
            <a className="text-sky-700 underline" href={`${process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api"}/reports/${pdfId}/download`}>
              Download PDF
            </a>
          ) : null}
        </div>
      </Card>
      <Card>
        <p className="mb-2 text-sm font-semibold">Excel Export</p>
        <a className="text-sky-700 underline" href={excelUrl}>
          Download current export
        </a>
      </Card>
    </div>
  );
}
