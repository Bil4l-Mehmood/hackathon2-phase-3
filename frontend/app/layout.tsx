import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Todo AI Assistant - Phase III",
  description: "AI-powered conversational Todo management (Agentic Dev Stack)",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
