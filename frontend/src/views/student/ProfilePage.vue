<template>
  <StudentLayout>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">My Profile</h2>
      <button v-if="!editing && !loading" class="btn btn-primary" @click="startEdit">Edit Profile</button>
    </div>

    <div v-if="loading" class="text-muted">Loading profile...</div>

    <div v-else>
      <div v-if="message" :class="'alert alert-' + messageType">{{ message }}</div>

      <div class="card shadow border-0 p-4 mb-4">
        <div class="d-flex align-items-center gap-4 flex-wrap">
          <img
            v-if="profile.profile_pic && !photoBroken"
            :src="photoLink"
            @error="photoBroken = true"
            alt="profile"
            class="rounded-circle"
            style="width:96px;height:96px;object-fit:cover;border:3px solid #e8eaf0"
          />
          <div v-else class="rounded-circle d-flex align-items-center justify-content-center"
               style="width:96px;height:96px;background:#4f46e5;color:#fff;font-size:2rem;font-weight:600">
            {{ initials }}
          </div>
          <div>
            <h5 class="mb-1">{{ profile.first_name }} {{ profile.last_name }}</h5>
            <p class="text-muted mb-2">{{ profile.branch || '-' }} &middot; {{ profile.email }}</p>
            <div class="input-group" style="max-width:360px">
              <input ref="photoInput" type="file" accept="image/*" class="form-control form-control-sm" @change="onPhotoChange" />
              <button class="btn btn-sm btn-outline-primary" :disabled="!selectedPhoto || uploadingPhoto" @click="uploadPhotoFile">
                {{ uploadingPhoto ? 'Uploading...' : 'Upload Photo' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!editing" class="card shadow border-0 p-4 mb-4">
        <h5 class="mb-3">Personal Details</h5>
        <div class="row">
          <div class="col-md-6 mb-2"><strong>Email:</strong> {{ profile.email }}</div>
          <div class="col-md-6 mb-2"><strong>Roll Number:</strong> {{ profile.roll_number || '-' }}</div>
          <div class="col-md-6 mb-2"><strong>Name:</strong> {{ profile.first_name }} {{ profile.last_name }}</div>
          <div class="col-md-6 mb-2"><strong>Phone:</strong> {{ profile.phone || '-' }}</div>
          <div class="col-md-6 mb-2"><strong>Branch:</strong> {{ profile.branch || '-' }}</div>
          <div class="col-md-6 mb-2"><strong>Year:</strong> {{ profile.year || '-' }}</div>
          <div class="col-md-6 mb-2"><strong>CGPA:</strong> {{ profile.cgpa || '-' }}</div>
          <div class="col-12 mb-2"><strong>Bio:</strong> {{ profile.bio || '-' }}</div>
        </div>
      </div>

      <div v-else class="card shadow border-0 p-4 mb-4">
        <h5 class="mb-3">Edit Personal Details</h5>
        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label">Email (cannot change)</label>
            <input type="email" class="form-control" :value="form.email" disabled />
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label">Roll Number (locked)</label>
            <input type="text" class="form-control" :value="form.roll_number" disabled />
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">First Name</label>
            <input type="text" class="form-control" v-model="form.first_name" />
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label">Last Name</label>
            <input type="text" class="form-control" v-model="form.last_name" />
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Phone</label>
            <input type="text" class="form-control" v-model="form.phone" />
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label">Branch (locked)</label>
            <input type="text" class="form-control" :value="form.branch" disabled />
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Year (locked)</label>
            <input type="number" class="form-control" :value="form.year" disabled />
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label">CGPA</label>
            <input type="number" step="0.01" min="0" max="10" class="form-control" v-model.number="form.cgpa" />
          </div>

          <div class="col-12 mb-3">
            <label class="form-label">Bio</label>
            <textarea class="form-control" rows="3" v-model="form.bio"></textarea>
          </div>
        </div>

        <div>
          <button class="btn btn-primary me-2" :disabled="saving" @click="saveProfile">
            {{ saving ? 'Saving...' : 'Save Changes' }}
          </button>
          <button class="btn btn-outline-secondary" :disabled="saving" @click="cancelEdit">Cancel</button>
        </div>
      </div>

      <div class="card shadow border-0 p-4">
        <h5 class="mb-3">Resume</h5>
        <p v-if="profile.resume_url" class="mb-3">Current resume:
          <a :href="resumeLink" target="_blank">View uploaded resume</a>
        </p>
        <p v-else class="text-muted mb-3">No resume uploaded yet.</p>
        <div class="input-group" style="max-width: 500px;">
          <input ref="fileInput" type="file" class="form-control" @change="onFileChange" />
          <button class="btn btn-success" :disabled="!selectedFile || uploading" @click="uploadResumeFile">
            {{ uploading ? 'Uploading...' : 'Upload' }}
          </button>
        </div>
      </div>
    </div>
  </StudentLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import StudentLayout from '../../layouts/StudentLayout.vue'
import { getProfile, updateProfile, uploadResume, uploadPhoto } from '../../services/student'

const API = 'http://127.0.0.1:5000'

const profile = ref({})
const form = ref({})
const editing = ref(false)
const loading = ref(true)
const saving = ref(false)
const uploading = ref(false)
const uploadingPhoto = ref(false)
const selectedFile = ref(null)
const selectedPhoto = ref(null)
const fileInput = ref(null)
const photoInput = ref(null)
const message = ref('')
const messageType = ref('success')
const photoBroken = ref(false) // <-- add this

const resumeLink = computed(() => (profile.value.resume_url ? API + profile.value.resume_url : '#'))
const photoLink = computed(() => (profile.value.profile_pic ? API + profile.value.profile_pic : ''))
const initials = computed(() => {
  const f = (profile.value.first_name || '?')[0]
  const l = (profile.value.last_name || '')[0] || ''
  return (f + l).toUpperCase()
})

const showMessage = (t, ty = 'success') => {
  message.value = t
  messageType.value = ty
  setTimeout(() => (message.value = ''), 4000)
}

const loadProfile = async () => {
  loading.value = true
  photoBroken.value = false // reset on load
  try {
    const res = await getProfile()
    profile.value = res.profile || {}
  } catch (e) {
    showMessage('Failed to load profile', 'danger')
  } finally {
    loading.value = false
  }
}

const startEdit = () => { form.value = { ...profile.value }; editing.value = true }
const cancelEdit = () => { editing.value = false }

const saveProfile = async () => {
  saving.value = true
  try {
    const payload = {
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      phone: form.value.phone,
      cgpa: form.value.cgpa,
      bio: form.value.bio
    }
    const res = await updateProfile(payload)
    if (res.success) {
      profile.value = { ...profile.value, ...res.profile }
      editing.value = false
      showMessage('Profile updated successfully')
    }
  } catch (e) {
    showMessage(e.response?.data?.error || 'Failed to update profile', 'danger')
  } finally {
    saving.value = false
  }
}

const onFileChange = (e) => { selectedFile.value = e.target.files[0] || null }
const uploadResumeFile = async () => {
  if (!selectedFile.value) return
  uploading.value = true
  try {
    const res = await uploadResume(selectedFile.value)
    if (res.success) {
      profile.value.resume_url = res.resume_url
      selectedFile.value = null
      if (fileInput.value) fileInput.value.value = ''
      showMessage('Resume uploaded successfully')
    }
  } catch (e) {
    showMessage(e.response?.data?.error || 'Failed to upload resume', 'danger')
  } finally {
    uploading.value = false
  }
}

const onPhotoChange = (e) => { selectedPhoto.value = e.target.files[0] || null }
const uploadPhotoFile = async () => {
  if (!selectedPhoto.value) return
  uploadingPhoto.value = true
  try {
    const res = await uploadPhoto(selectedPhoto.value)
    if (res.success) {
      profile.value.profile_pic = res.profile_pic
      photoBroken.value = false
      selectedPhoto.value = null
      if (photoInput.value) photoInput.value.value = ''
      showMessage('Photo uploaded successfully')
    }
  } catch (e) {
    showMessage(e.response?.data?.error || 'Failed to upload photo', 'danger')
  } finally {
    uploadingPhoto.value = false
  }
}

onMounted(loadProfile)
</script>