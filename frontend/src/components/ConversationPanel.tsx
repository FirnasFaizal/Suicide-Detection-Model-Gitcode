import { ChatMessage } from '../types'
import { EmptyState } from './EmptyState'

interface ConversationPanelProps {
  messages: ChatMessage[]
  isLoading: boolean
  conversationMode?: 'screening' | 'support_only'
}

const bubbleClass: Record<NonNullable<ChatMessage['tone']>, string> = {
  default: 'bg-[var(--card-strong)] text-[var(--text-primary)] border border-[var(--border-soft)]',
  caution: 'bg-[var(--alert-soft)]/85 text-[var(--text-primary)] border border-[var(--alert-border)]',
  system: 'bg-[var(--support-soft)] text-[var(--text-primary)] border border-[var(--support-border)]',
}

export const ConversationPanel = ({ messages, isLoading, conversationMode }: ConversationPanelProps) => {
  if (!messages.length) {
    return <EmptyState conversationMode={conversationMode ?? 'screening'} />
  }

  return (
    <div className="flex h-full max-h-[34rem] flex-col gap-5 overflow-y-auto pr-1">
      {messages.map((message) => {
        const isUser = message.role === 'user'

        return (
          <article key={message.id} className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-[92%] rounded-[22px] px-4 py-4 sm:max-w-[84%] ${
                isUser ? 'bg-[var(--accent-soft)] text-[var(--text-primary)] border border-[var(--support-border)]' : bubbleClass[message.tone || 'default']
              }`}
            >
              <div className="mb-2 flex flex-wrap items-center gap-2 text-[11px] uppercase tracking-[0.18em] opacity-65">
                <span>{isUser ? 'You' : 'MindSafe'}</span>
                {message.meta ? <span className="normal-case tracking-normal opacity-80">{message.meta}</span> : null}
              </div>
              <p className="whitespace-pre-wrap text-sm leading-7 sm:text-[15px]">{message.content}</p>
            </div>
          </article>
        )
      })}

      {isLoading ? (
        <div className="flex justify-start">
          <div className="rounded-[22px] border border-[var(--border-soft)] bg-[var(--card-strong)] px-4 py-3">
            <div className="flex items-center gap-2 text-sm text-[var(--text-secondary)]">
              <span className="h-2 w-2 animate-pulse rounded-full bg-[var(--accent-strong)]" />
              <span className="h-2 w-2 animate-pulse rounded-full bg-[var(--accent-strong)] [animation-delay:120ms]" />
              <span className="h-2 w-2 animate-pulse rounded-full bg-[var(--accent-strong)] [animation-delay:240ms]" />
              <span className="ml-2">Preparing a careful response...</span>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  )
}
