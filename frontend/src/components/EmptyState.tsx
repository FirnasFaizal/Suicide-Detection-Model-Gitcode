interface EmptyStateProps {
  conversationMode: 'screening' | 'support_only'
}

export const EmptyState = ({ conversationMode }: EmptyStateProps) => {
  return (
    <div className="flex h-full flex-col justify-between rounded-[24px] border border-dashed border-[var(--border-soft)] bg-[var(--card-muted)] p-6 sm:p-8">
      <div>
        <p className="eyebrow mb-4">Start here</p>
        <h2 className="max-w-xl text-2xl font-semibold tracking-[-0.02em] text-[var(--text-primary)] sm:text-3xl">
          Share what feels most important right now.
        </h2>
        <p className="mt-4 max-w-2xl text-sm leading-7 text-[var(--text-secondary)] sm:text-base">
          {conversationMode === 'screening'
            ? 'You will receive a supportive reply, and the latest message may also be screened. Results are not a diagnosis.'
            : 'Screening is temporarily unavailable, but you can still use this space for supportive conversation.'}
        </p>
      </div>

      <div className="mt-8 grid gap-4 lg:grid-cols-3">
        <div className="rounded-[20px] border border-[var(--border-soft)] bg-[var(--card-strong)] p-4">
          <p className="eyebrow mb-2">1. Say what is happening</p>
          <p className="text-sm leading-7 text-[var(--text-secondary)]">You do not need perfect words. A few honest sentences are enough.</p>
        </div>
        <div className="rounded-[20px] border border-[var(--border-soft)] bg-[var(--card-strong)] p-4">
          <p className="eyebrow mb-2">2. Review the reply</p>
          <p className="text-sm leading-7 text-[var(--text-secondary)]">MindSafe will answer in a calm, supportive tone and show next-step guidance.</p>
        </div>
        <div className="rounded-[20px] border border-[var(--border-soft)] bg-[var(--card-strong)] p-4">
          <p className="eyebrow mb-2">3. Get urgent help fast</p>
          <p className="text-sm leading-7 text-[var(--text-secondary)]">If you may act on self-harm thoughts in India, call 112 or 14416 right away.</p>
        </div>
      </div>
    </div>
  )
}
