"use client";

import React, { useState } from "react";
import {
  CheckSquare,
  Clock,
  User,
  ShieldCheck,
  Check,
  X,
  AlertCircle,
  Calendar,
  Filter,
  UserPlus,
  Quote,
  LayoutGrid,
  List,
  Sparkles,
  Zap,
} from "lucide-react";
import { api } from "@/lib/api";
import { ActionItem, TaskStatus, ApprovalStatus } from "@/lib/types";

export default function TasksPage() {
  const [tasks, setTasks] = useState(api.getActionItems());
  const [users] = useState(api.getUsers());
  const [viewMode, setViewMode] = useState<"list" | "matrix">("list");
  const [statusFilter, setStatusFilter] = useState<string>("All");
  const [approvalFilter, setApprovalFilter] = useState<string>("All");
  const [reassignModalTask, setReassignModalTask] = useState<ActionItem | null>(null);
  const [selectedUserForReassign, setSelectedUserForReassign] = useState<string>("");

  const filteredTasks = tasks.filter((t) => {
    if (statusFilter !== "All" && t.status !== statusFilter) return false;
    if (approvalFilter !== "All" && t.approval_status !== approvalFilter) return false;
    return true;
  });

  const handleApprove = (taskId: number) => {
    api.approveActionItem(taskId, "user-sarah-002");
    setTasks(api.getActionItems());
  };

  const handleReject = (taskId: number) => {
    const reason = prompt("Enter rejection reason:") || "Rejected in review";
    api.rejectActionItem(taskId, "user-sarah-002", reason);
    setTasks(api.getActionItems());
  };

  const handleStatusChange = (taskId: number, newStatus: TaskStatus) => {
    api.updateActionItemStatus(taskId, newStatus);
    setTasks(api.getActionItems());
  };

  const handleReassignSubmit = () => {
    if (reassignModalTask && selectedUserForReassign) {
      api.reassignActionItem(reassignModalTask.id, selectedUserForReassign);
      setTasks(api.getActionItems());
      setReassignModalTask(null);
      setSelectedUserForReassign("");
    }
  };

  // Quadrants for Eisenhower 2x2 Matrix
  const q1UrgentImportant = filteredTasks.filter(
    (t) => (t.priority === "Urgent" || t.priority === "High") && t.status !== "Completed"
  );
  const q2Strategic = filteredTasks.filter(
    (t) => t.status === "In Progress" && t.priority !== "Urgent"
  );
  const q3QuickWins = filteredTasks.filter(
    (t) => t.priority === "Medium" && t.status !== "Completed"
  );
  const q4Backlog = filteredTasks.filter(
    (t) => t.priority === "Low" || t.status === "Completed"
  );

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[var(--mt-border)]">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[0.68rem] font-bold uppercase tracking-wider text-brand-500 bg-brand-500/10 px-2.5 py-0.5 rounded-full border border-brand-500/20">
              Execution Engine & Priority Matrix
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--mt-text)]">
            My Commitments & Team Execution
          </h1>
          <p className="text-xs text-[var(--mt-text-secondary)] mt-1">
            Track commitments extracted from meeting dialogue, review lead sign-offs, and synchronize to calendars.
          </p>
        </div>

        {/* View Mode Toggle */}
        <div className="flex items-center gap-1.5 p-1 bg-[var(--mt-surface-soft)] rounded-xl border border-[var(--mt-border)] shadow-sm self-start md:self-auto text-xs">
          <button
            onClick={() => setViewMode("list")}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-semibold transition-all ${
              viewMode === "list"
                ? "bg-brand-500 text-white shadow-sm"
                : "text-[var(--mt-text-secondary)] hover:text-[var(--mt-text)]"
            }`}
          >
            <List className="w-3.5 h-3.5" />
            <span>List View</span>
          </button>
          <button
            onClick={() => setViewMode("matrix")}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-semibold transition-all ${
              viewMode === "matrix"
                ? "bg-brand-500 text-white shadow-sm"
                : "text-[var(--mt-text-secondary)] hover:text-[var(--mt-text)]"
            }`}
          >
            <LayoutGrid className="w-3.5 h-3.5" />
            <span>Eisenhower Matrix (2x2)</span>
          </button>
        </div>
      </div>

      {/* Filters Toolbar */}
      <div className="p-4 rounded-xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 text-xs font-semibold text-[var(--mt-text-secondary)]">
            <Filter className="w-3.5 h-3.5 text-brand-500" />
            <span>Status:</span>
          </div>
          {["All", "Pending", "In Progress", "Completed", "Blocked"].map((st) => (
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

        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-[var(--mt-text-secondary)]">
            Approval:
          </span>
          <select
            value={approvalFilter}
            onChange={(e) => setApprovalFilter(e.target.value)}
            className="px-3 py-1.5 rounded-lg text-xs font-medium bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-[var(--mt-text)] focus:outline-none focus:border-brand-500"
          >
            <option value="All">All Approvals</option>
            <option value="Approved">Approved</option>
            <option value="Draft">Draft</option>
            <option value="Pending Approval">Pending Approval</option>
            <option value="Rejected">Rejected</option>
          </select>
        </div>
      </div>

      {/* VIEW MODE 1: Standard List Grid */}
      {viewMode === "list" && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredTasks.length === 0 ? (
            <div className="col-span-full py-16 text-center text-xs text-[var(--mt-text-secondary)] bg-[var(--mt-surface)] rounded-2xl border border-[var(--mt-border)]">
              <CheckSquare className="w-8 h-8 mx-auto mb-2 text-[var(--mt-text-muted)]" />
              No action items match the selected filter criteria.
            </div>
          ) : (
            filteredTasks.map((t) => (
              <div
                key={t.id}
                className="p-5 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card hover:border-brand-500/30 transition-all flex flex-col justify-between gap-4 text-xs"
              >
                <div className="space-y-2.5">
                  <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span
                        className={`text-[0.65rem] font-bold px-2 py-0.5 rounded-full ${
                          t.priority === "Urgent"
                            ? "bg-rose-500/10 text-rose-600 border border-rose-500/20"
                            : t.priority === "High"
                            ? "bg-amber-500/10 text-amber-600 border border-amber-500/20"
                            : "bg-blue-500/10 text-blue-600 border border-blue-500/20"
                        }`}
                      >
                        {t.priority} Priority
                      </span>
                      <span className="text-[0.68rem] text-[var(--mt-text-muted)]">
                        Task #{t.id}
                      </span>
                    </div>

                    <span
                      className={`text-[0.68rem] font-bold px-2 py-0.5 rounded-full ${
                        t.approval_status === "Approved"
                          ? "bg-emerald-500/10 text-emerald-600 border border-emerald-500/20"
                          : t.approval_status === "Rejected"
                          ? "bg-rose-500/10 text-rose-600 border border-rose-500/20"
                          : "bg-amber-500/10 text-amber-600 border border-amber-500/20"
                      }`}
                    >
                      ● {t.approval_status}
                    </span>
                  </div>

                  <h3 className="text-sm font-bold text-[var(--mt-text)] leading-snug">
                    {t.task}
                  </h3>

                  <div className="flex flex-wrap items-center gap-4 text-[0.72rem] text-[var(--mt-text-secondary)]">
                    <span className="flex items-center gap-1.5 font-medium">
                      <User className="w-3.5 h-3.5 text-brand-500" />
                      {t.assigned_to}
                    </span>
                    <span className="flex items-center gap-1.5 font-medium">
                      <Calendar className="w-3.5 h-3.5 text-brand-500" />
                      Due: {t.deadline}
                    </span>
                    <span className="flex items-center gap-1.5 font-medium">
                      <Clock className="w-3.5 h-3.5 text-brand-500" />
                      ~{t.estimated_hours}h
                    </span>
                  </div>

                  {t.evidence_excerpt && (
                    <div className="p-3 rounded-xl bg-[var(--mt-surface-soft)] text-[0.7rem] text-[var(--mt-text-secondary)] border-l-2 border-brand-500 space-y-1">
                      <div className="flex items-center gap-1 font-semibold text-[var(--mt-text)]">
                        <Quote className="w-3 h-3 text-brand-500" /> Grounded Dialogue Citation:
                      </div>
                      <div className="italic leading-relaxed">
                        {t.evidence_excerpt}
                      </div>
                    </div>
                  )}

                  {t.is_blocked && (
                    <div className="p-2.5 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-600 dark:text-rose-400 text-[0.7rem] flex items-center gap-2">
                      <AlertCircle className="w-4 h-4 flex-shrink-0" />
                      <span>{t.blocker_reason || "Marked as blocked during active sprint"}</span>
                    </div>
                  )}
                </div>

                <div className="pt-3 border-t border-[var(--mt-border)] flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-1.5">
                    <span className="text-[0.68rem] text-[var(--mt-text-muted)]">Status:</span>
                    <select
                      value={t.status}
                      onChange={(e) => handleStatusChange(t.id, e.target.value as TaskStatus)}
                      className="px-2.5 py-1 rounded-md bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-xs font-semibold text-[var(--mt-text)]"
                    >
                      <option value="Draft">Draft</option>
                      <option value="Pending">Pending</option>
                      <option value="In Progress">In Progress</option>
                      <option value="Completed">Completed</option>
                      <option value="Blocked">Blocked</option>
                    </select>
                  </div>

                  <div className="flex items-center gap-1.5">
                    <button
                      onClick={() => setReassignModalTask(t)}
                      className="px-2.5 py-1 rounded-md bg-[var(--mt-surface-soft)] hover:bg-brand-500/10 text-[var(--mt-text)] border border-[var(--mt-border)] font-semibold text-[0.7rem] transition-colors flex items-center gap-1"
                    >
                      <UserPlus className="w-3 h-3 text-brand-500" />
                      Reassign
                    </button>

                    {t.approval_status !== "Approved" && (
                      <button
                        onClick={() => handleApprove(t.id)}
                        className="px-2.5 py-1 rounded-md bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-[0.7rem] transition-colors flex items-center gap-1"
                      >
                        <Check className="w-3 h-3" />
                        Approve
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* VIEW MODE 2: Eisenhower 2x2 Priority Matrix */}
      {viewMode === "matrix" && (
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-brand-500/10 border border-brand-500/20 text-xs text-[var(--mt-text)] flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-brand-500 flex-shrink-0" />
            <span>
              <strong>Eisenhower Decision Matrix:</strong> Prioritizes meeting action items dynamically based on urgency, estimated effort, and leader approval gating.
            </span>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Quadrant 1: Urgent & Important */}
            <div className="p-5 rounded-2xl bg-[var(--mt-surface)] border-2 border-rose-500/30 shadow-card space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-[var(--mt-border)]">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-rose-500" />
                  <h3 className="font-bold text-sm text-[var(--mt-text)]">
                    Q1: Do First (Urgent & Important)
                  </h3>
                </div>
                <span className="text-xs font-bold text-rose-600 px-2 py-0.5 rounded-full bg-rose-500/10">
                  {q1UrgentImportant.length} items
                </span>
              </div>
              <p className="text-[0.72rem] text-[var(--mt-text-secondary)]">
                Critical path deliverables requiring immediate execution to prevent launch blockers.
              </p>
              <div className="space-y-2.5">
                {q1UrgentImportant.map((t) => (
                  <div key={t.id} className="p-3 rounded-xl bg-rose-500/5 border border-rose-500/20 text-xs space-y-1.5">
                    <div className="font-bold text-[var(--mt-text)]">{t.task}</div>
                    <div className="flex items-center justify-between text-[0.7rem] text-[var(--mt-text-secondary)]">
                      <span>👤 {t.assigned_to}</span>
                      <span className="font-bold text-rose-600">Due: {t.deadline}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Quadrant 2: Strategic / Schedule */}
            <div className="p-5 rounded-2xl bg-[var(--mt-surface)] border-2 border-blue-500/30 shadow-card space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-[var(--mt-border)]">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-blue-500" />
                  <h3 className="font-bold text-sm text-[var(--mt-text)]">
                    Q2: Schedule (Strategic Execution)
                  </h3>
                </div>
                <span className="text-xs font-bold text-blue-600 px-2 py-0.5 rounded-full bg-blue-500/10">
                  {q2Strategic.length} items
                </span>
              </div>
              <p className="text-[0.72rem] text-[var(--mt-text-secondary)]">
                Core architecture and system stability deliverables scheduled for upcoming milestones.
              </p>
              <div className="space-y-2.5">
                {q2Strategic.map((t) => (
                  <div key={t.id} className="p-3 rounded-xl bg-blue-500/5 border border-blue-500/20 text-xs space-y-1.5">
                    <div className="font-bold text-[var(--mt-text)]">{t.task}</div>
                    <div className="flex items-center justify-between text-[0.7rem] text-[var(--mt-text-secondary)]">
                      <span>👤 {t.assigned_to}</span>
                      <span className="font-medium text-blue-600">Due: {t.deadline}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Quadrant 3: Quick Wins / Delegate */}
            <div className="p-5 rounded-2xl bg-[var(--mt-surface)] border-2 border-amber-500/30 shadow-card space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-[var(--mt-border)]">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-amber-500" />
                  <h3 className="font-bold text-sm text-[var(--mt-text)]">
                    Q3: Quick Wins (Delegate / Review)
                  </h3>
                </div>
                <span className="text-xs font-bold text-amber-600 px-2 py-0.5 rounded-full bg-amber-500/10">
                  {q3QuickWins.length} items
                </span>
              </div>
              <p className="text-[0.72rem] text-[var(--mt-text-secondary)]">
                Test updates and administrative sign-offs that can be distributed across peer team members.
              </p>
              <div className="space-y-2.5">
                {q3QuickWins.map((t) => (
                  <div key={t.id} className="p-3 rounded-xl bg-amber-500/5 border border-amber-500/20 text-xs space-y-1.5">
                    <div className="font-bold text-[var(--mt-text)]">{t.task}</div>
                    <div className="flex items-center justify-between text-[0.7rem] text-[var(--mt-text-secondary)]">
                      <span>👤 {t.assigned_to}</span>
                      <span>Due: {t.deadline}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Quadrant 4: Backlog / Monitor */}
            <div className="p-5 rounded-2xl bg-[var(--mt-surface)] border-2 border-emerald-500/30 shadow-card space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-[var(--mt-border)]">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-emerald-500" />
                  <h3 className="font-bold text-sm text-[var(--mt-text)]">
                    Q4: Completed & Low Priority
                  </h3>
                </div>
                <span className="text-xs font-bold text-emerald-600 px-2 py-0.5 rounded-full bg-emerald-500/10">
                  {q4Backlog.length} items
                </span>
              </div>
              <p className="text-[0.72rem] text-[var(--mt-text-secondary)]">
                Completed deliverables and future backlog items requiring low immediate management oversight.
              </p>
              <div className="space-y-2.5">
                {q4Backlog.map((t) => (
                  <div key={t.id} className="p-3 rounded-xl bg-emerald-500/5 border border-emerald-500/20 text-xs space-y-1.5">
                    <div className="font-bold text-[var(--mt-text)]">{t.task}</div>
                    <div className="flex items-center justify-between text-[0.7rem] text-[var(--mt-text-secondary)]">
                      <span>👤 {t.assigned_to}</span>
                      <span className="text-emerald-600 font-semibold">● {t.status}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Reassign Modal */}
      {reassignModalTask && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-[var(--mt-surface)] border border-[var(--mt-border)] rounded-2xl w-full max-w-md p-6 shadow-2xl space-y-4 text-xs">
            <div className="flex items-center justify-between pb-2 border-b border-[var(--mt-border)]">
              <h3 className="font-bold text-sm text-[var(--mt-text)]">
                Reassign Task #{reassignModalTask.id}
              </h3>
              <button
                onClick={() => setReassignModalTask(null)}
                className="text-[var(--mt-text-muted)] hover:text-[var(--mt-text)]"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <p className="text-[var(--mt-text-secondary)]">
              Transfer ownership of: <strong>{reassignModalTask.task}</strong>
            </p>

            <select
              value={selectedUserForReassign}
              onChange={(e) => setSelectedUserForReassign(e.target.value)}
              className="w-full p-2.5 rounded-xl bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-xs text-[var(--mt-text)]"
            >
              <option value="">Select team member...</option>
              {users.map((u) => (
                <option key={u.id} value={u.id}>
                  {u.full_name} ({u.role} — {u.department})
                </option>
              ))}
            </select>

            <div className="flex items-center justify-end gap-2 pt-2">
              <button
                onClick={() => setReassignModalTask(null)}
                className="px-3 py-1.5 rounded-lg text-xs font-semibold text-[var(--mt-text-secondary)] hover:bg-[var(--mt-surface-soft)]"
              >
                Cancel
              </button>
              <button
                onClick={handleReassignSubmit}
                disabled={!selectedUserForReassign}
                className="px-4 py-1.5 rounded-lg text-xs font-semibold bg-brand-500 hover:bg-brand-600 text-white disabled:opacity-50"
              >
                Confirm Reassignment
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
