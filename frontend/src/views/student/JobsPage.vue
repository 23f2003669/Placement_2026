<template>
  <StudentLayout>

    <h2 class="mb-4">Available Jobs</h2>

    <div class="mb-4" style="max-width: 500px;">
      <input
        type="text"
        class="form-control"
        placeholder="Search by job title or company..."
        v-model="searchQuery"
      />
    </div>

    <div v-if="message" :class="'alert alert-' + messageType">
      {{ message }}
    </div>

    <div v-if="loading" class="text-muted">Loading jobs...</div>

    <div v-else-if="filteredJobs.length === 0" class="text-muted">
      No jobs found.
    </div>

    <div v-else class="row">
      <div class="col-md-6 mb-4" v-for="job in filteredJobs" :key="job.id">
        <div class="card shadow border-0 h-100 p-3">

          <div class="d-flex justify-content-between align-items-start">
            <h5 class="mb-1">{{ job.job_title }}</h5>
            <span
              class="badge"
              :class="job.is_eligible ? 'bg-success' : 'bg-danger'"
            >
              {{ job.is_eligible ? 'Eligible' : 'Not Eligible' }}
            </span>
          </div>

          <p class="text-muted mb-2">{{ job.company_name }}</p>

          <p class="mb-1" v-if="job.location">
            <strong>Location:</strong> {{ job.location }}
          </p>

          <p class="mb-1" v-if="job.salary_min || job.salary_max">
            <strong>Salary:</strong>
            {{ formatSalaryRange(job.salary_min, job.salary_max) }}
          </p>

          <p class="mb-1" v-if="job.min_cgpa">
            <strong>Min CGPA:</strong> {{ job.min_cgpa }}
          </p>

          <p class="mb-1" v-if="job.eligible_branches">
            <strong>Branches:</strong> {{ job.eligible_branches }}
          </p>

          <p class="mb-2">
            <strong>Deadline:</strong> {{ formatDate(job.application_deadline) }}
          </p>

          <ul
            class="small text-danger mb-2"
            v-if="!job.is_eligible && job.ineligibility_reasons.length"
          >
            <li v-for="(reason, i) in job.ineligibility_reasons" :key="i">
              {{ reason }}
            </li>
          </ul>

          <div class="mt-auto">
            <button
              v-if="appliedJobIds.includes(job.id)"
              class="btn btn-secondary w-100"
              disabled
            >
              Applied
            </button>
            <button
              v-else
              class="btn btn-primary w-100"
              :disabled="!job.is_eligible || applyingId === job.id"
              @click="apply(job.id)"
            >
              {{ applyingId === job.id ? 'Applying...' : 'Apply' }}
            </button>
          </div>

        </div>
      </div>
    </div>

  </StudentLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import StudentLayout from '../../layouts/StudentLayout.vue'
import { getJobs, getMyApplications, applyJob } from '../../services/student'
import { formatSalaryRange } from '../../utils/format'

const jobs = ref([])
const appliedJobIds = ref([])
const searchQuery = ref('')
const loading = ref(true)
const applyingId = ref(null)
const message = ref('')
const messageType = ref('success')

const filteredJobs = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return jobs.value
  return jobs.value.filter(j =>
    j.job_title.toLowerCase().includes(q) ||
    (j.company_name || '').toLowerCase().includes(q)
  )
})

const showMessage = (text, type = 'success') => {
  message.value = text
  messageType.value = type
  setTimeout(() => { message.value = '' }, 4000)
}

const formatDate = (isoString) => {
  if (!isoString) return 'N/A'
  return new Date(isoString).toLocaleDateString()
}

const loadJobs = async () => {
  loading.value = true
  try {
    const jobsRes = await getJobs()
    jobs.value = jobsRes.jobs || []

    const appsRes = await getMyApplications()
    appliedJobIds.value = (appsRes.applications || []).map(a => a.job_id)
  } catch (error) {
    console.error('Error loading jobs:', error)
    showMessage('Failed to load jobs', 'danger')
  } finally {
    loading.value = false
  }
}

const apply = async (jobId) => {
  applyingId.value = jobId
  try {
    const res = await applyJob(jobId)
    if (res.success) {
      appliedJobIds.value.push(jobId)
      showMessage('Applied successfully', 'success')
    }
  } catch (error) {
    const msg = error.response?.data?.error || 'Failed to apply'
    showMessage(msg, 'danger')
  } finally {
    applyingId.value = null
  }
}

onMounted(() => {
  loadJobs()
})
</script>
