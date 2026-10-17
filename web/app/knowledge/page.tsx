"use client";

import React, { useState } from "react";
import {
  Sparkles,
  Search,
  BookOpen,
  MessageSquare,
  Send,
  Quote,
  CheckCircle2,
  Clock,
  Layers,
} from "lucide-react";
import { api } from "@/lib/api";

export default function KnowledgeSearchPage() {
  const [activeTab, setActiveTab] = useState<"search" | "ask">("search");
  const [query, setQuery] = useState("OAuth PKCE");
  const [searchResults, setSearchResults] = useState(api.searchKnowledge("OAuth PKCE"));

  const [question, setQuestion] = useState("Why was OAuth 2.0 PKCE prioritized?");
  const [conversation, setConversation] = useState<
    Array<{ q: string; a: string; sources: Array<{ title: string; excerpt: string }> }>
  >([
    {
      q: "Why was OAuth 2.0 PKCE prioritized?",
      a: "During the Q3 Architecture & Security Alignment review, engineering leadership mandated OAuth 2.0 PKCE because the implicit authorization flow was flagged as a severe security vulnerability during external penetration testing. PKCE prevents interception of authorization codes on single-page and mobile applications.",
      sources: [
        {
          title: "Q3 Architecture & Security Alignment",
          excerpt:
            "Sarah Jenkins: The team decided to mandate OAuth 2.0 with PKCE and retain audit logs for 90 days.",
        },
        {
          title: "Decision Register #201",
          excerpt: "All web and mobile clients must migrate to authorization code flow with PKCE by Q4.",
        },
      ],
    },
  ]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    const res = api.searchKnowledge(query);
    setSearchResults(res);
  };

  const handleAsk = (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;
    const res = api.askAI(question);
    setConversation([...conversation, { q: question, a: res.answer, sources: res.sources }]);
    setQuestion("");
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[var(--mt-border)]">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[0.68rem] font-bold uppercase tracking-wider text-brand-500 bg-brand-500/10 px-2.5 py-0.5 rounded-full border border-brand-500/20">
              Vector RAG Engine
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--mt-text)]">
            Organizational Knowledge & Semantic Search
          </h1>
          <p className="text-xs text-[var(--mt-text-secondary)] mt-1">
            Perform cosine similarity vector queries across meeting transcripts, or synthesize strategic answers using RAG.
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-[var(--mt-border)] flex items-center gap-4">
        <button
          onClick={() => setActiveTab("search")}
          className={`pb-2.5 text-xs font-semibold border-b-2 transition-all flex items-center gap-1.5 ${
            activeTab === "search"
              ? "border-brand-500 text-brand-500"
              : "border-transparent text-[var(--mt-text-secondary)] hover:text-[var(--mt-text)]"
          }`}
        >
          <Search className="w-3.5 h-3.5" />
          <span>Semantic Vector Search</span>
        </button>
        <button
          onClick={() => setActiveTab("ask")}
          className={`pb-2.5 text-xs font-semibold border-b-2 transition-all flex items-center gap-1.5 ${
            activeTab === "ask"
              ? "border-brand-500 text-brand-500"
              : "border-transparent text-[var(--mt-text-secondary)] hover:text-[var(--mt-text)]"
          }`}
        >
          <MessageSquare className="w-3.5 h-3.5" />
          <span>RAG Question & Answer</span>
        </button>
      </div>

      {activeTab === "search" ? (
        <div className="space-y-6">
          <form onSubmit={handleSearch} className="flex gap-3">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-[var(--mt-text-muted)] absolute left-3.5 top-3" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Query vector index (e.g., 'database pooling', 'OAuth PKCE', 'SLA retention')..."
                className="w-full pl-10 pr-4 py-2.5 rounded-xl text-xs bg-[var(--mt-surface)] border border-[var(--mt-border)] text-[var(--mt-text)] focus:outline-none focus:border-brand-500 shadow-sm"
              />
            </div>
            <button
              type="submit"
              className="px-5 py-2.5 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold text-xs shadow-md shadow-brand-500/20 transition-all flex items-center gap-2"
            >
              <span>Search Vectors</span>
            </button>
          </form>

          {/* Results Summary */}
          <div className="flex items-center justify-between text-xs text-[var(--mt-text-secondary)]">
            <span>
              Found <strong className="text-[var(--mt-text)]">{searchResults.results.length}</strong> semantic match segments
            </span>
            <span className="text-[0.7rem] text-[var(--mt-text-muted)]">
              Latency: {searchResults.search_time_ms}ms
            </span>
          </div>

          <div className="space-y-3">
            {searchResults.results.map((r) => (
              <div
                key={r.id}
                className="p-5 rounded-xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card space-y-2 text-xs"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-[0.68rem] px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-500 border border-brand-500/20 uppercase tracking-wide">
                    {r.type}
                  </span>
                  <span className="text-[0.68rem] text-emerald-600 dark:text-emerald-400 font-bold">
                    Similarity: {Math.round(r.similarity * 100)}%
                  </span>
                </div>

                <div className="font-bold text-sm text-[var(--mt-text)]">{r.title}</div>
                <div className="text-[var(--mt-text-secondary)] leading-relaxed">{r.content}</div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="space-y-4">
            {conversation.map((item, idx) => (
              <div key={idx} className="space-y-2">
                <div className="p-3.5 rounded-xl bg-brand-500/10 text-brand-600 dark:text-brand-300 text-xs font-semibold max-w-xl ml-auto">
                  {item.q}
                </div>
                <div className="p-5 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card text-xs text-[var(--mt-text)] leading-relaxed space-y-3">
                  <div>{item.a}</div>
                  {item.sources && item.sources.length > 0 && (
                    <div className="pt-3 border-t border-[var(--mt-border)] space-y-1.5">
                      <div className="text-[0.7rem] font-bold uppercase tracking-wider text-brand-500">
                        Evidence Grounding & Citations:
                      </div>
                      {item.sources.map((s, i) => (
                        <div key={i} className="p-2 rounded-lg bg-[var(--mt-surface-soft)] text-[0.7rem] text-[var(--mt-text-secondary)]">
                          <strong>{s.title}:</strong> &ldquo;{s.excerpt}&rdquo;
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>

          <form onSubmit={handleAsk} className="flex gap-3">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask anything across all indexed meetings..."
              className="flex-1 px-4 py-2.5 rounded-xl text-xs bg-[var(--mt-surface)] border border-[var(--mt-border)] text-[var(--mt-text)] focus:outline-none focus:border-brand-500"
            />
            <button
              type="submit"
              className="px-5 py-2.5 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold text-xs shadow-sm flex items-center gap-1.5"
            >
              <Send className="w-3.5 h-3.5" /> Synthesize
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
