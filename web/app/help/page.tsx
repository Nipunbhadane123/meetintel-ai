"use client";

import React from "react";
import {
  BookOpen,
  Sparkles,
  CheckCircle2,
  Cpu,
  Layers,
  ShieldCheck,
  Cable,
  ArrowRight,
} from "lucide-react";
import Link from "next/link";

export default function HelpPage() {
  const sections = [
    {
      title: "1. Rapid Ingestion & Meeting Processing",
      desc: "Upload any audio or video recording from Google Meet, Zoom, or local recordings. MeetIntel AI validates file specs, normalizes audio to 16kHz mono, and initiates Whisper transcription with Pyannote speaker clustering.",
    },
    {
      title: "2. Decision & Commitment Extraction",
      desc: "Our dual-engine LLM analysis extracts decisions with rationale and alternatives, while binding action items to verified team members. Tasks with confidence < 0.90 are routed to the Team Lead review queue.",
    },
    {
      title: "3. Calendar Sync & Absentee Follow-ups",
      desc: "Approved action items with deadlines are automatically scheduled on the assignee's Google Calendar. Participants marked as Absent receive an executive debrief email via enterprise SMTP.",
    },
    {
      title: "4. Semantic Knowledge Search & RAG",
      desc: "Every meeting transcript, summary, and decision is indexed into the vector store. Search using natural language queries to synthesize answers across multiple meetings with verified citations.",
    },
  ];

  return (
    <div className="max-w-4xl space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[var(--mt-border)]">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[0.68rem] font-bold uppercase tracking-wider text-brand-500 bg-brand-500/10 px-2.5 py-0.5 rounded-full border border-brand-500/20">
              User Manual & System Docs
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--mt-text)]">
            Help & Platform Learning Guide
          </h1>
          <p className="text-xs text-[var(--mt-text-secondary)] mt-1">
            Everything you need to know about navigating MeetIntel AI, understanding workflows, and deploying to production.
          </p>
        </div>
      </div>

      {/* Guide Cards */}
      <div className="space-y-4">
        {sections.map((sec, i) => (
          <div
            key={i}
            className="p-6 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card space-y-2 text-xs"
          >
            <h3 className="text-sm font-bold text-[var(--mt-text)] flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-brand-500" />
              <span>{sec.title}</span>
            </h3>
            <p className="text-[var(--mt-text-secondary)] leading-relaxed pl-6">
              {sec.desc}
            </p>
          </div>
        ))}
      </div>

      {/* Documentation Links Card */}
      <div className="p-6 rounded-2xl bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] space-y-3 text-xs">
        <h3 className="font-bold text-[var(--mt-text)] flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-brand-500" />
          <span>Technical Architecture Guides</span>
        </h3>
        <p className="text-[var(--mt-text-secondary)]">
          In-depth technical audits and deployment guides are available in the repository `docs/` folder:
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1 font-mono text-[0.72rem] text-brand-500">
          <div>• docs/VERCEL_DEPLOYMENT_AUDIT.md</div>
          <div>• docs/DEPLOYMENT_GUIDE.md</div>
          <div>• docs/PRODUCTION_CHECKLIST.md</div>
          <div>• docs/DEPLOYMENT_TROUBLESHOOTING.md</div>
        </div>
      </div>
    </div>
  );
}
