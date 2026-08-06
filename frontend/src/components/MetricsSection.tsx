"use client";

import { useState, type ReactNode } from "react";
import { AnimatePresence, motion } from "framer-motion";
import {
  BookOpen,
  Braces,
  ChevronDown,
  FolderTree,
  HeartPulse,
  Package,
  ShieldCheck,
} from "lucide-react";

import type { RepositoryResponse } from "@/lib/api/types";

interface MetricsSectionProps {
  repository: RepositoryResponse;
}

type MetricRecord = Record<string, unknown>;

function formatLabel(key: string) {
  return key.replaceAll("_", " ");
}

function isMetricRecord(value: unknown): value is MetricRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function renderMetricValue(value: unknown): ReactNode {
  if (typeof value === "boolean") {
    return value ? (
      <span className="text-emerald-300">✓ Yes</span>
    ) : (
      <span className="text-zinc-500">✕ No</span>
    );
  }

  if (Array.isArray(value)) {
    if (value.length === 0) {
      return <span className="text-zinc-500">None</span>;
    }

    return (
      <ul className="space-y-1.5">
        {value.map((item, index) => (
          <li key={index} className="text-zinc-300">
            {renderMetricValue(item)}
          </li>
        ))}
      </ul>
    );
  }

  if (isMetricRecord(value)) {
    const entries = Object.entries(value);

    if (entries.length === 0) {
      return <span className="text-zinc-500">None</span>;
    }

    return (
      <dl className="space-y-2 border-l border-white/10 pl-3">
        {entries.map(([key, item]) => (
          <div key={key} className="flex flex-col gap-1 sm:flex-row sm:justify-between sm:gap-6">
            <dt className="text-zinc-500">{formatLabel(key)}</dt>
            <dd className="break-words text-zinc-300">{renderMetricValue(item)}</dd>
          </div>
        ))}
      </dl>
    );
  }

  return <span className="text-zinc-200">{String(value)}</span>;
}

export function MetricsSection({ repository }: MetricsSectionProps) {
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({});

  const sections: Array<{
    name: string;
    icon: typeof BookOpen;
    metrics: object | null;
  }> = [
    {
      name: "Documentation",
      icon: BookOpen,
      metrics: repository.documentation_metrics,
    },
    {
      name: "Structure",
      icon: FolderTree,
      metrics: repository.structure_metrics,
    },
    {
      name: "Code",
      icon: Braces,
      metrics: repository.code_metrics,
    },
    {
      name: "Dependency",
      icon: Package,
      metrics: repository.dependency_metrics,
    },
    {
      name: "Security",
      icon: ShieldCheck,
      metrics: repository.security_metrics,
    },
    {
      name: "Project Health",
      icon: HeartPulse,
      metrics: repository.project_health_metrics,
    },
  ];

  return (
    <section className="space-y-3">
      {sections.map(({ name, icon: Icon, metrics }) => {
        const isExpanded = expandedSections[name] ?? false;

        return (
          <article
            key={name}
            className="overflow-hidden rounded-2xl border border-white/10 bg-white/[0.035] shadow-[0_1px_0_rgba(255,255,255,0.05)_inset] backdrop-blur-xl"
          >
            <button
              type="button"
              onClick={() =>
                setExpandedSections((current) => ({
                  ...current,
                  [name]: !isExpanded,
                }))
              }
              aria-expanded={isExpanded}
              className="flex w-full items-center justify-between gap-4 px-5 py-5 text-left sm:px-6"
            >
              <span className="flex items-center gap-3 text-sm font-medium text-zinc-100">
                <span className="flex size-8 items-center justify-center rounded-lg border border-blue-300/15 bg-blue-400/[0.07]">
                  <Icon className="size-4 text-blue-200" />
                </span>
                {name}
              </span>
              <ChevronDown
                className={`size-4 text-zinc-500 transition-transform duration-200 ${
                  isExpanded ? "rotate-180" : ""
                }`}
              />
            </button>

            <AnimatePresence initial={false}>
              {isExpanded ? (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.24, ease: "easeOut" }}
                  className="overflow-hidden"
                >
                  <div className="border-t border-white/10 px-5 py-5 sm:px-6">
                    {metrics ? (
                      <dl className="grid gap-x-8 gap-y-4 sm:grid-cols-2">
                        {Object.entries(metrics).map(([key, value]) => (
                          <div
                            key={key}
                            className="min-w-0 rounded-xl border border-white/[0.07] bg-black/15 px-4 py-3"
                          >
                            <dt className="text-xs font-medium tracking-[0.1em] text-zinc-500 uppercase">
                              {formatLabel(key)}
                            </dt>
                            <dd className="mt-2 break-words text-sm leading-6">
                              {renderMetricValue(value)}
                            </dd>
                          </div>
                        ))}
                      </dl>
                    ) : (
                      <p className="text-sm text-zinc-500">Metrics unavailable.</p>
                    )}
                  </div>
                </motion.div>
              ) : null}
            </AnimatePresence>
          </article>
        );
      })}
    </section>
  );
}
