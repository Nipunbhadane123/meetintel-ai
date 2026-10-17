"use client";

import React, { useState } from "react";
import {
  CalendarDays,
  Sparkles,
  CheckSquare,
  Scale,
  Users,
  Clock,
  ArrowRight,
  BookOpen,
} from "lucide-react";
import { api } from "@/lib/api";

export default function MeetingPrepPage() {
  const [prepTopic, setPrepTopic] = useState("Q4 Architecture & Multi-Tenant Database Migration");
  const [isGenerated, setIsGenerated] = useState(true);

  const pendingItems = api.getActionItems({ status: "Pending" });
  const decisions = api.getDecisions().slice(0, 2);

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[var(--mt-border)]">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[0.68rem] font-bold uppercase tracking-wider text-brand-500 bg-brand-500/10 px-2.5 py-0.5 rounded-full border border-brand-500/20">
              Executive Briefing Engine
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--mt-text)]">
            AI Meeting Preparation & Context Brief
          </h1>
          <p className="text-xs text-[var(--mt-text-secondary)] mt-1">
            Generate briefings, compile outstanding action items, and synthesize historical context before entering a meeting.
          </p>
        </div>
      </div>

      {/* Topic selector card */}
      <div className="p-5 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card space-y-3">
        <label className="text-xs font-bold text-[var(--mt-text)] block">
          Upcoming Meeting Title or Topic:
        </label>
        <div className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={prepTopic}
            onChange={(e) => setPrepTopic(e.target.value)}
            className="flex-1 px-3.5 py-2 rounded-xl text-xs bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-[var(--mt-text)] focus:outline-none focus:border-brand-500"
          />
          <button
            onClick={() => setIsGenerated(true)}
            className="px-5 py-2 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold text-xs shadow-md shadow-brand-500/20 transition-all flex items-center justify-center gap-2"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Generate Briefing</span>
          </button>
        </div>
      </div>

      {/* Generated Briefing Sections */}
      {isGenerated && (
        <div className="space-y-6">
          {/* Executive Strategy Memo */}
          <div className="p-6 rounded-2xl bg-gradient-to-br from-brand-500/10 via-[var(--mt-surface)] to-[var(--mt-surface)] border border-brand-500/25 shadow-card space-y-3">
            <div className="flex items-center gap-2 text-xs font-bold text-brand-500">
              <Sparkles className="w-4 h-4" />
              <span>AI Executive Briefing Memo</span>
            </div>
            <h3 className="text-base font-bold text-[var(--mt-text)]">
              {prepTopic}
            </h3>
            <p className="text-xs text-[var(--mt-text-secondary)] leading-relaxed">
              Based on historical telemetry across Acme Global meetings, primary blockers revolve around database connection pooling on staging replicas. Key stakeholders require confirmation on OAuth 2.0 PKCE code freeze before committing to new schema rollouts.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Recommended Agenda */}
            <div className="p-5 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card space-y-4 text-xs">
              <h3 className="font-bold text-sm text-[var(--mt-text)] flex items-center gap-2">
                <Clock className="w-4 h-4 text-brand-500" /> Recommended Agenda
              </h3>
              <div className="space-y-2.5">
                {[
                  { time: "00:00 - 00:05", title: "Objective alignment & attendance roll call" },
                  { time: "00:05 - 00:15", title: "Review OAuth 2.0 PKCE progress with Alex Chen" },
                  { time: "00:15 - 00:25", title: "Staging database replica bottleneck resolution" },
                  { time: "00:25 - 00:30", title: "Finalize task assignments and calendar commitments" },
                ].map((item, i) => (
                  <div key={i} className="p-2.5 rounded-lg bg-[var(--mt-surface-soft)] flex items-center justify-between">
                    <span className="font-semibold text-[var(--mt-text)]">{item.title}</span>
                    <span className="text-[0.68rem] text-[var(--mt-text-muted)] font-mono">{item.time}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Unresolved Carry-over Action Items */}
            <div className="p-5 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card space-y-4 text-xs">
              <h3 className="font-bold text-sm text-[var(--mt-text)] flex items-center gap-2">
                <CheckSquare className="w-4 h-4 text-amber-500" /> Carry-Over Commitments
              </h3>
              <div className="space-y-2.5">
                {pendingItems.slice(0, 3).map((item) => (
                  <div key={item.id} className="p-2.5 rounded-lg bg-[var(--mt-surface-soft)] space-y-1">
                    <div className="font-semibold text-[var(--mt-text)]">{item.task}</div>
                    <div className="flex items-center justify-between text-[0.68rem] text-[var(--mt-text-muted)]">
                      <span>Owner: {item.assigned_to}</span>
                      <span>Due: {item.deadline}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
