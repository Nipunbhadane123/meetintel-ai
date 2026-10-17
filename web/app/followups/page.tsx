"use client";

import React, { useState } from "react";
import {
  MailCheck,
  Send,
  Calendar,
  CheckCircle2,
  Clock,
  User,
  ShieldCheck,
  FileText,
} from "lucide-react";
import { api } from "@/lib/api";

export default function FollowupsPage() {
  const [followups, setFollowups] = useState(api.getFollowups());

  const handleSend = (id: string) => {
    api.sendFollowup(id);
    setFollowups(api.getFollowups());
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[var(--mt-border)]">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[0.68rem] font-bold uppercase tracking-wider text-brand-500 bg-brand-500/10 px-2.5 py-0.5 rounded-full border border-brand-500/20">
              Ecosystem Orchestration
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--mt-text)]">
            Calendar Sync & Absentee Follow-ups
          </h1>
          <p className="text-xs text-[var(--mt-text-secondary)] mt-1">
            Automate personalized debriefs for absent attendees and verify two-way Google Calendar event synchronization.
          </p>
        </div>
      </div>

      {/* Sync Summary Banner */}
      <div className="p-5 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-600 flex items-center justify-center flex-shrink-0">
            <Calendar className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xs font-bold text-[var(--mt-text)]">
              Two-Way Google Calendar Synchronization
            </div>
            <div className="text-[0.72rem] text-[var(--mt-text-secondary)] mt-0.5">
              Approved tasks with deadlines are automatically scheduled on team member primary calendars.
            </div>
          </div>
        </div>

        <span className="text-xs font-semibold px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-600 border border-emerald-500/20 flex items-center gap-1.5 flex-shrink-0">
          <CheckCircle2 className="w-3.5 h-3.5" /> 100% Calendar Sync Health
        </span>
      </div>

      {/* Absentee Follow-up Cards */}
      <div className="space-y-4">
        <h2 className="text-base font-bold text-[var(--mt-text)] flex items-center gap-2">
          <MailCheck className="w-4 h-4 text-brand-500" />
          <span>Drafted Absentee Briefings</span>
        </h2>

        {followups.map((f) => (
          <div
            key={f.id}
            className="p-6 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card hover:border-brand-500/30 transition-all space-y-4 text-xs"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-[var(--mt-border)]">
              <div>
                <span className="text-[0.68rem] text-brand-500 font-bold uppercase tracking-wider">
                  Automated Debrief • {f.meeting_title}
                </span>
                <h3 className="text-sm font-bold text-[var(--mt-text)] mt-0.5">
                  {f.subject}
                </h3>
              </div>

              <span
                className={`text-[0.68rem] font-bold px-2.5 py-0.5 rounded-full ${
                  f.status === "Sent"
                    ? "bg-emerald-500/10 text-emerald-600 border border-emerald-500/20"
                    : "bg-amber-500/10 text-amber-600 border border-amber-500/20"
                }`}
              >
                ● {f.status}
              </span>
            </div>

            <div className="p-4 rounded-xl bg-[var(--mt-surface-soft)] text-[var(--mt-text)] leading-relaxed space-y-2">
              <div className="font-semibold text-brand-500">
                To: {f.recipient_name} &lt;{f.recipient_email}&gt;
              </div>
              <p className="text-[var(--mt-text-secondary)]">{f.summary_preview}</p>
            </div>

            <div className="flex items-center justify-between pt-2">
              <span className="text-[0.7rem] text-[var(--mt-text-muted)]">
                {f.sent_at ? `Dispatched on ${new Date(f.sent_at).toLocaleString()}` : "Ready for lead dispatch"}
              </span>

              {f.status !== "Sent" ? (
                <button
                  onClick={() => handleSend(f.id)}
                  className="px-4 py-1.5 rounded-lg bg-brand-500 hover:bg-brand-600 text-white font-semibold text-xs shadow-sm flex items-center gap-1.5"
                >
                  <Send className="w-3.5 h-3.5" /> Dispatch Follow-up
                </button>
              ) : (
                <span className="text-emerald-600 dark:text-emerald-400 font-semibold flex items-center gap-1 text-xs">
                  <ShieldCheck className="w-3.5 h-3.5" /> Delivered via SMTP
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
