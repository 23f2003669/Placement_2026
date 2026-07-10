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
              <th>Status</th>
              <th>Profile</th>
              <th>Feedback</th>
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
                <span class="badge" :class="{
                  'bg-primary': applicant.application_status === 'applied',
                  'bg-warning text-dark': applicant.application_status === 'shortlisted',
                  'bg-info': applicant.application_status === 'interview',
                  'bg-success': applicant.application_status === 'selected',
                  'bg-danger': applicant.application_status === 'rejected'
                }">{{ applicant.application_status }}</span>
              </td>
              <td>
                <button class="btn btn-outline-primary btn-sm" @click="openProfile(applicant)">View</button>
              </td>
              <td class="small text-muted" style="max-width:200px">
                {{ applicant.company_feedback || '-' }}
              </td>
              <td>
                <button v-if="applicant.application_status === 'applied'"
                  class="btn btn-success btn-sm me-1"
                  @click="handleShortlist(applicant.application_id)">Shortlist</button>
                <button v-if="applicant.application_status === 'applied'"
                  class="btn btn-danger btn-sm"
                  @click="openRejectModal(applicant.application_id)">Reject</button>
                <button v-if="applicant.application_status === 'shortlisted'"
                  class="btn btn-primary btn-sm"
                  @click="openInterviewModal(applicant.application_id)">Interview</button>
                <button v-if="applicant.application_status === 'interview'"
                  class="btn btn-success btn-sm me-1"
                  @click="openSelectModal(applicant.application_id)">Select</button>
                <button v-if="applicant.application_status === 'interview'"
                  class="btn btn-danger btn-sm"
                  @click="openRejectModal(applicant.application_id)">Reject</button>
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
            <div class="mb-3">
              <label class="form-label">Meeting Link (Google Meet / Zoom)</label>
              <input type="url" class="form-control" placeholder="https://meet.google.com/..." v-model="interviewForm.link" />
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
              <label class="form-label">Salary (per annum)</label>
              <input type="number" min="0" class="form-control" v-model="selectedForm.salary" />
            </div>
            <div class="mb-3">
              <label class="form-label">Joining Date</label>
              <input type="date" class="form-control" v-model="selectedForm.joining_date" />
            </div>
            <div class="mb-3">
              <label class="form-label">Feedback (optional)</label>
              <textarea class="form-control" rows="2" placeholder="Great communication, strong fundamentals..." v-model="selectedForm.feedback"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showSelectModal = false">Cancel</button>
            <button class="btn btn-success" @click="submitSelection">Confirm</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Reject Modal (with feedback) -->
    <div v-if="showRejectModal" class="modal fade show d-block" style="background:rgba(0,0,0,0.5)">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Reject Applicant</h5>
            <button class="btn-close" @click="showRejectModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Reason / Feedback for the student</label>
              <textarea class="form-control" rows="3" placeholder="Reason for rejection (shared with the student)..." v-model="rejectFeedback"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showRejectModal = false">Cancel</button>
            <button class="btn btn-danger" @click="submitReject">Reject</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Student Profile Modal -->
    <div v-if="showProfileModal" class="modal fade show d-block" style="background:rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Student Profile</h5>
            <button class="btn-close" @click="showProfileModal = false"></button>
          </div>
          <div class="modal-body" v-if="profileData">
            <div class="d-flex align-items-center gap-4 mb-4 flex-wrap">
              <img v-if="profileData.profile_pic" :src="`http://127.0.0.1:5000${profileData.profile_pic}`"
                   class="rounded-circle" style="width:90px;height:90px;object-fit:cover;border:3px solid #e8eaf0" />
              <div v-else class="rounded-circle d-flex align-items-center justify-content-center"
                   style="width:90px;height:90px;background:#4f46e5;color:#fff;font-size:1.8rem;font-weight:600">
                {{ (profileData.student_name || '?')[0] }}
              </div>
              <div>
                <h4 class="mb-1">{{ profileData.student_name }}</h4>
                <p class="text-muted mb-0">{{ profileData.branch }} &middot; Year {{ profileData.year }}</p>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6 mb-2"><strong>Email:</strong> {{ profileData.email }}</div>
              <div class="col-md-6 mb-2"><strong>Roll Number:</strong> {{ profileData.roll_number || '-' }}</div>
              <div class="col-md-6 mb-2"><strong>Phone:</strong> {{ profileData.phone || '-' }}</div>
              <div class="col-md-6 mb-2"><strong>CGPA:</strong> {{ profileData.cgpa }}</div>
              <div class="col-12 mb-2"><strong>Bio:</strong> {{ profileData.bio || '-' }}</div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              v-if="profileData && profileData.resume_url"
              class="btn btn-outline-primary"
              @click="openResume(profileData.resume_url)"
            >
              View Resume
            </button>
            <button class="btn btn-secondary" @click="showProfileModal = false">Close</button>
          </div>
        </div>
      </div>
    </div>

  </CompanyLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { formatDateTime } from '../../utils/date'
import CompanyLayout from '../../layouts/CompanyLayout.vue'
import { getApplicants, shortlistStudent, rejectApplication, scheduleInterview, sendResult, downloadResume } from '../../services/company'

const route = useRoute()
const applicants = ref([])
const loading = ref(true)
const showInterviewModal = ref(false)
const showSelectModal = ref(false)
const showRejectModal = ref(false)
const showProfileModal = ref(false)
const profileData = ref(null)
const selectedInterviewApplicationId = ref(null)
const selectedApplicationId = ref(null)
const rejectApplicationId = ref(null)
const rejectFeedback = ref('')
const interviewForm = ref({ date: '', time: '', link: '' })
const selectedForm = ref({ salary: '', joining_date: '', feedback: '' })

const openProfile = (applicant) => {
  profileData.value = applicant
  showProfileModal.value = true
}

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

const openRejectModal = (id) => {
  rejectApplicationId.value = id
  rejectFeedback.value = ''
  showRejectModal.value = true
}

const submitReject = async () => {
  try {
    await rejectApplication(rejectApplicationId.value, rejectFeedback.value || null)
    showRejectModal.value = false
    await loadApplicants()
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to reject')
  }
}

const openInterviewModal = (id) => {
  selectedInterviewApplicationId.value = id
  interviewForm.value = { date: '', time: '', link: '' }
  showInterviewModal.value = true
}

const submitInterview = async () => {
  try {
    const dt = `${interviewForm.value.date}T${interviewForm.value.time}:00`
    await scheduleInterview(selectedInterviewApplicationId.value, dt, interviewForm.value.link || null)
    showInterviewModal.value = false
    await loadApplicants()
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to schedule interview')
  }
}

const openSelectModal = (id) => {
  selectedApplicationId.value = id
  selectedForm.value = { salary: '', joining_date: '', feedback: '' }
  showSelectModal.value = true
}

const submitSelection = async () => {
  try {
    await sendResult(
      selectedApplicationId.value,
      'selected',
      selectedForm.value.salary,
      selectedForm.value.joining_date,
      selectedForm.value.feedback || null
    )
    showSelectModal.value = false
    await loadApplicants()
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to select student')
  }
}

const openResume = async (resumeUrl) => {
  try {
    const blob = await downloadResume(resumeUrl) // token attached by axios
    const url = URL.createObjectURL(blob)
    window.open(url, '_blank')
    setTimeout(() => URL.revokeObjectURL(url), 10000)
  } catch (error) {
    alert(error.response?.data?.error || 'Unable to open resume')
  }
}


onMounted(() => {
  loadApplicants()
})
</script>
