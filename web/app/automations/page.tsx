"use client";

import React, { useState } from "react";
import {
  Zap,
  Play,
  CheckCircle2,
  AlertTriangle,
  Clock,
  ShieldCheck,
  ToggleLeft,
  ToggleRight,
} from "lucide-react";
import { api } from "@/lib/api";
import { WorkflowRule } from "@/lib/types";

export default function AutomationsPage() {
  const [rules, setRules] = useState<WorkflowRule[]>(api.getWorkflowRules());
  const [feedback, setFeedback] = useState<string | null>(null);

  const handleToggle = (id: string) => {
    api.toggleWorkflowRule(id);
    setRules(api.getWorkflowRules());
  };

  const handleTrigger = (id: string) => {
    const res = api.triggerWorkflowRule(id);
    setRules(api.getWorkflowRules());
    setFeedback(res.message);
    setTimeout(() => setFeedback(null), 3000);
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[var(--mt-border)]">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[0.68rem] font-bold uppercase tracking-wider text-brand-500 bg-brand-500/10 px-2.5 py-0.5 rounded-full border border-brand-500/20">
              Rule Automation Engine
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--mt-text)]">
            Workflow Automations & Event Triggers
          </h1>
          <p className="text-xs text-[var(--mt-text-secondary)] mt-1">
            Define automated rules that trigger calendar syncs, absentee dispatches, and risk escalations upon meeting completion.
          </p>
        </div>
      </div>

      {feedback && (
        <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs font-semibold flex items-center gap-2 animate-in fade-in">
          <CheckCircle2 className="w-4 h-4" />
          <span>{feedback}</span>
        </div>
      )}

      {/* Rules Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {rules.map((r) => (
          <div
            key={r.id}
            className="p-5 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card hover:border-brand-500/30 transition-all flex flex-col justify-between gap-4 text-xs"
          >
            <div className="space-y-2.5">
              <div className="flex items-center justify-between">
                <span className="font-bold text-[0.68rem] px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-500 border border-brand-500/20 uppercase tracking-wide">
                  Event: {r.trigger_event}
                </span>

                <button
                  onClick={() => handleToggle(r.id)}
                  className="flex items-center gap-1.5 text-xs font-semibold transition-colors"
                >
                  {r.is_enabled ? (
                    <span className="text-emerald-600 flex items-center gap-1">
                      <ToggleRight className="w-5 h-5" /> Enabled
                    </span>
                  ) : (
                    <span className="text-[var(--mt-text-muted)] flex items-center gap-1">
                      <ToggleLeft className="w-5 h-5" /> Disabled
                    </span>
                  )}
                </button>
              </div>

              <div>
                <h3 className="text-sm font-bold text-[var(--mt-text)]">{r.name}</h3>
                <p className="text-xs text-[var(--mt-text-secondary)] mt-1 leading-relaxed">
                  {r.description}
                </p>
              </div>

              <div className="p-2.5 rounded-lg bg-[var(--mt-surface-soft)] font-mono text-[0.7rem] text-[var(--mt-text-secondary)]">
                Condition: {r.condition_json}
              </div>

              <div className="flex items-center justify-between text-[0.7rem] text-[var(--mt-text-muted)] pt-1">
                <span>Executions: <strong className="text-[var(--mt-text)]">{r.success_count}</strong></span>
                <span>
                  Last Triggered:{" "}
                  {r.last_triggered_at
                    ? new Date(r.last_triggered_at).toLocaleTimeString()
                    : "Idle"}
                </span>
              </div>
            </div>

            <div className="pt-3 border-t border-[var(--mt-border)] flex items-center justify-end">
              <button
                onClick={() => handleTrigger(r.id)}
                className="px-3.5 py-1.5 rounded-lg bg-[var(--mt-surface-soft)] hover:bg-brand-500 hover:text-white border border-[var(--mt-border)] text-xs font-semibold text-[var(--mt-text)] transition-all flex items-center gap-1.5"
              >
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>Test Run Trigger</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
