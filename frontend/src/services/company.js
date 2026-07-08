import api from './api'

export const getMyJobs = async () => {
  const response = await api.get('/api/company/my-jobs')
  return response.data
}

export const getApplicants = async (jobId) => {
  const response = await api.get(`/api/company/job/${jobId}/applicants`)
  return response.data
}

export const shortlistStudent = async (applicationId) => {
  const response = await api.post(`/api/company/shortlist-student/${applicationId}`)
  return response.data
}

export const rejectApplication = async (applicationId, feedback = null) => {
  const response = await api.post(`/api/company/reject-application/${applicationId}`, { feedback })
  return response.data
}

export const scheduleInterview = async (applicationId, interviewDate, interviewLink = null) => {
  const response = await api.post(`/api/company/schedule-interview/${applicationId}`, {
    interview_date: interviewDate,
    interview_link: interviewLink
  })
  return response.data
}

export const sendResult = async (applicationId, result, salary = null, joiningDate = null, feedback = null) => {
  const response = await api.post(`/api/company/send-result/${applicationId}`, {
    result,
    salary,
    joining_date: joiningDate,
    feedback
  })
  return response.data
}

export const closeJob = async (jobId) => {
  const response = await api.post(`/api/company/close-job/${jobId}`)
  return response.data
}