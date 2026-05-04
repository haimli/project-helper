<script setup lang="ts">
import { onMounted, nextTick, ref } from 'vue'
import ChatMessage from '../components/ChatMessage.vue'
import ChatInput from '../components/ChatInput.vue'
import ToolCallBlock from '../components/ToolCallBlock.vue'
import { useChatStore } from '../stores/chat'
import { useProjectStore } from '../stores/project'
import { createSSEConnection } from '../utils/sse'
import { renderMarkdown } from '../utils/markdown'
import '../styles/markdown.scss'

const props = defineProps<{ projectId: string }>()
const chatStore = useChatStore()
const projectStore = useProjectStore()
const messagesContainer = ref<HTMLElement>()
const projectIdNum = ref(parseInt(props.projectId))
let abortController: AbortController | null = null

onMounted(async () => {
  await chatStore.fetchSessions(projectIdNum.value)
  if (chatStore.sessions.length === 0) {
    await chatStore.newSession(projectIdNum.value)
  } else {
    chatStore.currentSession = chatStore.sessions[0]
    await chatStore.fetchMessages(chatStore.currentSession.id)
  }
})

async function handleSend(content: string) {
  if (!chatStore.currentSession) {
    await chatStore.newSession(projectIdNum.value)
  }

  chatStore.messages.push({
    id: Date.now() - 1,
    session_id: chatStore.currentSession!.id,
    role: 'user',
    content,
    tool_name: null,
    tool_input: null,
    created_at: new Date().toISOString(),
  })

  chatStore.streamTokens = ''
  chatStore.toolCalls = []
  chatStore.isStreaming = true

  await nextTick()
  scrollToBottom()

  const url = `/api/chat/${chatStore.currentSession!.id}/messages`
  abortController = createSSEConnection(
    url,
    { content },
    (event) => {
      chatStore.handleStreamEvent(event)
      nextTick(() => scrollToBottom())
    },
    (err) => {
      console.error('Chat SSE error:', err)
      chatStore.isStreaming = false
    },
  )

  // Wait for stream to finish (poll)
  const checkDone = setInterval(() => {
    if (!chatStore.isStreaming) {
      clearInterval(checkDone)
      chatStore.finalizeMessage()
    }
  }, 500)
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

function handleNewSession() {
  chatStore.reset()
  chatStore.newSession(projectIdNum.value)
}
</script>

<template>
  <div class="chat-view">
    <div class="chat-header">
      <h2>Chat with Code</h2>
      <button class="new-session-btn" @click="handleNewSession">+ New Chat</button>
    </div>

    <div ref="messagesContainer" class="messages-container">
      <div v-if="chatStore.messages.length === 0 && !chatStore.isStreaming" class="empty-state">
        <p>Ask a question about this project's source code.</p>
        <div class="suggestions">
          <button @click="handleSend('What does the main entry point of this project do?')">What does the main entry point do?</button>
          <button @click="handleSend('Explain the overall architecture of this project')">Explain the architecture</button>
          <button @click="handleSend('How does the data flow through the system?')">How does data flow?</button>
        </div>
      </div>

      <template v-else>
        <ChatMessage
          v-for="msg in chatStore.messages"
          :key="msg.id"
          :message="msg"
        />

        <!-- Tool calls during streaming -->
        <ToolCallBlock
          v-if="chatStore.toolCalls.length"
          :events="chatStore.toolCalls"
        />

        <!-- Streaming response -->
        <div v-if="chatStore.isStreaming && chatStore.streamTokens" class="streaming-message">
          <div class="message-avatar">AI</div>
          <div class="message-body">
            <div class="message-role">Assistant</div>
            <div class="message-text markdown-body typing-cursor" v-html="renderMarkdown(chatStore.streamTokens)" />
          </div>
        </div>
      </template>
    </div>

    <div class="input-container">
      <ChatInput @send="handleSend" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.chat-view {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 108px);
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-card);

  h2 {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
  }
}

.new-session-btn {
  font-size: 13px;
  padding: 6px 14px;
  background: transparent;
  color: var(--accent-primary);
  border: 1px solid var(--accent-primary);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);

  &:hover {
    background: var(--accent-glow);
  }
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-muted);

  p {
    font-size: 16px;
    margin-bottom: 20px;
  }
}

.suggestions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: center;

  button {
    padding: 8px 16px;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    color: var(--text-secondary);
    font-size: 13px;
    cursor: pointer;
    transition: all var(--transition-fast);

    &:hover {
      border-color: var(--accent-primary);
      color: var(--accent-primary);
    }
  }
}

.streaming-message {
  display: flex;
  gap: 12px;
  padding: 16px 0;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
  background: var(--bg-card);
  color: var(--accent-primary);
  border: 1px solid var(--border-color);
}

.message-body {
  display: flex;
  flex-direction: column;
  max-width: 80%;
}

.message-role {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.message-text {
  padding: 12px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm) var(--radius-md) var(--radius-md) var(--radius-sm);
  font-size: 14px;
  line-height: 1.6;
}

.input-container {
  padding: 12px 20px 16px;
  border-top: 1px solid var(--border-color);
  background: var(--bg-card);
}
</style>
