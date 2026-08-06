"use client";

import { motion } from "framer-motion";
import { Braces, FileText, GitBranch, Layers3, Sparkles } from "lucide-react";

import type { AnalysisResponse } from "@/lib/api/types";

interface DashboardProps {
  analysis: AnalysisResponse;
}

export function Dashboard({ analysis }: DashboardProps) {
  const { repository, classification, score } = analysis;
  const languages = Object.entries(repository.languages);
  const technologies = Object.values(repository.technology_stack).flat();

  return (
    <main className="relative min-h-screen overflow-hidden bg-[#09090b] px-6 py-10 text-white sm:px-10 sm:py-14">
      <div className="absolute inset-x-0 top-0 h-px bg-white/10" />
      <div className="absolute inset-x-0 top-0 h-[32rem] bg-[radial-gradient(ellipse_65%_55%_at_50%_0%,rgba(42,90,180,0.14),transparent)]" />

      <motion.section
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, ease: "easeOut" }}
        className="relative mx-auto w-full max-w-6xl"
      >
        <div className="flex flex-col justify-between gap-10 lg:flex-row lg:items-end">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.045] px-3.5 py-2 text-[11px] font-medium tracking-[0.16em] text-zinc-300 uppercase shadow-[0_1px_0_rgba(255,255,255,0.06)_inset] backdrop-blur-xl">
              <Sparkles className="size-3.5 text-blue-300" />
              Engineering analysis
            </div>

            <div className="mt-7 flex items-center gap-2 text-sm text-zinc-400">
              <GitBranch className="size-4" />
              <span>{repository.owner}</span>
              <span className="text-zinc-700">/</span>
              <span>{repository.name}</span>
            </div>

            <h1 className="mt-3 text-4xl font-semibold tracking-[-0.05em] text-white sm:text-6xl">
              {repository.name}
            </h1>
            <p className="mt-5 max-w-2xl text-base leading-7 text-zinc-400 sm:text-lg sm:leading-8">
              {classification.repository_purpose}
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.045] px-7 py-6 shadow-[0_1px_0_rgba(255,255,255,0.06)_inset] backdrop-blur-xl">
            <p className="text-xs font-medium tracking-[0.14em] text-zinc-400 uppercase">
              Engineering score
            </p>
            <p className="mt-2 text-5xl font-semibold tracking-[-0.06em] text-white">
              {score.overall_score}
              <span className="ml-1 text-lg font-medium tracking-normal text-zinc-500">
                /100
              </span>
            </p>
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.1, ease: "easeOut" }}
          className="mt-10 grid gap-4 border-y border-white/10 py-6 sm:grid-cols-2 lg:grid-cols-4"
        >
          <div>
            <p className="text-xs font-medium tracking-[0.12em] text-zinc-500 uppercase">
              Primary category
            </p>
            <p className="mt-2 text-sm font-medium text-zinc-100">
              {classification.primary_category}
            </p>
          </div>
          <div>
            <p className="text-xs font-medium tracking-[0.12em] text-zinc-500 uppercase">
              Confidence
            </p>
            <p className="mt-2 text-sm font-medium text-zinc-100">
              {classification.confidence}%
            </p>
          </div>
          <div className="flex gap-3">
            <FileText className="mt-0.5 size-4 shrink-0 text-blue-300" />
            <div>
              <p className="text-xs font-medium tracking-[0.12em] text-zinc-500 uppercase">
                Total files
              </p>
              <p className="mt-2 text-sm font-medium text-zinc-100">
                {repository.total_files.toLocaleString()}
              </p>
            </div>
          </div>
          <div className="flex gap-3">
            <Braces className="mt-0.5 size-4 shrink-0 text-blue-300" />
            <div>
              <p className="text-xs font-medium tracking-[0.12em] text-zinc-500 uppercase">
                Total lines
              </p>
              <p className="mt-2 text-sm font-medium text-zinc-100">
                {repository.total_lines.toLocaleString()}
              </p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.18, ease: "easeOut" }}
          className="mt-8 grid gap-5 lg:grid-cols-2"
        >
          <section className="rounded-2xl border border-white/10 bg-white/[0.035] p-6 shadow-[0_1px_0_rgba(255,255,255,0.05)_inset] backdrop-blur-xl">
            <div className="flex items-center gap-2 text-sm font-medium text-zinc-200">
              <Braces className="size-4 text-blue-300" />
              Languages
            </div>
            <div className="mt-5 flex flex-wrap gap-2">
              {languages.map(([language, count]) => (
                <span
                  key={language}
                  className="rounded-lg border border-white/10 bg-black/20 px-3 py-1.5 text-sm text-zinc-300"
                >
                  {language}
                  <span className="ml-2 text-zinc-500">{count}</span>
                </span>
              ))}
            </div>
          </section>

          <section className="rounded-2xl border border-white/10 bg-white/[0.035] p-6 shadow-[0_1px_0_rgba(255,255,255,0.05)_inset] backdrop-blur-xl">
            <div className="flex items-center gap-2 text-sm font-medium text-zinc-200">
              <Layers3 className="size-4 text-blue-300" />
              Technology stack
            </div>
            <div className="mt-5 flex flex-wrap gap-2">
              {technologies.map((technology) => (
                <span
                  key={technology}
                  className="rounded-lg border border-blue-300/15 bg-blue-400/[0.07] px-3 py-1.5 text-sm text-blue-100"
                >
                  {technology}
                </span>
              ))}
            </div>
          </section>
        </motion.div>
      </motion.section>
    </main>
  );
}
