import api from './index'

export interface Project {
  id: number
  repo_url: string
  repo_name: string
  status: 'pending' | 'analyzing' | 'completed' | 'failed'
  error_message: string | null
  created_at: string
  updated_at: string
}

export interface ProjectListResponse {
  items: Project[]
  total: number
}

export interface Report {
  id: number
  project_id: number
  overview: string
  tech_stack: string
  directory_structure: string
  core_modules: string
  data_flow: string
  design_patterns: string
  reading_suggestions: string
  created_at: string
}

export async function submitAnalysis(repoUrl: string): Promise<Project> {
  const { data } = await api.post('/projects/analyze', { repo_url: repoUrl })
  return data
}

export async function getProjects(skip = 0, limit = 20): Promise<ProjectListResponse> {
  const { data } = await api.get('/projects', { params: { skip, limit } })
  return data
}

export async function getProject(projectId: number): Promise<Project> {
  const { data } = await api.get(`/projects/${projectId}`)
  return data
}

export async function getReport(projectId: number): Promise<Report> {
  const { data } = await api.get(`/projects/${projectId}/report`)
  return data
}

export async function deleteProject(projectId: number): Promise<void> {
  await api.delete(`/projects/${projectId}`)
}
