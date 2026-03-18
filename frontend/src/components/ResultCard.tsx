import { DetectionResult } from '../types'

interface ResultCardProps {
  detection: DetectionResult | null
  status: 'screened' | 'model_unavailable' | null
}

export const ResultCard = ({ detection, status }: ResultCardProps) => {
  if (!detection || status !== 'screened') {
    return (
      <section className="panel-surface p-5 sm:p-6">
        <p className="eyebrow mb-2">Screening summary</p>
        <h2 className="text-lg font-semibold tracking-[-0.02em] text-[var(--text-primary)]">No screening result yet.</h2>
        <p className="mt-3 text-sm leading-7 text-[var(--text-secondary)]">A brief summary will appear here after you send a message.</p>
      </section>
    )
  }

  const confidencePercent = Math.round(detection.confidence * 100)
  const isHighRisk = detection.risk_level === 'high'

  return (
    <section className="panel-surface p-5 sm:p-6">
      <div className="mb-4 flex items-start justify-between gap-4">
        <div>
          <p className="eyebrow mb-2">Screening summary</p>
          <h2 className="text-lg font-semibold tracking-[-0.02em] text-[var(--text-primary)]">
            {isHighRisk ? 'The latest message may need urgent human support.' : 'The latest message did not show high-risk suicide language.'}
          </h2>
        </div>
        <span
          className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] ${
            isHighRisk ? 'bg-[var(--alert-soft)] text-[var(--alert-strong)]' : 'bg-[var(--support-soft)] text-[var(--support-strong)]'
          }`}
        >
          {isHighRisk ? 'Elevated risk' : 'Lower risk'}
        </span>
      </div>

      <p className="text-sm leading-7 text-[var(--text-secondary)]">{detection.summary}</p>

      <div className="mt-4 rounded-[18px] border border-[var(--border-soft)] bg-[var(--card-muted)] p-4">
        <div className="flex items-center justify-between gap-4 text-sm">
          <span className="font-medium text-[var(--text-primary)]">Model confidence</span>
          <span className="text-[var(--text-secondary)]">{confidencePercent}%</span>
        </div>
        <p className="mt-3 text-sm leading-7 text-[var(--text-secondary)]">{detection.recommended_action}</p>
      </div>
    </section>
  )
}
