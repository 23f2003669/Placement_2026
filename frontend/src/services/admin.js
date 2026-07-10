import api from './api'

// Dashboard + analytics
export const getDashboardStats = async () =>
  (await api.get('/api/admin/dashboard')).data

export const getAdminAnalytics = async () =>
  (await api.get('/api/admin/analytics')).data

// Companies
export const getCompanies = async (search = '') =>
  (await api.get('/api/admin/companies', {
    params: search ? { search } : {}
  })).data

export const approveCompany = async (id) =>
  (await api.post(`/api/admin/approve-company/${id}`, {})).data

export const rejectCompany = async (id) =>
  (await api.post(`/api/admin/reject-company/${id}`, {})).data

// Students
export const getStudents = async (search = '') =>
  (await api.get('/api/admin/students', {
    params: search ? { search } : {}
  })).data

export const blacklistStudent = async (id) =>
  (await api.post(`/api/admin/blacklist-student/${id}`, {})).data

export const unblacklistStudent = async (id) =>
  (await api.post(`/api/admin/unblacklist-student/${id}`, {})).data

// Jobs
export const getJobs = async () =>
  (await api.get('/api/admin/job-positions')).data

export const approveJob = async (id) =>
  (await api.post(`/api/admin/approve-job/${id}`, {})).data

export const rejectJob = async (id) =>
  (await api.post(`/api/admin/reject-job/${id}`, {})).data

// Applications
export const getApplications = async () =>
  (await api.get('/api/admin/applications')).data

// Placements
export const getPlacements = async () =>
  (await api.get('/api/admin/placements')).data