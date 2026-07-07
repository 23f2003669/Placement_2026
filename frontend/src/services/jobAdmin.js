import api from './api'

export const getJobs = async () => {

  const token = localStorage.getItem('token')

  const response = await api.get(
    '/api/admin/job-positions',
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )

  return response.data
}

export const approveJob = async (id) => {

  const token = localStorage.getItem('token')

  return await api.post(
    `/api/admin/approve-job/${id}`,
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )
}

export const rejectJob = async (id) => {
  const response = await api.post(
    `/api/admin/reject-job/${id}`,
    {}
  )
  return response.data
}