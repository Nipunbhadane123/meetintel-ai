"use client";

import React, { useState } from "react";
import {
  ShieldCheck,
  CheckCircle2,
  Clock,
  Filter,
  User,
  Activity,
  Layers,
} from "lucide-react";
import { api } from "@/lib/api";

export default function AuditPage() {
  const [events] = useState(api.getAuditEvents(50));
  const [filterAction, setFilterAction] = useState("All");

  const filtered = events.filter((e) => {
    if (filterAction !== "All" && e.action !== filterAction) return false;
    return true;
  });

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[var(--mt-border)]">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[0.68rem] font-bold uppercase tracking-wider text-brand-500 bg-brand-500/10 px-2.5 py-0.5 rounded-full border border-brand-500/20">
              Immutable Governance
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--mt-text)]">
            Audit Trail & Compliance Log
          </h1>
          <p className="text-xs text-[var(--mt-text-secondary)] mt-1">
            Tamper-evident chronological record of all user and worker actions, task sign-offs, calendar syncs, and system triggers.
          </p>
        </div>
      </div>

      {/* Filter toolbar */}
      <div className="p-4 rounded-xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card flex items-center gap-2 overflow-x-auto">
        <span className="text-xs font-semibold text-[var(--mt-text-secondary)] whitespace-nowrap">
          Action Filter:
        </span>
        {["All", "APPROVE", "CREATE", "UPDATE", "SYNC", "TRIGGER", "SEND"].map((act) => (
          <button
            key={act}
            onClick={() => setFilterAction(act)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all ${
              filterAction === act
                ? "bg-brand-500 text-white font-semibold shadow-sm"
                : "bg-[var(--mt-surface-soft)] text-[var(--mt-text)] hover:bg-brand-500/10"
            }`}
          >
            {act}
          </button>
        ))}
      </div>

      {/* Audit List */}
      <div className="p-6 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card divide-y divide-[var(--mt-border)] text-xs">
        {filtered.map((e) => (
          <div key={e.id} className="py-4 first:pt-0 last:pb-0 flex flex-col sm:flex-row sm:items-start justify-between gap-3">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span
                  className={`text-[0.65rem] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider ${
                    e.action === "APPROVE"
                      ? "bg-emerald-500/10 text-emerald-600 border border-emerald-500/20"
                      : e.action === "CREATE"
                      ? "bg-blue-500/10 text-blue-600 border border-blue-500/20"
                      : e.action === "TRIGGER"
                      ? "bg-purple-500/10 text-purple-600 border border-purple-500/20"
                      : "bg-amber-500/10 text-amber-600 border border-amber-500/20"
                  }`}
                >
                  {e.action}
                </span>

                <span className="font-bold text-[var(--mt-text)]">{e.actor}</span>
                <span className="text-[0.7rem] text-[var(--mt-text-muted)]">
                  • {e.entity_type} #{e.entity_id}
                </span>
              </div>

              <div className="text-[var(--mt-text-secondary)] leading-relaxed pt-0.5">
                {e.details}
              </div>
            </div>

            <div className="text-[0.68rem] text-[var(--mt-text-muted)] font-mono whitespace-nowrap flex-shrink-0">
              {new Date(e.timestamp).toLocaleTimeString()}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
