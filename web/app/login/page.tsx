"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { Card } from "@/components/card";
import { api } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin123");
  const [error, setError] = useState("");

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await api.login(username, password);
      router.push("/overview");
    } catch (err) {
      setError(String(err));
    }
  };

  return (
    <div className="mx-auto max-w-md py-16">
      <Card>
        <h1 className="mb-4 text-xl font-semibold">KRI Dashboard Login</h1>
        <form className="space-y-3" onSubmit={onSubmit}>
          <input className="w-full rounded border px-3 py-2" value={username} onChange={(e) => setUsername(e.target.value)} />
          <input className="w-full rounded border px-3 py-2" value={password} type="password" onChange={(e) => setPassword(e.target.value)} />
          <button className="w-full rounded bg-slate-900 px-4 py-2 text-white" type="submit">
            Sign in
          </button>
          {error ? <p className="text-sm text-red-700">{error}</p> : null}
        </form>
      </Card>
    </div>
  );
}
