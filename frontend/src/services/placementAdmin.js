import api from './api'

export const getPlacements = async () => {

  const token = localStorage.getItem('token')

  const response = await api.get(
    '/api/admin/placements',
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )

  return response.data
}