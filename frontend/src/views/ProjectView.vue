<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AnalysisProgress from '../components/AnalysisProgress.vue'
import ReportView from '../components/ReportView.vue'
import { useProjectStore } from '../stores/project'
import { createProgressSSE } from '../utils/sse'

const props = defineProps<{ id: string }>()
const route = useRoute()
const router = useRouter()
const store = useProjectStore()
const projectId = ref(parseInt(props.id))

let eventSource: EventSource | null = null

onMounted(async () => {
  await store.fetchProjects()
  const existing = store.projects.find(p => p.id === projectId.value)

  if (existing?.status === 'completed') {
    store.currentProject = existing
    await store.fetchReport(projectId.value)
  } else if (existing?.status === 'analyzing' || existing?.status === 'pending') {
    store.currentProject = existing
    connectProgress()
  }
})

onUnmounted(() => {
  disconnectProgress()
})

function connectProgress() {
  store.progressEvents = []
  const url = `/api/projects/${projectId.value}/progress`
  eventSource = new EventSource(url)

  eventSource.addEventListener('progress', (e) => {
    try {
      const data = JSON.parse(e.data)
      store.addProgressEvent(data)
      if (data.stage === 'complete') {
        disconnectProgress()
        store.fetchReport(projectId.value)
        if (store.currentProject) {
          store.currentProject.status = 'completed'
        }
      } else if (data.stage === 'error') {
        disconnectProgress()
        if (store.currentProject) {
          store.currentProject.status = 'failed'
          store.currentProject.error_message = data.detail
        }
      }
    } catch { /* ignore parse errors */ }
  })

  eventSource.onerror = () => {
    disconnectProgress()
  }
}

function disconnectProgress() {
  if (eventSource) {
    eventSource.close()
    eventSource = null
  }
}

function goToChat() {
  router.push({ name: 'chat', params: { projectId: projectId.value } })
}
</script>

<template>
  <div class="project-view">
    <div v-if="!store.currentProject" class="loading-state">
      <p>Loading project...</p>
    </div>

    <template v-else>
      <div class="project-header">
        <div class="header-info">
          <h1 class="project-name">{{ store.currentProject.repo_name }}</h1>
          <p class="project-url">{{ store.currentProject.repo_url }}</p>
        </div>
        <div class="header-actions">
          <button
            v-if="store.currentProject.status === 'completed'"
            class="chat-btn"
            @click="goToChat"
          >
            Chat with Code →
          </button>
        </div>
      </div>

      <!-- Analysis in progress -->
      <AnalysisProgress
        v-if="store.currentProject.status === 'analyzing' || store.currentProject.status === 'pending'"
        :events="store.progressEvents"
      />

      <!-- Error state -->
      <div v-else-if="store.currentProject.status === 'failed'" class="error-state">
        <h2>Analysis Failed</h2>
        <p>{{ store.currentProject.error_message }}</p>
      </div>

      <!-- Report -->
      <ReportView
        v-else-if="store.currentReport"
        :report="store.currentReport"
      />
    </template>
  </div>
</template>

<style scoped lang="scss">
.project-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.project-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
}

.project-name {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--accent-primary);
  margin-bottom: 4px;
}

.project-url {
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--text-muted);
}

.chat-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: var(--bg-primary);
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all var(--transition-fast);

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px var(--accent-glow-strong);
  }
}

.loading-state, .error-state {
  padding: 40px;
  text-align: center;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
}

.error-state {
  h2 {
    color: var(--error);
    margin-bottom: 8px;
  }

  p {
    color: var(--text-secondary);
  }
}
</style>
