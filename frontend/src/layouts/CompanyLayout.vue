<template>
  <div class="d-flex">

    <!-- Sidebar -->
    <div class="text-white p-3 d-flex flex-column"
         style="width:260px;min-height:100vh;background:linear-gradient(180deg,#059669 0%,#047857 55%,#065f46 100%)">

      <div class="d-flex align-items-center gap-2 mb-1 px-2 pt-2">
        <i class="bi bi-building" style="font-size:1.6rem"></i>
        <h4 class="mb-0 fw-bold" style="color:#fff">Placement Portal</h4>
      </div>
      <p class="small px-2 mb-4" style="opacity:.75">Company Portal</p>

      <ul class="nav flex-column flex-grow-1">
        <li class="nav-item mb-1" v-for="item in navItems" :key="item.to">
          <router-link :to="item.to" class="nav-link text-white d-flex align-items-center gap-2">
            <i :class="item.icon" style="width:20px"></i>
            <span>{{ item.label }}</span>
          </router-link>
        </li>
      </ul>

      <button class="btn btn-danger w-100" @click="logout">
        <i class="bi bi-box-arrow-right me-1"></i> Logout
      </button>

    </div>

    <div class="flex-grow-1 p-4">
      <slot />
    </div>

  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const navItems = [
  { to: '/company/dashboard', label: 'Dashboard', icon: 'bi bi-speedometer2' },
  { to: '/company/jobs', label: 'My Jobs', icon: 'bi bi-briefcase' },
  { to: '/company/create-job', label: 'Create Job', icon: 'bi bi-plus-circle' }
]

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>
