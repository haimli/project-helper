import api from './index'

export interface ChatSession {
  id: number
  project_id: number
  title: string
  created_at: string
}

export interface ChatMessage {
  id: number
  session_id: number
  role: 'user' | 'assistant' | 'tool'
  content: string
  tool_name: string | null
  tool_input: string | null
  created_at: string
}

export async function createSession(projectId: number): Promise<ChatSession> {
  const { data } = await api.post('/chat/sessions', { project_id: projectId })
  return data
}

export async function getSessions(projectId: number): Promise<ChatSession[]> {
  const { data } = await api.get('/chat/sessions', { params: { project_id: projectId } })
  return data.items
}

export async function getMessages(sessionId: number): Promise<ChatMessage[]> {
  const { data } = await api.get(`/chat/${sessionId}/messages`)
  return data.items
}
