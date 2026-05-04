<script setup lang="ts">
import { ref } from 'vue'
import type { StreamMessage } from '../stores/chat'

defineProps<{
  events: StreamMessage[]
}>()

const expanded = ref<Record<number, boolean>>({})

function toggle(index: number) {
  expanded.value[index] = !expanded.value[index]
}
</script>

<template>
  <div class="tool-call-block">
    <div v-for="(event, index) in events" :key="index" class="tool-event">
      <template v-if="event.type === 'tool_call'">
        <div class="tool-header" @click="toggle(index)">
          <span class="tool-icon">⚙</span>
          <span class="tool-name">{{ event.tool }}</span>
          <span class="tool-toggle">{{ expanded[index] ? '▼' : '▶' }}</span>
        </div>
        <div v-if="expanded[index]" class="tool-detail">
          <pre>{{ JSON.stringify(event.input, null, 2) }}</pre>
        </div>
      </template>
      <template v-else-if="event.type === 'tool_result'">
        <div class="tool-header result" @click="toggle(index)">
          <span class="tool-icon">✓</span>
          <span class="tool-name">Result: {{ event.tool }}</span>
          <span class="tool-toggle">{{ expanded[index] ? '▼' : '▶' }}</span>
        </div>
        <div v-if="expanded[index]" class="tool-detail">
          <pre>{{ event.output }}</pre>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped lang="scss">
.tool-call-block {
  margin: 8px 0;
}

.tool-event {
  margin-bottom: 4px;
}

.tool-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 13px;
  transition: background var(--transition-fast);

  &:hover {
    background: var(--bg-card-hover);
  }

  &.result {
    border-color: rgba(52, 211, 153, 0.3);

    .tool-icon {
      color: var(--success);
    }
  }
}

.tool-icon {
  font-size: 14px;
  color: var(--accent-secondary);
}

.tool-name {
  flex: 1;
  font-family: var(--font-mono);
  color: var(--text-secondary);
}

.tool-toggle {
  color: var(--text-muted);
  font-size: 11px;
}

.tool-detail {
  margin-top: 4px;
  padding: 8px 12px;
  background: var(--bg-code);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  overflow-x: auto;

  pre {
    font-family: var(--font-mono);
    font-size: 12px;
    line-height: 1.5;
    color: var(--text-secondary);
    margin: 0;
    white-space: pre-wrap;
    word-break: break-all;
  }
}
</style>
