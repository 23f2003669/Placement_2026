<template>
  <StudentLayout>

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">My Applications</h2>
      <button
        class="btn btn-success"
        :disabled="exporting || applications.length === 0"
        @click="startExport"
      >
        {{ exporting ? 'Exporting...' : 'Export as CSV' }}
      </button>
    </div>

    <div v-if="exportMsg" :class="'alert alert-' + exportMsgType">
      {{ exportMsg }}
    </div>

    <div v-if="loading" class="text-muted">Loading applications...</div>

    <div v-else-if="applications.length === 0" class="text-muted">
      You have not applied to any jobs yet.
    </div>

    <div v-else class="card shadow border-0">
      <div class="card-body">
        <table class="table table-hover align-middle">
          <thead>
            <tr>
              <th>Job Title</th>
              <th>Company</th>
              <th>Status</th>
              <th>Applied On</th>
              <th>Interview Date</th>
              <th>Feedback</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in applications" :key="app.application_id">
              <td>{{ app.job_title }}</td>
              <td>{{ app.company_name }}</td>
              <td>
                <span class="badge" :class="statusClass(app.status)">
                  {{ statusLabel(app.status) }}
                </span>
              </td>
              <td>{{ formatDate(app.applied_on) }}</td>
              <td>{{ formatDate(app.interview_date) }}</td>
              <td>{{ app.company_feedback || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </StudentLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import StudentLayout from '../../layouts/StudentLayout.vue'
import { getMyApplications, exportApplications, getExportStatus } from '../../services/student'

const applications = ref([])
const loading = ref(true)
const exporting = ref(false)
const exportMsg = ref('')
const exportMsgType = ref('info')

const formatDate = (isoString) => {
  if (!isoString) return '-'
  return new Date(isoString).toLocaleDateString()
}

const statusLabel = (status) => {
  const labels = {
    applied: 'Applied',
    shortlisted: 'Shortlisted',
    interview: 'Interview',
    selected: 'Selected',
    rejected: 'Rejected'
  }
  return labels[status] || status
}

const statusClass = (status) => {
  const classes = {
    applied: 'bg-secondary',
    shortlisted: 'bg-info text-dark',
    interview: 'bg-warning text-dark',
    selected: 'bg-success',
    rejected: 'bg-danger'
  }
  return classes[status] || 'bg-secondary'
}

const loadApplications = async () => {
  loading.value = true
  try {
    const res = await getMyApplications()
    applications.value = res.applications || []
  } catch (error) {
    console.error('Error loading applications:', error)
  } finally {
    loading.value = false
  }
}

const downloadCsv = (csvString, filename) => {
  const blob = new Blob([csvString], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename || 'applications.csv'
  a.click()
  URL.revokeObjectURL(url)
}

const showExportMsg = (text, type = 'info') => {
  exportMsg.value = text
  exportMsgType.value = type
}

const startExport = async () => {
  exporting.value = true
  showExportMsg('Export started, preparing your file...', 'info')
  try {
    const res = await exportApplications()
    const taskId = res.task_id
    if (!taskId) {
      showExportMsg('Could not start export.', 'danger')
      exporting.value = false
      return
    }
    pollStatus(taskId, 0)
  } catch (error) {
    showExportMsg('Failed to start export.', 'danger')
    exporting.value = false
  }
}

const pollStatus = async (taskId, attempt) => {
  if (attempt >= 15) {
    showExportMsg('Export is taking too long. Make sure the Celery worker is running.', 'warning')
    exporting.value = false
    return
  }
  try {
    const res = await getExportStatus(taskId)
    if (res.status === 'completed') {
      const result = res.data
      downloadCsv(result.data, result.filename)
      showExportMsg('CSV downloaded successfully.', 'success')
      exporting.value = false
    } else if (res.status === 'failed') {
      showExportMsg('Export failed on the server.', 'danger')
      exporting.value = false
    } else {
      setTimeout(() => pollStatus(taskId, attempt + 1), 2000)
    }
  } catch (error) {
    showExportMsg('Error checking export status.', 'danger')
    exporting.value = false
  }
}

onMounted(() => {
  loadApplications()
})
</script>
