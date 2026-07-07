<template>
  <CompanyLayout>
    <h1 class="mb-4">Applicants</h1>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else class="card shadow border-0">
      <div class="card-body">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Branch</th>
              <th>CGPA</th>
              <th>Resume</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="applicant in applicants" :key="applicant.application_id">
              <td>{{ applicant.student_name }}</td>
              <td>{{ applicant.email }}</td>
              <td>{{ applicant.branch }}</td>
              <td>{{ applicant.cgpa }}</td>
              <td>
                <a v-if="applicant.resume_url"
                  :href="`http://127.0.0.1:5000${applicant.resume_url}`"
                  target="_blank"
                  class="btn btn-outline-primary btn-sm">View</a>
                <span v-else class="text-muted small">None</span>
              </td>
              <td>
                <span class="badge" :class="{
                  'bg-primary': applicant.application_status === 'applied',
                  'bg-warning text-dark': applicant.application_status === 'shortlisted',
                  'bg-info': applicant.application_status === 'interview',
                  'bg-success': applicant.application_status === 'selected',
                  'bg-danger': applicant.application_status === 'rejected'
                }">{{ applicant.application_status }}</span>
              </td>
              <td>
                <button v-if="applicant.application_status === 'applied'"
                  class="btn btn-success btn-sm me-1"
                  @click="handleShortlist(applicant.application_id)">Shortlist</button>
                <button v-if="applicant.application_status === 'applied'"
                  class="btn btn-danger btn-sm"
                  @click="handleReject(applicant.application_id)">Reject</button>
                <button v-if="applicant.application_status === 'shortlisted'"
                  class="btn btn-primary btn-sm"
                  @click="openInterviewModal(applicant.application_id)">Interview</button>
                <button v-if="applicant.application_status === 'interview'"
                  class="btn btn-success btn-sm me-1"
                  @click="openSelectModal(applicant.application_id)">Select</button>
                <button v-if="applicant.application_status === 'interview'"
                  class="btn btn-danger btn-sm"
                  @click="handleReject(applicant.application_id)">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="applicants.length === 0" class="text-muted text-center py-3">No applicants yet.</p>
      </div>
    </div>

    <!-- Interview Modal -->
    <div v-if="showInterviewModal" class="modal fade show d-block" style="background:rgba(0,0,0,0.5)">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Schedule Interview</h5>
            <button class="btn-close" @click="showInterviewModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Date</label>
              <input type="date" class="form-control" v-model="interviewForm.date" />
            </div>
            <div class="mb-3">
              <label class="form-label">Time</label>
              <input type="time" class="form-control" v-model="interviewForm.time" />
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showInterviewModal = false">Cancel</button>
            <button class="btn btn-primary" @click="submitInterview">Schedule</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Select Modal -->
    <div v-if="showSelectModal" class="modal fade show d-block" style="background:rgba(0,0,0,0.5)">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Select Candidate</h5>
            <button class="btn-close" @click="showSelectModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Salary</label>
              <input type="number" class="form-control" v-model="selectedForm.salary" />
            </div>
            <div class="mb-3">
              <label class="form-label">Joining Date</label>
              <input type="date" class="form-control" v-model="selectedForm.joining_date" />
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showSelectModal = false">Cancel</button>
            <button class="btn btn-success" @click="submitSelection">Confirm</button>
          </div>
        </div>
      </div>
    </div>

  </CompanyLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import CompanyLayout from '../../layouts/CompanyLayout.vue'
import { getApplicants, shortlistStudent, rejectApplication, scheduleInterview, sendResult } from '../../services/company'

const route = useRoute()
const applicants = ref([])
const loading = ref(true)
const showInterviewModal = ref(false)
const showSelectModal = ref(false)
const selectedInterviewApplicationId = ref(null)
const selectedApplicationId = ref(null)
const interviewForm = ref({ date: '', time: '' })
const selectedForm = ref({ salary: '', joining_date: '' })

const loadApplicants = async () => {
  try {
    loading.value = true
    const response = await getApplicants(route.params.jobId)
    applicants.value = response.applicants
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to load applicants')
  } finally {
    loading.value = false
  }
}

const handleShortlist = async (id) => {
  try {
    await shortlistStudent(id)
    await loadApplicants()
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to shortlist')
  }
}

const handleReject = async (id) => {
  try {
    await rejectApplication(id)
    await loadApplicants()
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to reject')
  }
}

const openInterviewModal = (id) => {
  selectedInterviewApplicationId.value = id
  showInterviewModal.value = true
}

const submitInterview = async () => {
  try {
    const dt = `${interviewForm.value.date}T${interviewForm.value.time}:00`
    await scheduleInterview(selectedInterviewApplicationId.value, dt)
    showInterviewModal.value = false
    interviewForm.value = { date: '', time: '' }
    await loadApplicants()
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to schedule interview')
  }
}

const openSelectModal = (id) => {
  selectedApplicationId.value = id
  showSelectModal.value = true
}

const submitSelection = async () => {
  try {
    await sendResult(selectedApplicationId.value, 'selected', selectedForm.value.salary, selectedForm.value.joining_date)
    showSelectModal.value = false
    selectedForm.value = { salary: '', joining_date: '' }
    await loadApplicants()
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to select student')
  }
}

onMounted(() => {
  loadApplicants()
})
</script>