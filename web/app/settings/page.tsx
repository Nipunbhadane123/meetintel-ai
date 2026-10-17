"use client";

import React, { useState } from "react";
import {
  Settings,
  User,
  Sparkles,
  Shield,
  Save,
  CheckCircle2,
  Sliders,
} from "lucide-react";
import { api } from "@/lib/api";

export default function SettingsPage() {
  const currentUser = api.getCurrentUser();
  const [fullName, setFullName] = useState(currentUser.full_name);
  const [email, setEmail] = useState(currentUser.email);
  const [department, setDepartment] = useState(currentUser.department);
  const [provider, setProvider] = useState("gemini");
  const [geminiModel, setGeminiModel] = useState("gemini-2.5-flash");
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="max-w-4xl space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[var(--mt-border)]">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[0.68rem] font-bold uppercase tracking-wider text-brand-500 bg-brand-500/10 px-2.5 py-0.5 rounded-full border border-brand-500/20">
              Platform Configuration
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--mt-text)]">
            Preferences & AI Configuration
          </h1>
          <p className="text-xs text-[var(--mt-text-secondary)] mt-1">
            Configure profile credentials, select AI intelligence providers, and customize execution parameters.
          </p>
        </div>
      </div>

      {saved && (
        <div className="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs font-semibold flex items-center gap-2 animate-in fade-in">
          <CheckCircle2 className="w-4 h-4" />
          <span>Configuration saved successfully.</span>
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-6">
        {/* User Profile Card */}
        <div className="p-6 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card space-y-4 text-xs">
          <div className="flex items-center gap-2 font-bold text-sm text-[var(--mt-text)] pb-2 border-b border-[var(--mt-border)]">
            <User className="w-4 h-4 text-brand-500" />
            <span>Profile & Organizational Identity</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="font-semibold text-[var(--mt-text-secondary)] block mb-1">
                Full Name
              </label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full px-3 py-2 rounded-xl text-xs bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-[var(--mt-text)] focus:outline-none focus:border-brand-500"
              />
            </div>

            <div>
              <label className="font-semibold text-[var(--mt-text-secondary)] block mb-1">
                Corporate Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 rounded-xl text-xs bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-[var(--mt-text)] focus:outline-none focus:border-brand-500"
              />
            </div>

            <div>
              <label className="font-semibold text-[var(--mt-text-secondary)] block mb-1">
                Department
              </label>
              <input
                type="text"
                value={department}
                onChange={(e) => setDepartment(e.target.value)}
                className="w-full px-3 py-2 rounded-xl text-xs bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-[var(--mt-text)] focus:outline-none focus:border-brand-500"
              />
            </div>

            <div>
              <label className="font-semibold text-[var(--mt-text-secondary)] block mb-1">
                Assigned RBAC Role
              </label>
              <input
                type="text"
                disabled
                value={currentUser.role}
                className="w-full px-3 py-2 rounded-xl text-xs bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-[var(--mt-text-muted)] cursor-not-allowed"
              />
            </div>
          </div>
        </div>

        {/* AI Provider Config */}
        <div className="p-6 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card space-y-4 text-xs">
          <div className="flex items-center gap-2 font-bold text-sm text-[var(--mt-text)] pb-2 border-b border-[var(--mt-border)]">
            <Sparkles className="w-4 h-4 text-brand-500" />
            <span>AI Intelligence Provider & Failover Chain</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="font-semibold text-[var(--mt-text-secondary)] block mb-1">
                Primary Intelligence Provider
              </label>
              <select
                value={provider}
                onChange={(e) => setProvider(e.target.value)}
                className="w-full px-3 py-2 rounded-xl text-xs bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-[var(--mt-text)] focus:outline-none focus:border-brand-500"
              >
                <option value="gemini">Google Gemini (Recommended & Primary)</option>
                <option value="openai">OpenAI GPT-4o-mini</option>
                <option value="demo">Demo Deterministic Fallback</option>
              </select>
            </div>

            <div>
              <label className="font-semibold text-[var(--mt-text-secondary)] block mb-1">
                Gemini Model Selection
              </label>
              <select
                value={geminiModel}
                onChange={(e) => setGeminiModel(e.target.value)}
                className="w-full px-3 py-2 rounded-xl text-xs bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-[var(--mt-text)] focus:outline-none focus:border-brand-500"
              >
                <option value="gemini-2.5-flash">gemini-2.5-flash (Fast & Structured)</option>
                <option value="gemini-2.5-pro">gemini-2.5-pro (Deep Reasoning)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Submit */}
        <div className="flex justify-end">
          <button
            type="submit"
            className="px-6 py-2.5 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold text-xs shadow-md shadow-brand-500/20 transition-all flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            <span>Save Preferences</span>
          </button>
        </div>
      </form>
    </div>
  );
}
