<template>
  <div class="d-flex">

    <!-- Sidebar -->
    <div
      class="bg-success text-white p-3"
      style="width:280px;min-height:100vh;"
    >

      <h3 class="mb-4">
        Placement Portal
      </h3>

      <p class="small text-light">
        Company Portal
      </p>

      <ul class="nav flex-column">

        <li class="nav-item mb-2">
          <router-link
            to="/company/dashboard"
            class="nav-link text-white"
          >
            <i class="bi bi-speedometer2 me-2"></i>
            Dashboard
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link
            to="/company/jobs"
            class="nav-link text-white"
          >
            <i class="bi bi-briefcase me-2"></i>
            My Jobs
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link
            to="/company/create-job"
            class="nav-link text-white"
          >
            <i class="bi bi-plus-circle me-2"></i>
            Create Job
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