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

          <p class="mb-1"><strong>Salary:</strong> {{ formatSalary(p.salary) }}</p>
          <p class="mb-1" v-if="p.joining_date"><strong>Joining Date:</strong> {{ formatDate(p.joining_date) }}</p>
          <p class="mb-3" v-if="p.placed_on"><strong>Placed On:</strong> {{ formatDate(p.placed_on) }}</p>

          <button class="btn btn-primary btn-sm mt-auto" :disabled="downloadingId === p.id" @click="downloadOffer(p.id)">
            <i class="bi bi-download me-1"></i>
            {{ downloadingId === p.id ? 'Generating...' : 'Download Offer Letter' }}
          </button>

        </div>
      </div>
    </div>

  </StudentLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import StudentLayout from '../../layouts/StudentLayout.vue'
import { getPlacements, downloadOfferLetter } from '../../services/student'
import { formatSalary } from '../../utils/format'

const placements = ref([])
const loading = ref(true)
const downloadingId = ref(null)

const formatDate = (iso) => iso ? new Date(iso).toLocaleDateString() : '-'

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

const downloadOffer = async (placementId) => {
  downloadingId.value = placementId
  try {
    const blob = await downloadOfferLetter(placementId)
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `offer_letter_${placementId}.pdf`
    a.style.display = 'none'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  } catch (error) {
    alert('Failed to download offer letter')
  } finally {
    downloadingId.value = null
  }
}

onMounted(() => loadPlacements())
</script>
