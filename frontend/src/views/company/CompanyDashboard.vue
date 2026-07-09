<template>
  <CompanyLayout>

    <div v-if="loading" class="text-muted">Loading dashboard...</div>

    <!-- Approval pending/rejected -->
    <div v-else-if="statusMsg" class="card shadow border-0 p-5 text-center">
      <i class="bi bi-hourglass-split" style="font-size:2.5rem;color:#f59e0b"></i>
      <h4 class="mt-3">{{ statusMsg }}</h4>
    </div>

    <div v-else>
      <!-- Welcome banner -->
      <div class="card shadow border-0 p-4 mb-4"
           style="background:linear-gradient(120deg,#059669,#10b981);color:#fff">
        <div class="d-flex align-items-center justify-content-between flex-wrap gap-3">
          <div class="d-flex align-items-center gap-3">
            <div class="rounded-circle d-flex align-items-center justify-content-center"
                 style="width:72px;height:72px;background:rgba(255,255,255,.25);font-size:1.6rem;font-weight:600">
              {{ (company.company_name || '?')[0] }}
            </div>
            <div>
              <h3 class="mb-1" style="color:#fff">{{ company.company_name }}</h3>
              <p class="mb-0" style="opacity:.9">{{ company.industry || 'Company' }} &middot; {{ company.location || '-' }}</p>
            </div>
          </div>
          <div class="d-flex gap-2">
            <router-link to="/company/create-job" class="btn btn-light btn-sm fw-semibold">
              <i class="bi bi-plus-circle me-1"></i>Post Job
            </router-link>
            <router-link to="/company/jobs" class="btn btn-outline-light btn-sm fw-semibold">
              <i class="bi bi-briefcase me-1"></i>My Jobs
            </router-link>
          </div>
        </div>
      </div>

      <!-- Stat cards -->
      <div class="row g-3 mb-4">
        <div class="col-6 col-md-3" v-for="s in statCards" :key="s.label">
          <div class="card shadow border-0 p-3 h-100 stat-card">
            <div class="d-flex align-items-center gap-3">
              <div class="rounded d-flex align-items-center justify-content-center"
                   :style="`width:48px;height:48px;background:${s.bg};color:${s.color};font-size:1.4rem`">
                <i :class="s.icon"></i>
              </div>
              <div>
                <h4 class="mb-0">{{ s.value }}</h4>
                <small class="text-muted">{{ s.label }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-4">
        <!-- Applicants per job chart -->
        <div class="col-md-7">
          <div class="card shadow border-0 p-4 h-100">
            <h6 class="mb-3 section-title">Applicants per Job</h6>
            <div v-if="jobs.length" style="max-height:300px">
              <Bar :data="jobChart" :options="barOptions" />
            </div>
            <div v-else class="text-muted small d-flex align-items-center justify-content-center" style="min-height:200px">
              No jobs posted yet.
            </div>
          </div>
        </div>

        <!-- Recent jobs -->
        <div class="col-md-5">
          <div class="card shadow border-0 p-4 h-100">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h6 class="mb-0 section-title">Recent Jobs</h6>
              <router-link to="/company/jobs" class="small">View all</router-link>
            </div>
            <div v-if="jobs.length === 0" class="text-muted small">No jobs yet.</div>
            <div v-else class="list-group list-group-flush">
              <div v-for="j in recentJobs" :key="j.id"
                   class="list-group-item d-flex justify-content-between align-items-center px-2 py-3 recent-row">
                <div>
                  <div class="fw-semibold">{{ j.job_title }}</div>
                  <small class="text-muted">{{ j.applicants_count }} applicant(s)</small>
                </div>
                <span class="badge" :class="j.status === 'approved' ? 'bg-success' : j.status === 'closed' ? 'bg-secondary' : 'bg-warning text-dark'">
                  {{ j.status }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </CompanyLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../services/api'
import CompanyLayout from '../../layouts/CompanyLayout.vue'
import { getMyJobs } from '../../services/company'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from 'chart.js'
ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)

const loading = ref(true)
const statusMsg = ref('')
const company = ref({})
const stats = ref({})
const jobs = ref([])

const statCards = computed(() => [
  { label: 'Total Jobs', value: stats.value.total_jobs || 0, icon: 'bi bi-briefcase', bg: '#ecfdf5', color: '#059669' },
  { label: 'Applicants', value: stats.value.total_applicants || 0, icon: 'bi bi-people', bg: '#eef2ff', color: '#4f46e5' },
  { label: 'Shortlisted', value: stats.value.shortlisted_candidates || 0, icon: 'bi bi-star', bg: '#fff7ed', color: '#f59e0b' },
  { label: 'Active Jobs', value: jobs.value.filter(j => j.status === 'approved').length, icon: 'bi bi-check-circle', bg: '#eff6ff', color: '#3b82f6' }
])

const recentJobs = computed(() =>
  [...jobs.value].sort((a, b) => new Date(b.posted_on) - new Date(a.posted_on)).slice(0, 5)
)

const jobChart = computed(() => ({
  labels: jobs.value.map(j => j.job_title),
  datasets: [{ label: 'Applicants', data: jobs.value.map(j => j.applicants_count), backgroundColor: '#10b981', borderRadius: 6 }]
}))
const barOptions = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } }

const load = async () => {
  loading.value = true
  try {
    const res = await api.get('/api/company/dashboard')
    company.value = res.data.data.company
    stats.value = res.data.data.statistics
    const jobsRes = await getMyJobs()
    jobs.value = jobsRes.jobs || []
  } catch (e) {
    const err = e.response?.data?.error
    if (err === 'pending') statusMsg.value = 'Your company registration is pending admin approval.'
    else if (err === 'rejected') statusMsg.value = 'Your company registration was rejected.'
    else console.error('dashboard error', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => load())
</script>

<style scoped>
.stat-card { transition: transform .18s ease, box-shadow .18s ease; }
.stat-card:hover { transform: translateY(-4px); }
.section-title { text-transform: uppercase; letter-spacing: .06em; font-size: .8rem; color: #6b7280; font-weight: 600; }
.recent-row { border-radius: 10px; transition: background .15s ease; }
.recent-row:hover { background: #f0fdf4; }
</style>
