import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import LoginPage from '../views/LoginPage.vue'
import RegisterPage from '../views/RegisterPage.vue'
import CompanyRegister from '../views/CompanyRegister.vue'
import StudentDashboard from '../views/student/StudentDashboard.vue'
import StudentJobsPage from '../views/student/JobsPage.vue'
import StudentApplicationsPage from '../views/student/ApplicationsPage.vue'
import StudentPlacementsPage from '../views/student/PlacementsPage.vue'
import StudentProfilePage from '../views/student/ProfilePage.vue'
import CompanyDashboard from '../views/company/CompanyDashboard.vue'
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import ApplicationsPage from '../views/admin/ApplicationsPage.vue'
import CompaniesPage from '../views/admin/CompaniesPage.vue'
import JobsPage from '../views/admin/JobsPage.vue'
import StudentsPage from '../views/admin/StudentsPage.vue'
import PlacementsPage from '../views/admin/PlacementsPage.vue'
import CreateJobPage from '../views/company/CreateJobPage.vue'
import CompanyJobsPage from '../views/company/JobsPage.vue'
import ApplicantsPage from '../views/company/ApplicantsPage.vue'
import { isAuthenticated } from './auth'

const routes = [
  { path: '/', component: LandingPage, meta: { title: 'Placement Portal' } },

  { path: '/login', component: LoginPage, meta: { title: 'Login • Placement Portal' } },
  { path: '/register', component: RegisterPage, meta: { title: 'Student Register • Placement Portal' } },
  { path: '/register-company', component: CompanyRegister, meta: { title: 'Company Register • Placement Portal' } },

  { path: '/student/dashboard', component: StudentDashboard, meta: { requiresAuth: true, title: 'Student Dashboard • Placement Portal' } },
  { path: '/student/jobs', component: StudentJobsPage, meta: { requiresAuth: true, title: 'Available Jobs • Placement Portal' } },
  { path: '/student/applications', component: StudentApplicationsPage, meta: { requiresAuth: true, title: 'My Applications • Placement Portal' } },
  { path: '/student/placements', component: StudentPlacementsPage, meta: { requiresAuth: true, title: 'My Placements • Placement Portal' } },
  { path: '/student/profile', component: StudentProfilePage, meta: { requiresAuth: true, title: 'My Profile • Placement Portal' } },

  { path: '/company/dashboard', component: CompanyDashboard, meta: { requiresAuth: true, title: 'Company Dashboard • Placement Portal' } },
  { path: '/company/create-job', component: CreateJobPage, meta: { requiresAuth: true, title: 'Create Job • Placement Portal' } },
  { path: '/company/jobs', component: CompanyJobsPage, meta: { requiresAuth: true, title: 'My Jobs • Placement Portal' } },
  { path: '/company/applicants/:jobId', component: ApplicantsPage, meta: { requiresAuth: true, title: 'Applicants • Placement Portal' } },

  { path: '/admin/dashboard', component: AdminDashboard, meta: { requiresAuth: true, title: 'Admin Dashboard • Placement Portal' } },
  { path: '/admin/applications', component: ApplicationsPage, meta: { requiresAuth: true, title: 'Admin Applications • Placement Portal' } },
  { path: '/admin/companies', component: CompaniesPage, meta: { requiresAuth: true, title: 'Admin Companies • Placement Portal' } },
  { path: '/admin/jobs', component: JobsPage, meta: { requiresAuth: true, title: 'Admin Jobs • Placement Portal' } },
  { path: '/admin/students', component: StudentsPage, meta: { requiresAuth: true, title: 'Admin Students • Placement Portal' } },
  { path: '/admin/placements', component: PlacementsPage, meta: { requiresAuth: true, title: 'Admin Placements • Placement Portal' } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  document.title = to.meta?.title || 'Placement Portal'

  if (to.meta.requiresAuth && !isAuthenticated()) {
    return '/login'
  }

  const user = JSON.parse(localStorage.getItem('user') || 'null')
  const role = user?.role

  // Prevent logged-in users from going back to auth pages
  if (isAuthenticated() && ['/login', '/register', '/register-company'].includes(to.path)) {
    if (role === 'admin') return '/admin/dashboard'
    if (role === 'company') return '/company/dashboard'
    if (role === 'student') return '/student/dashboard'
  }

  if (to.path.startsWith('/admin') && role !== 'admin') return '/login'
  if (to.path.startsWith('/company') && role !== 'company') return '/login'
  if (to.path.startsWith('/student') && role !== 'student') return '/login'
})

export default router