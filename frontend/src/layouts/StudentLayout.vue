<template>
  <div class="d-flex">

    <!-- Sidebar -->
    <div
      class="bg-primary text-white p-3"
      style="width:280px; min-height:100vh"
    >

      <h3 class="mb-4">
        Student Portal
      </h3>

      <ul class="nav flex-column">

        <li class="nav-item mb-2">
          <router-link
            to="/student/dashboard"
            class="nav-link text-white"
          >
            Dashboard
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link
            to="/student/jobs"
            class="nav-link text-white"
          >
            Available Jobs
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link
            to="/student/applications"
            class="nav-link text-white"
          >
            My Applications
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link
            to="/student/placements"
            class="nav-link text-white"
          >
            Placements
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link
            to="/student/profile"
            class="nav-link text-white"
          >
            Profile
          </router-link>
        </li>

      </ul>

      <button
        class="btn btn-danger w-100 mt-4"
        @click="logout"
      >
        Logout
      </button>

    </div>

    <!-- Main Content -->

    <div class="flex-grow-1 p-4">
      <slot />
    </div>

  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>