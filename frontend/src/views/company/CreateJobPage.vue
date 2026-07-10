<template>
  <CompanyLayout>
    <h1 class="mb-4">Create New Job</h1>

    <div class="card shadow border-0">
      <div class="card-body">
        <form @submit.prevent="createJob">

          <div class="mb-3">
            <label class="form-label">Job Title *</label>
            <input type="text" class="form-control" v-model="form.job_title" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Job Description *</label>
            <textarea class="form-control" rows="4" v-model="form.job_description" required></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label">Skills Required</label>
            <input type="text" class="form-control" placeholder="e.g. Python, React" v-model="form.skills_required" />
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Salary Min</label>
              <input type="number" class="form-control" v-model="form.salary_min" />
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Salary Max</label>
              <input type="number" class="form-control" v-model="form.salary_max" />
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label">Location</label>
            <input type="text" class="form-control" v-model="form.location" />
          </div>

          <div class="mb-3">
            <label class="form-label">Job Type</label>
            <select class="form-control" v-model="form.job_type">
              <option value="Full Time">Full Time</option>
              <option value="Internship">Internship</option>
            </select>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Minimum CGPA</label>
              <input type="number" step="0.01" class="form-control" v-model="form.min_cgpa" />
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Max Backlogs</label>
              <input type="number" class="form-control" v-model="form.max_backlog" />
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label">Eligible Branches</label>
            <input type="text" class="form-control" placeholder="CSE,ECE,IT" v-model="form.eligible_branches" />
          </div>

          <div class="mb-3">
            <label class="form-label">Eligible Years</label>
            <input type="text" class="form-control" placeholder="3,4" v-model="form.eligible_years" />
          </div>

          <div class="mb-4">
            <label class="form-label">Application Deadline *</label>
           <input type="datetime-local" class="form-control" v-model="form.application_deadline" :min="minDeadline" required />
          </div>

          <button class="btn btn-success" type="submit" :disabled="loading">
            {{ loading ? 'Creating...' : 'Create Job' }}
          </button>

        </form>
      </div>
    </div>
  </CompanyLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import CompanyLayout from '../../layouts/CompanyLayout.vue'
import api from '../../services/api'

const router = useRouter()
const loading = ref(false)
const minDeadline = new Date().toISOString().slice(0, 16)
const form = ref({
  job_title: '',
  job_description: '',
  skills_required: '',
  salary_min: '',
  salary_max: '',
  location: '',
  job_type: 'Full Time',
  min_cgpa: '',
  eligible_branches: '',
  eligible_years: '',
  max_backlog: '',
  application_deadline: ''
})

const createJob = async () => {
  try {
    loading.value = true
    if (form.value.salary_min && form.value.salary_max &&
        Number(form.value.salary_min) > Number(form.value.salary_max)) {
      alert('Salary Min cannot be greater than Salary Max')
      return
    }
    const payload = {
      ...form.value,
      application_deadline: new Date(form.value.application_deadline).toISOString()
    }
    const response = await api.post('/api/company/create-job', payload)
    alert(response.data.message)
    router.push('/company/jobs')
  } catch (error) {
    alert(error.response?.data?.error || 'Failed to create job')
  } finally {
    loading.value = false
  }
}
</script>