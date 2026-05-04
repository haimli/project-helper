<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import RepoInput from '../components/RepoInput.vue'
import { useProjectStore } from '../stores/project'

const router = useRouter()
const store = useProjectStore()

onMounted(() => {
  store.fetchProjects()
})

async function handleSubmit(url: string) {
  const project = await store.analyze(url)
  router.push({ name: 'project', params: { id: project.id } })
}

function goToproject(id: number) {
  router.push({ name: 'project', params: { id } })
}
</script>

<template>
  <div class="home-view">
    <section class="hero">
      <h1 class="hero-title">
        <span class="title-accent">Project</span> Helper
      </h1>
      <p class="hero-subtitle">Understand any open-source project's source code in minutes, not days.</p>
      <RepoInput @submit="handleSubmit" />
    </section>

    <section v-if="store.projects.length" class="recent-projects">
      <h2 class="section-title">Recent Projects</h2>
      <div class="project-grid">
        <div
          v-for="project in store.projects"
          :key="project.id"
          class="project-card"
          @click="goToproject(project.id)"
        >
          <div class="card-header">
            <span class="repo-name">{{ project.repo_name }}</span>
            <span class="status-badge" :class="project.status">{{ project.status }}</span>
          </div>
          <p class="repo-url">{{ project.repo_url }}</p>
          <span class="card-time">{{ new Date(project.created_at).toLocaleDateString() }}</span>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped lang="scss">
.home-view {
  display: flex;
  flex-direction: column;
  gap: 48px;
}

.hero {
  text-align: center;
  padding: 80px 20px 60px;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  letter-spacing: -1px;
  margin-bottom: 16px;

  .title-accent {
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
}

.hero-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 40px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--text-primary);
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.project-card {
  padding: 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-normal);

  &:hover {
    border-color: var(--border-color-hover);
    transform: translateY(-2px);
    box-shadow: var(--shadow-card);
  }
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.repo-name {
  font-weight: 600;
  color: var(--accent-primary);
  font-size: 15px;
}

.status-badge {
  font-size: 11px;
  padding: 2px 10px;
  border-radius: 20px;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;

  &.completed {
    background: rgba(52, 211, 153, 0.1);
    color: var(--success);
  }

  &.analyzing, &.pending {
    background: rgba(251, 191, 36, 0.1);
    color: var(--warning);
  }

  &.failed {
    background: rgba(248, 113, 113, 0.1);
    color: var(--error);
  }
}

.repo-url {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-time {
  font-size: 12px;
  color: var(--text-muted);
}
</style>
