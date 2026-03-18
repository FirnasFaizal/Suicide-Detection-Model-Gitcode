import { AnalyzeRequestPayload, AnalyzeResponse, ApiError, HealthResponse } from '../types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

async function parseJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let message = 'Something went wrong. Please try again.'

    try {
      const errorData = (await response.json()) as ApiError
      message = errorData.detail || errorData.message || message
    } catch {
      message = response.statusText || message
    }

    throw new Error(message)
  }

  return (await response.json()) as T
}

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`)
  return parseJson<HealthResponse>(response)
}

export async function analyzeText(payload: AnalyzeRequestPayload): Promise<AnalyzeResponse> {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  return parseJson<AnalyzeResponse>(response)
}
