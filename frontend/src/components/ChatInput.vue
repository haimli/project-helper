<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  send: [content: string]
}>()

const input = ref('')

function handleSubmit() {
  const content = input.value.trim()
  if (!content) return
  emit('send', content)
  input.value = ''
}
</script>

<template>
  <div class="chat-input">
    <textarea
      v-model="input"
      class="input-field"
      placeholder="Ask about this project's source code..."
      rows="1"
      @keydown.enter.exact.prevent="handleSubmit"
    />
    <button class="send-btn" :disabled="!input.trim()" @click="handleSubmit">
      ↑
    </button>
  </div>
</template>

<style scoped lang="scss">
.chat-input {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  padding: 12px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  transition: border-color var(--transition-normal);

  &:focus-within {
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px var(--accent-glow);
  }
}

.input-field {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-size: 14px;
  font-family: var(--font-sans);
  resize: none;
  max-height: 120px;
  line-height: 1.5;

  &::placeholder {
    color: var(--text-muted);
  }
}

.send-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: var(--bg-primary);
  border: none;
  border-radius: 50%;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all var(--transition-fast);

  &:hover:not(:disabled) {
    transform: scale(1.1);
    box-shadow: 0 0 12px var(--accent-glow-strong);
  }

  &:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }
}
</style>
