<script setup lang="ts">
import { computed, onMounted } from 'vue'
import type { Report } from '../api/projects'
import { renderMarkdown } from '../utils/markdown'
import '../styles/markdown.scss'

const props = defineProps<{
  report: Report
}>()

const overviewHtml = computed(() => renderMarkdown(props.report.overview))
const dataFlowHtml = computed(() => renderMarkdown(props.report.data_flow))

const techStack = computed(() => {
  try {
    return JSON.parse(props.report.tech_stack)
  } catch {
    return null
  }
})

const coreModules = computed(() => {
  try {
    return JSON.parse(props.report.core_modules)
  } catch {
    return []
  }
})

const designPatterns = computed(() => {
  try {
    return JSON.parse(props.report.design_patterns)
  } catch {
    return []
  }
})

const readingSuggestions = computed(() => {
  try {
    return JSON.parse(props.report.reading_suggestions)
  } catch {
    return []
  }
})

const activeSection = computed(() => {
  return [
    { id: 'overview', label: 'Overview' },
    { id: 'tech-stack', label: 'Tech Stack' },
    { id: 'directory', label: 'Directory' },
    { id: 'modules', label: 'Core Modules' },
    { id: 'data-flow', label: 'Data Flow' },
    { id: 'patterns', label: 'Patterns' },
    { id: 'reading', label: 'Reading Guide' },
  ]
})
</script>

<template>
  <div class="report-view">
    <nav class="report-nav">
      <a v-for="section in activeSection" :key="section.id" :href="`#${section.id}`" class="nav-link">
        {{ section.label }}
      </a>
    </nav>

    <div class="report-content">
      <!-- Overview -->
      <section id="overview" class="report-section animate-fade-in">
        <h2 class="section-title">Project Overview</h2>
        <div class="markdown-body" v-html="overviewHtml" />
      </section>

      <!-- Tech Stack -->
      <section id="tech-stack" class="report-section animate-fade-in">
        <h2 class="section-title">Tech Stack</h2>
        <div v-if="techStack" class="tech-stack-grid">
          <div v-if="techStack.languages?.length" class="tech-category">
            <h3>Languages</h3>
            <div class="tech-tags">
              <span v-for="lang in techStack.languages" :key="lang.name" class="tech-tag">
                {{ lang.name }} <small>{{ lang.proportion }}</small>
              </span>
            </div>
          </div>
          <div v-if="techStack.frameworks?.length" class="tech-category">
            <h3>Frameworks</h3>
            <div class="tech-tags">
              <span v-for="fw in techStack.frameworks" :key="fw.name" class="tech-tag accent">
                {{ fw.name }} <small>{{ fw.purpose }}</small>
              </span>
            </div>
          </div>
          <div v-if="techStack.build_tools?.length" class="tech-category">
            <h3>Build Tools</h3>
            <div class="tech-tags">
              <span v-for="tool in techStack.build_tools" :key="tool" class="tech-tag">{{ tool }}</span>
            </div>
          </div>
        </div>
        <p v-else class="empty-text">No tech stack data available.</p>
      </section>

      <!-- Directory Structure -->
      <section id="directory" class="report-section animate-fade-in">
        <h2 class="section-title">Directory Structure</h2>
        <pre class="directory-tree"><code>{{ report.directory_structure }}</code></pre>
      </section>

      <!-- Core Modules -->
      <section id="modules" class="report-section animate-fade-in">
        <h2 class="section-title">Core Modules</h2>
        <div v-if="coreModules.length" class="modules-list">
          <div v-for="mod in coreModules" :key="mod.name" class="module-card">
            <div class="module-header">
              <span class="module-name">{{ mod.name }}</span>
              <span class="module-path">{{ mod.path }}</span>
            </div>
            <p class="module-desc">{{ mod.responsibility }}</p>
            <div v-if="mod.depends_on?.length" class="module-deps">
              <span class="deps-label">Depends on:</span>
              <span v-for="dep in mod.depends_on" :key="dep" class="dep-tag">{{ dep }}</span>
            </div>
          </div>
        </div>
        <p v-else class="empty-text">No module data available.</p>
      </section>

      <!-- Data Flow -->
      <section id="data-flow" class="report-section animate-fade-in">
        <h2 class="section-title">Data Flow</h2>
        <div class="markdown-body" v-html="dataFlowHtml" />
      </section>

      <!-- Design Patterns -->
      <section id="patterns" class="report-section animate-fade-in">
        <h2 class="section-title">Design Patterns</h2>
        <div v-if="designPatterns.length" class="patterns-list">
          <div v-for="pattern in designPatterns" :key="pattern.name" class="pattern-card">
            <h3 class="pattern-name">{{ pattern.name }}</h3>
            <p class="pattern-desc">{{ pattern.description }}</p>
            <div v-if="pattern.examples?.length" class="pattern-examples">
              <span v-for="ex in pattern.examples" :key="ex" class="example-tag">{{ ex }}</span>
            </div>
          </div>
        </div>
        <p v-else class="empty-text">No pattern data available.</p>
      </section>

      <!-- Reading Suggestions -->
      <section id="reading" class="report-section animate-fade-in">
        <h2 class="section-title">Reading Guide</h2>
        <div v-if="readingSuggestions.length" class="reading-list">
          <div v-for="item in readingSuggestions" :key="item.order" class="reading-item">
            <span class="reading-order">{{ item.order }}</span>
            <div class="reading-info">
              <h3>{{ item.title }}</h3>
              <p>{{ item.reason }}</p>
              <code v-if="item.path" class="reading-path">{{ item.path }}</code>
            </div>
          </div>
        </div>
        <p v-else class="empty-text">No reading guide available.</p>
      </section>
    </div>
  </div>
</template>

<style scoped lang="scss">
.report-view {
  display: flex;
  gap: 24px;
}

.report-nav {
  position: sticky;
  top: 80px;
  width: 180px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;

  .nav-link {
    font-size: 13px;
    color: var(--text-muted);
    padding: 6px 12px;
    border-radius: var(--radius-sm);
    transition: all var(--transition-fast);

    &:hover {
      color: var(--text-primary);
      background: var(--bg-card);
      text-decoration: none;
    }
  }
}

.report-content {
  flex: 1;
  min-width: 0;
}

.report-section {
  margin-bottom: 40px;
  padding: 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color);
  color: var(--accent-primary);
}

// Tech Stack
.tech-stack-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.tech-category h3 {
  font-size: 0.85rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 8px;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tech-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 14px;
  color: var(--text-primary);

  small {
    color: var(--text-muted);
    font-size: 12px;
  }

  &.accent {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }
}

// Directory Tree
.directory-tree {
  background: var(--bg-code);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 16px;
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
}

// Modules
.modules-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.module-card {
  padding: 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);

  &:hover {
    border-color: var(--border-color-hover);
  }
}

.module-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.module-name {
  font-weight: 600;
  color: var(--accent-primary);
}

.module-path {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-muted);
}

.module-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.module-deps {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.deps-label {
  font-size: 12px;
  color: var(--text-muted);
}

.dep-tag {
  font-size: 12px;
  padding: 2px 8px;
  background: var(--bg-card);
  border-radius: var(--radius-sm);
  color: var(--accent-secondary);
}

// Patterns
.patterns-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.pattern-card {
  padding: 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
}

.pattern-name {
  font-size: 16px;
  color: var(--accent-primary);
  margin-bottom: 8px;
}

.pattern-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.pattern-examples {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.example-tag {
  font-family: var(--font-mono);
  font-size: 12px;
  padding: 2px 8px;
  background: var(--bg-card);
  border-radius: var(--radius-sm);
  color: var(--text-muted);
}

// Reading Guide
.reading-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.reading-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
}

.reading-order {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-primary);
  color: var(--bg-primary);
  border-radius: 50%;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.reading-info {
  flex: 1;

  h3 {
    font-size: 15px;
    margin-bottom: 4px;
  }

  p {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 6px;
  }
}

.reading-path {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-muted);
  background: var(--bg-card);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
}

.empty-text {
  color: var(--text-muted);
  font-style: italic;
}
</style>
