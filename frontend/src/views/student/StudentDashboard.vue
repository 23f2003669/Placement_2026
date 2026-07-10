<template>
  <StudentLayout>
    <div v-if="loading" class="text-muted">Loading dashboard...</div>

    <div v-else>
      <!-- Welcome header + quick actions -->
      <div class="card shadow border-0 p-4 mb-4 welcome-banner"
           style="background:linear-gradient(120deg,#4f46e5,#6366f1);color:#fff">
        <div class="d-flex align-items-center justify-content-between flex-wrap gap-3">
          <div class="d-flex align-items-center gap-3">
            <img
              v-if="student.profile_pic && !photoBroken"
              :src="`http://127.0.0.1:5000${student.profile_pic}`"
              @error="photoBroken = true"
              class="rounded-circle"
              style="width:72px;height:72px;object-fit:cover;border:3px solid rgba(255,255,255,.5)"
            />
            <div v-else class="rounded-circle d-flex align-items-center justify-content-center"
                 style="width:72px;height:72px;background:rgba(255,255,255,.25);font-size:1.6rem;font-weight:600">
              {{ initials }}
            </div>
            <div>
              <h3 class="mb-1" style="color:#fff">Welcome, {{ student.first_name }}!</h3>
              <p class="mb-0" style="opacity:.9">{{ student.branch }} &middot; Year {{ student.year }} &middot; CGPA {{ student.cgpa }}</p>
            </div>
          </div>
          <div class="d-flex gap-2">
            <router-link to="/student/jobs" class="btn btn-light btn-sm fw-semibold">
              <i class="bi bi-search me-1"></i>Browse Jobs
            </router-link>
            <router-link to="/student/profile" class="btn btn-outline-light btn-sm fw-semibold">
              <i class="bi bi-person me-1"></i>Profile
            </router-link>
          </div>
        </div>
      </div>

      <!-- rest of your existing dashboard template stays same -->
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
        <div class="col-md-5">
          <div class="card shadow border-0 p-4 h-100">
            <h6 class="mb-3 section-title">Application Status</h6>
            <div v-if="hasApps" style="max-width:240px;margin:0 auto">
              <Doughnut :data="statusChart" :options="chartOptions" :plugins="[centerTextPlugin]" />
            </div>
            <div v-else class="text-muted small d-flex align-items-center justify-content-center" style="min-height:200px">
              No applications yet. Browse jobs to get started.
            </div>
          </div>
        </div>

        <div class="col-md-7">
          <div class="card shadow border-0 p-4 h-100">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h6 class="mb-0 section-title">Recent Applications</h6>
              <router-link to="/student/applications" class="small">View all</router-link>
            </div>
            <div v-if="recentApps.length === 0" class="text-muted small d-flex align-items-center justify-content-center" style="min-height:200px">
              No recent activity yet.
            </div>
            <div v-else class="list-group list-group-flush">
              <div v-for="a in recentApps" :key="a.application_id"
                   class="list-group-item d-flex justify-content-between align-items-center px-2 py-3 recent-row">
                <div class="d-flex align-items-center gap-3">
                  <div class="rounded-circle d-flex align-items-center justify-content-center"
                       style="width:40px;height:40px;background:#eef2ff;color:#4f46e5;font-weight:600">
                    {{ (a.company_name || '?')[0] }}
                  </div>
                  <div>
                    <div class="fw-semibold">{{ a.job_title }}</div>
                    <small class="text-muted">{{ a.company_name }} &middot; {{ formatDate(a.applied_on) }}</small>
                  </div>
                </div>
                <span class="badge" :class="statusClass(a.status)">{{ a.status }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </StudentLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { formatDate } from '../../utils/date'
import StudentLayout from '../../layouts/StudentLayout.vue'
import { getDashboard, getMyApplications } from '../../services/student'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
ChartJS.register(ArcElement, Tooltip, Legend)

const loading = ref(true)
const student = ref({})
const stats = ref({})
const applications = ref([])
const photoBroken = ref(false) // <-- add this

const initials = computed(() => {
  const f = (student.value.first_name || '?')[0]
  const l = (student.value.last_name || '')[0] || ''
  return (f + l).toUpperCase()
})

const statCards = computed(() => [
  { label: 'Applications', value: stats.value.total_applications || 0, icon: 'bi bi-file-earmark-text', bg: '#eef2ff', color: '#4f46e5' },
  { label: 'Shortlisted', value: stats.value.shortlisted || 0, icon: 'bi bi-star', bg: '#fff7ed', color: '#f59e0b' },
  { label: 'Selected', value: stats.value.selected || 0, icon: 'bi bi-check-circle', bg: '#ecfdf5', color: '#10b981' },
  { label: 'Placements', value: stats.value.total_placements || 0, icon: 'bi bi-briefcase', bg: '#eff6ff', color: '#3b82f6' }
])

const hasApps = computed(() => applications.value.length > 0)
const recentApps = computed(() =>
  [...applications.value].sort((a, b) => new Date(b.applied_on) - new Date(a.applied_on)).slice(0, 5)
)

const statusChart = computed(() => {
  const counts = {}
  applications.value.forEach(a => { counts[a.status] = (counts[a.status] || 0) + 1 })
  const labels = Object.keys(counts)
  return {
    labels,
    datasets: [{ data: labels.map(k => counts[k]), backgroundColor: ['#6b7280', '#06b6d4', '#f59e0b', '#10b981', '#ef4444'], borderWidth: 0 }]
  }
})

const chartOptions = { responsive: true, maintainAspectRatio: true, plugins: { legend: { position: 'bottom' } }, cutout: '68%' }

const centerTextPlugin = {
  id: 'centerText',
  beforeDraw(chart) {
    const { ctx, chartArea } = chart
    if (!chartArea) return
    const total = chart.data.datasets[0].data.reduce((a, b) => a + b, 0)
    const cx = (chartArea.left + chartArea.right) / 2
    const cy = (chartArea.top + chartArea.bottom) / 2
    ctx.save()
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillStyle = '#111827'
    ctx.font = '700 26px Sora, sans-serif'
    ctx.fillText(total, cx, cy - 6)
    ctx.fillStyle = '#6b7280'
    ctx.font = '500 12px Inter, sans-serif'
    ctx.fillText('Total', cx, cy + 16)
    ctx.restore()
  }
}

const statusClass = (s) => ({ applied:'bg-secondary', shortlisted:'bg-info text-dark', interview:'bg-warning text-dark', selected:'bg-success', rejected:'bg-danger' }[s] || 'bg-secondary')

const load = async () => {
  loading.value = true
  photoBroken.value = false // reset on load
  try {
    const dash = await getDashboard()
    student.value = dash.data.student
    stats.value = dash.data.statistics
    const apps = await getMyApplications()
    applications.value = apps.applications || []
  } catch (e) {
    console.error('dashboard error', e)
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.stat-card { transition: transform .18s ease, box-shadow .18s ease; }
.stat-card:hover { transform: translateY(-4px); }
.section-title { text-transform: uppercase; letter-spacing: .06em; font-size: .8rem; color: #6b7280; font-weight: 600; }
.recent-row { border-radius: 10px; transition: background .15s ease; }
.recent-row:hover { background: #f7f8fc; }
.welcome-banner { position: relative; overflow: hidden; }
</style>