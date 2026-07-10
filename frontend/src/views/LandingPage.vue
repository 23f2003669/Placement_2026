<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar px-4 px-md-5 py-3" style="background:linear-gradient(120deg,#4f46e5,#6366f1)">
      <div class="d-flex align-items-center gap-2">
        <i class="bi bi-briefcase-fill text-white fs-5"></i>
        <span class="text-white fw-semibold fs-5">Placement Portal</span>
      </div>
      <div class="d-flex gap-2 ms-auto">
        <router-link to="/login" class="btn btn-outline-light btn-sm px-3">Login</router-link>
      </div>
    </nav>

    <!-- Hero -->
    <section class="text-white text-center py-5" style="background:linear-gradient(120deg,#4f46e5,#6366f1)">
      <div class="container py-5">
        <span class="badge bg-light text-primary mb-4 px-3 py-2">Campus Recruitment, Simplified</span>
        <h1 class="display-3 fw-bold mb-4">Your Gateway to<br>the Right Career</h1>
        <p class="lead mb-5 mx-auto" style="max-width:600px;opacity:.92">
          Connect students, companies, and the placement cell on one platform.
          Apply to drives, track applications, and get placed.
        </p>
        <div class="d-flex gap-3 justify-content-center flex-wrap">
          <router-link to="/register" class="btn btn-light btn-lg px-5 fw-semibold">
            <i class="bi bi-mortarboard-fill me-2"></i>Join as Student
          </router-link>
          <router-link to="/register-company" class="btn btn-outline-light btn-lg px-5 fw-semibold">
            <i class="bi bi-buildings-fill me-2"></i>Join as Company
          </router-link>
        </div>

        <!-- Live stats -->
        <div class="row g-3 mt-5 pt-3">
          <div class="col-6 col-md-3" v-for="s in statCards" :key="s.label">
            <div class="p-3 rounded-3" style="background:rgba(255,255,255,.12)">
              <div class="fs-3 fw-bold">{{ s.value }}</div>
              <div class="small" style="opacity:.85">{{ s.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="py-5" style="background:#f4f6fb">
      <div class="container py-4">
        <h2 class="text-center fw-bold mb-2">How it works</h2>
        <p class="text-center text-muted mb-5">Three roles, one seamless flow</p>
        <div class="row g-4">
          <div class="col-md-4" v-for="f in features" :key="f.title">
            <div class="card shadow border-0 h-100 p-4 text-center">
              <div class="rounded-circle d-flex align-items-center justify-content-center mx-auto mb-3"
                   :style="`width:64px;height:64px;background:${f.bg};color:${f.color};font-size:1.8rem`">
                <i :class="f.icon"></i>
              </div>
              <h5>{{ f.title }}</h5>
              <p class="text-muted small mb-0">{{ f.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="text-center py-4 text-muted small" style="background:#f4f6fb">
      Placement Portal &middot; Built for campus recruitment
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'
import { formatSalaryShort } from '../utils/format'

const stats = ref({})

const statCards = computed(() => [
  { label: 'Students Placed', value: stats.value.students_placed ?? '—' },
  { label: 'Recruiters', value: stats.value.recruiters ?? '—' },
  { label: 'Active Drives', value: stats.value.active_drives ?? '—' },
  { label: 'Highest Package', value: stats.value.highest_package ? formatSalaryShort(stats.value.highest_package) : '—' }
])

const features = [
  { title: 'For Students', desc: 'Browse drives, apply, track status, and download offer letters.', icon: 'bi bi-mortarboard-fill', bg: '#eef2ff', color: '#4f46e5' },
  { title: 'For Companies', desc: 'Post drives, review applicants, schedule interviews, and select talent.', icon: 'bi bi-buildings-fill', bg: '#ecfdf5', color: '#059669' },
  { title: 'For Admin', desc: 'Approve companies and drives, manage users, and view analytics.', icon: 'bi bi-shield-lock-fill', bg: '#f5f3ff', color: '#7c3aed' }
]

onMounted(async () => {
  try {
    const res = await api.get('/api/public/stats')
    stats.value = res.data.stats || {}
  } catch (e) { console.error('stats error', e) }
})
</script>
