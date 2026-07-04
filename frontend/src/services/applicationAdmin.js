import api from './api'

export const getApplications = async () => {

  const token = localStorage.getItem('token')

  const response = await api.get(
    '/api/admin/applications',
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )

  return response.data
}