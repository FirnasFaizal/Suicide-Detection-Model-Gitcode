import { Component, ReactNode } from 'react'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(): State {
    return { hasError: true }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex min-h-screen items-center justify-center bg-[var(--bg)] p-4 text-[var(--text-primary)]">
          <div className="panel-surface max-w-lg p-8 text-center">
            <p className="eyebrow mb-3">MindSafe</p>
            <h1 className="font-display text-4xl tracking-[-0.03em]">Something interrupted the session.</h1>
            <p className="mt-4 text-sm leading-7 text-[var(--text-secondary)]">
              Please refresh the page to continue. If you need urgent support right now, contact a local emergency service or crisis line immediately.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="mt-6 inline-flex rounded-full bg-[var(--accent-strong)] px-6 py-3 text-sm font-semibold text-white"
            >
              Refresh page
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
