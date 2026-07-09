<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow border-0 p-4">
          <h2 class="text-center mb-4">
            Student Registration
          </h2>

          <form @submit.prevent="register">
            <!-- First Name -->
            <div class="mb-3">
              <label class="form-label">
                First Name *
              </label>
              <input
                type="text"
                class="form-control"
                placeholder="Enter first name"
                v-model="formData.first_name"
                required
              />
            </div>

            <!-- Last Name -->
            <div class="mb-3">
              <label class="form-label">
                Last Name
              </label>
              <input
                type="text"
                class="form-control"
                placeholder="Enter last name"
                v-model="formData.last_name"
              />
            </div>

            <!-- Email -->
            <div class="mb-3">
              <label class="form-label">
                Email *
              </label>
              <input
                type="email"
                class="form-control"
                placeholder="Enter email"
                v-model="formData.email"
                required
              />
            </div>

            <!-- Password -->
            <div class="mb-3">
              <label class="form-label">
                Password *
              </label>
              <input
                type="password"
                class="form-control"
                placeholder="Enter password"
                v-model="formData.password"
                required
              />
            </div>

            <!-- Roll Number -->
            <div class="mb-3">
              <label class="form-label">
                Roll Number
              </label>
              <input
                type="text"
                class="form-control"
                placeholder="Enter roll number"
                v-model="formData.roll_number"
              />
            </div>

            <!-- Branch -->
            <div class="mb-3">
              <label class="form-label">
                Branch
              </label>
              <select class="form-control" v-model="formData.branch">
                <option value="">Select Branch</option>
                <option value="CSE">CSE</option>
                <option value="ECE">ECE</option>
                <option value="ME">ME</option>
                <option value="CE">CE</option>
                <option value="IT">IT</option>
              </select>
            </div>

            <!-- Year -->
            <div class="mb-3">
              <label class="form-label">
                Year
              </label>
              <select class="form-control" v-model.number="formData.year">
                <option value="">Select Year</option>
                <option value="1">1st Year</option>
                <option value="2">2nd Year</option>
                <option value="3">3rd Year</option>
                <option value="4">4th Year</option>
              </select>
            </div>

            <!-- CGPA -->
            <div class="mb-4">
              <label class="form-label">
                CGPA
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="10"
                class="form-control"
                placeholder="Enter CGPA"
                v-model.number="formData.cgpa"
              />
            </div>

            <button
              type="submit"
              class="btn btn-success w-100"
              :disabled="loading"
            >
              {{ loading ? 'Registering...' : 'Register' }}
            </button>
          </form>

          <p class="text-center mt-3">
            Already have an account?
            <router-link to="/login">
              Login
            </router-link>
          </p>
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
    loading.value = true

    const response = await api.post(
      '/api/auth/register-student',
      formData.value
    )

    localStorage.setItem(
      'token',
      response.data.access_token
    )

    localStorage.setItem(
      'user',
      JSON.stringify(response.data.user)
    )

    router.push('/student/dashboard')

  } catch (error) {
    console.error(error)
    alert(error.response?.data?.error ||
      error.message ||
      'Registration Failed')
  } finally {
    loading.value = false
  }
}
</script>