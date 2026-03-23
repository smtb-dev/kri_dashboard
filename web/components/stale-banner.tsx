export function StaleBanner({ stale, lastUploadAt, days }: { stale: boolean; lastUploadAt?: string | null; days?: number | null }) {
  if (!stale) return null;
  return (
    <div className="mb-4 rounded-lg border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-800">
      Data is stale: last refreshed on {lastUploadAt ? new Date(lastUploadAt).toISOString().slice(0, 10) : "N/A"} ({days ?? "?"} days ago).
    </div>
  );
}
