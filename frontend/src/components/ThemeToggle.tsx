import { useTheme } from '../contexts/ThemeContext'

export const ThemeToggle = () => {
  const { theme, toggleTheme } = useTheme()

  return (
    <button
      onClick={toggleTheme}
      className="fixed right-4 top-4 z-50 inline-flex h-12 w-12 items-center justify-center rounded-full border border-[var(--border-soft)] bg-[var(--card-strong)]/92 text-[var(--text-primary)] shadow-[0_16px_40px_rgba(22,34,34,0.12)] backdrop-blur transition hover:translate-y-[-1px] sm:right-6 sm:top-6"
      aria-label="Toggle theme"
    >
      {theme === 'light' ? (
        <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M21 12.79A9 9 0 1 1 11.21 3c0 .2-.01.39-.01.59A7.79 7.79 0 0 0 21 12.79Z" />
        </svg>
      ) : (
        <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M12 3v1.5m0 15V21m9-9h-1.5M4.5 12H3m14.36 6.36-1.06-1.06M7.7 7.7 6.64 6.64m10.72 0L16.3 7.7M7.7 16.3l-1.06 1.06M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" />
        </svg>
      )}
    </button>
  )
}
