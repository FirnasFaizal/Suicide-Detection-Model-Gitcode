interface LoadingStateProps {
  mode: 'screening' | 'support_only'
}

export const LoadingState = ({ mode }: LoadingStateProps) => {
  return (
    <div className="border-t border-[var(--border-soft)] bg-[var(--card-muted)]/85 px-4 py-4 sm:px-6">
      <div className="flex items-center gap-4 rounded-[22px] border border-[var(--border-soft)] bg-[var(--card-strong)] px-4 py-4 shadow-sm">
        <div className="relative h-10 w-10 flex-shrink-0">
          <div className="absolute inset-0 rounded-full border-2 border-[var(--border-strong)]" />
          <div className="absolute inset-0 animate-spin rounded-full border-2 border-[var(--accent-strong)] border-t-transparent" />
        </div>
        <div>
          <p className="font-semibold text-[var(--text-primary)]">
            {mode === 'screening' ? 'Reviewing your message and preparing a supportive reply' : 'Preparing a supportive response'}
          </p>
          <p className="text-sm text-[var(--text-secondary)]">
            {mode === 'screening'
              ? 'The classifier is being checked first, then the assistant response is drafted.'
              : 'MindSafe is staying in support-only mode because screening is temporarily unavailable.'}
          </p>
        </div>
      </div>
    </div>
  )
}
