'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';

interface ToolCall {
  tool_name: string;
  arguments: Record<string, unknown>;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  toolCalls?: ToolCall[];
}

// Strip any /api/v1 suffix so we can build /api/{user_id}/chat correctly.
// NEXT_PUBLIC_API_URL may be set to "https://host/api/v1" (Phase II convention)
// but the chat endpoint lives at /api/{user_id}/chat (no /v1).
const _rawBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_BASE = _rawBase.replace(/\/api\/v1\/?$/, '');

export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Get JWT and user_id from localStorage.
  // The app stores only 'auth_token' — user_id is decoded from the JWT payload (sub claim).
  const getAuthInfo = (): { token: string; userId: number } | null => {
    if (typeof window === 'undefined') return null;
    const token = localStorage.getItem('auth_token');
    if (!token) return null;
    try {
      // JWT is three base64url parts separated by '.' — the payload is the middle part
      const payloadB64 = token.split('.')[1];
      if (!payloadB64) return null;
      // base64url → base64 → JSON
      const payload = JSON.parse(atob(payloadB64.replace(/-/g, '+').replace(/_/g, '/')));
      const userId = parseInt(payload.sub, 10);
      if (isNaN(userId)) return null;
      return { token, userId };
    } catch {
      return null;
    }
  };

  useEffect(() => {
    const auth = getAuthInfo();
    if (!auth) {
      router.push('/login');
    }
  }, [router]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;

    const auth = getAuthInfo();
    if (!auth) {
      router.push('/login');
      return;
    }

    setError(null);
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: trimmed }]);
    setIsLoading(true);

    try {
      const resp = await fetch(`${API_BASE}/api/${auth.userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${auth.token}`,
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: trimmed,
        }),
      });

      if (resp.status === 401) {
        localStorage.removeItem('auth_token');
        router.push('/login');
        return;
      }

      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${resp.status}`);
      }

      const data = await resp.json();
      setConversationId(data.conversation_id);
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: data.response,
          toolCalls: data.tool_calls?.length ? data.tool_calls : undefined,
        },
      ]);
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Something went wrong';
      setError(msg);
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: `⚠️ Error: ${msg}` },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <div style={styles.header}>
          <h1 style={styles.title}>Task Assistant</h1>
          <p style={styles.subtitle}>
            Manage your tasks with natural language
          </p>
        </div>

        <div style={styles.messageList}>
          {messages.length === 0 && (
            <div style={styles.emptyState}>
              <p>👋 Hi! I can help you manage your tasks.</p>
              <p style={styles.hint}>
                Try: &ldquo;Add a task to buy groceries&rdquo; or &ldquo;Show my tasks&rdquo;
              </p>
            </div>
          )}

          {messages.map((msg, i) => (
            <div
              key={i}
              style={{
                ...styles.bubble,
                ...(msg.role === 'user' ? styles.userBubble : styles.assistantBubble),
              }}
            >
              <div style={styles.bubbleLabel}>
                {msg.role === 'user' ? 'You' : 'Assistant'}
              </div>
              <div style={styles.bubbleContent}>{msg.content}</div>
              {msg.toolCalls && msg.toolCalls.length > 0 && (
                <div style={styles.toolCallBadge}>
                  🔧 {msg.toolCalls.map(tc => tc.tool_name).join(', ')}
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div style={{ ...styles.bubble, ...styles.assistantBubble }}>
              <div style={styles.bubbleLabel}>Assistant</div>
              <div style={styles.typing}>thinking…</div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        {error && <div style={styles.errorBanner}>{error}</div>}

        <div style={styles.inputRow}>
          <textarea
            style={styles.textarea}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a message… (Enter to send, Shift+Enter for new line)"
            rows={2}
            disabled={isLoading}
          />
          <button
            style={{
              ...styles.sendButton,
              ...(isLoading ? styles.sendButtonDisabled : {}),
            }}
            onClick={sendMessage}
            disabled={isLoading || !input.trim()}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  page: {
    minHeight: '100vh',
    backgroundColor: '#111827',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '1rem',
  },
  container: {
    width: '100%',
    maxWidth: '720px',
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
    height: 'calc(100vh - 120px)',
  },
  header: {
    textAlign: 'center',
  },
  title: {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    color: 'white',
    margin: 0,
  },
  subtitle: {
    color: '#9ca3af',
    fontSize: '0.875rem',
    marginTop: '0.25rem',
  },
  messageList: {
    flex: 1,
    overflowY: 'auto',
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
    padding: '1rem',
    backgroundColor: '#1f2937',
    borderRadius: '0.75rem',
  },
  emptyState: {
    textAlign: 'center',
    color: '#6b7280',
    padding: '2rem',
    lineHeight: '1.8',
  },
  hint: {
    fontSize: '0.875rem',
    fontStyle: 'italic',
  },
  bubble: {
    padding: '0.75rem 1rem',
    borderRadius: '0.75rem',
    maxWidth: '80%',
  },
  userBubble: {
    backgroundColor: '#3b82f6',
    color: 'white',
    alignSelf: 'flex-end',
  },
  assistantBubble: {
    backgroundColor: '#374151',
    color: '#f3f4f6',
    alignSelf: 'flex-start',
  },
  bubbleLabel: {
    fontSize: '0.7rem',
    fontWeight: '600',
    opacity: 0.7,
    marginBottom: '0.25rem',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
  },
  bubbleContent: {
    fontSize: '0.9rem',
    lineHeight: '1.5',
    whiteSpace: 'pre-wrap',
  },
  toolCallBadge: {
    marginTop: '0.5rem',
    fontSize: '0.7rem',
    color: '#60a5fa',
    opacity: 0.8,
  },
  typing: {
    color: '#9ca3af',
    fontStyle: 'italic',
    fontSize: '0.875rem',
  },
  errorBanner: {
    backgroundColor: '#7f1d1d',
    color: '#fca5a5',
    padding: '0.5rem 1rem',
    borderRadius: '0.5rem',
    fontSize: '0.875rem',
  },
  inputRow: {
    display: 'flex',
    gap: '0.75rem',
    alignItems: 'flex-end',
  },
  textarea: {
    flex: 1,
    padding: '0.75rem',
    borderRadius: '0.5rem',
    border: '1px solid #374151',
    backgroundColor: '#1f2937',
    color: 'white',
    fontSize: '0.9rem',
    resize: 'none',
    outline: 'none',
    fontFamily: 'inherit',
  },
  sendButton: {
    padding: '0.75rem 1.5rem',
    backgroundColor: '#3b82f6',
    color: 'white',
    border: 'none',
    borderRadius: '0.5rem',
    fontWeight: '600',
    cursor: 'pointer',
    fontSize: '0.875rem',
  },
  sendButtonDisabled: {
    backgroundColor: '#374151',
    cursor: 'not-allowed',
  },
};
