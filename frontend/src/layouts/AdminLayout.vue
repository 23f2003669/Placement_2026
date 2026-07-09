<template>
  <div class="d-flex">
    <div class="text-white p-3 d-flex flex-column"
         style="width:260px;min-height:100vh;background:linear-gradient(180deg,#7c3aed 0%,#6d28d9 55%,#5b21b6 100%)">
      <div class="d-flex align-items-center gap-2 mb-1 px-2 pt-2">
        <i class="bi bi-shield-lock" style="font-size:1.6rem"></i>
        <h4 class="mb-0 fw-bold" style="color:#fff">Placement Portal</h4>
      </div>
      <p class="small px-2 mb-4" style="opacity:.75">Admin Portal</p>
      <ul class="nav flex-column flex-grow-1">
        <li class="nav-item mb-1" v-for="item in navItems" :key="item.to">
          <router-link :to="item.to" class="nav-link text-white d-flex align-items-center gap-2">
            <i :class="item.icon" style="width:20px"></i><span>{{ item.label }}</span>
          </router-link>
        </li>
      </ul>
      <button class="btn btn-danger w-100" @click="logout">
        <i class="bi bi-box-arrow-right me-1"></i> Logout
      </button>
    </div>
    <div class="flex-grow-1 p-4"><slot /></div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const navItems = [
  { to: '/admin/dashboard', label: 'Dashboard', icon: 'bi bi-speedometer2' },
  { to: '/admin/companies', label: 'Companies', icon: 'bi bi-building' },
  { to: '/admin/students', label: 'Students', icon: 'bi bi-mortarboard' },
  { to: '/admin/jobs', label: 'Jobs', icon: 'bi bi-briefcase' },
  { to: '/admin/applications', label: 'Applications', icon: 'bi bi-file-earmark-text' },
  { to: '/admin/placements', label: 'Placements', icon: 'bi bi-award' }
]
const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>
