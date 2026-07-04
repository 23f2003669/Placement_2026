<template>
  <CompanyLayout>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-success" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-muted mt-2">Loading dashboard...</p>
    </div>

    <div v-else>

      <h1 class="mb-4">Company Dashboard</h1>

      <!-- Company Info -->
      <div
        v-if="company"
        class="card shadow border-0 p-4 mb-4"
      >
        <div class="d-flex align-items-center justify-content-between mb-3">
          <h5 class="mb-0">{{ company.company_name }}</h5>
          <span
            class="badge"
            :class="{
              'bg-success': company.approval_status === 'approved',
              'bg-warning text-dark': company.approval_status === 'pending',
              'bg-danger': company.approval_status === 'rejected'
            }"
          >
            {{ company.approval_status }}
          </span>
        </div>

        <div class="row">
          <div class="col-md-6">
            <p><strong>Industry:</strong> {{ company.industry || 'N/A' }}</p>
            <p><strong>Location:</strong> {{ company.location || 'N/A' }}</p>
          </div>
          <div class="col-md-6">
            <p><strong>Website:</strong> {{ company.website || 'N/A' }}</p>
          </div>
        </div>
      </div>

      <!-- Stats -->
      <div v-if="statistics" class="row g-4">

        <div class="col-md-4">
          <div class="card shadow border-0">
            <div class="card-body text-center">
              <h2 class="text-primary">{{ statistics.total_jobs }}</h2>
              <p class="mb-0 text-muted">Total Jobs</p>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow border-0">
            <div class="card-body text-center">
              <h2 class="text-warning">{{ statistics.total_applicants }}</h2>
              <p class="mb-0 text-muted">Applicants</p>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow border-0">
            <div class="card-body text-center">
              <h2 class="text-success">{{ statistics.shortlisted_candidates }}</h2>
              <p class="mb-0 text-muted">Shortlisted</p>
            </div>
          </div>
        </div>

      </div>

    </div>

  </CompanyLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../services/api'
import CompanyLayout from '../../layouts/CompanyLayout.vue'

const router = useRouter()
const company = ref(null)
const statistics = ref(null)
const loading = ref(true)

const loadDashboard = async () => {
  try {
    const response = await api.get('/api/company/dashboard')
    company.value = response.data.data.company
    statistics.value = response.data.data.statistics

  } catch (error) {
  const status = error.response?.status
  const errorMsg = error.response?.data?.error

  if (status === 403) {
    if (errorMsg === 'pending') {
      alert('Your company registration is pending admin approval. Please wait.')
    } else if (errorMsg === 'rejected') {
      alert('Your company registration has been rejected by admin. Please contact the institute.')
    } else if (errorMsg === 'Your company has been blacklisted') {
      alert('Your company has been blacklisted. Contact admin.')
    } else {
      alert(errorMsg || 'Access denied.')
    }
    router.push('/login')
    return
  }

  if (status === 401) {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
    return
  }

  alert(errorMsg || 'Failed to load dashboard')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDashboard()
})
</script>