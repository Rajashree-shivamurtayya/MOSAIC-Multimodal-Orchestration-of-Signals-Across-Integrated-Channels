import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AppShell } from "@/components/layout/AppShell";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "MOSAIC | Multimodal Signals",
  description: "Multi-Model Orchestration of Signals Across Integrated Channels",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.className} h-full antialiased`}>
      <body className="min-h-full flex flex-col bg-[var(--color-bg-base)] text-[var(--color-text-primary)]">
        <AppShell>
          {children}
        </AppShell>
      </body>
    </html>
  );
}
