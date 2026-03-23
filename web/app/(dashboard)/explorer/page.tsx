"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { ColumnDef, flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import { Card } from "@/components/card";
import { Sparkline } from "@/components/sparkline";
import { StaleBanner } from "@/components/stale-banner";
import { api } from "@/lib/api";

type KRI = { id: number; category: string; sub_category: string };
type Obs = { id: number; kri_definition_id: number; entry_date: string; current_value: number };

export default function ExplorerPage() {
  const [kri, setKri] = useState<KRI[]>([]);
  const [obs, setObs] = useState<Obs[]>([]);
  const [summary, setSummary] = useState<{ stale: boolean; last_upload_at: string | null; days_since_upload: number | null } | null>(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    Promise.all([api.listKri(), api.observations(), api.summary()]).then(([kriRows, obsRows, summaryRow]) => {
      setKri(kriRows);
      setObs(obsRows);
      setSummary(summaryRow);
    });
  }, []);

  const byKri = useMemo(() => {
    const map = new Map<number, Obs[]>();
    for (const row of obs) {
      const arr = map.get(row.kri_definition_id) ?? [];
      arr.push(row);
      map.set(row.kri_definition_id, arr);
    }
    return map;
  }, [obs]);

  const rows = kri.filter((k) => k.sub_category.toLowerCase().includes(search.toLowerCase()) || k.category.toLowerCase().includes(search.toLowerCase()));

  const columns = useMemo<ColumnDef<KRI>[]>(
    () => [
      { accessorKey: "category", header: "Category" },
      {
        accessorKey: "sub_category",
        header: "Subcategory",
        cell: (info) => <Link href={`/kri/${info.row.original.id}`}>{String(info.getValue())}</Link>
      },
      {
        id: "sparkline",
        header: "Sparkline",
        cell: (info) => {
          const series = (byKri.get(info.row.original.id) ?? []).slice(0, 14).map((x) => x.current_value);
          return <Sparkline values={series.length > 0 ? series : [0]} />;
        }
      }
    ],
    [byKri]
  );

  const table = useReactTable({ data: rows, columns, getCoreRowModel: getCoreRowModel() });

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">KRI Explorer</h1>
      {summary ? <StaleBanner stale={summary.stale} lastUploadAt={summary.last_upload_at} days={summary.days_since_upload} /> : null}
      <Card>
        <input
          className="w-full rounded border px-3 py-2 text-sm"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search category or subcategory"
        />
      </Card>
      <Card>
        <table className="w-full text-sm">
          <thead className="text-left text-slate-500">
            {table.getHeaderGroups().map((hg) => (
              <tr key={hg.id}>
                {hg.headers.map((h) => (
                  <th key={h.id}>{flexRender(h.column.columnDef.header, h.getContext())}</th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr className="border-t" key={row.id}>
                {row.getVisibleCells().map((cell) => (
                  <td className="py-2" key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
