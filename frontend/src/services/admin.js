import api from './api'

const getAuthHeader = () => ({
  headers: {
    Authorization: `Bearer ${localStorage.getItem('token')}`
  }
})

export const getDashboardStats = async () => {
  const response = await api.get(
    '/api/admin/dashboard',
    getAuthHeader()
  )
  return response.data
}

export const getCompanies = async () => {
  const response = await api.get(
    '/api/admin/companies',
    getAuthHeader()
  )
  return response.data
}

export const getStudents = async () => {
  const response = await api.get(
    '/api/admin/students',
    getAuthHeader()
  )
  return response.data
}

export const getApplications = async () => {
  const response = await api.get(
    '/api/admin/applications',
    getAuthHeader()
  )
  return response.data
}

export const approveCompany = async (id) => {

  const response = await api.post(
    `/api/admin/approve-company/${id}`,
    {},
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    }
  )

  return response.data
}

export const rejectCompany = async (id) => {

  const response = await api.post(
    `/api/admin/reject-company/${id}`,
    {},
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    }
  )

  return response.data
}
export const getAdminAnalytics = async () => {
  const response = await api.get('/api/admin/analytics', getAuthHeader())
  return response.data
}
