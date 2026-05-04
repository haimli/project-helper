import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  submitAnalysis,
  getProjects,
  getReport,
  type Project,
  type Report,
} from '../api/projects'

export const useProjectStore = defineStore('project', () => {
  const projects = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)
  const currentReport = ref<Report | null>(null)
  const progressEvents = ref<{ stage: string; progress: number; detail: string }[]>([])
  const loading = ref(false)

  async function fetchProjects() {
    loading.value = true
    try {
      const res = await getProjects()
      projects.value = res.items
    } finally {
      loading.value = false
    }
  }

  async function analyze(repoUrl: string): Promise<Project> {
    loading.value = true
    try {
      const project = await submitAnalysis(repoUrl)
      currentProject.value = project
      progressEvents.value = []
      return project
    } finally {
      loading.value = false
    }
  }

  async function fetchReport(projectId: number) {
    loading.value = true
    try {
      currentReport.value = await getReport(projectId)
    } finally {
      loading.value = false
    }
  }

  function addProgressEvent(event: { stage: string; progress: number; detail: string }) {
    progressEvents.value.push(event)
  }

  function reset() {
    currentProject.value = null
    currentReport.value = null
    progressEvents.value = []
  }

  return {
    projects,
    currentProject,
    currentReport,
    progressEvents,
    loading,
    fetchProjects,
    analyze,
    fetchReport,
    addProgressEvent,
    reset,
  }
})
