"use client";

import { useEffect, useState } from "react";
import { KpiCard } from "@/components/kpi-card";
import { RedsMonthChart } from "@/components/reds-month-chart";
import { StaleBanner } from "@/components/stale-banner";
import { TopRedsTable } from "@/components/top-reds-table";
import { api, DashboardSummary } from "@/lib/api";

export default function OverviewPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [redsPerMonth, setRedsPerMonth] = useState<Array<{ month: string; reds: number }>>([]);
  const [topReds, setTopReds] = useState<Array<{ category: string; sub_category: string; red_count: number }>>([]);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    Promise.all([api.summary(), api.redsPerMonth(), api.topReds()])
      .then(([summaryData, redsData, topData]) => {
        setSummary(summaryData);
        setRedsPerMonth(redsData);
        setTopReds(topData);
      })
      .catch((err: unknown) => setError(String(err)));
  }, []);

  if (error) {
    return <p className="text-sm text-red-700">Failed to load overview data: {error}</p>;
  }
  if (!summary) {
    return <p className="text-sm text-slate-600">Loading overview...</p>;
  }

  return (
    <div className="space-y-6">
      <StaleBanner stale={summary.stale} lastUploadAt={summary.last_upload_at} days={summary.days_since_upload} />
      <section className="grid grid-cols-1 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <KpiCard label="Reds MTD" value={summary.reds_mtd} />
        <KpiCard label="Reds YTD" value={summary.reds_ytd} />
        <KpiCard label="Ambers MTD" value={summary.ambers_mtd} />
        <KpiCard label="Ambers YTD" value={summary.ambers_ytd} />
        <KpiCard label="Total KRIs" value={summary.total_kris} />
        <KpiCard label="Last Upload" value={summary.last_upload_at ? new Date(summary.last_upload_at).toISOString().slice(0, 10) : "N/A"} />
      </section>
      <RedsMonthChart data={redsPerMonth} />
      <TopRedsTable rows={topReds} />
    </div>
  );
}
