"use client";

import React, { useState, useEffect } from "react";
import { Search, X, Sparkles, ArrowRight } from "lucide-react";
import { api } from "@/lib/api";
import Link from "next/link";

interface SearchModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const SearchModal: React.FC<SearchModalProps> = ({ isOpen, onClose }) => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        // Toggle or open
      }
      if (e.key === "Escape") {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [onClose]);

  useEffect(() => {
    if (query.trim()) {
      const searchRes = api.searchKnowledge(query);
      setResults(searchRes.results);
    } else {
      setResults([]);
    }
  }, [query]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 bg-black/60 backdrop-blur-sm p-4 animate-in fade-in duration-150">
      <div className="bg-[var(--mt-surface)] border border-[var(--mt-border)] rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden flex flex-col">
        {/* Search Input */}
        <div className="p-4 border-b border-[var(--mt-border)] flex items-center gap-3">
          <Search className="w-5 h-5 text-brand-500 flex-shrink-0" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search transcripts, decisions, and action items (e.g., 'OAuth', 'database')..."
            className="w-full bg-transparent text-sm text-[var(--mt-text)] placeholder-[var(--mt-text-muted)] focus:outline-none"
            autoFocus
          />
          <button
            onClick={onClose}
            className="p-1 rounded-md text-[var(--mt-text-muted)] hover:text-[var(--mt-text)] hover:bg-[var(--mt-surface-soft)] transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Results Area */}
        <div className="max-h-96 overflow-y-auto p-4 space-y-2">
          {query.trim() === "" ? (
            <div className="py-8 text-center text-xs text-[var(--mt-text-secondary)]">
              <Sparkles className="w-6 h-6 mx-auto mb-2 text-brand-500/40" />
              Type a keyword to run vector semantic search across organizational knowledge.
            </div>
          ) : results.length === 0 ? (
            <div className="py-8 text-center text-xs text-[var(--mt-text-secondary)]">
              No results found for &ldquo;{query}&rdquo;.
            </div>
          ) : (
            results.map((res) => (
              <div
                key={res.id}
                className="p-3 rounded-xl border border-[var(--mt-border)] hover:border-brand-500/30 hover:bg-[var(--mt-surface-soft)] transition-all flex flex-col gap-1 text-xs"
              >
                <div className="flex items-center justify-between text-[0.7rem] text-brand-500 font-bold uppercase tracking-wide">
                  <span>{res.type}</span>
                  <span className="text-[var(--mt-text-muted)] font-normal">
                    {res.title}
                  </span>
                </div>
                <div className="text-[var(--mt-text)] line-clamp-2">
                  {res.content}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-[var(--mt-border)] bg-[var(--mt-surface-soft)]/60 text-[0.7rem] text-[var(--mt-text-muted)] flex items-center justify-between">
          <span>Press ESC to exit</span>
          <Link
            href="/knowledge"
            onClick={onClose}
            className="text-brand-500 font-semibold hover:underline flex items-center gap-1"
          >
            Advanced Semantic RAG <ArrowRight className="w-3 h-3" />
          </Link>
        </div>
      </div>
    </div>
  );
};
