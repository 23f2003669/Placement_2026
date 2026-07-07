import api from './api'

export const getStudents = async (search = '') => {
  const response = await api.get('/api/admin/students', {
    params: { search }
  })
  return response.data
}

export const blacklistStudent = async (id) => {

  const response = await api.post(
    `/api/admin/blacklist-student/${id}`,
    {},
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    }
  )

  return response.data
}

export const unblacklistStudent = async (id) => {

  const response = await api.post(
    `/api/admin/unblacklist-student/${id}`,
    {},
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    }
  )

  return response.data
}