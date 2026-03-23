import "./globals.css";
import Link from "next/link";
import type { ReactNode } from "react";

export const metadata = {
  title: "KRI Dashboard",
  description: "Internal security KRI dashboard demo"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="border-b bg-white">
          <nav className="mx-auto flex max-w-7xl gap-6 px-6 py-4 text-sm font-medium">
            <Link href="/">Overview</Link>
            <Link href="/explorer">KRI Explorer</Link>
            <Link href="/uploads">Uploads</Link>
            <Link href="/reports">Reports</Link>
          </nav>
        </header>
        <main className="mx-auto max-w-7xl px-6 py-6">{children}</main>
      </body>
    </html>
  );
}
