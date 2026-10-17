"use client";

import React, { useState } from "react";
import {
  Scale,
  CheckCircle2,
  Quote,
  Filter,
  Sparkles,
  Calendar,
  Layers,
} from "lucide-react";
import { api } from "@/lib/api";

export default function DecisionsPage() {
  const [decisions] = useState(api.getDecisions());
  const [statusFilter, setStatusFilter] = useState("All");

  const filtered = decisions.filter((d) => {
    if (statusFilter !== "All" && d.status !== statusFilter) return false;
    return true;
  });

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[var(--mt-border)]">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[0.68rem] font-bold uppercase tracking-wider text-brand-500 bg-brand-500/10 px-2.5 py-0.5 rounded-full border border-brand-500/20">
              Corporate Memory
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--mt-text)]">
            Executive Decision Register
          </h1>
          <p className="text-xs text-[var(--mt-text-secondary)] mt-1">
            Official immutable record of agreed architectural decisions, consensus rationale, and considered alternatives.
          </p>
        </div>
      </div>

      {/* Filter toolbar */}
      <div className="p-4 rounded-xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card flex items-center gap-3">
        <span className="text-xs font-semibold text-[var(--mt-text-secondary)]">
          Filter by Status:
        </span>
        {["All", "Approved", "Proposed"].map((st) => (
          <button
            key={st}
            onClick={() => setStatusFilter(st)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              statusFilter === st
                ? "bg-brand-500 text-white font-semibold shadow-sm"
                : "bg-[var(--mt-surface-soft)] text-[var(--mt-text)] hover:bg-brand-500/10"
            }`}
          >
            {st}
          </button>
        ))}
      </div>

      {/* Decisions List */}
      <div className="space-y-4">
        {filtered.map((d) => (
          <div
            key={d.id}
            className="p-6 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card hover:border-brand-500/30 transition-all space-y-4 text-xs"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-[var(--mt-border)]">
              <div>
                <span className="text-[0.68rem] text-brand-500 font-bold uppercase tracking-wider">
                  Decision #{d.id} • {d.meeting_title}
                </span>
                <h3 className="text-base font-bold text-[var(--mt-text)] mt-0.5">
                  {d.title}
                </h3>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-[0.68rem] font-bold text-emerald-600 bg-emerald-500/10 px-2.5 py-0.5 rounded-full border border-emerald-500/20">
                  ● {d.status}
                </span>
                <span className="text-[0.68rem] text-[var(--mt-text-muted)]">
                  Confidence: {Math.round(d.confidence * 100)}%
                </span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-3.5 rounded-xl bg-[var(--mt-surface-soft)] space-y-1">
                <span className="font-bold text-[var(--mt-text)]">
                  Consensus Rationale:
                </span>
                <p className="text-[var(--mt-text-secondary)] leading-relaxed">
                  {d.rationale || "Agreed by unanimous vote during engineering architecture alignment."}
                </p>
              </div>

              <div className="p-3.5 rounded-xl bg-[var(--mt-surface-soft)] space-y-1">
                <span className="font-bold text-[var(--mt-text)]">
                  Alternatives Evaluated:
                </span>
                <p className="text-[var(--mt-text-secondary)] leading-relaxed">
                  {d.alternatives || "Legacy architecture retaining client secrets (dismissed as high vulnerability)."}
                </p>
              </div>
            </div>

            {d.evidence_excerpt && (
              <div className="p-3 rounded-xl bg-[var(--mt-surface-soft)]/60 border-l-2 border-brand-500 italic text-[0.72rem] text-[var(--mt-text-secondary)] flex items-start gap-2">
                <Quote className="w-3.5 h-3.5 text-brand-500 flex-shrink-0 mt-0.5" />
                <span>&ldquo;{d.evidence_excerpt}&rdquo;</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
