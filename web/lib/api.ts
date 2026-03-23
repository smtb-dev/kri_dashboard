const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    credentials: "include",
    cache: "no-store"
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(body || `Request failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export type DashboardSummary = {
  reds_mtd: number;
  reds_ytd: number;
  ambers_mtd: number;
  ambers_ytd: number;
  total_kris: number;
  last_upload_at: string | null;
  stale: boolean;
  days_since_upload: number | null;
};

export const api = {
  me: () => apiFetch<{ id: number; username: string; role: string }>("/auth/me"),
  login: (username: string, password: string) =>
    apiFetch("/auth/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ username, password }) }),
  summary: () => apiFetch<DashboardSummary>("/dashboard/summary"),
  redsPerMonth: () => apiFetch<Array<{ month: string; reds: number }>>("/dashboard/reds-per-month"),
  topReds: () => apiFetch<Array<{ category: string; sub_category: string; red_count: number }>>("/dashboard/top-reds"),
  listKri: () => apiFetch<Array<{ id: number; category: string; sub_category: string }>>("/kri"),
  observations: (query = "") => apiFetch<Array<{ id: number; kri_definition_id: number; entry_date: string; current_value: number }>>(`/observations${query}`),
  kriDetail: (id: string) => apiFetch(`/kri/${id}`),
  upload: async (file: File) => {
    const form = new FormData();
    form.append("file", file);
    const res = await fetch(`${API_BASE}/uploads`, { method: "POST", body: form, credentials: "include" });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  reportPdf: (month: string) =>
    apiFetch<{ id: string; filename: string }>("/reports/pdf", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ month }) })
};
