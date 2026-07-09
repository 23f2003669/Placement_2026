<template>
  <AdminLayout>

    <h1 class="mb-4">Job Positions</h1>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else class="card shadow border-0">

      <div class="card-body">

        <table class="table table-hover">

          <thead>
            <tr>
              <th>Job Title</th>
              <th>Company</th>
              <th>Salary</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>

            <tr v-for="job in jobs" :key="job.id">

              <td>{{ job.job_title }}</td>
              <td>{{ job.company_name }}</td>
              <td>{{ formatSalaryRange(job.salary_min, job.salary_max) }}</td>

              <td>
                <span
                  class="badge"
                  :class="{
                    'bg-success': job.status === 'approved',
                    'bg-warning text-dark': job.status === 'pending',
                    'bg-danger': job.status === 'rejected',
                    'bg-secondary': job.status === 'closed'
                  }"
                >
                  {{ job.status }}
                </span>
              </td>

              <td>
                <div v-if="job.status === 'pending'" class="d-flex gap-2">
                  <button
                    class="btn btn-success btn-sm"
                    @click="handleApprove(job.id)"
                    :disabled="actionLoading === job.id"
                  >
                    Approve
                  </button>
                  <button
                    class="btn btn-danger btn-sm"
                    @click="handleReject(job.id)"
                    :disabled="actionLoading === job.id"
                  >
                    Reject
                  </button>
                </div>
                <span v-else class="text-muted small">No action needed</span>
              </td>

            </tr>

          </tbody>

        </table>

        <p v-if="jobs.length === 0" class="text-muted text-center py-3">
          No job positions found.
        </p>

      </div>

    </div>

  </AdminLayout>
</template>

<script setup>
import { formatSalaryRange } from '../../utils/format'
import { ref, onMounted } from 'vue'
import AdminLayout from '../../layouts/AdminLayout.vue'
import { getJobs, approveJob, rejectJob } from '../../services/jobAdmin'

const jobs = ref([])
const loading = ref(true)
const actionLoading = ref(null)

const loadJobs = async () => {
  try {
    loading.value = true
    const response = await getJobs()
    jobs.value = response.job_positions
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to load jobs')
  } finally {
    loading.value = false
  }
}

const handleApprove = async (id) => {
  try {
    actionLoading.value = id
    await approveJob(id)
    await loadJobs()
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to approve job')
  } finally {
    actionLoading.value = null
  }
}

const handleReject = async (id) => {
  try {
    actionLoading.value = id
    await rejectJob(id)
    await loadJobs()
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to reject job')
  } finally {
    actionLoading.value = null
  }
}

onMounted(() => {
  loadJobs()
})
</script>