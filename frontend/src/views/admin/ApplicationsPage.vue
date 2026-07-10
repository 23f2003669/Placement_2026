<template>
  <AdminLayout>

    <h1 class="mb-4">Applications</h1>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else class="card shadow border-0">
      <div class="card-body">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Student</th>
              <th>Email</th>
              <th>Company</th>
              <th>Job</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in applications" :key="app.application_id">
              <td>{{ app.student_name }}</td>
              <td>{{ app.student_email }}</td>
              <td>{{ app.company_name }}</td>
              <td>{{ app.job_title }}</td>
              <td>
                <span
                  class="badge"
                  :class="{
                    'bg-primary': app.status === 'applied',
                    'bg-warning text-dark': app.status === 'shortlisted',
                    'bg-info': app.status === 'interview',
                    'bg-success': app.status === 'selected',
                    'bg-danger': app.status === 'rejected'
                  }"
                >
                  {{ app.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="applications.length === 0" class="text-muted text-center py-3">
          No applications found.
        </p>
      </div>
    </div>

  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '../../layouts/AdminLayout.vue'
import { getApplications } from '../../services/admin'

const applications = ref([])
const loading = ref(true)

const loadApplications = async () => {
  try {
    loading.value = true
    const response = await getApplications()
    applications.value = response.applications
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to load applications')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadApplications()
})
</script>