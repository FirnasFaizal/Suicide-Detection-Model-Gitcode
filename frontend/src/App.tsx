import { useEffect, useMemo, useState } from 'react'
import { ErrorBoundary } from './components/ErrorBoundary'
import { Header } from './components/Header'
import { ConversationPanel } from './components/ConversationPanel'
import { LoadingState } from './components/LoadingState'
import { ResponsePanel } from './components/ResponsePanel'
import { ResultCard } from './components/ResultCard'
import { StatusBanner } from './components/StatusBanner'
import { SupportResources } from './components/SupportResources'
import { TextInputPanel } from './components/TextInputPanel'
import { ThemeToggle } from './components/ThemeToggle'
import { ThemeProvider } from './contexts/ThemeContext'
import { analyzeText, getHealth } from './lib/api'
import { AnalyzeResponse, ChatMessage, HealthResponse } from './types'

function createMessage(role: ChatMessage['role'], content: string, tone?: ChatMessage['tone'], meta?: string): ChatMessage {
  return {
    id: `${role}-${Date.now()}-${Math.random().toString(16).slice(2)}`,
    role,
    content,
    tone,
    meta,
  }
}

const defaultResources = [
  {
    title: 'Emergency services',
    contact: 'Call 112 (India emergency response)',
    description: 'Use this immediately if there is imminent danger or you may act on self-harm thoughts.',
  },
  {
    title: 'Tele-MANAS',
    contact: 'Call 14416 or 1-800-891-4416',
    description: '24/7 India mental health helpline for immediate emotional support and guidance.',
  },
  {
    title: 'AASRA',
    contact: 'Call +91 22 27546669',
    description: '24/7 suicide prevention and emotional crisis support in India.',
  },
  {
    title: 'iCall',
    contact: 'Call 9152987821 (India)',
    description: 'Mental health counseling and emotional support line.',
  },
]

function AppContent() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [latestResponse, setLatestResponse] = useState<AnalyzeResponse | null>(null)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadHealth = async () => {
      try {
        const response = await getHealth()
        setHealth(response)
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Unable to connect to the support service right now.'
        setError(message)
      }
    }

    void loadHealth()
  }, [])

  const resourceList = useMemo(() => latestResponse?.support_resources || defaultResources, [latestResponse])

  const screeningState = latestResponse?.status === 'screened' ? latestResponse.detection?.risk_level ?? 'lower' : null

  const handleAnalyze = async (text: string) => {
    const userMessage = createMessage('user', text)
    const nextConversation = [...messages, userMessage]

    setMessages(nextConversation)
    setIsLoading(true)
    setError(null)

    try {
      const response = await analyzeText({
        text,
        conversation: nextConversation.slice(-6).map(({ role, content }) => ({ role, content })),
      })

      setLatestResponse(response)
      setHealth((current) =>
        current
          ? {
              ...current,
              model_available: response.model_available,
              status_headline: response.status_headline,
              model_status_message: response.model_status_message,
              conversation_mode: response.conversation_mode,
            }
          : {
              status: 'healthy',
              model_available: response.model_available,
              status_headline: response.status_headline,
              model_status_message: response.model_status_message,
              llm_provider: 'llm',
              llm_available: true,
              llm_status_message: 'Supportive response service is available.',
              conversation_mode: response.conversation_mode,
            },
      )

      const meta =
        response.status === 'model_unavailable'
          ? 'Support-only reply'
          : response.detection?.risk_level === 'high'
            ? 'Screened - urgent support guidance'
            : 'Screened reply'

      setMessages((current) => [
        ...current,
        createMessage(
          'assistant',
          response.assistant_message,
          response.status === 'model_unavailable' ? 'system' : response.detection?.risk_level === 'high' ? 'caution' : 'default',
          meta,
        ),
      ])
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Something went wrong. Please try again.'
      setError(message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text-primary)] transition-colors duration-300">
      <div className="pointer-events-none fixed inset-0 bg-[linear-gradient(180deg,rgba(96,133,129,0.08),transparent_22%)]" />
      <ThemeToggle />

      <main className="relative mx-auto flex min-h-screen w-full max-w-6xl flex-col px-4 py-4 sm:px-6 lg:px-8 lg:py-6">
        <Header mode={health?.conversation_mode ?? 'screening'} />

        <div className="grid gap-5 lg:grid-cols-[minmax(0,1.4fr)_minmax(310px,0.82fr)] lg:items-start">
          <section className="panel-surface flex min-h-[720px] flex-col overflow-hidden">
            <StatusBanner health={health} error={error} response={latestResponse} />

            <div className="flex-1 px-4 py-4 sm:px-6">
              <ConversationPanel messages={messages} isLoading={isLoading} conversationMode={health?.conversation_mode} />
            </div>

            {isLoading && <LoadingState mode={health?.conversation_mode ?? 'screening'} />}

            <div className="border-t border-[var(--border-soft)] bg-[var(--card-strong)]/75 p-4 sm:p-6">
              <TextInputPanel
                onSubmit={handleAnalyze}
                isLoading={isLoading}
                conversationMode={health?.conversation_mode ?? 'screening'}
                modelAvailable={health?.model_available ?? true}
              />
            </div>
          </section>

          <aside className="space-y-4 lg:sticky lg:top-6">
            <SupportResources resources={resourceList} emphasizeUrgent={screeningState === 'high'} />

            <ResponsePanel response={latestResponse} />

            <ResultCard detection={latestResponse?.detection ?? null} status={latestResponse?.status ?? null} />
          </aside>
        </div>
      </main>
    </div>
  )
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <AppContent />
      </ThemeProvider>
    </ErrorBoundary>
  )
}

export default App
