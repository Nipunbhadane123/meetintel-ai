"use client";

import React, { useState } from "react";
import { Sidebar } from "./Sidebar";
import { Navbar } from "./Navbar";
import { api } from "@/lib/api";
import { UserRole } from "@/lib/types";
import { SearchModal } from "./SearchModal";

export const AppShell: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [role, setRole] = useState<UserRole>("Team Lead");
  const [user, setUser] = useState(api.getCurrentUser());
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  const handleRoleChange = (newRole: UserRole) => {
    setRole(newRole);
    const updatedUser = api.setRole(newRole);
    setUser(updatedUser);
  };

  return (
    <div className="flex min-h-screen bg-[var(--mt-bg)] text-[var(--mt-text)]">
      {/* Sidebar Navigation */}
      <Sidebar
        currentRole={role}
        userName={user.full_name}
        userEmail={user.email}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar
          currentRole={role}
          onRoleChange={handleRoleChange}
          onSearchClick={() => setIsSearchOpen(true)}
        />
        <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto overflow-y-auto">
          {children}
        </main>
      </div>

      {/* Global Search & Command Modal */}
      <SearchModal
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
      />
    </div>
  );
};
