<template>
  <div class="d-flex">

    <!-- Sidebar -->
    <div
      class="bg-dark text-white p-3"
      style="
        width: 280px;
        min-height: 100vh;
      "
    >

      <h3 class="mb-4">
        Placement Portal
      </h3>

      <ul class="nav flex-column">

        <!-- Dashboard -->
        <li class="nav-item mb-2">
          <router-link
            to="/admin/dashboard"
            class="nav-link text-white"
          >
            <i class="bi bi-speedometer2 me-2"></i>
            Dashboard
          </router-link>
        </li>

        <!-- Companies -->
        <li class="nav-item mb-2">
          <router-link
            to="/admin/companies"
            class="nav-link text-white"
          >
            <i class="bi bi-buildings me-2"></i>
            Companies
          </router-link>
        </li>

        <!-- Students -->
        <li class="nav-item mb-2">
          <router-link to="/admin/students" class="nav-link text-white">
            <i class="bi bi-mortarboard me-2"></i>
            Students
          </router-link>
        </li>

        <!-- Jobs -->
        <li class="nav-item mb-2">
          <router-link
            to="/admin/jobs"
            class="nav-link text-white"
          >
            <i class="bi bi-briefcase me-2"></i>
            Jobs
          </router-link>
        </li>
     
        <!-- Applications -->
        <li class="nav-item mb-2">
          <router-link
            to="/admin/applications"
            class="nav-link text-white"
          >
            <i class="bi bi-file-earmark-text me-2"></i>
            Applications
          </router-link>
        </li>

        <!-- Placements -->
        <li class="nav-item mb-2">
          <router-link
            to="/admin/placements"
            class="nav-link text-white"
          >
            <i class="bi bi-award me-2"></i>
            Placements
          </router-link>
        </li>

      </ul>

      <button
        class="btn btn-danger mt-4 w-100"
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