import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

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
      <body className="min-h-full flex flex-col bg-[#0b0c10] text-[#f3f4f6]">
        {children}
      </body>
    </html>
  );
}
