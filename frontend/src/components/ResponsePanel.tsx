import { AnalyzeResponse } from '../types'

interface ResponsePanelProps {
  response: AnalyzeResponse | null
}

export const ResponsePanel = ({ response }: ResponsePanelProps) => {
  if (!response) {
    return (
      <section className="panel-surface p-5 sm:p-6">
        <p className="eyebrow mb-2">Latest guidance</p>
        <h2 className="text-lg font-semibold tracking-[-0.02em] text-[var(--text-primary)]">A supportive reply will appear here.</h2>
        <p className="mt-3 text-sm leading-7 text-[var(--text-secondary)]">This space keeps the latest guidance easy to review without adding extra clutter.</p>
      </section>
    )
  }

  const isSupportOnly = response.status === 'model_unavailable'
  const isHighRisk = response.detection?.risk_level === 'high'

  return (
    <section className="panel-surface p-5 sm:p-6">
      <div className="mb-4 flex items-start justify-between gap-4">
        <div>
          <p className="eyebrow mb-2">Latest guidance</p>
          <h2 className="text-lg font-semibold tracking-[-0.02em] text-[var(--text-primary)]">{response.guidance_title}</h2>
        </div>
        <span
          className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] ${
            isSupportOnly
              ? 'bg-[var(--support-soft)] text-[var(--support-strong)]'
              : isHighRisk
                ? 'bg-[var(--alert-soft)] text-[var(--alert-strong)]'
                : 'bg-[var(--accent-soft)] text-[var(--accent-strong)]'
          }`}
        >
          {isSupportOnly ? 'Support only' : isHighRisk ? 'Urgent support' : 'Screened'}
        </span>
      </div>

      <div className="rounded-[18px] border border-[var(--border-soft)] bg-[var(--card-muted)] p-4">
        <p className="whitespace-pre-wrap text-sm leading-7 text-[var(--text-primary)] sm:text-[15px]">
          {response.assistant_message}
        </p>
      </div>

      <div className="mt-4 rounded-[18px] border border-[var(--border-soft)] bg-[var(--ink-soft)] px-4 py-4 text-sm leading-7 text-[var(--text-secondary)]">
        <p className="font-semibold text-[var(--text-primary)]">Care note</p>
        <p className="mt-1">{response.care_recommendation}</p>
      </div>

      <div className="mt-3 rounded-[18px] bg-[var(--ink-soft)] px-4 py-4 text-sm leading-7 text-[var(--text-secondary)]">
        <p className="font-semibold text-[var(--text-primary)]">Service note</p>
        <p className="mt-1">{response.model_status_message}</p>
      </div>

      <p className="mt-4 text-xs leading-6 text-[var(--text-muted)]">{response.disclaimer}</p>
    </section>
  )
}
