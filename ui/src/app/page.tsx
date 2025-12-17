'use client';

import { CopilotKit } from '@copilotkit/react-core';
import { CopilotSidebar } from '@copilotkit/react-ui';
import '@copilotkit/react-ui/styles.css';

export default function Home() {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit" agent="strands_agent">
      <CopilotSidebar
        defaultOpen={true}
        clickOutsideToClose={false}
        labels={{
          title: 'AgentCore Local',
          initial: 'こんにちは！何かお手伝いできることはありますか？現在時刻を聞いてみてください。',
        }}
      >
        <main style={{
          padding: '2rem',
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <div style={{ maxWidth: '800px', width: '100%' }}>
            <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem', textAlign: 'center' }}>
              AgentCore Local
            </h1>
            <p style={{ fontSize: '1.2rem', marginBottom: '2rem', textAlign: 'center', opacity: 0.8 }}>
              Strands Agent + Ollama + CopilotKit
            </p>

            <div style={{
              background: 'rgba(0,0,0,0.05)',
              padding: '2rem',
              borderRadius: '8px',
              marginBottom: '2rem'
            }}>
              <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>技術スタック</h2>
              <ul style={{ listStyle: 'none', padding: 0 }}>
                <li style={{ marginBottom: '0.5rem' }}>
                  <strong>Agent:</strong> Strands Agents SDK
                </li>
                <li style={{ marginBottom: '0.5rem' }}>
                  <strong>LLM:</strong> Ollama (qwen3:8b)
                </li>
                <li style={{ marginBottom: '0.5rem' }}>
                  <strong>Frontend:</strong> Next.js + CopilotKit
                </li>
                <li style={{ marginBottom: '0.5rem' }}>
                  <strong>Backend:</strong> FastAPI + AG-UI Protocol
                </li>
              </ul>
            </div>

            <div style={{
              background: 'rgba(0,100,200,0.1)',
              padding: '1.5rem',
              borderRadius: '8px',
              border: '1px solid rgba(0,100,200,0.3)'
            }}>
              <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>使い方</h3>
              <p style={{ marginBottom: '0.5rem' }}>
                右側のチャットパネルからエージェントと対話できます。
              </p>
              <p style={{ opacity: 0.8 }}>
                試しに「今何時ですか?」と聞いてみてください。エージェントがツールを使って正確な時刻を返します。
              </p>
            </div>
          </div>
        </main>
      </CopilotSidebar>
    </CopilotKit>
  );
}
