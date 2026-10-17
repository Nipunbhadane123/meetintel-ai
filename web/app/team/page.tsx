"use client";

import React, { useState } from "react";
import { Users, Shield, Briefcase, Mail, CheckCircle2, Clock } from "lucide-react";
import { api } from "@/lib/api";

export default function TeamPage() {
  const [users] = useState(api.getUsers());
  const tasks = api.getActionItems();

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[var(--mt-border)]">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[0.68rem] font-bold uppercase tracking-wider text-brand-500 bg-brand-500/10 px-2.5 py-0.5 rounded-full border border-brand-500/20">
              Governance & Directory
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--mt-text)]">
            Team Directory & Access Control
          </h1>
          <p className="text-xs text-[var(--mt-text-secondary)] mt-1">
            Manage organization members, assigned roles, departmental divisions, and commitment workloads.
          </p>
        </div>
      </div>

      {/* Team Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {users.map((u) => {
          const userTasks = tasks.filter((t) => t.assigned_user_id === u.id);
          const completedCount = userTasks.filter((t) => t.status === "Completed").length;

          return (
            <div
              key={u.id}
              className="p-6 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card hover:border-brand-500/30 transition-all flex flex-col justify-between gap-4 text-xs"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-brand-500 to-indigo-600 text-white font-bold text-sm flex items-center justify-center shadow-sm">
                    {u.full_name.charAt(0)}
                  </div>

                  <span
                    className={`text-[0.68rem] font-bold px-2.5 py-0.5 rounded-full ${
                      u.role === "Admin"
                        ? "bg-purple-500/10 text-purple-600 border border-purple-500/20"
                        : u.role === "Team Lead"
                        ? "bg-brand-500/10 text-brand-600 border border-brand-500/20"
                        : "bg-emerald-500/10 text-emerald-600 border border-emerald-500/20"
                    }`}
                  >
                    {u.role}
                  </span>
                </div>

                <div>
                  <h3 className="text-sm font-bold text-[var(--mt-text)]">
                    {u.full_name}
                  </h3>
                  <div className="text-[0.72rem] text-[var(--mt-text-secondary)] mt-0.5">
                    @{u.username}
                  </div>
                </div>

                <div className="space-y-1.5 text-[0.72rem] text-[var(--mt-text-secondary)] pt-1">
                  <div className="flex items-center gap-1.5">
                    <Mail className="w-3.5 h-3.5 text-brand-500" />
                    <span>{u.email}</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Briefcase className="w-3.5 h-3.5 text-brand-500" />
                    <span>{u.department}</span>
                  </div>
                </div>
              </div>

              {/* Workload metric */}
              <div className="pt-3 border-t border-[var(--mt-border)] flex items-center justify-between text-[0.7rem] text-[var(--mt-text-muted)]">
                <span>Active Commitments:</span>
                <span className="font-bold text-[var(--mt-text)]">
                  {userTasks.length} Assigned ({completedCount} Done)
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
