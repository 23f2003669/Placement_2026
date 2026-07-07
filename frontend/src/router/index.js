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
  { path: '/', component: LandingPage },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { path: '/register-company', component: CompanyRegister },
  { path: '/student/dashboard', component: StudentDashboard, meta: { requiresAuth: true } },
  { path: '/student/jobs', component: StudentJobsPage, meta: { requiresAuth: true } },
  { path: '/student/applications', component: StudentApplicationsPage, meta: { requiresAuth: true } },
  { path: '/student/placements', component: StudentPlacementsPage, meta: { requiresAuth: true } },
  { path: '/student/profile', component: StudentProfilePage, meta: { requiresAuth: true } },
  { path: '/company/dashboard', component: CompanyDashboard, meta: { requiresAuth: true } },
  { path: '/admin/dashboard', component: AdminDashboard, meta: { requiresAuth: true } },
  { path: '/admin/applications', component: ApplicationsPage, meta: { requiresAuth: true } },
  { path: '/admin/companies', component: CompaniesPage, meta: { requiresAuth: true } },
  { path: '/admin/jobs', component: JobsPage, meta: { requiresAuth: true } },
  { path: '/admin/students', component: StudentsPage, meta: { requiresAuth: true } },
  { path: '/admin/placements', component: PlacementsPage, meta: { requiresAuth: true } },
  { path: '/company/create-job', component: CreateJobPage, meta: { requiresAuth: true } },
  { path: '/company/jobs', component: CompanyJobsPage, meta: { requiresAuth: true } },
  { path: '/company/applicants/:jobId', component: ApplicantsPage, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    return '/login'
  }
})

export default router
