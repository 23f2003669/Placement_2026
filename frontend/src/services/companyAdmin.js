import api from './api'

export const getCompanies = async () => {

  const token = localStorage.getItem('token')

  const response = await api.get(
    '/api/admin/companies',
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )

  return response.data
}

export const approveCompany = async (id) => {

  const token = localStorage.getItem('token')

  return await api.post(
    `/api/admin/approve-company/${id}`,
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )
}

export const rejectCompany = async (id) => {

  const token = localStorage.getItem('token')

  return await api.post(
    `/api/admin/reject-company/${id}`,
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )
}