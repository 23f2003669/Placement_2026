<template>
  <AdminLayout>
    <h1 class="mb-4">Companies Management</h1>

    <div class="mb-3">
      <input
        type="text"
        class="form-control"
        placeholder="Search by company name or industry..."
        v-model="searchQuery"
        @input="loadCompanies"
      />
    </div>

    <div class="card shadow border-0">
      <div class="card-body">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Company</th>
              <th>Industry</th>
              <th>HR Email</th>
              <th>HR Contact</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="company in companies" :key="company.id">
              <td>{{ company.company_name }}</td>
              <td>{{ company.industry }}</td>
              <td>{{ company.hr_email }}</td>
              <td>{{ company.hr_phone }}</td>
              <td>
                <span v-if="company.approval_status === 'approved'" class="badge bg-success">Approved</span>
                <span v-else-if="company.approval_status === 'rejected'" class="badge bg-danger">Rejected</span>
                <span v-else class="badge bg-warning text-dark">Pending</span>
              </td>
              <td>
                <button
                  v-if="company.approval_status !== 'approved'"
                  class="btn btn-success btn-sm me-2"
                  @click="handleApprove(company.id)"
                >Approve</button>
                <button
                  v-if="company.approval_status !== 'rejected'"
                  class="btn btn-danger btn-sm"
                  @click="handleReject(company.id)"
                >Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="companies.length === 0" class="text-muted text-center py-3">No companies found.</p>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '../../layouts/AdminLayout.vue'
import { getCompanies, approveCompany, rejectCompany } from '../../services/admin'

const companies = ref([])
const searchQuery = ref('')

const loadCompanies = async () => {
  try {
    const response = await getCompanies(searchQuery.value)
    companies.value = response.companies
  } catch (error) {
    console.error('Companies Error:', error)
  }
}

const handleApprove = async (companyId) => {
  try {
    await approveCompany(companyId)
    await loadCompanies()
  } catch (error) {
    alert('Failed to approve company')
  }
}

const handleReject = async (companyId) => {
  try {
    await rejectCompany(companyId)
    await loadCompanies()
  } catch (error) {
    alert('Failed to reject company')
  }
}

onMounted(() => {
  loadCompanies()
})
</script>