"use client";

import { motion, type Variants } from "framer-motion";
import { CircleAlert, Info, ShieldAlert, TriangleAlert } from "lucide-react";

import type { FindingResponse } from "@/lib/api/types";

interface FindingsPanelProps {
  findings: FindingResponse[];
}

const severityOrder = ["CRITICAL", "HIGH", "MEDIUM", "LOW"] as const;

const severityMeta = {
  CRITICAL: {
    icon: ShieldAlert,
    badge: "border-red-300/25 bg-red-400/[0.12] text-red-200",
    accent: "border-red-400/30",
    iconColor: "text-red-300",
  },
  HIGH: {
    icon: TriangleAlert,
    badge: "border-red-300/20 bg-red-400/[0.08] text-red-200",
    accent: "border-red-400/20",
    iconColor: "text-red-300",
  },
  MEDIUM: {
    icon: CircleAlert,
    badge: "border-amber-300/20 bg-amber-400/[0.08] text-amber-200",
    accent: "border-amber-400/20",
    iconColor: "text-amber-300",
  },
  LOW: {
    icon: Info,
    badge: "border-blue-300/15 bg-blue-400/[0.07] text-blue-100",
    accent: "border-blue-400/15",
    iconColor: "text-blue-300",
  },
};

const listVariants: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.05,
    },
  },
};

const findingVariants: Variants = {
  hidden: { opacity: 0, y: 10 },
  visible: { opacity: 1, y: 0 },
};

export function FindingsPanel({ findings }: FindingsPanelProps) {
  const groups = severityOrder.map((severity) => ({
    severity,
    findings: findings.filter((finding) => finding.severity === severity),
  }));

  if (findings.length === 0) {
    return (
      <section className="rounded-2xl border border-white/10 bg-white/[0.035] px-6 py-12 text-center shadow-[0_1px_0_rgba(255,255,255,0.05)_inset] backdrop-blur-xl">
        <p className="text-base font-medium text-zinc-200">No findings detected</p>
        <p className="mt-2 text-sm text-zinc-500">
          This repository passed the current engineering checks.
        </p>
      </section>
    );
  }

  return (
    <div className="space-y-10">
      {groups.map(({ severity, findings: severityFindings }) => {
        if (severityFindings.length === 0) {
          return null;
        }

        const meta = severityMeta[severity];
        const Icon = meta.icon;

        return (
          <section key={severity}>
            <div className="mb-4 flex items-center gap-3">
              <Icon className={`size-4 ${meta.iconColor}`} />
              <h2 className="text-sm font-medium tracking-[0.14em] text-zinc-300 uppercase">
                {severity}
              </h2>
              <span className="text-sm text-zinc-600">{severityFindings.length}</span>
            </div>

            <motion.div
              variants={listVariants}
              initial="hidden"
              animate="visible"
              className="space-y-3"
            >
              {severityFindings.map((finding) => (
                <motion.article
                  key={finding.id}
                  variants={findingVariants}
                  transition={{ duration: 0.3, ease: "easeOut" }}
                  className={`rounded-2xl border bg-white/[0.035] p-5 shadow-[0_1px_0_rgba(255,255,255,0.05)_inset] backdrop-blur-xl sm:p-6 ${meta.accent}`}
                >
                  <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                    <div className="min-w-0">
                      <div className="flex flex-wrap items-center gap-3">
                        <span
                          className={`rounded-md border px-2.5 py-1 text-[11px] font-semibold tracking-[0.12em] uppercase ${meta.badge}`}
                        >
                          {severity}
                        </span>
                        <span className="font-mono text-xs text-zinc-500">
                          {finding.id}
                        </span>
                      </div>
                      <h3 className="mt-4 text-lg font-medium tracking-[-0.02em] text-zinc-100">
                        {finding.title}
                      </h3>
                      <p className="mt-2 text-sm leading-6 text-zinc-400">
                        {finding.message}
                      </p>
                    </div>
                  </div>

                  <div className="mt-5 border-t border-white/8 pt-4">
                    <p className="text-[11px] font-medium tracking-[0.12em] text-zinc-500 uppercase">
                      Recommendation
                    </p>
                    <p className="mt-2 text-sm leading-6 text-zinc-300">
                      {finding.recommendation}
                    </p>
                  </div>
                </motion.article>
              ))}
            </motion.div>
          </section>
        );
      })}
    </div>
  );
}
