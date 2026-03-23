"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card } from "@/components/card";
import { Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "@/lib/api";

export default function KriDetailPage() {
  const params = useParams<{ id: string }>();
  const id = params.id;
  const [detail, setDetail] = useState<any>(null);
  const [data, setData] = useState<Array<{ date: string; value: number }>>([]);

  useEffect(() => {
    Promise.all([api.kriDetail(id), api.observations(`?kri_id=${id}`)]).then(([detailData, obs]) => {
      setDetail(detailData);
      setData(obs.slice(0, 180).map((o) => ({ date: o.entry_date, value: o.current_value })));
    });
  }, [id]);

  if (!detail) return <p>Loading...</p>;

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">{detail.kri.sub_category}</h1>
      <Card>
        <h2 className="mb-3 text-sm font-semibold">Time series with thresholds</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line dataKey="value" stroke="#0f766e" dot={false} />
              {detail.threshold?.amber_value != null ? <ReferenceLine y={detail.threshold.amber_value} stroke="#f59e0b" /> : null}
              {detail.threshold?.red_value != null ? <ReferenceLine y={detail.threshold.red_value} stroke="#dc2626" /> : null}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </Card>
      <Card>
        <h2 className="mb-3 text-sm font-semibold">Threshold details</h2>
        <pre className="overflow-x-auto text-xs">{JSON.stringify(detail.threshold, null, 2)}</pre>
      </Card>
      <Card>
        <h2 className="mb-3 text-sm font-semibold">Breach log</h2>
        <table className="w-full text-sm">
          <thead>
            <tr>
              <th className="text-left">Date</th>
              <th className="text-left">Severity</th>
              <th className="text-left">Value</th>
              <th className="text-left">Threshold Version</th>
            </tr>
          </thead>
          <tbody>
            {detail.breaches.map((b: any) => (
              <tr key={b.id} className="border-t">
                <td className="py-2">{b.entry_date}</td>
                <td className="py-2">{b.severity}</td>
                <td className="py-2">{b.current_value}</td>
                <td className="py-2">{b.threshold_version}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
