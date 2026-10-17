"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import {
  UploadCloud,
  FileAudio,
  CheckCircle2,
  AlertCircle,
  Play,
  RotateCcw,
  Sparkles,
  ShieldCheck,
} from "lucide-react";

export default function UploadPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);

  const pipelineSteps = [
    { title: "Audio Extraction & Preprocessing", desc: "16kHz mono normalization via FFmpeg" },
    { title: "Whisper Transcription", desc: "Timestamped dialogue and word alignment" },
    { title: "Speaker Diarization", desc: "Pyannote audio biometric clustering" },
    { title: "AI Decision & Action Item Extraction", desc: "Structured analysis via Google Gemini" },
    { title: "Semantic Knowledge Indexing", desc: "Vector embeddings and cosine indexing" },
  ];

  const handleFileDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const startProcessing = () => {
    if (!file) return;
    setIsProcessing(true);
    setCurrentStep(0);

    // Simulated progress transitions
    const stepInterval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < 4) {
          return prev + 1;
        } else {
          clearInterval(stepInterval);
          setTimeout(() => {
            router.push("/meetings/demo-meeting-q3-security");
          }, 1200);
          return prev;
        }
      });
    }, 1500);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="text-center space-y-1.5 pb-2">
        <span className="text-[0.68rem] font-bold uppercase tracking-wider text-brand-500 bg-brand-500/10 px-2.5 py-0.5 rounded-full border border-brand-500/20">
          Ingestion & Pipeline
        </span>
        <h1 className="text-2xl font-bold tracking-tight text-[var(--mt-text)]">
          Process New Meeting Recording
        </h1>
        <p className="text-xs text-[var(--mt-text-secondary)]">
          Upload audio/video files for automated transcription, speaker identification, and task extraction.
        </p>
      </div>

      {!isProcessing ? (
        <div className="space-y-4">
          {/* Dropzone */}
          <div
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleFileDrop}
            className="p-10 rounded-2xl border-2 border-dashed border-[var(--mt-border)] hover:border-brand-500/50 bg-[var(--mt-surface)] text-center space-y-4 transition-all"
          >
            <div className="w-14 h-14 rounded-2xl bg-brand-500/10 text-brand-500 flex items-center justify-center mx-auto">
              <UploadCloud className="w-7 h-7" />
            </div>

            <div>
              <h3 className="text-sm font-bold text-[var(--mt-text)]">
                {file ? file.name : "Drag and drop your meeting recording here"}
              </h3>
              <p className="text-xs text-[var(--mt-text-secondary)] mt-1">
                Supports WAV, MP3, MP4, M4A, AAC, and FLAC (Up to 500 MB)
              </p>
            </div>

            <div className="pt-2">
              <label className="cursor-pointer px-4 py-2 rounded-xl bg-[var(--mt-surface-soft)] hover:bg-brand-500 hover:text-white border border-[var(--mt-border)] text-xs font-semibold text-[var(--mt-text)] transition-all inline-block shadow-sm">
                <span>Browse Files</span>
                <input
                  type="file"
                  accept="audio/*,video/*,.mp3,.wav,.mp4,.m4a,.aac,.flac"
                  onChange={handleFileSelect}
                  className="hidden"
                />
              </label>
            </div>
          </div>

          {/* Selected File Card */}
          {file && (
            <div className="p-4 rounded-xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-card flex items-center justify-between">
              <div className="flex items-center gap-3">
                <FileAudio className="w-8 h-8 text-brand-500 flex-shrink-0" />
                <div>
                  <div className="text-xs font-bold text-[var(--mt-text)] truncate">
                    {file.name}
                  </div>
                  <div className="text-[0.7rem] text-[var(--mt-text-secondary)]">
                    {(file.size / (1024 * 1024)).toFixed(1)} MB • Audio Recording
                  </div>
                </div>
              </div>

              <button
                onClick={startProcessing}
                className="px-5 py-2 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold text-xs shadow-md shadow-brand-500/20 transition-all flex items-center gap-2"
              >
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>Start AI Pipeline</span>
              </button>
            </div>
          )}
        </div>
      ) : (
        /* Processing Pipeline Progress */
        <div className="p-8 rounded-2xl bg-[var(--mt-surface)] border border-[var(--mt-border)] shadow-2xl space-y-6">
          <div className="text-center space-y-1">
            <div className="inline-flex items-center gap-2 text-xs font-bold text-brand-500">
              <Sparkles className="w-4 h-4 animate-spin" />
              <span>Pipeline In Execution</span>
            </div>
            <h3 className="text-base font-bold text-[var(--mt-text)]">
              Analyzing &ldquo;{file?.name || "Meeting Recording"}&rdquo;
            </h3>
          </div>

          <div className="space-y-4 pt-2">
            {pipelineSteps.map((step, idx) => {
              const isPast = idx < currentStep;
              const isCurrent = idx === currentStep;

              return (
                <div
                  key={idx}
                  className={`p-3.5 rounded-xl border transition-all flex items-center gap-3 text-xs ${
                    isCurrent
                      ? "border-brand-500 bg-brand-500/5 shadow-sm"
                      : isPast
                      ? "border-emerald-500/30 bg-emerald-500/5"
                      : "border-[var(--mt-border)] opacity-40"
                  }`}
                >
                  <div
                    className={`w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs flex-shrink-0 ${
                      isPast
                        ? "bg-emerald-500 text-white"
                        : isCurrent
                        ? "bg-brand-500 text-white animate-pulse"
                        : "bg-[var(--mt-surface-soft)] text-[var(--mt-text-muted)]"
                    }`}
                  >
                    {isPast ? <CheckCircle2 className="w-4 h-4" /> : idx + 1}
                  </div>

                  <div className="flex-1">
                    <div className="font-bold text-[var(--mt-text)]">
                      {step.title}
                    </div>
                    <div className="text-[0.7rem] text-[var(--mt-text-secondary)]">
                      {step.desc}
                    </div>
                  </div>

                  {isCurrent && (
                    <span className="text-[0.68rem] font-bold text-brand-500 animate-pulse">
                      Running...
                    </span>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
