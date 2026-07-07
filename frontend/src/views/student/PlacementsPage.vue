<template>
  <StudentLayout>

    <h2 class="mb-4">My Placements</h2>

    <div v-if="loading" class="text-muted">Loading placements...</div>

    <div v-else-if="placements.length === 0" class="text-muted">
      No placements yet.
    </div>

    <div v-else class="row">
      <div class="col-md-6 mb-4" v-for="p in placements" :key="p.id">
        <div class="card shadow border-0 h-100 p-3">

          <div class="d-flex justify-content-between align-items-start">
            <h5 class="mb-1">{{ p.job_title }}</h5>
            <span class="badge bg-success">{{ p.status }}</span>
          </div>

          <p class="text-muted mb-2">{{ p.company_name }}</p>

          <p class="mb-1">
            <strong>Salary:</strong> {{ p.salary }} {{ p.currency }}
          </p>

          <p class="mb-1" v-if="p.joining_date">
            <strong>Joining Date:</strong> {{ formatDate(p.joining_date) }}
          </p>

          <p class="mb-0" v-if="p.placed_on">
            <strong>Placed On:</strong> {{ formatDate(p.placed_on) }}
          </p>

        </div>
      </div>
    </div>

  </StudentLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import StudentLayout from '../../layouts/StudentLayout.vue'
import { getPlacements } from '../../services/student'

const placements = ref([])
const loading = ref(true)

const formatDate = (isoString) => {
  if (!isoString) return '-'
  return new Date(isoString).toLocaleDateString()
}

const loadPlacements = async () => {
  loading.value = true
  try {
    const res = await getPlacements()
    placements.value = res.placements || []
  } catch (error) {
    console.error('Error loading placements:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPlacements()
})
</script>
