import { SupportResource } from '../types'

interface SupportResourcesProps {
  resources: SupportResource[]
  emphasizeUrgent?: boolean
}

const indiaUrgentResources = [
  {
    title: 'Emergency response',
    contact: '112',
    href: 'tel:112',
    description: 'Call immediately if there is immediate danger or you may act on self-harm thoughts.',
  },
  {
    title: 'Tele-MANAS',
    contact: '14416 / 1-800-891-4416',
    href: 'tel:14416',
    description: '24/7 India mental health helpline for urgent emotional support and referral guidance.',
  },
  {
    title: 'iCall',
    contact: '9152987821',
    href: 'tel:9152987821',
    description: 'India mental health support and counseling helpline.',
  },
  {
    title: 'AASRA',
    contact: '+91 22 27546669',
    href: 'tel:+912227546669',
    description: '24/7 suicide prevention and emotional crisis support.',
  },
]

export const SupportResources = ({ resources, emphasizeUrgent = false }: SupportResourcesProps) => {
  return (
    <section className="panel-surface p-5 sm:p-6">
      <p className="eyebrow mb-2">Get help now</p>
      <h2 className="text-lg font-semibold tracking-[-0.02em] text-[var(--text-primary)]">
        {emphasizeUrgent ? 'Please reach a person or helpline in India right away.' : 'Keep immediate support close by.'}
      </h2>
      <p className="mt-3 text-sm leading-7 text-[var(--text-secondary)]">
        If you feel unsafe, do not stay alone with it. Call now, or ask someone nearby to stay with you while you call.
      </p>

      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        {indiaUrgentResources.map((resource) => (
          <a
            key={resource.title}
            href={resource.href}
            className={`rounded-[18px] border p-4 transition ${
              resource.contact === '112' || emphasizeUrgent
                ? 'border-[var(--alert-border)] bg-[var(--alert-soft)]/60'
                : 'border-[var(--border-soft)] bg-[var(--card-muted)]'
            }`}
          >
            <p className="text-sm font-semibold text-[var(--text-primary)]">{resource.title}</p>
            <p className="mt-1 text-base font-semibold text-[var(--accent-strong)]">{resource.contact}</p>
            <p className="mt-2 text-sm leading-6 text-[var(--text-secondary)]">{resource.description}</p>
          </a>
        ))}
      </div>

      <div className="mt-5 rounded-[18px] border border-[var(--border-soft)] bg-[var(--ink-soft)] p-4">
        <p className="text-sm font-semibold text-[var(--text-primary)]">Simple next steps</p>
        <div className="mt-3 space-y-2 text-sm leading-6 text-[var(--text-secondary)]">
          <p>1. Move closer to another person if you can.</p>
          <p>2. Call <span className="font-semibold text-[var(--text-primary)]">112</span> or <span className="font-semibold text-[var(--text-primary)]">14416</span>.</p>
          <p>3. Tell someone directly: “I do not feel safe being alone right now.”</p>
        </div>
      </div>

      <div className="mt-5 border-t border-[var(--border-soft)] pt-5">
        <p className="eyebrow mb-2">More support</p>
        <div className="space-y-3">
          {resources.map((resource) => (
            <article key={resource.title} className="rounded-[16px] bg-[var(--card-muted)] px-4 py-3">
              <h3 className="font-medium text-[var(--text-primary)]">{resource.title}</h3>
              <p className="mt-1 text-sm font-medium text-[var(--accent-strong)]">{resource.contact}</p>
              <p className="mt-1 text-sm leading-6 text-[var(--text-secondary)]">{resource.description}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
