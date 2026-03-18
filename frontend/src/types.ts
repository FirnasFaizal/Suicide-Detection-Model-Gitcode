export interface SupportResource {
  title: string
  contact: string
  description: string
}

export interface DetectionResult {
  label: 'suicide' | 'non-suicide'
  confidence: number
  risk_level: 'high' | 'lower'
  summary: string
  recommended_action: string
}

export interface AnalyzeResponse {
  status: 'screened' | 'model_unavailable'
  conversation_mode: 'screening' | 'support_only'
  model_available: boolean
  status_headline: string
  model_status_message: string
  assistant_message: string
  guidance_title: string
  care_recommendation: string
  disclaimer: string
  detection: DetectionResult | null
  support_resources: SupportResource[]
}

export interface HealthResponse {
  status: 'healthy'
  model_available: boolean
  status_headline: string
  model_status_message: string
  llm_provider: string
  llm_available: boolean
  llm_status_message: string
  conversation_mode: 'screening' | 'support_only'
}

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  tone?: 'default' | 'caution' | 'system'
  meta?: string
}

export interface AnalyzeRequestPayload {
  text: string
  conversation: Array<Pick<ChatMessage, 'role' | 'content'>>
}

export interface ApiError {
  detail?: string
  message?: string
}
