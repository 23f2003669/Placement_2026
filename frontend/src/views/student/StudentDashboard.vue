<template>
  <StudentLayout>

<h2 class="mb-4">
  📊 Student Dashboard
</h2>

<!-- Student Info Card -->
<div
  class="card shadow border-0 p-4 mb-4"
  v-if="student"
>
  <h5 class="mb-3">
    👤 Student Information
  </h5>

  <div class="row">

    <div class="col-md-6">
      <p>
        <strong>Name:</strong>
        {{ student.first_name }} {{ student.last_name }}
      </p>

      <p>
        <strong>Email:</strong>
        {{ student.email }}
      </p>

      <p>
        <strong>Roll Number:</strong>
        {{ student.roll_number || 'N/A' }}
      </p>
    </div>

    <div class="col-md-6">
      <p>
        <strong>Branch:</strong>
        {{ student.branch || 'N/A' }}
      </p>

      <p>
        <strong>Year:</strong>
        {{ student.year || 'N/A' }}
      </p>

      <p>
        <strong>CGPA:</strong>
        {{ student.cgpa || 'N/A' }}
      </p>
    </div>

  </div>
</div>

<!-- Statistics Cards -->
<div
  class="row mb-4"
  v-if="statistics"
>

  <div class="col-md-3">
    <div class="card shadow border-0 text-center p-4">
      <h3 class="text-primary">
        {{ statistics.total_applications }}
      </h3>
      <p>Applications</p>
    </div>
  </div>

  <div class="col-md-3">
    <div class="card shadow border-0 text-center p-4">
      <h3 class="text-warning">
        {{ statistics.shortlisted }}
      </h3>
      <p>Shortlisted</p>
    </div>
  </div>

  <div class="col-md-3">
    <div class="card shadow border-0 text-center p-4">
      <h3 class="text-info">
        {{ statistics.selected }}
      </h3>
      <p>Selected</p>
    </div>
  </div>

  <div class="col-md-3">
    <div class="card shadow border-0 text-center p-4">
      <h3 class="text-success">
        {{ statistics.total_placements }}
      </h3>
      <p>Placements</p>
    </div>
  </div>

</div>

  </StudentLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../services/api'
import StudentLayout from '../../layouts/StudentLayout.vue'

const router = useRouter()

const loading = ref(true)
const student = ref(null)
const statistics = ref(null)

const loadDashboard = async () => {
  try {
    const response = await api.get('/api/student/dashboard')

    if (response.data.success) {
      student.value = response.data.data.student
      statistics.value = response.data.data.statistics
    }
  } catch (error) {
    console.error('Error loading dashboard:', error)
    alert('Failed to load dashboard')
    router.push('/login')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDashboard()
})
</script>
