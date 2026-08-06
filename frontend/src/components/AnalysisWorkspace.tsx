"use client";

import { useState } from "react";

import { analyzeRepository } from "@/lib/api";
import type { AnalysisResponse } from "@/lib/api/types";

import { Dashboard } from "./Dashboard";
import { FindingsPanel } from "./FindingsPanel";
import { Landing } from "./Landing";
import { MetricsSection } from "./MetricsSection";
import { ScoreGrid } from "./ScoreGrid";

type AnalysisStatus = "idle" | "loading" | "success" | "error";

export function AnalysisWorkspace() {
  const [status, setStatus] = useState<AnalysisStatus>("idle");
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState("");
  const [submittedUrl, setSubmittedUrl] = useState("");

  async function handleAnalyze(url: string) {
    setSubmittedUrl(url);
    setStatus("loading");
    setError("");

    try {
      const result = await analyzeRepository(url);
      setAnalysis(result);
      setStatus("success");
    } catch (caughtError) {
      setError(
        caughtError instanceof Error
          ? caughtError.message
          : "Repository analysis could not be completed.",
      );
      setStatus("error");
    }
  }

  if (status === "idle") {
    return <Landing onAnalyze={handleAnalyze} />;
  }

  if (status === "loading") {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#09090b] px-6 text-white">
        <div className="text-center">
          <div className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-white/15 border-t-blue-400" />
          <p className="mt-6 text-lg font-medium">Analyzing repository</p>
          <p className="mt-2 text-sm text-zinc-400">
            Collecting engineering signals. This may take a moment.
          </p>
        </div>
      </main>
    );
  }

  if (status === "error") {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#09090b] px-6 text-white">
        <div className="w-full max-w-md text-center">
          <p className="text-xl font-semibold">Analysis unavailable</p>
          <p className="mt-3 text-sm leading-6 text-zinc-400">{error}</p>
          <button
            type="button"
            onClick={() => handleAnalyze(submittedUrl)}
            className="mt-8 rounded-xl bg-blue-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-300"
          >
            Try again
          </button>
        </div>
      </main>
    );
  }

  if (!analysis) {
    return null;
  }

  return (
    <div className="min-h-screen bg-[#09090b] text-white">
      <Dashboard analysis={analysis} />

      <div className="mx-auto w-full max-w-6xl space-y-14 px-6 pb-20 sm:px-10">
        <section>
          <div className="mb-6">
            <p className="text-xs font-medium tracking-[0.14em] text-blue-300 uppercase">
              Engineering score
            </p>
            <h2 className="mt-2 text-2xl font-semibold tracking-[-0.035em] text-white">
              Domain performance
            </h2>
          </div>
          <ScoreGrid score={analysis.score} />
        </section>

        <section>
          <div className="mb-6">
            <p className="text-xs font-medium tracking-[0.14em] text-blue-300 uppercase">
              Engineering findings
            </p>
            <h2 className="mt-2 text-2xl font-semibold tracking-[-0.035em] text-white">
              What needs attention
            </h2>
          </div>
          <FindingsPanel findings={analysis.findings} />
        </section>

        <section>
          <div className="mb-6">
            <p className="text-xs font-medium tracking-[0.14em] text-blue-300 uppercase">
              Extracted metrics
            </p>
            <h2 className="mt-2 text-2xl font-semibold tracking-[-0.035em] text-white">
              Engineering detail
            </h2>
          </div>
          <MetricsSection repository={analysis.repository} />
        </section>
      </div>
    </div>
  );
}
