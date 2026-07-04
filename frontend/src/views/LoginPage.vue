<template>
  <div
    class="min-vh-100 d-flex align-items-center justify-content-center"
    style="background: linear-gradient(135deg, #0d6efd 0%, #6610f2 100%);"
  >
    <div class="col-md-4 col-sm-10 col-11">
      <div class="card border-0 shadow-lg rounded-3">
        <div class="card-body p-4 p-md-5">

          <div class="text-center mb-4">
            <i class="bi bi-briefcase-fill text-primary fs-1"></i>
            <h2 class="fw-semibold mt-2 text-dark">Placement Portal</h2>
            <p class="text-muted small">Sign in to your account</p>
          </div>

          <form @submit.prevent="login">

            <div class="mb-3">
              <label class="form-label fw-semibold">Email</label>
              <input
                type="email"
                class="form-control form-control-lg"
                placeholder="Enter your email"
                v-model="email"
                required
                autocomplete="email"
              />
            </div>

            <div class="mb-4">
              <label class="form-label fw-semibold">Password</label>
              <input
                type="password"
                class="form-control form-control-lg"
                placeholder="Enter your password"
                v-model="password"
                required
                autocomplete="current-password"
              />
            </div>

            <button
              type="submit"
              class="btn btn-primary btn-lg w-100"
              :disabled="loading"
            >
              <span
                v-if="loading"
                class="spinner-border spinner-border-sm me-2"
              ></span>
              {{ loading ? 'Signing in...' : 'Login' }}
            </button>

          </form>

          <hr class="my-4" />

          <div class="text-center small">
            <span class="text-muted">New student? </span>
            <router-link to="/register" class="text-primary fw-semibold">
              Register here
            </router-link>
          </div>
          <div class="text-center small mt-2">
            <span class="text-muted">Registering a company? </span>
            <router-link to="/register-company" class="text-primary fw-semibold">
              Company registration
            </router-link>
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
const email = ref('')
const password = ref('')
const loading = ref(false)

const login = async () => {
  try {
    loading.value = true
    const response = await api.post('/api/auth/login', {
      email: email.value,
      password: password.value
    })

    localStorage.setItem('token', response.data.access_token)
    localStorage.setItem('user', JSON.stringify(response.data.user))

    const role = response.data.user.role
    if (role === 'admin') router.push('/admin/dashboard')
    else if (role === 'student') router.push('/student/dashboard')
    else if (role === 'company') router.push('/company/dashboard')

  } catch (error) {
    alert(
      error.response?.data?.error ||
      'Login failed. Check your credentials.'
    )
  } finally {
    loading.value = false
  }
}
</script>