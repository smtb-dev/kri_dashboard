import Link from "next/link";
import { Card } from "./card";

type Row = { id?: number; category: string; sub_category: string; red_count: number };

export function TopRedsTable({ rows }: { rows: Row[] }) {
  return (
    <Card>
      <h3 className="mb-4 text-sm font-semibold">Top 10 KRIs by red breach count</h3>
      <table className="w-full text-sm">
        <thead className="text-left text-slate-500">
          <tr>
            <th className="pb-2">Category</th>
            <th className="pb-2">Subcategory</th>
            <th className="pb-2 text-right">Red Count</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr key={`${row.sub_category}-${idx}`} className="border-t">
              <td className="py-2">{row.category}</td>
              <td className="py-2">{row.id ? <Link href={`/kri/${row.id}`}>{row.sub_category}</Link> : row.sub_category}</td>
              <td className="py-2 text-right font-medium">{row.red_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </Card>
  );
}
