<script setup lang="ts">
defineProps<{
  events: { stage: string; progress: number; detail: string }[]
}>()

const stageLabels: Record<string, string> = {
  cloning: 'Cloning Repository',
  scanning: 'Scanning Directory',
  analyzing_tech_stack: 'Analyzing Tech Stack',
  identifying_modules: 'Identifying Core Modules',
  analyzing_data_flow: 'Analyzing Data Flow',
  detecting_patterns: 'Detecting Design Patterns',
  generating_guide: 'Generating Reading Guide',
  saving_report: 'Saving Report',
  complete: 'Analysis Complete',
  error: 'Analysis Failed',
}
</script>

<template>
  <div class="analysis-progress">
    <div v-if="events.length === 0" class="progress-idle animate-pulse-glow">
      <div class="idle-icon">⟳</div>
      <p>Preparing analysis...</p>
    </div>

    <template v-else>
      <div v-for="(event, index) in events" :key="index" class="progress-step animate-fade-in">
        <div class="step-header">
          <span class="step-status" :class="{ active: index === events.length - 1, done: index < events.length - 1 }">
            <template v-if="index < events.length - 1">✓</template>
            <template v-else>●</template>
          </span>
          <span class="step-label">{{ stageLabels[event.stage] || event.stage }}</span>
          <span class="step-percent">{{ event.progress }}%</span>
        </div>
        <p class="step-detail">{{ event.detail }}</p>
      </div>

      <div class="progress-bar-container">
        <div
          class="progress-bar-fill"
          :style="{ width: `${events[events.length - 1]?.progress || 0}%` }"
        />
      </div>
    </template>
  </div>
</template>

<style scoped lang="scss">
.analysis-progress {
  padding: 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
}

.progress-idle {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-secondary);

  .idle-icon {
    font-size: 32px;
    color: var(--accent-primary);
    animation: spin 2s linear infinite;
  }

  p {
    margin-top: 12px;
  }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.progress-step {
  margin-bottom: 16px;

  &:last-child {
    margin-bottom: 0;
  }
}

.step-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 4px;
}

.step-status {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  background: var(--bg-secondary);
  color: var(--text-muted);
  border: 1px solid var(--border-color);

  &.active {
    color: var(--accent-primary);
    border-color: var(--accent-primary);
    box-shadow: 0 0 8px var(--accent-glow);
  }

  &.done {
    color: var(--success);
    border-color: var(--success);
    background: rgba(52, 211, 153, 0.1);
  }
}

.step-label {
  font-weight: 500;
  color: var(--text-primary);
  flex: 1;
}

.step-percent {
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--accent-primary);
}

.step-detail {
  font-size: 13px;
  color: var(--text-secondary);
  padding-left: 30px;
}

.progress-bar-container {
  margin-top: 20px;
  height: 4px;
  background: var(--bg-secondary);
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  border-radius: 2px;
  transition: width 0.5s ease;
}
</style>
