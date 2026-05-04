<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  submit: [url: string]
}>()

const repoUrl = ref('')
const loading = ref(false)

function isValidGithubUrl(url: string): boolean {
  return /^https?:\/\/github\.com\/[^/]+\/[^/]+\/?$/.test(url.trim())
}

function handleSubmit() {
  const url = repoUrl.value.trim()
  if (!url) return
  if (!isValidGithubUrl(url)) {
    alert('Please enter a valid GitHub repository URL (e.g., https://github.com/user/repo)')
    return
  }
  emit('submit', url)
}
</script>

<template>
  <div class="repo-input">
    <div class="input-wrapper">
      <span class="input-icon">⌘</span>
      <input
        v-model="repoUrl"
        type="text"
        placeholder="Enter a GitHub repository URL, e.g. https://github.com/user/repo"
        class="input-field"
        @keyup.enter="handleSubmit"
      />
      <button class="submit-btn" :disabled="!repoUrl.trim()" @click="handleSubmit">
        <span class="btn-text">Analyze</span>
        <span class="btn-arrow">→</span>
      </button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.repo-input {
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 6px 6px 6px 16px;
  transition: border-color var(--transition-normal), box-shadow var(--transition-normal);

  &:focus-within {
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px var(--accent-glow), var(--shadow-glow);
  }
}

.input-icon {
  color: var(--text-muted);
  font-size: 18px;
  margin-right: 12px;
}

.input-field {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-size: 15px;
  font-family: var(--font-mono);
  padding: 12px 0;

  &::placeholder {
    color: var(--text-muted);
  }
}

.submit-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: var(--bg-primary);
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all var(--transition-fast);

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px var(--accent-glow-strong);
  }

  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .btn-arrow {
    transition: transform var(--transition-fast);
  }

  &:hover:not(:disabled) .btn-arrow {
    transform: translateX(3px);
  }
}
</style>
