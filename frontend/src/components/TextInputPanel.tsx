import { useState } from 'react'

interface TextInputPanelProps {
  onSubmit: (text: string) => void
  isLoading: boolean
  conversationMode: 'screening' | 'support_only'
  modelAvailable: boolean
}

export const TextInputPanel = ({ onSubmit, isLoading, conversationMode, modelAvailable }: TextInputPanelProps) => {
  const [text, setText] = useState('')
  const maxLength = 1500

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault()

    if (!text.trim() || isLoading) {
      return
    }

    onSubmit(text.trim())
    setText('')
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="rounded-[24px] border border-[var(--border-soft)] bg-[var(--card-muted)] p-4">
        <div className="mb-3 flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
          <label htmlFor="message" className="eyebrow block">
            Your message
          </label>
          <div className="text-xs leading-5 text-[var(--text-muted)] sm:max-w-[18rem] sm:text-right">
            MindSafe keeps this session in your browser only.
          </div>
        </div>
        <p className="mb-3 text-sm leading-6 text-[var(--text-secondary)]">
          {conversationMode === 'screening'
            ? 'Describe what is happening. You will receive a supportive reply, and the latest message may also be screened.'
            : 'Describe what is happening. Screening is currently unavailable, but MindSafe can still respond supportively.'}
        </p>
        <textarea
          id="message"
          value={text}
          onChange={(event) => setText(event.target.value)}
          placeholder={
            modelAvailable
              ? 'Example: I feel overwhelmed and do not know how to handle today.'
              : 'Example: I need a calm place to explain what has been weighing on me.'
          }
          maxLength={maxLength}
          rows={5}
          disabled={isLoading}
          className="min-h-[144px] w-full resize-none rounded-[18px] border border-transparent bg-[var(--card-strong)] px-4 py-4 text-[15px] leading-7 text-[var(--text-primary)] outline-none transition placeholder:text-[var(--text-muted)] focus:border-[var(--accent-strong)] disabled:opacity-60"
        />

        <div className="mt-3 flex items-center justify-between gap-3 text-xs leading-5 text-[var(--text-muted)]">
          <span>{conversationMode === 'screening' ? 'Screening + supportive reply' : 'Support-only reply'}</span>
          <span>{text.length} / {maxLength}</span>
        </div>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div className="text-sm leading-6 text-[var(--text-secondary)]">
          <p>{conversationMode === 'screening' ? 'Start by sharing what feels most important right now.' : 'Start by sharing what feels most important right now.'}</p>
          <p className="text-[var(--text-muted)]">If there is immediate danger in India, call 112 now.</p>
        </div>

        <button
          type="submit"
          disabled={!text.trim() || isLoading}
          className="inline-flex items-center justify-center rounded-full bg-[var(--accent-strong)] px-6 py-3 text-sm font-semibold text-white shadow-[0_14px_40px_rgba(47,125,115,0.24)] transition hover:translate-y-[-1px] hover:bg-[var(--accent-stronger)] disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isLoading ? 'Preparing response...' : conversationMode === 'screening' ? 'Review message' : 'Send message'}
        </button>
      </div>
    </form>
  )
}
