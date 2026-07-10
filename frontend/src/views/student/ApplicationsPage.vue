<template>
  <StudentLayout>

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">My Applications</h2>
      <button class="btn btn-success" :disabled="exporting || applications.length === 0" @click="startExport">
        {{ exporting ? 'Exporting...' : 'Export as CSV' }}
      </button>
    </div>

    <div v-if="exportMsg" :class="'alert alert-' + exportMsgType">{{ exportMsg }}</div>
    <div v-if="loading" class="text-muted">Loading applications...</div>
    <div v-else-if="applications.length === 0" class="text-muted">You have not applied to any jobs yet.</div>

    <div v-else class="card shadow border-0">
      <div class="card-body">
        <table class="table table-hover align-middle">
          <thead>
            <tr>
              <th>Job Title</th>
              <th>Company</th>
              <th>Status</th>
              <th>Applied On</th>
              <th>Interview</th>
              <th>Feedback</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in applications" :key="app.application_id">
              <td>{{ app.job_title }}</td>
              <td>{{ app.company_name }}</td>
              <td>
                <span class="badge" :class="statusClass(app.status)">{{ statusLabel(app.status) }}</span>
              </td>
              <td>{{ formatDate(app.applied_on) }}</td>
              <td>
                <div v-if="app.interview_date">
                  {{ formatDateTime(app.interview_date) }}
                  <a v-if="app.interview_link" :href="app.interview_link" target="_blank"
                     class="btn btn-sm btn-primary ms-1">Join</a>
                </div>
                <span v-else class="text-muted">-</span>
              </td>
              <td class="small text-muted" style="max-width:220px">{{ app.company_feedback || '-' }}</td>
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
import { formatDate, formatDateTime } from '../../utils/date'
import { getMyApplications, exportApplications, getExportStatus } from '../../services/student'

const applications = ref([])
const loading = ref(true)
const exporting = ref(false)
const exportMsg = ref('')
const exportMsgType = ref('info')


const statusLabel = (s) => ({ applied:'Applied', shortlisted:'Shortlisted', interview:'Interview', selected:'Selected', rejected:'Rejected' }[s] || s)
const statusClass = (s) => ({ applied:'bg-secondary', shortlisted:'bg-info text-dark', interview:'bg-warning text-dark', selected:'bg-success', rejected:'bg-danger' }[s] || 'bg-secondary')

const loadApplications = async () => {
  loading.value = true
  try {
    const res = await getMyApplications()
    applications.value = res.applications || []
  } catch (e) { console.error(e) } finally { loading.value = false }
}

const downloadCsv = (csv, filename) => {
  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = filename || 'applications.csv'; a.click()
  URL.revokeObjectURL(url)
}
const showExportMsg = (t, ty='info') => { exportMsg.value = t; exportMsgType.value = ty }

const startExport = async () => {
  exporting.value = true
  showExportMsg('Export started, preparing your file...', 'info')
  try {
    const res = await exportApplications()
    if (!res.task_id) { showExportMsg('Could not start export.', 'danger'); exporting.value = false; return }
    pollStatus(res.task_id, 0)
  } catch (e) { showExportMsg('Failed to start export.', 'danger'); exporting.value = false }
}
const pollStatus = async (taskId, attempt) => {
  if (attempt >= 15) { showExportMsg('Taking too long. Is the Celery worker running?', 'warning'); exporting.value = false; return }
  try {
    const res = await getExportStatus(taskId)
    if (res.status === 'completed') { downloadCsv(res.data.data, res.data.filename); showExportMsg('CSV downloaded.', 'success'); exporting.value = false }
    else if (res.status === 'failed') { showExportMsg('Export failed on server.', 'danger'); exporting.value = false }
    else { setTimeout(() => pollStatus(taskId, attempt + 1), 2000) }
  } catch (e) { showExportMsg('Error checking status.', 'danger'); exporting.value = false }
}

onMounted(() => loadApplications())
</script>
