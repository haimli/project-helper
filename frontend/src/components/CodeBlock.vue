<script setup lang="ts">
import { computed, ref } from 'vue'
import hljs from 'highlight.js'

const props = defineProps<{
  code: string
  language?: string
}>()

const copied = ref(false)

const highlighted = computed(() => {
  const lang = props.language && hljs.getLanguage(props.language) ? props.language : 'plaintext'
  return hljs.highlight(props.code, { language: lang }).value
})

function copyCode() {
  navigator.clipboard.writeText(props.code)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}
</script>

<template>
  <div class="code-block-wrapper">
    <div class="code-header">
      <span class="code-lang">{{ language || 'code' }}</span>
      <button class="copy-btn" @click="copyCode">
        {{ copied ? 'Copied!' : 'Copy' }}
      </button>
    </div>
    <pre class="code-content"><code class="hljs" v-html="highlighted" /></pre>
  </div>
</template>

<style scoped lang="scss">
.code-block-wrapper {
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  overflow: hidden;
  margin: 8px 0;
}

.code-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 12px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.code-lang {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-muted);
  text-transform: uppercase;
}

.copy-btn {
  font-size: 12px;
  color: var(--text-muted);
  background: none;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 2px 8px;
  cursor: pointer;
  transition: all var(--transition-fast);

  &:hover {
    color: var(--accent-primary);
    border-color: var(--accent-primary);
  }
}

.code-content {
  padding: 16px;
  overflow-x: auto;
  margin: 0;
  background: var(--bg-code);

  code {
    font-family: var(--font-mono);
    font-size: 13px;
    line-height: 1.6;
  }
}
</style>
