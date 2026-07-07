<template>
  <AdminLayout>

    <h1 class="mb-4">Placements</h1>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else class="card shadow border-0">
      <div class="card-body">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Student</th>
              <th>Company</th>
              <th>Job Title</th>
              <th>Salary</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="placement in placements" :key="placement.placement_id">
              <td>{{ placement.student_name }}</td>
              <td>{{ placement.company_name }}</td>
              <td>{{ placement.job_title }}</td>
              <td>₹{{ placement.salary }}</td>
              <td>
                <span class="badge bg-success">{{ placement.status }}</span>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="placements.length === 0" class="text-muted text-center py-3">
          No placements yet.
        </p>
      </div>
    </div>

  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '../../layouts/AdminLayout.vue'
import { getPlacements } from '../../services/placementAdmin'

const placements = ref([])
const loading = ref(true)

const loadPlacements = async () => {
  try {
    loading.value = true
    const response = await getPlacements()
    placements.value = response.placements
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to load placements')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPlacements()
})
</script>