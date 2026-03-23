import type { ReactNode } from "react";

export function Card({ children }: { children: ReactNode }) {
  return <div className="rounded-xl border bg-white p-4 shadow-sm">{children}</div>;
}
