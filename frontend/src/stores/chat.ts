import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  createSession,
  getSessions,
  getMessages,
  type ChatSession,
  type ChatMessage,
} from '../api/chat'

export interface StreamMessage {
  type: 'token' | 'tool_call' | 'tool_result' | 'done' | 'error'
  content?: string
  tool?: string
  input?: any
  output?: string
  detail?: string
}

export const useChatStore = defineStore('chat', () => {
  const sessions = ref<ChatSession[]>([])
  const currentSession = ref<ChatSession | null>(null)
  const messages = ref<ChatMessage[]>([])
  const streamTokens = ref('')
  const toolCalls = ref<StreamMessage[]>([])
  const isStreaming = ref(false)
  const loading = ref(false)

  async function fetchSessions(projectId: number) {
    loading.value = true
    try {
      sessions.value = await getSessions(projectId)
    } finally {
      loading.value = false
    }
  }

  async function newSession(projectId: number) {
    const session = await createSession(projectId)
    currentSession.value = session
    messages.value = []
    streamTokens.value = ''
    toolCalls.value = []
    return session
  }

  async function fetchMessages(sessionId: number) {
    loading.value = true
    try {
      messages.value = await getMessages(sessionId)
    } finally {
      loading.value = false
    }
  }

  function handleStreamEvent(event: { event: string; data: any }) {
    if (event.event === 'token') {
      streamTokens.value += event.data.content || ''
      isStreaming.value = true
    } else if (event.event === 'tool_call') {
      toolCalls.value.push({
        type: 'tool_call',
        tool: event.data.tool,
        input: event.data.input,
      })
    } else if (event.event === 'tool_result') {
      toolCalls.value.push({
        type: 'tool_result',
        tool: event.data.tool,
        output: event.data.output,
      })
    } else if (event.event === 'done') {
      isStreaming.value = false
    } else if (event.event === 'error') {
      isStreaming.value = false
      streamTokens.value += `\n\n**Error:** ${event.data.detail}`
    }
  }

  function finalizeMessage() {
    if (streamTokens.value) {
      messages.value.push({
        id: Date.now(),
        session_id: currentSession.value?.id || 0,
        role: 'assistant',
        content: streamTokens.value,
        tool_name: null,
        tool_input: null,
        created_at: new Date().toISOString(),
      })
    }
    streamTokens.value = ''
    toolCalls.value = []
    isStreaming.value = false
  }

  function reset() {
    currentSession.value = null
    messages.value = []
    streamTokens.value = ''
    toolCalls.value = []
    isStreaming.value = false
  }

  return {
    sessions,
    currentSession,
    messages,
    streamTokens,
    toolCalls,
    isStreaming,
    loading,
    fetchSessions,
    newSession,
    fetchMessages,
    handleStreamEvent,
    finalizeMessage,
    reset,
  }
})
