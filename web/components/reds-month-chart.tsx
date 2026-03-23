"use client";

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Card } from "./card";

export function RedsMonthChart({ data }: { data: Array<{ month: string; reds: number }> }) {
  return (
    <Card>
      <h3 className="mb-4 text-sm font-semibold">Reds per month</h3>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="reds" fill="#dc2626" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
