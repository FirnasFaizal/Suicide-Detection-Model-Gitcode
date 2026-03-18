interface HeaderProps {
  mode: 'screening' | 'support_only'
}

export const Header = ({ mode }: HeaderProps) => {
  return (
    <header className="mb-6 rounded-[28px] border border-[var(--border-soft)] bg-[var(--card-strong)] p-5 shadow-[0_12px_36px_rgba(22,34,34,0.06)] sm:p-7 lg:mb-7">
      <div className="flex flex-col gap-5">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
          <div className="max-w-3xl">
            <p className="eyebrow mb-3">MindSafe</p>
            <h1 className="font-display text-[2.25rem] leading-tight tracking-[-0.03em] text-[var(--text-primary)] sm:text-[3rem]">
              A calmer space to talk and find help quickly.
            </h1>
            <p className="mt-3 max-w-2xl text-sm leading-7 text-[var(--text-secondary)] sm:text-base">
              Share what is happening in your own words. MindSafe keeps the conversation simple, shows help clearly, and uses the pretrained model only for screening.
            </p>
          </div>

          <div className="rounded-[20px] border border-[var(--border-soft)] bg-[var(--card-muted)] px-4 py-4 text-sm text-[var(--text-secondary)]">
            <p className="eyebrow mb-2">Current mode</p>
            <p className="font-semibold text-[var(--text-primary)]">
              {mode === 'screening' ? 'Screening and support' : 'Support-only mode'}
            </p>
            <p className="mt-2 max-w-[16rem] leading-6">
              {mode === 'screening'
                ? 'The latest message is screened, then a supportive reply follows.'
                : 'Supportive conversation remains available while screening is offline.'}
            </p>
          </div>
        </div>

        <div className="rounded-[22px] border border-[var(--alert-border)] bg-[var(--alert-soft)]/55 px-4 py-4 sm:px-5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[var(--alert-strong)]">If you need urgent help in India</p>
              <p className="mt-2 text-sm leading-6 text-[var(--text-primary)] sm:text-[15px]">
                Call <span className="font-semibold">112</span> for emergency help, <span className="font-semibold">14416</span> for Tele-MANAS, or <span className="font-semibold">9152987821</span> for iCall.
              </p>
            </div>

            <a
              href="tel:112"
              className="inline-flex items-center justify-center rounded-full bg-[var(--alert-strong)] px-4 py-2 text-sm font-semibold text-white transition hover:opacity-95"
            >
              Call 112 now
            </a>
          </div>
        </div>
      </div>
    </header>
  )
}
