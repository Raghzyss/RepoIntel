"use client";

import { useState, type FormEvent } from "react";

interface LandingProps {
  onAnalyze: (url: string) => void;
}

export function Landing({ onAnalyze }: LandingProps) {
  const [url, setUrl] = useState("");
  const [error, setError] = useState("");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const repositoryUrl = url.trim();

    if (!repositoryUrl) {
      setError("Enter a GitHub repository URL to begin.");
      return;
    }

    setError("");
    onAnalyze(repositoryUrl);
  }

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[#09090b] px-6 py-24 text-white sm:py-32">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_70%_50%_at_50%_0%,rgba(42,90,180,0.14),transparent)]" />
      <div className="absolute inset-x-0 top-0 h-px bg-white/10" />
      <div className="absolute left-1/2 top-1/2 h-[38rem] w-[38rem] -translate-x-1/2 -translate-y-1/2 rounded-full border border-blue-400/[0.06]" />
      <div className="absolute left-1/2 top-1/2 h-[28rem] w-[28rem] -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/[0.035]" />

      <section className="relative w-full max-w-3xl text-center">
        <div className="mb-10 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.045] px-3.5 py-2 text-[11px] font-medium tracking-[0.16em] text-zinc-300 uppercase shadow-[0_1px_0_rgba(255,255,255,0.06)_inset] backdrop-blur-xl">
          <span className="h-1.5 w-1.5 rounded-full bg-blue-400 shadow-[0_0_12px_rgba(96,165,250,0.8)]" />
          Repository Intelligence
        </div>

        <h1 className="text-6xl font-semibold tracking-[-0.065em] text-white sm:text-7xl md:text-8xl">
          RepoIntel
        </h1>

        <p className="mt-7 text-xl font-medium tracking-[-0.025em] text-zinc-200 sm:text-2xl">
          Know the code before you trust it.
        </p>

        <p className="mx-auto mt-5 max-w-2xl text-base leading-7 text-zinc-400 sm:text-lg sm:leading-8">
          Turn any GitHub repository into a clear engineering brief—with
          deterministic analysis of its architecture, code quality,
          dependencies, security posture, and project health.
        </p>

        <form className="mx-auto mt-14 max-w-2xl" onSubmit={handleSubmit} noValidate>
          <label className="sr-only" htmlFor="repository-url">
            GitHub repository URL
          </label>

          <div className="flex flex-col gap-3 rounded-2xl border border-white/10 bg-white/[0.055] p-2.5 shadow-[0_24px_80px_-24px_rgba(0,0,0,0.75),0_1px_0_rgba(255,255,255,0.06)_inset] backdrop-blur-xl sm:flex-row">
            <input
              id="repository-url"
              type="url"
              value={url}
              onChange={(event) => setUrl(event.target.value)}
              placeholder="https://github.com/owner/repository"
              className="min-w-0 flex-1 rounded-xl border border-transparent bg-black/20 px-5 py-4 text-base text-white outline-none placeholder:text-zinc-500 transition focus:border-blue-400/30 focus:bg-black/30 focus:ring-4 focus:ring-blue-400/10"
            />
            <button
              type="submit"
              className="rounded-xl border border-blue-300/20 bg-blue-500 px-6 py-4 text-sm font-semibold text-white shadow-[0_1px_0_rgba(255,255,255,0.22)_inset,0_10px_24px_-10px_rgba(59,130,246,0.7)] transition duration-200 hover:bg-blue-400 hover:shadow-[0_1px_0_rgba(255,255,255,0.26)_inset,0_14px_30px_-10px_rgba(59,130,246,0.8)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-300"
            >
              Analyze Repository
            </button>
          </div>

          {error ? (
            <p className="mt-4 text-left text-sm text-red-300" role="alert">
              {error}
            </p>
          ) : null}
        </form>

        <p className="mt-7 text-sm text-zinc-500">
          Built for engineering teams evaluating what lies beneath the README.
        </p>
      </section>
    </main>
  );
}
