<template>
  <AdminLayout>
    <div v-if="loading" class="text-muted">Loading dashboard...</div>
    <div v-else>
      <!-- Welcome banner -->
      <div class="card shadow border-0 p-4 mb-4"
           style="background:linear-gradient(120deg,#7c3aed,#8b5cf6);color:#fff">
        <div class="d-flex align-items-center justify-content-between flex-wrap gap-3">
          <div class="d-flex align-items-center gap-3">
            <div class="rounded-circle d-flex align-items-center justify-content-center"
                 style="width:72px;height:72px;background:rgba(255,255,255,.25);font-size:1.6rem">
              <i class="bi bi-shield-lock"></i>
            </div>
            <div>
              <h3 class="mb-1" style="color:#fff">Admin Dashboard</h3>
              <p class="mb-0" style="opacity:.9">Institute Placement Cell &middot; Overview</p>
            </div>
          </div>
          <div class="d-flex gap-2">
            <router-link to="/admin/companies" class="btn btn-light btn-sm fw-semibold">
              <i class="bi bi-building me-1"></i>Companies
            </router-link>
            <router-link to="/admin/students" class="btn btn-outline-light btn-sm fw-semibold">
              <i class="bi bi-mortarboard me-1"></i>Students
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

      <!-- Pending Approvals -->
      <div class="row g-3 mb-4" v-if="pendingCompanies || pendingJobs">
        <div class="col-md-6" v-if="pendingCompanies">
          <router-link to="/admin/companies" class="text-decoration-none">
            <div class="card border-0 p-3 pending-card" style="background:#fffbeb;border-left:4px solid #f59e0b !important">
              <div class="d-flex align-items-center gap-3">
                <i class="bi bi-hourglass-split" style="font-size:1.6rem;color:#f59e0b"></i>
                <div>
                  <h5 class="mb-0" style="color:#92400e">{{ pendingCompanies }} Company registration(s) pending</h5>
                  <small class="text-muted">Click to review and approve</small>
                </div>
              </div>
            </div>
          </router-link>
        </div>
        <div class="col-md-6" v-if="pendingJobs">
          <router-link to="/admin/jobs" class="text-decoration-none">
            <div class="card border-0 p-3 pending-card" style="background:#fffbeb;border-left:4px solid #f59e0b !important">
              <div class="d-flex align-items-center gap-3">
                <i class="bi bi-hourglass-split" style="font-size:1.6rem;color:#f59e0b"></i>
                <div>
                  <h5 class="mb-0" style="color:#92400e">{{ pendingJobs }} Job posting(s) pending</h5>
                  <small class="text-muted">Click to review and approve</small>
                </div>
              </div>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Charts -->
      <AdminCharts />
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '../../layouts/AdminLayout.vue'
import AdminCharts from '../../components/AdminCharts.vue'
import { getDashboardStats } from '../../services/admin'

const loading = ref(true)
const data = ref({})

const pendingCompanies = computed(() => data.value.companies?.pending || 0)
const pendingJobs = computed(() => data.value.job_positions?.pending || 0)

const statCards = computed(() => [
  { label: 'Students', value: data.value.students?.total || 0, icon: 'bi bi-mortarboard', bg: '#f5f3ff', color: '#7c3aed' },
  { label: 'Companies', value: data.value.companies?.total || 0, icon: 'bi bi-building', bg: '#eef2ff', color: '#4f46e5' },
  { label: 'Jobs', value: data.value.job_positions?.total || 0, icon: 'bi bi-briefcase', bg: '#ecfdf5', color: '#059669' },
  { label: 'Applications', value: data.value.applications?.total || 0, icon: 'bi bi-file-earmark-text', bg: '#eff6ff', color: '#3b82f6' }
])

const load = async () => {
  loading.value = true
  try {
    const res = await getDashboardStats()
    data.value = res.data || res
  } catch (e) { console.error('admin dashboard error', e) }
  finally { loading.value = false }
}

onMounted(() => load())
</script>

<style scoped>
.stat-card { transition: transform .18s ease, box-shadow .18s ease; }
.stat-card:hover { transform: translateY(-4px); }
.pending-card { border-radius: 12px; transition: transform .18s ease, box-shadow .18s ease; }
.pending-card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(245,158,11,.2); }
.pending-card { border-radius: 12px; transition: transform .18s ease, box-shadow .18s ease; }
.pending-card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(245,158,11,.2); }
</style>
