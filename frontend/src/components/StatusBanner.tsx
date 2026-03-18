import { AnalyzeResponse, HealthResponse } from '../types'

interface StatusBannerProps {
  health: HealthResponse | null
  error: string | null
  response: AnalyzeResponse | null
}

export const StatusBanner = ({ health, error, response }: StatusBannerProps) => {
  if (error) {
    return (
      <div className="border-b border-[var(--alert-border)] bg-[var(--alert-soft)]/80 px-4 py-4 text-sm text-[var(--text-primary)] sm:px-6">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[var(--alert-strong)]">Service issue</p>
        <p className="mt-2 font-semibold">MindSafe could not reach the backend service.</p>
        <p className="mt-1 leading-6 text-[var(--text-secondary)]">{error}</p>
      </div>
    )
  }

  if (!health) {
    return (
      <div className="border-b border-[var(--border-soft)] bg-[var(--card-muted)] px-4 py-4 text-sm text-[var(--text-secondary)] sm:px-6">
        Checking service readiness...
      </div>
    )
  }

  const isHighRisk = response?.detection?.risk_level === 'high'

  return (
    <div
      className={`border-b px-4 py-4 sm:px-6 ${
        isHighRisk
          ? 'border-[var(--alert-border)] bg-[var(--alert-soft)]/75'
          : health.model_available
            ? 'border-[var(--support-border)] bg-[var(--support-soft)]/70'
            : 'border-[var(--border-soft)] bg-[var(--card-muted)]'
      }`}
    >
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[var(--text-muted)]">What happens next</p>
          <p className="mt-2 font-semibold text-[var(--text-primary)]">{response?.status_headline || health.status_headline}</p>
          <p className="mt-1 text-sm leading-6 text-[var(--text-secondary)]">
            {isHighRisk ? response?.care_recommendation : health.model_status_message}
          </p>
        </div>

        <div className="rounded-full border border-[var(--border-soft)] bg-[var(--card-strong)] px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] text-[var(--text-secondary)]">
          {health.conversation_mode === 'screening' ? 'Screening active' : 'Support only'}
        </div>
      </div>
    </div>
  )
}
