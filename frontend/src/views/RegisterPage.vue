<template>
  <div class="auth-page d-flex align-items-center py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-7 col-xl-6">
          <div class="card auth-card border-0 shadow-lg">
            <div class="card-body p-4 p-md-5">
              <div class="text-center mb-4">
                <h2 class="fw-bold mb-1">Student Registration</h2>
                <p class="text-muted mb-0">Create your Placement Portal account</p>
              </div>

              <form @submit.prevent="register">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">First Name *</label>
                    <input type="text" class="form-control form-control-lg" placeholder="Enter first name" v-model.trim="formData.first_name" required />
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Last Name</label>
                    <input type="text" class="form-control form-control-lg" placeholder="Enter last name" v-model.trim="formData.last_name" />
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label fw-semibold">Email *</label>
                  <input type="email" class="form-control form-control-lg" placeholder="Enter email" v-model.trim="formData.email" required />
                </div>

                <div class="mb-3">
                  <label class="form-label fw-semibold">Password *</label>
                  <input type="password" class="form-control form-control-lg" placeholder="Min 6 characters" v-model="formData.password" minlength="6" required />
                </div>

                <div class="mb-3">
                  <label class="form-label fw-semibold">Roll Number *</label>
                  <input type="text" class="form-control form-control-lg" placeholder="Enter roll number" v-model.trim="formData.roll_number" required />
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Branch *</label>
                    <select class="form-select form-select-lg" v-model="formData.branch" required>
                      <option value="">Select Branch</option>
                      <option v-for="b in branchOptions" :key="b" :value="b">{{ b }}</option>
                    </select>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">Year *</label>
                    <select class="form-select form-select-lg" v-model.number="formData.year" required>
                      <option value="">Select Year</option>
                      <option :value="1">1st Year</option>
                      <option :value="2">2nd Year</option>
                      <option :value="3">3rd Year</option>
                      <option :value="4">4th Year</option>
                    </select>
                  </div>
                </div>

                <div class="mb-4">
                  <label class="form-label fw-semibold">CGPA</label>
                  <input type="number" step="0.01" min="0" max="10" class="form-control form-control-lg" placeholder="Enter CGPA" v-model.number="formData.cgpa" />
                </div>

                <button type="submit" class="btn btn-success btn-lg w-100 fw-semibold" :disabled="loading">
                  {{ loading ? 'Registering...' : 'Register' }}
                </button>
              </form>

              <p class="text-center mt-4 mb-0">
                Already have an account?
                <router-link to="/login" class="fw-semibold text-decoration-none">Login</router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const loading = ref(false)

const branchOptions = ['CSE', 'IT', 'ECE', 'EEE', 'ME', 'CE', 'CHE', 'BT', 'MCA', 'MBA', 'Other']

const formData = ref({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  roll_number: '',
  branch: '',
  year: '',
  cgpa: ''
})

const register = async () => {
  try {
    if (!formData.value.roll_number || !formData.value.branch || !formData.value.year) {
      alert('Roll number, branch and year are required.')
      return
    }

    loading.value = true
    const response = await api.post('/api/auth/register-student', formData.value)

    localStorage.setItem('token', response.data.access_token)
    localStorage.setItem('user', JSON.stringify(response.data.user))
    router.push('/student/dashboard')
  } catch (error) {
    alert(error.response?.data?.error || error.message || 'Registration Failed')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #eef2ff 0%, #f8fafc 50%, #ecfeff 100%);
}
.auth-card {
  border-radius: 18px;
}
.form-control,
.form-select {
  border-radius: 12px;
}
</style>