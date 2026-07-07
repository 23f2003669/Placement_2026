<template>
  <CompanyLayout>
    <h1 class="mb-4">My Jobs</h1>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else class="card shadow border-0">
      <div class="card-body">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Job Title</th>
              <th>Location</th>
              <th>Type</th>
              <th>Salary</th>
              <th>Status</th>
              <th>Applicants</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="job in jobs" :key="job.id">
              <td>{{ job.job_title }}</td>
              <td>{{ job.location || 'N/A' }}</td>
              <td>{{ job.job_type || 'N/A' }}</td>
              <td>₹{{ job.salary_min || 0 }} - ₹{{ job.salary_max || 0 }}</td>
              <td>
                <span class="badge" :class="{
                  'bg-success': job.status === 'approved',
                  'bg-warning text-dark': job.status === 'pending',
                  'bg-secondary': job.status === 'closed',
                  'bg-danger': job.status === 'rejected'
                }">{{ job.status }}</span>
              </td>
              <td>{{ job.applicants_count || 0 }}</td>
              <td>
                <router-link
                  :to="`/company/applicants/${job.id}`"
                  class="btn btn-primary btn-sm me-2"
                >View Applicants</router-link>
                <button
                  v-if="job.status === 'approved'"
                  class="btn btn-secondary btn-sm"
                  @click="handleClose(job.id)"
                >Close</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="jobs.length === 0" class="text-muted text-center py-3">No jobs posted yet.</p>
      </div>
    </div>
  </CompanyLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CompanyLayout from '../../layouts/CompanyLayout.vue'
import { getMyJobs, closeJob } from '../../services/company'

const jobs = ref([])
const loading = ref(true)

const loadJobs = async () => {
  try {
    loading.value = true
    const response = await getMyJobs()
    jobs.value = response.jobs || []
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to load jobs')
  } finally {
    loading.value = false
  }
}

const handleClose = async (jobId) => {
  try {
    await closeJob(jobId)
    await loadJobs()
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to close job')
  }
}

onMounted(() => {
  loadJobs()
})
</script>