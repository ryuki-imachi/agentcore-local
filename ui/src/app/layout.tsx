import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AgentCore Local - AG-UI',
  description: 'Local AgentCore Runtime with Strands Agent and CopilotKit',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
