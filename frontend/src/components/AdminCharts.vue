<template>
  <div class="mb-4">
    <h4 class="mb-3">Analytics</h4>
    <div v-if="loading" class="text-muted">Loading charts...</div>
    <div v-else class="row g-4">
      <div class="col-md-4">
        <div class="card shadow border-0 p-3 h-100">
          <h6 class="text-center mb-3">Application Status</h6>
          <Doughnut v-if="hasStatus" :data="statusData" :options="pieOptions" />
          <p v-else class="text-muted text-center small mb-0">No application data yet</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card shadow border-0 p-3 h-100">
          <h6 class="text-center mb-3">Students by Branch</h6>
          <Bar v-if="hasBranch" :data="branchData" :options="barOptions" />
          <p v-else class="text-muted text-center small mb-0">No student data yet</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card shadow border-0 p-3 h-100">
          <h6 class="text-center mb-3">Jobs by Status</h6>
          <Bar v-if="hasJobs" :data="jobsData" :options="barOptions" />
          <p v-else class="text-muted text-center small mb-0">No job data yet</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Doughnut, Bar } from 'vue-chartjs'
import {
  Chart as ChartJS, ArcElement, Tooltip, Legend,
  CategoryScale, LinearScale, BarElement, Title
} from 'chart.js'
import { getAdminAnalytics } from '../services/admin'

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title)

const loading = ref(true)
const analytics = ref({ application_status: {}, students_by_branch: {}, jobs_by_status: {} })

const palette = ['#4e73df', '#1cc88a', '#f6c23e', '#e74a3b', '#36b9cc', '#858796']
const pieOptions = { responsive: true, maintainAspectRatio: true, aspectRatio: 1.4, plugins: { legend: { position: 'bottom' } }, cutout: '58%' }
const barOptions = {
  responsive: true,
  plugins: { legend: { display: false } },
  scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
}

const hasStatus = computed(() => Object.keys(analytics.value.application_status || {}).length > 0)
const hasBranch = computed(() => Object.keys(analytics.value.students_by_branch || {}).length > 0)
const hasJobs = computed(() => Object.keys(analytics.value.jobs_by_status || {}).length > 0)

const statusData = computed(() => {
  const d = analytics.value.application_status || {}
  const labels = Object.keys(d)
  return { labels, datasets: [{ data: labels.map(k => d[k]), backgroundColor: palette }] }
})
const branchData = computed(() => {
  const d = analytics.value.students_by_branch || {}
  const labels = Object.keys(d)
  return { labels, datasets: [{ label: 'Students', data: labels.map(k => d[k]), backgroundColor: '#4e73df' }] }
})
const jobsData = computed(() => {
  const d = analytics.value.jobs_by_status || {}
  const labels = Object.keys(d)
  return { labels, datasets: [{ label: 'Jobs', data: labels.map(k => d[k]), backgroundColor: '#1cc88a' }] }
})

const load = async () => {
  loading.value = true
  try {
    const res = await getAdminAnalytics()
    analytics.value = res.analytics || {}
  } catch (e) {
    console.error('analytics error', e)
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
