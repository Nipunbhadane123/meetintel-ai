import type { Metadata } from "next";
import "./globals.css";
import { AppShell } from "@/components/AppShell";

export const metadata: Metadata = {
  title: "MeetIntel AI — AI-Powered Meeting Intelligence & Execution Platform",
  description:
    "Transform audio and video meetings into structured decisions, automated calendar commitments, absentee follow-ups, and organizational knowledge.",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased selection:bg-brand-500/20 selection:text-brand-600">
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
