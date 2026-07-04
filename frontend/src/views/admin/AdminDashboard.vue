<template>
  <AdminLayout>

    <h1 class="mb-4">
      Admin Dashboard
    </h1>

    <!-- Stats -->

    <div class="row g-4 mb-4">

      <div class="col-md-3">
        <div class="card shadow border-0">
          <div class="card-body text-center">
            <h2>{{ stats.students }}</h2>
            <p class="text-muted mb-0">
              Students
            </p>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card shadow border-0">
          <div class="card-body text-center">
            <h2>{{ stats.companies }}</h2>
            <p class="text-muted mb-0">
              Companies
            </p>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card shadow border-0">
          <div class="card-body text-center">
            <h2>{{ stats.applications }}</h2>
            <p class="text-muted mb-0">
              Applications
            </p>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card shadow border-0">
          <div class="card-body text-center">
            <h2>{{ stats.placements }}</h2>
            <p class="text-muted mb-0">
              Placements
            </p>
          </div>
        </div>
      </div>

    </div>

    <!-- Pending Companies -->

    <div
      v-if="pendingCompanies.length > 0"
      class="card shadow border-0 mb-4"
    >

      <div class="card-header bg-white">
        <h5 class="mb-0">
          Pending Company Approvals
        </h5>
      </div>

      <div class="card-body">

        <table class="table">

          <thead>
            <tr>
              <th>Company</th>
              <th>Industry</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="company in pendingCompanies"
              :key="company.id"
            >

              <td>
                {{ company.company_name }}
              </td>

              <td>
                {{ company.industry }}
              </td>

              <td>

                <button
                  class="btn btn-success btn-sm me-2"
                  @click="handleApprove(company.id)"
                >
                  Approve
                </button>

                <button
                  class="btn btn-danger btn-sm"
                  @click="handleReject(company.id)"
                >
                  Reject
                </button>

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

    <!-- Recent Companies -->

    <div class="card shadow border-0 mb-4">

      <div class="card-header bg-white">
        <h5 class="mb-0">
          Recent Companies
        </h5>
      </div>

      <div class="card-body">

        <table class="table">

          <thead>
            <tr>
              <th>Company</th>
              <th>Industry</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="company in recentCompanies"
              :key="company.id"
            >

              <td>{{ company.company_name }}</td>

              <td>{{ company.industry }}</td>

              <td>

                <span
                  v-if="company.approval_status === 'approved'"
                  class="badge bg-success"
                >
                  Approved
                </span>

                <span
                  v-else-if="company.approval_status === 'rejected'"
                  class="badge bg-danger"
                >
                  Rejected
                </span>

                <span
                  v-else
                  class="badge bg-warning text-dark"
                >
                  Pending
                </span>

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

    <!-- Recent Students -->

    <div class="card shadow border-0 mb-4">

      <div class="card-header bg-white">
        <h5 class="mb-0">
          Recent Students
        </h5>
      </div>

      <div class="card-body">

        <table class="table">

          <thead>
            <tr>
              <th>Name</th>
              <th>Branch</th>
              <th>CGPA</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="student in recentStudents"
              :key="student.id"
            >

              <td>
                {{ student.first_name }}
                {{ student.last_name }}
              </td>

              <td>{{ student.branch }}</td>

              <td>{{ student.cgpa }}</td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

    <!-- Recent Applications -->

    <div class="card shadow border-0">

      <div class="card-header bg-white">
        <h5 class="mb-0">
          Recent Applications
        </h5>
      </div>

      <div class="card-body">

        <table class="table">

          <thead>
            <tr>
              <th>Student</th>
              <th>Company</th>
              <th>Job</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="application in recentApplications"
              :key="application.application_id"
            >

              <td>{{ application.student_name }}</td>

              <td>{{ application.company_name }}</td>

              <td>{{ application.job_title }}</td>

              <td>{{ application.status }}</td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '../../layouts/AdminLayout.vue'

import {
  getDashboardStats,
  getCompanies,
  getStudents,
  getApplications,
  approveCompany,
  rejectCompany
} from '../../services/admin'

const stats = ref({
  students: 0,
  companies: 0,
  applications: 0,
  placements: 0
})

const recentCompanies = ref([])
const recentStudents = ref([])
const recentApplications = ref([])
const pendingCompanies = ref([])

const loadDashboard = async () => {

  try {

    const dashboard =
      await getDashboardStats()

    stats.value.students =
      dashboard.data.students.total

    stats.value.companies =
      dashboard.data.companies.total

    stats.value.applications =
      dashboard.data.applications.total

    stats.value.placements =
      dashboard.data.placements.total

    const companiesResponse =
      await getCompanies()

    recentCompanies.value =
      companiesResponse.companies.slice(0, 5)

    pendingCompanies.value =
      companiesResponse.companies.filter(
        company =>
          company.approval_status === 'pending'
      )

    const studentsResponse =
      await getStudents()

    recentStudents.value =
      studentsResponse.students.slice(0, 5)

    const applicationsResponse =
      await getApplications()

    recentApplications.value =
      applicationsResponse.applications.slice(0, 5)

  }

  catch (error) {

    console.error(
      'Dashboard Error:',
      error
    )

  }

}

const handleApprove = async (id) => {

  try {

    await approveCompany(id)

    await loadDashboard()

  }

  catch (error) {

    console.error(error)

  }

}

const handleReject = async (id) => {

  try {

    await rejectCompany(id)

    await loadDashboard()

  }

  catch (error) {

    console.error(error)

  }

}

onMounted(() => {

  loadDashboard()

})
</script>