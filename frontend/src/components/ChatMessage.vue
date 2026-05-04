<script setup lang="ts">
import { computed } from 'vue'
import type { ChatMessage as ChatMessageType } from '../api/chat'
import { renderMarkdown } from '../utils/markdown'
import '../styles/markdown.scss'

const props = defineProps<{
  message: ChatMessageType
}>()

const isUser = computed(() => props.message.role === 'user')
const isTool = computed(() => props.message.role === 'tool')
const contentHtml = computed(() => {
  if (isUser.value) return props.message.content
  return renderMarkdown(props.message.content)
})
</script>

<template>
  <div class="chat-message" :class="{ 'is-user': isUser, 'is-tool': isTool }">
    <div class="message-avatar">
      <template v-if="isUser">U</template>
      <template v-else-if="isTool">T</template>
      <template v-else>AI</template>
    </div>
    <div class="message-body">
      <div class="message-role">
        <template v-if="isUser">You</template>
        <template v-else-if="isTool">Tool: {{ message.tool_name }}</template>
        <template v-else>Assistant</template>
      </div>
      <div v-if="isUser" class="message-text">{{ message.content }}</div>
      <div v-else class="message-text markdown-body" v-html="contentHtml" />
      <div v-if="isTool && message.tool_input" class="tool-input">
        <strong>Input:</strong> {{ message.tool_input }}
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.chat-message {
  display: flex;
  gap: 12px;
  padding: 16px 0;

  &.is-user {
    flex-direction: row-reverse;

    .message-body {
      align-items: flex-end;
    }

    .message-text {
      background: var(--accent-primary);
      color: var(--bg-primary);
      border-radius: var(--radius-md) var(--radius-sm) var(--radius-sm) var(--radius-md);
    }
  }
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

  .is-user & {
    background: var(--accent-primary);
    color: var(--bg-primary);
  }

  .is-tool & {
    background: var(--accent-secondary);
    color: white;
  }
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

.tool-input {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 4px;
  padding: 4px 8px;
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
}
</style>
