"use client";

import { motion, type Variants } from "framer-motion";
import {
  Braces,
  FileText,
  FolderTree,
  HeartPulse,
  Package,
  ShieldCheck,
} from "lucide-react";

import type { DomainScoreResponse, OverallScoreResponse } from "@/lib/api/types";

interface ScoreGridProps {
  score: OverallScoreResponse;
}

const gridVariants: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.06,
    },
  },
};

const cardVariants: Variants = {
  hidden: { opacity: 0, y: 10 },
  visible: { opacity: 1, y: 0 },
};

export function ScoreGrid({ score }: ScoreGridProps) {
  const domains: Array<{
    name: string;
    value: DomainScoreResponse;
    icon: typeof FileText;
  }> = [
    { name: "Documentation", value: score.documentation, icon: FileText },
    { name: "Structure", value: score.structure, icon: FolderTree },
    { name: "Code", value: score.code, icon: Braces },
    { name: "Dependency", value: score.dependency, icon: Package },
    { name: "Security", value: score.security, icon: ShieldCheck },
    { name: "Health", value: score.health, icon: HeartPulse },
  ];

  return (
    <motion.section
      variants={gridVariants}
      initial="hidden"
      animate="visible"
      className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
    >
      {domains.map(({ name, value, icon: Icon }) => (
        <motion.article
          key={name}
          variants={cardVariants}
          transition={{ duration: 0.35, ease: "easeOut" }}
          className="rounded-2xl border border-white/10 bg-white/[0.035] p-5 shadow-[0_1px_0_rgba(255,255,255,0.05)_inset] backdrop-blur-xl"
        >
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-2.5">
              <span className="flex size-8 items-center justify-center rounded-lg border border-blue-300/15 bg-blue-400/[0.07]">
                <Icon className="size-4 text-blue-200" />
              </span>
              <p className="text-sm font-medium text-zinc-200">{name}</p>
            </div>
            <p className="text-lg font-semibold tracking-[-0.03em] text-white">
              {value.current_score}
              <span className="ml-1 text-sm font-medium tracking-normal text-zinc-500">
                /{value.max_score}
              </span>
            </p>
          </div>

          <div className="mt-5 h-1.5 overflow-hidden rounded-full bg-white/[0.08]">
            <div
              className="h-full rounded-full bg-blue-400 transition-[width] duration-500"
              style={{
                width: `${(value.current_score / value.max_score) * 100}%`,
              }}
            />
          </div>
        </motion.article>
      ))}
    </motion.section>
  );
}
