"use client";

import React, { useState } from "react";
import {
  FolderKanban,
  Plus,
  Calendar,
  CheckCircle2,
  AlertTriangle,
  Clock,
  ArrowRight,
} from "lucide-react";
import { api } from "@/lib/api";
import { Project } from "@/lib/types";

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>(api.getProjects());
  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [targetDate, setTargetDate] = useState("2026-11-30");

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    const newP = api.createProject(name, description, targetDate);
    setProjects(api.getProjects());
    setName("");
    setDescription("");
    setShowModal(false);
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[var(--mt-border)]">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[0.68rem] font-bold uppercase tracking-wider text-brand-500 bg-brand-500/10 px-2.5 py-0.5 rounded-full border border-brand-500/20">
              Strategic Portfolio
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--mt-text)]">
            Projects & Milestones
          </h1>
          <p className="text-xs text-[var(--mt-text-secondary)] mt-1">
            Track multi-meeting initiative rollups, health statuses, and cross-functional commitments.
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold text-xs shadow-md shadow-brand-500/20 transition-all flex items-center gap-2 self-start md:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>New Project</span>
        </button>
      </div>

      {/* Projects Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {projects.map((p) => {
          const totalTasks = p.action_items_count || 3;
          const completedTasks = p.completed_items_count || 1;
          const pct = Math.round((completedTasks / totalTasks) * 100);

          return (
            <div
              key={p.id}
              className="p-5 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card hover:border-brand-500/30 transition-all flex flex-col justify-between gap-4"
            >
              <div className="space-y-2.5">
                <div className="flex items-center justify-between">
                  <span
                    className={`text-[0.65rem] font-bold px-2 py-0.5 rounded-full ${
                      p.status === "Active"
                        ? "bg-brand-500/10 text-brand-600 border border-brand-500/20"
                        : p.status === "At Risk"
                        ? "bg-rose-500/10 text-rose-600 border border-rose-500/20"
                        : "bg-emerald-500/10 text-emerald-600 border border-emerald-500/20"
                    }`}
                  >
                    ● {p.status}
                  </span>
                  <span className="text-[0.68rem] text-[var(--mt-text-muted)] flex items-center gap-1">
                    <Calendar className="w-3 h-3" />
                    Target: {new Date(p.target_date).toLocaleDateString("en-US", { month: "short", day: "numeric" })}
                  </span>
                </div>

                <h3 className="text-base font-bold text-[var(--mt-text)] leading-snug">
                  {p.name}
                </h3>
                <p className="text-xs text-[var(--mt-text-secondary)] leading-relaxed">
                  {p.description}
                </p>
              </div>

              {/* Progress Bar */}
              <div className="space-y-1.5 pt-2 border-t border-[var(--mt-border)]">
                <div className="flex items-center justify-between text-[0.7rem] font-medium text-[var(--mt-text-secondary)]">
                  <span>Commitments Progress</span>
                  <span className="font-bold text-[var(--mt-text)]">
                    {completedTasks}/{totalTasks} ({pct}%)
                  </span>
                </div>
                <div className="w-full h-1.5 rounded-full bg-[var(--mt-surface-soft)] overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all ${
                      p.status === "At Risk" ? "bg-rose-500" : "bg-brand-500"
                    }`}
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <form
            onSubmit={handleCreate}
            className="bg-[var(--mt-surface)] border border-[var(--mt-border)] rounded-2xl p-6 w-full max-w-md shadow-2xl space-y-4"
          >
            <h3 className="text-base font-bold text-[var(--mt-text)]">Create Initiative</h3>
            <div>
              <label className="text-xs font-semibold text-[var(--mt-text-secondary)] block mb-1">
                Project Name
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Q4 SOC2 Compliance Audit"
                className="w-full px-3 py-2 rounded-xl text-xs bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-[var(--mt-text)] focus:outline-none focus:border-brand-500"
                required
              />
            </div>
            <div>
              <label className="text-xs font-semibold text-[var(--mt-text-secondary)] block mb-1">
                Objective / Description
              </label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Brief summary of strategic deliverable..."
                rows={3}
                className="w-full px-3 py-2 rounded-xl text-xs bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-[var(--mt-text)] focus:outline-none focus:border-brand-500"
              />
            </div>
            <div className="flex items-center justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={() => setShowModal(false)}
                className="px-3 py-1.5 rounded-lg text-xs font-semibold text-[var(--mt-text-secondary)] hover:bg-[var(--mt-surface-soft)]"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-1.5 rounded-lg text-xs font-semibold bg-brand-500 hover:bg-brand-600 text-white"
              >
                Create Project
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
