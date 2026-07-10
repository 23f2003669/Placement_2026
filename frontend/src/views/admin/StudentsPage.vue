<template>
  <AdminLayout>
    <h1 class="mb-4">Students Management</h1>

    <div class="mb-3">
      <input
        type="text"
        class="form-control"
        placeholder="Search by name, roll number..."
        v-model="searchQuery"
        @input="loadStudents"
      />
    </div>

    <div class="card shadow border-0">
      <div class="card-body">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Branch</th>
              <th>CGPA</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in students" :key="student.id">
              <td>{{ student.first_name }} {{ student.last_name }}</td>
              <td>{{ student.email }}</td>
              <td>{{ student.branch }}</td>
              <td>{{ student.cgpa }}</td>
              <td>
                <span v-if="student.is_blacklisted" class="badge bg-danger">Blacklisted</span>
                <span v-else class="badge bg-success">Active</span>
              </td>
              <td>
                <button
                  v-if="!student.is_blacklisted"
                  class="btn btn-danger btn-sm"
                  @click="handleBlacklist(student.id)"
                >Blacklist</button>
                <button
                  v-else
                  class="btn btn-success btn-sm"
                  @click="handleUnblacklist(student.id)"
                >Unblacklist</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="students.length === 0" class="text-muted text-center py-3">No students found.</p>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '../../layouts/AdminLayout.vue'
import { getStudents, blacklistStudent, unblacklistStudent } from '../../services/admin'

const students = ref([])
const searchQuery = ref('')

const loadStudents = async () => {
  try {
    const response = await getStudents(searchQuery.value)
    students.value = response.students
  } catch (error) {
    console.error(error)
  }
}

const handleBlacklist = async (id) => {
  try {
    await blacklistStudent(id)
    await loadStudents()
  } catch (error) {
    console.error(error)
  }
}

const handleUnblacklist = async (id) => {
  try {
    await unblacklistStudent(id)
    await loadStudents()
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  loadStudents()
})
</script>