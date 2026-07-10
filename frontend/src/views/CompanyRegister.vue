<template>
  <div class="auth-page d-flex align-items-center py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-7 col-xl-6">
          <div class="card auth-card border-0 shadow-lg">
            <div class="card-body p-4 p-md-5">
              <div class="text-center mb-4">
                <h2 class="fw-bold mb-1">Company Registration</h2>
                <p class="text-muted mb-0">Register your company for campus hiring</p>
              </div>

              <form @submit.prevent="registerCompany">
                <div class="mb-3">
                  <label class="form-label fw-semibold">Company Name *</label>
                  <input v-model.trim="form.company_name" class="form-control form-control-lg" required />
                </div>

                <div class="mb-3">
                  <label class="form-label fw-semibold">Email *</label>
                  <input v-model.trim="form.email" type="email" class="form-control form-control-lg" required />
                </div>

                <div class="mb-3">
                  <label class="form-label fw-semibold">Password *</label>
                  <input v-model="form.password" type="password" minlength="6" class="form-control form-control-lg" required />
                </div>

                <div class="mb-3">
                  <label class="form-label fw-semibold">Industry</label>
                  <input v-model.trim="form.industry" class="form-control form-control-lg" placeholder="e.g. FinTech, SaaS, AI" />
                </div>

                <div class="mb-3">
                  <label class="form-label fw-semibold">Website</label>
                  <input v-model.trim="form.website" type="url" class="form-control form-control-lg" placeholder="https://example.com" />
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">HR Email</label>
                    <input v-model.trim="form.hr_email" type="email" class="form-control form-control-lg" />
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label fw-semibold">HR Phone</label>
                    <input v-model.trim="form.hr_phone" type="tel" class="form-control form-control-lg" />
                  </div>
                </div>

                <div class="mb-4">
                  <label class="form-label fw-semibold">Location</label>
                  <input v-model.trim="form.location" class="form-control form-control-lg" placeholder="City, State" />
                </div>

                <button type="submit" class="btn btn-primary btn-lg w-100 fw-semibold" :disabled="loading">
                  {{ loading ? 'Registering...' : 'Register Company' }}
                </button>

                <p class="text-center mt-4 mb-0">
                  Already have an account?
                  <router-link to="/login" class="fw-semibold text-decoration-none">Login</router-link>
                </p>
              </form>
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

const form = ref({
  company_name: '',
  email: '',
  password: '',
  industry: '',
  website: '',
  hr_email: '',
  hr_phone: '',
  location: ''
})

const registerCompany = async () => {
  try {
    loading.value = true
    const response = await api.post('/api/auth/register-company', form.value)
    alert(response.data.message || 'Registration successful! Please wait for admin approval.')
    setTimeout(() => router.push('/login'), 1400)
  } catch (error) {
    alert(error.response?.data?.error || 'Registration failed')
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
.form-control {
  border-radius: 12px;
}
</style>