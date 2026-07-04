<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">

            <h2 class="mb-4 text-center">
              Company Registration
            </h2>

            <form @submit.prevent="registerCompany">

              <div class="mb-3">
                <label>Company Name *</label>
                <input
                  v-model="form.company_name"
                  class="form-control"
                  required
                >
              </div>

              <div class="mb-3">
                <label>Email *</label>
                <input
                  v-model="form.email"
                  type="email"
                  class="form-control"
                  required
                >
              </div>

              <div class="mb-3">
                <label>Password *</label>
                <input
                  v-model="form.password"
                  type="password"
                  class="form-control"
                  required
                >
              </div>

              <div class="mb-3">
                <label>Industry</label>
                <input
                  v-model="form.industry"
                  class="form-control"
                >
              </div>

              <div class="mb-3">
                <label>Website</label>
                <input
                  v-model="form.website"
                  class="form-control"
                >
              </div>

              <div class="mb-3">
                <label>HR Email</label>
                <input
                  v-model="form.hr_email"
                  class="form-control"
                >
              </div>

              <div class="mb-3">
                <label>HR Phone</label>
                <input
                  v-model="form.hr_phone"
                  class="form-control"
                >
              </div>

              <div class="mb-3">
                <label>Location</label>
                <input
                  v-model="form.location"
                  class="form-control"
                >
              </div>

              <button
                type="submit"
                class="btn btn-primary w-100"
                :disabled="loading"
              >
                {{ loading ? 'Registering...' : 'Register Company' }}
              </button>

              <p class="text-center mt-3">
                Already have an account?
                <router-link to="/login">Login</router-link>
              </p>

            </form>

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

    const response = await api.post(
      '/api/auth/register-company',
      form.value
    )

    alert(response.data.message)
    router.push('/login')

  } catch (error) {
    alert(
      error.response?.data?.error ||
      'Registration failed'
    )
  } finally {
    loading.value = false
  }
}
</script>