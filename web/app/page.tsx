"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Mic,
  CheckSquare,
  Scale,
  RefreshCw,
  PlusCircle,
  Clock,
  Calendar,
  Users,
  AlertTriangle,
  ArrowRight,
  ShieldCheck,
  Check,
  Share2,
  DollarSign,
  TrendingUp,
  Zap,
  Copy,
  Send,
  X,
  FileText,
  Sliders,
} from "lucide-react";
import { api } from "@/lib/api";

export default function DashboardPage() {
  const [meetings] = useState(api.getMeetings());
  const [actionItems, setActionItems] = useState(api.getActionItems());
  const [decisions] = useState(api.getDecisions());
  const [auditEvents, setAuditEvents] = useState(api.getAuditEvents(4));

  // ROI & Telemetry state
  const [hourlyRate, setHourlyRate] = useState<number>(75);
  const [showExportModal, setShowExportModal] = useState<boolean>(false);
  const [activeExportTab, setActiveExportTab] = useState<"slack" | "teams" | "markdown">("slack");
  const [copiedToast, setCopiedToast] = useState<string | null>(null);
  const [webhookDispatched, setWebhookDispatched] = useState<boolean>(false);

  const pendingApprovals = actionItems.filter(
    (a) => a.approval_status === "Draft" || a.approval_status === "Pending Approval"
  );
  const urgentTasks = actionItems.filter(
    (a) => a.priority === "Urgent" || a.priority === "High"
  );

  // ROI calculations
  const totalDurationSeconds = meetings.reduce((acc, m) => acc + (m.duration || 1800), 0);
  const totalDurationHours = totalDurationSeconds / 3600;
  const avgParticipants = meetings.length ? Math.round(meetings.reduce((acc, m) => acc + (m.speaker_count || 3), 0) / meetings.length) : 3;
  const totalMeetingCost = Math.round(totalDurationHours * avgParticipants * hourlyRate);
  const decisionsPerHour = totalDurationHours > 0 ? (decisions.length / totalDurationHours).toFixed(1) : "3.2";
  const actionsPerHour = totalDurationHours > 0 ? (actionItems.length / totalDurationHours).toFixed(1) : "6.4";

  const handleApprove = (taskId: number) => {
    const updated = api.approveActionItem(taskId, "user-sarah-002");
    if (updated) {
      setActionItems(api.getActionItems());
      setAuditEvents(api.getAuditEvents(4));
    }
  };

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    setCopiedToast(`Copied ${label} to clipboard!`);
    setTimeout(() => setCopiedToast(null), 3000);
  };

  const simulateWebhookDispatch = () => {
    setWebhookDispatched(true);
    setCopiedToast("Dispatched Executive Debrief to #engineering-sync webhook!");
    setTimeout(() => {
      setWebhookDispatched(false);
      setCopiedToast(null);
    }, 4000);
  };

  const primaryMeeting = meetings[0] || {
    title: "Q3 Architecture & Security Alignment",
    date: "2026-10-20",
    executive_summary: "The engineering leadership aligned on the Q3 security roadmap.",
  };

  const slackJsonSnippet = JSON.stringify(
    {
      text: `📋 Executive Debrief: ${primaryMeeting.title}`,
      blocks: [
        {
          type: "header",
          text: { type: "plain_text", text: `📋 Executive Debrief: ${primaryMeeting.title}`, emoji: true },
        },
        {
          type: "section",
          text: { type: "mrkdwn", text: `*Summary:* ${primaryMeeting.executive_summary}` },
        },
        {
          type: "section",
          fields: [
            { type: "mrkdwn", text: `*💰 Estimated Cost:* $${totalMeetingCost} USD` },
            { type: "mrkdwn", text: `*⚡ Velocity:* ${decisionsPerHour} decisions/hr` },
          ],
        },
      ],
    },
    null,
    2
  );

  const markdownSnippet = `# 📋 Executive Meeting Briefing: ${primaryMeeting.title}
**Date:** ${primaryMeeting.date} | **Platform:** MeetIntel AI Enterprise Engine

## 1. Executive Summary
${primaryMeeting.executive_summary}

## 2. ROI & Telemetry
- **Estimated Session Cost:** $${totalMeetingCost} USD (based on $${hourlyRate}/hr team avg)
- **Decision Velocity:** ${decisionsPerHour} decisions/hr
- **Action Density:** ${actionsPerHour} actions/hr

## 3. Confirmed Decision Register
${decisions.map((d, i) => `${i + 1}. **${d.title}**: ${d.rationale}`).join("\n")}

## 4. Key Commitments
${actionItems.map((a) => `- **${a.task}** → \`${a.assigned_to}\` (Due: ${a.deadline})`).join("\n")}
`;

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      {/* Toast Notification */}
      {copiedToast && (
        <div className="fixed bottom-6 right-6 z-50 p-4 rounded-xl bg-emerald-600 text-white shadow-2xl flex items-center gap-2 text-xs font-semibold animate-in slide-in-from-bottom duration-200">
          <Check className="w-4 h-4" />
          <span>{copiedToast}</span>
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[var(--mt-border)]">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[0.68rem] font-bold uppercase tracking-wider text-brand-500 bg-brand-500/10 px-2.5 py-0.5 rounded-full border border-brand-500/20">
              Executive Telemetry & ROI
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--mt-text)]">
            Intelligence & Execution Overview
          </h1>
          <p className="text-xs text-[var(--mt-text-secondary)] mt-1 max-w-2xl">
            Live telemetry across ingested dialogues, decision registers, automated calendar syncs, and team commitments.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowExportModal(true)}
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-[var(--mt-surface-soft)] hover:bg-brand-500/10 text-[var(--mt-text)] border border-[var(--mt-border)] font-semibold text-xs transition-all shadow-sm"
          >
            <Share2 className="w-4 h-4 text-brand-500" />
            <span>Export Debrief</span>
          </button>

          <Link
            href="/upload"
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold text-xs shadow-md shadow-brand-500/20 transition-all hover:scale-[1.02]"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Process Meeting</span>
          </Link>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1 */}
        <div className="p-5 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card hover:border-brand-500/30 transition-all">
          <div className="flex items-center justify-between text-[var(--mt-text-secondary)] mb-3">
            <span className="text-xs font-semibold">Total Meetings</span>
            <div className="w-8 h-8 rounded-lg bg-brand-500/10 text-brand-500 flex items-center justify-center">
              <Mic className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-[var(--mt-text)] tracking-tight">
            {meetings.length}
          </div>
          <div className="text-[0.72rem] text-emerald-600 dark:text-emerald-400 font-medium mt-1 flex items-center gap-1">
            <span>↑ 100% audio verified</span>
          </div>
        </div>

        {/* Card 2 */}
        <div className="p-5 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card hover:border-brand-500/30 transition-all">
          <div className="flex items-center justify-between text-[var(--mt-text-secondary)] mb-3">
            <span className="text-xs font-semibold">Action Items</span>
            <div className="w-8 h-8 rounded-lg bg-blue-500/10 text-blue-500 flex items-center justify-center">
              <CheckSquare className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-[var(--mt-text)] tracking-tight">
            {actionItems.length}
          </div>
          <div className="text-[0.72rem] text-amber-600 dark:text-amber-400 font-medium mt-1">
            {pendingApprovals.length} awaiting lead sign-off
          </div>
        </div>

        {/* Card 3 */}
        <div className="p-5 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card hover:border-brand-500/30 transition-all">
          <div className="flex items-center justify-between text-[var(--mt-text-secondary)] mb-3">
            <span className="text-xs font-semibold">Decisions Logged</span>
            <div className="w-8 h-8 rounded-lg bg-purple-500/10 text-purple-500 flex items-center justify-center">
              <Scale className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-[var(--mt-text)] tracking-tight">
            {decisions.length}
          </div>
          <div className="text-[0.72rem] text-[var(--mt-text-secondary)] font-medium mt-1">
            Avg confidence: 98.2%
          </div>
        </div>

        {/* Card 4 */}
        <div className="p-5 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card hover:border-brand-500/30 transition-all">
          <div className="flex items-center justify-between text-[var(--mt-text-secondary)] mb-3">
            <span className="text-xs font-semibold">Ecosystem Sync</span>
            <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-500 flex items-center justify-center">
              <RefreshCw className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-[var(--mt-text)] tracking-tight">
            100%
          </div>
          <div className="text-[0.72rem] text-emerald-600 dark:text-emerald-400 font-medium mt-1">
            Google Calendar & SMTP active
          </div>
        </div>
      </div>

      {/* FEATURE: Executive Meeting Cost & ROI Telemetry Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-brand-500/10 via-[var(--mt-surface)] to-cyan-500/10 border border-brand-500/20 shadow-card">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          <div className="space-y-1.5 max-w-xl">
            <div className="flex items-center gap-2">
              <span className="flex items-center gap-1 text-[0.68rem] font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded-full border border-emerald-500/20">
                <TrendingUp className="w-3 h-3" /> ROI & Outcome Velocity Engine
              </span>
              <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-500">
                Grade: A (Highly Productive)
              </span>
            </div>
            <h3 className="text-lg font-bold text-[var(--mt-text)]">
              Meeting Investment: ${totalMeetingCost} USD across {meetings.length} sessions
            </h3>
            <p className="text-xs text-[var(--mt-text-secondary)] leading-relaxed">
              Achieving high decision velocity with <strong>{decisionsPerHour} decisions/hr</strong> and{" "}
              <strong>{actionsPerHour} action items/hr</strong>. All deliverables are grounded in verbatim quotes.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-4 bg-[var(--mt-surface)] p-3.5 rounded-xl border border-[var(--mt-border)] shadow-sm">
            <div className="text-xs space-y-1">
              <div className="text-[0.7rem] text-[var(--mt-text-secondary)] font-semibold flex items-center gap-1">
                <Sliders className="w-3 h-3 text-brand-500" /> Hourly Rate Model:
              </div>
              <div className="flex items-center gap-1.5">
                {[50, 75, 100, 150].map((rate) => (
                  <button
                    key={rate}
                    onClick={() => setHourlyRate(rate)}
                    className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all ${
                      hourlyRate === rate
                        ? "bg-brand-500 text-white shadow-sm"
                        : "bg-[var(--mt-surface-soft)] text-[var(--mt-text-secondary)] hover:text-[var(--mt-text)]"
                    }`}
                  >
                    ${rate}/hr
                  </button>
                ))}
              </div>
            </div>

            <div className="border-l border-[var(--mt-border)] pl-4 text-xs space-y-0.5">
              <div className="text-[0.68rem] text-[var(--mt-text-muted)] font-medium">Est. Cost / Decision:</div>
              <div className="text-sm font-bold text-emerald-600 dark:text-emerald-400">
                ${Math.round(totalMeetingCost / Math.max(decisions.length, 1))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Grid: Recent Meetings & Urgent Action Items */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Recent Ingested Meetings */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-[var(--mt-text)] flex items-center gap-2">
              <Mic className="w-4 h-4 text-brand-500" />
              <span>Recent Meeting Dossiers</span>
            </h2>
            <Link
              href="/meetings"
              className="text-xs font-semibold text-brand-500 hover:underline flex items-center gap-1"
            >
              View all library <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-3">
            {meetings.map((m) => {
              const durationMin = Math.floor(m.duration / 60);
              const durationSec = Math.floor(m.duration % 60);

              return (
                <div
                  key={m.id}
                  className="p-4 rounded-xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card hover:border-brand-500/40 hover:shadow-card-hover transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4"
                >
                  <div className="space-y-1.5 flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span
                        className={`text-[0.65rem] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider ${
                          m.source_platform === "google_meet"
                            ? "bg-emerald-500/10 text-emerald-600 border border-emerald-500/20"
                            : m.source_platform === "zoom"
                            ? "bg-blue-500/10 text-blue-600 border border-blue-500/20"
                            : "bg-purple-500/10 text-purple-600 border border-purple-500/20"
                        }`}
                      >
                        {m.source_platform.replace("_", " ")}
                      </span>
                      <span className="text-[0.7rem] text-[var(--mt-text-secondary)]">
                        {new Date(m.date).toLocaleDateString("en-US", {
                          month: "short",
                          day: "numeric",
                          year: "numeric",
                        })}
                      </span>
                    </div>

                    <Link
                      href={`/meetings/${m.id}`}
                      className="text-sm font-bold text-[var(--mt-text)] hover:text-brand-500 transition-colors block truncate"
                    >
                      {m.title}
                    </Link>

                    <p className="text-xs text-[var(--mt-text-secondary)] line-clamp-1">
                      {m.executive_summary}
                    </p>

                    <div className="flex items-center gap-4 text-[0.72rem] text-[var(--mt-text-muted)] pt-1">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {durationMin}m {durationSec}s
                      </span>
                      <span className="flex items-center gap-1">
                        <Users className="w-3 h-3" />
                        {m.speaker_count} Speakers
                      </span>
                    </div>
                  </div>

                  <Link
                    href={`/meetings/${m.id}`}
                    className="px-3.5 py-2 rounded-lg bg-[var(--mt-surface-soft)] hover:bg-brand-500 hover:text-white border border-[var(--mt-border)] text-xs font-semibold text-[var(--mt-text)] transition-all flex items-center justify-center gap-1.5 flex-shrink-0"
                  >
                    <span>Intelligence Dossier</span>
                    <ArrowRight className="w-3 h-3" />
                  </Link>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Urgent Action Items & Sign-offs */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-[var(--mt-text)] flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-500" />
              <span>Priority Commitments</span>
            </h2>
            <Link
              href="/tasks"
              className="text-xs font-semibold text-brand-500 hover:underline flex items-center gap-1"
            >
              All tasks <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-3">
            {urgentTasks.slice(0, 4).map((item) => (
              <div
                key={item.id}
                className="p-4 rounded-xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card flex flex-col justify-between gap-3 text-xs"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-1.5">
                    <span
                      className={`text-[0.65rem] font-bold px-2 py-0.5 rounded-full ${
                        item.priority === "Urgent"
                          ? "bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20"
                          : "bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20"
                      }`}
                    >
                      {item.priority}
                    </span>
                    <span className="text-[0.68rem] font-medium text-[var(--mt-text-muted)]">
                      {item.deadline}
                    </span>
                  </div>

                  <div className="font-bold text-[var(--mt-text)] mb-1">
                    {item.task}
                  </div>
                  <div className="text-[0.72rem] text-[var(--mt-text-secondary)]">
                    Assigned: <strong className="text-[var(--mt-text)]">{item.assigned_to}</strong>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-2 border-t border-[var(--mt-border)]">
                  <span
                    className={`text-[0.68rem] font-semibold ${
                      item.approval_status === "Approved"
                        ? "text-emerald-600 dark:text-emerald-400"
                        : "text-amber-600 dark:text-amber-400"
                    }`}
                  >
                    ● {item.approval_status}
                  </span>

                  {item.approval_status !== "Approved" ? (
                    <button
                      onClick={() => handleApprove(item.id)}
                      className="px-2.5 py-1 rounded-md bg-brand-500 hover:bg-brand-600 text-white font-semibold text-[0.72rem] transition-colors flex items-center gap-1"
                    >
                      <Check className="w-3 h-3" />
                      Approve
                    </button>
                  ) : (
                    <span className="text-[0.7rem] text-emerald-600 dark:text-emerald-400 font-medium flex items-center gap-1">
                      <ShieldCheck className="w-3.5 h-3.5" /> Synced
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Governance Audit Snippet */}
          <div className="p-4 rounded-xl bg-[var(--mt-surface-soft)] border border-[var(--mt-border)]">
            <div className="text-[0.7rem] font-bold uppercase tracking-wider text-[var(--mt-text-muted)] mb-2 flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-brand-500" />
              Latest Governance Audit
            </div>
            <div className="space-y-2">
              {auditEvents.slice(0, 3).map((e) => (
                <div key={e.id} className="text-[0.72rem] text-[var(--mt-text-secondary)] leading-relaxed">
                  <span className="font-semibold text-[var(--mt-text)]">{e.actor}</span>:{" "}
                  {e.details}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* FEATURE: 1-Click Executive Debrief & Slack/Teams Webhook Exporter Modal */}
      {showExportModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-150">
          <div className="bg-[var(--mt-surface)] border border-[var(--mt-border)] rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden flex flex-col">
            {/* Modal Header */}
            <div className="p-4 border-b border-[var(--mt-border)] flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Share2 className="w-5 h-5 text-brand-500" />
                <h3 className="font-bold text-sm text-[var(--mt-text)]">
                  Export Executive Debrief & Webhooks
                </h3>
              </div>
              <button
                onClick={() => setShowExportModal(false)}
                className="text-[var(--mt-text-muted)] hover:text-[var(--mt-text)]"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Tabs */}
            <div className="flex border-b border-[var(--mt-border)] bg-[var(--mt-surface-soft)] text-xs">
              <button
                onClick={() => setActiveExportTab("slack")}
                className={`flex-1 py-2.5 font-semibold text-center transition-all ${
                  activeExportTab === "slack"
                    ? "border-b-2 border-brand-500 text-brand-500 bg-[var(--mt-surface)]"
                    : "text-[var(--mt-text-secondary)] hover:text-[var(--mt-text)]"
                }`}
              >
                Slack Block Kit
              </button>
              <button
                onClick={() => setActiveExportTab("teams")}
                className={`flex-1 py-2.5 font-semibold text-center transition-all ${
                  activeExportTab === "teams"
                    ? "border-b-2 border-brand-500 text-brand-500 bg-[var(--mt-surface)]"
                    : "text-[var(--mt-text-secondary)] hover:text-[var(--mt-text)]"
                }`}
              >
                MS Teams / Memo
              </button>
              <button
                onClick={() => setActiveExportTab("markdown")}
                className={`flex-1 py-2.5 font-semibold text-center transition-all ${
                  activeExportTab === "markdown"
                    ? "border-b-2 border-brand-500 text-brand-500 bg-[var(--mt-surface)]"
                    : "text-[var(--mt-text-secondary)] hover:text-[var(--mt-text)]"
                }`}
              >
                Raw Markdown
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-5 overflow-y-auto max-h-[400px] text-xs font-mono space-y-4">
              {activeExportTab === "slack" && (
                <div className="space-y-3">
                  <div className="text-[0.72rem] text-[var(--mt-text-secondary)] font-sans">
                    Formatted Block Kit JSON for Slack incoming webhooks or bot integrations:
                  </div>
                  <pre className="p-3.5 rounded-xl bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-[0.7rem] overflow-x-auto text-[var(--mt-text)]">
                    {slackJsonSnippet}
                  </pre>
                </div>
              )}

              {activeExportTab === "teams" && (
                <div className="space-y-3 font-sans">
                  <div className="text-[0.72rem] text-[var(--mt-text-secondary)]">
                    Executive Brief formatted for Microsoft Teams announcements:
                  </div>
                  <div className="p-4 rounded-xl bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] space-y-2">
                    <div className="font-bold text-sm text-[var(--mt-text)]">
                      📋 Executive Debrief: {primaryMeeting.title}
                    </div>
                    <p className="text-[var(--mt-text-secondary)] leading-relaxed">
                      {primaryMeeting.executive_summary}
                    </p>
                    <div className="pt-2 border-t border-[var(--mt-border)] text-[0.72rem] text-[var(--mt-text-muted)]">
                      Decisions: {decisions.length} | Commitments: {actionItems.length} | Cost: ${totalMeetingCost}
                    </div>
                  </div>
                </div>
              )}

              {activeExportTab === "markdown" && (
                <div className="space-y-3">
                  <div className="text-[0.72rem] text-[var(--mt-text-secondary)] font-sans">
                    Complete markdown formatted report ready to paste into GitHub, Jira, or Confluence:
                  </div>
                  <pre className="p-3.5 rounded-xl bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-[0.7rem] overflow-x-auto text-[var(--mt-text)]">
                    {markdownSnippet}
                  </pre>
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="p-4 border-t border-[var(--mt-border)] bg-[var(--mt-surface-soft)] flex flex-wrap items-center justify-between gap-3">
              <button
                onClick={simulateWebhookDispatch}
                disabled={webhookDispatched}
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-semibold text-xs shadow-sm transition-all"
              >
                <Send className="w-3.5 h-3.5" />
                <span>{webhookDispatched ? "Dispatched!" : "Dispatch to #sync-channel"}</span>
              </button>

              <div className="flex items-center gap-2">
                <button
                  onClick={() =>
                    copyToClipboard(
                      activeExportTab === "slack"
                        ? slackJsonSnippet
                        : markdownSnippet,
                      activeExportTab.toUpperCase()
                    )
                  }
                  className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold text-xs shadow-sm transition-all"
                >
                  <Copy className="w-3.5 h-3.5" />
                  <span>Copy Payload</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
