<template>
  <AdminLayout>
    <h1 class="mb-4">Job Positions</h1>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else class="card shadow border-0">
      <div class="card-body">

        <div class="mb-3">
          <input
            type="text"
            class="form-control"
            placeholder="Search by job title, company, or status..."
            v-model="searchQuery"
          />
        </div>

        <div class="table-responsive">
          <table class="table table-hover align-middle">
            <thead>
              <tr>
                <th>Job Title</th>
                <th>Company</th>
                <th class="salary-col">Salary</th>
                <th class="status-col">Status</th>
                <th class="action-col">Action</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="job in filteredJobs" :key="job.id">
                <td>{{ job.job_title }}</td>
                <td>{{ job.company_name }}</td>

                <td
                  class="salary-col"
                  :title="`${formatSalaryFull(job.salary_min)} – ${formatSalaryFull(job.salary_max)}`"
                >
                  {{ formatSalaryRange(job.salary_min, job.salary_max) }}
                </td>

                <td class="status-col">
                  <span
                    class="badge"
                    :class="{
                      'bg-success': job.status === 'approved',
                      'bg-warning text-dark': job.status === 'pending',
                      'bg-danger': job.status === 'rejected',
                      'bg-secondary': job.status === 'closed'
                    }"
                  >
                    {{ formatStatus(job.status) }}
                  </span>
                </td>

                <td class="action-col">
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
        </div>

        <p v-if="filteredJobs.length === 0" class="text-muted text-center py-3">
          No job positions found.
        </p>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import AdminLayout from '../../layouts/AdminLayout.vue'
import { getJobs, approveJob, rejectJob } from '../../services/admin'
import { formatSalaryRange, formatSalaryFull, formatStatus } from '../../utils/format'

const jobs = ref([])
const loading = ref(true)
const actionLoading = ref(null)
const searchQuery = ref('')

const filteredJobs = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return jobs.value

  return jobs.value.filter((job) =>
    (job.job_title || '').toLowerCase().includes(q) ||
    (job.company_name || '').toLowerCase().includes(q) ||
    (job.status || '').toLowerCase().includes(q)
  )
})

const loadJobs = async () => {
  try {
    loading.value = true
    const response = await getJobs()
    jobs.value = response.job_positions || []
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

onMounted(loadJobs)
</script>

<style scoped>
.salary-col {
  min-width: 280px;
}
.status-col {
  width: 140px;
}
.action-col {
  width: 220px;
}
</style>