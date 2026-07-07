import api from './api'

// Dashboard statistics
export const getDashboard = async () => {
  const response = await api.get('/api/student/dashboard')
  return response.data
}

// Available (approved) jobs, optional search text
export const getJobs = async (search = '') => {
  const response = await api.get('/api/student/jobs', {
    params: search ? { search } : {}
  })
  return response.data
}

// Apply to a job
export const applyJob = async (jobId) => {
  const response = await api.post(`/api/student/apply-job/${jobId}`, {})
  return response.data
}

// Student's own applications (status tracking)
export const getMyApplications = async () => {
  const response = await api.get('/api/student/my-applications')
  return response.data
}

// Placement history
export const getPlacements = async () => {
  const response = await api.get('/api/student/placements')
  return response.data
}

// Profile: fetch (prefill) and update
export const getProfile = async () => {
  const response = await api.get('/api/student/profile')
  return response.data
}

export const updateProfile = async (profileData) => {
  const response = await api.put('/api/student/profile', profileData)
  return response.data
}

// Resume upload (multipart form-data, not JSON)
export const uploadResume = async (file) => {
  const formData = new FormData()
  formData.append('resume', file)
  const response = await api.post('/api/student/upload-resume', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return response.data
}

// CSV export: trigger async job, then poll status
export const exportApplications = async () => {
  const response = await api.post('/api/student/export-applications', {})
  return response.data
}

export const getExportStatus = async (taskId) => {
  const response = await api.get(`/api/student/export-status/${taskId}`)
  return response.data
}