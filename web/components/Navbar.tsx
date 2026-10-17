"use client";

import React, { useState } from "react";
import {
  Search,
  Moon,
  Sun,
  Bell,
  CheckCircle2,
  ChevronDown,
  UserCheck,
} from "lucide-react";
import { UserRole } from "@/lib/types";

interface NavbarProps {
  currentRole: UserRole;
  onRoleChange: (role: UserRole) => void;
  onSearchClick: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentRole,
  onRoleChange,
  onSearchClick,
}) => {
  const [isDark, setIsDark] = useState(false);
  const [showRoleMenu, setShowRoleMenu] = useState(false);

  const toggleTheme = () => {
    const nextDark = !isDark;
    setIsDark(nextDark);
    if (nextDark) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  };

  const roles: UserRole[] = ["Admin", "Team Lead", "Employee"];

  return (
    <header className="h-14 border-b border-[var(--mt-border)] bg-[var(--mt-surface)] px-6 flex items-center justify-between sticky top-0 z-20 transition-colors">
      {/* Search trigger */}
      <button
        onClick={onSearchClick}
        className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-xs text-[var(--mt-text-secondary)] hover:text-[var(--mt-text)] hover:border-brand-500/30 transition-all w-64 text-left"
      >
        <Search className="w-3.5 h-3.5 text-[var(--mt-text-muted)]" />
        <span className="flex-1 truncate">Search meetings, decisions...</span>
        <kbd className="px-1.5 py-0.5 rounded bg-[var(--mt-surface)] text-[0.65rem] font-semibold border border-[var(--mt-border)] text-[var(--mt-text-muted)]">
          ⌘K
        </kbd>
      </button>

      {/* Right Actions */}
      <div className="flex items-center gap-3">
        {/* Operational badge */}
        <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-[0.72rem] font-semibold">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
          System Operational
        </div>

        {/* Role Switcher (Crucial for Pair Programming & Review) */}
        <div className="relative">
          <button
            onClick={() => setShowRoleMenu(!showRoleMenu)}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-[var(--mt-surface-soft)] border border-[var(--mt-border)] text-xs font-semibold text-[var(--mt-text)] hover:border-brand-500/40 transition-all"
            title="Switch user role to test permissions"
          >
            <UserCheck className="w-3.5 h-3.5 text-brand-500" />
            <span>Role: {currentRole}</span>
            <ChevronDown className="w-3 h-3 text-[var(--mt-text-muted)]" />
          </button>

          {showRoleMenu && (
            <div className="absolute right-0 mt-1.5 w-48 rounded-xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-dropdown py-1 z-50">
              <div className="px-3 py-1.5 text-[0.65rem] font-bold text-[var(--mt-text-muted)] uppercase tracking-wider border-b border-[var(--mt-border)]">
                Simulate Role Identity
              </div>
              {roles.map((r) => (
                <button
                  key={r}
                  onClick={() => {
                    onRoleChange(r);
                    setShowRoleMenu(false);
                  }}
                  className={`w-full text-left px-3 py-2 text-xs font-medium flex items-center justify-between hover:bg-[var(--mt-surface-soft)] transition-colors ${
                    currentRole === r
                      ? "text-brand-500 font-bold bg-brand-500/5"
                      : "text-[var(--mt-text)]"
                  }`}
                >
                  <span>{r}</span>
                  {currentRole === r && (
                    <CheckCircle2 className="w-3.5 h-3.5 text-brand-500" />
                  )}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className="p-2 rounded-lg text-[var(--mt-text-secondary)] hover:text-[var(--mt-text)] hover:bg-[var(--mt-surface-soft)] transition-colors"
          title={isDark ? "Switch to Light Theme" : "Switch to Dark Theme"}
        >
          {isDark ? (
            <Sun className="w-4 h-4 text-amber-400" />
          ) : (
            <Moon className="w-4 h-4" />
          )}
        </button>

        {/* Notifications */}
        <button
          onClick={() => alert("Notification center: 1 new follow-up ready for review.")}
          className="p-2 rounded-lg text-[var(--mt-text-secondary)] hover:text-[var(--mt-text)] hover:bg-[var(--mt-surface-soft)] transition-colors relative"
          title="Notifications"
        >
          <Bell className="w-4 h-4" />
          <span className="w-2 h-2 rounded-full bg-brand-500 absolute top-1.5 right-1.5" />
        </button>
      </div>
    </header>
  );
};
