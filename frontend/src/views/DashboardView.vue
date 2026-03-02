<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import axios from 'axios'

const props = defineProps({
  t: {
    type: Function,
    required: true,
  },
  language: {
    type: String,
    default: 'en',
  },
  isRtl: {
    type: Boolean,
    default: false,
  },
})

const API_BASE = (import.meta.env.VITE_API_BASE || 'https://alkhat-api.onrender.com').replace(/\/$/, '')
const api = axios.create({
  baseURL: `${API_BASE}/api`,
})

const token = ref(localStorage.getItem('khututs-token') || '')
const loginError = ref('')
const loginLoading = ref(false)

const loginForm = reactive({
  username: '',
  password: '',
})

const truckForm = reactive({
  title: '',
  description: '',
  image: null,
})

const projectForm = reactive({
  title: '',
  description: '',
  date: '',
  image: null,
})

const trucks = ref([])
const projects = ref([])
const stats = ref([])
const loading = ref(false)
const actionStatus = ref('')

const isAuthenticated = computed(() => Boolean(token.value))

const setAuthToken = (value) => {
  token.value = value
  if (value) {
    api.defaults.headers.common.Authorization = `Token ${value}`
    localStorage.setItem('khututs-token', value)
  } else {
    delete api.defaults.headers.common.Authorization
    localStorage.removeItem('khututs-token')
  }
}

const toFormData = (data) => {
  const formData = new FormData()
  Object.entries(data).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== '') {
      formData.append(key, value)
    }
  })
  return formData
}

const statLabelMap = (key) => {
  const map = {
    years: 'statYears',
    projects: 'statProjects',
    fleet: 'statFleet',
    safety: 'statSafety',
  }
  return props.t(map[key] || key)
}

const loadDashboard = async () => {
  loading.value = true
  actionStatus.value = ''
  try {
    const [truckRes, projectRes, statRes] = await Promise.all([
      api.get('/trucks/'),
      api.get('/projects/'),
      api.get('/stats/'),
    ])
    trucks.value = Array.isArray(truckRes.data) ? truckRes.data : []
    projects.value = Array.isArray(projectRes.data) ? projectRes.data : []
    stats.value = Array.isArray(statRes.data) ? statRes.data : []
  } catch (error) {
    actionStatus.value = props.t('loginError')
  } finally {
    loading.value = false
  }
}

const login = async () => {
  loginError.value = ''
  loginLoading.value = true
  try {
    const formData = toFormData(loginForm)
    const { data } = await api.post('/auth/token/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    setAuthToken(data.token)
    await loadDashboard()
  } catch (error) {
    loginError.value = props.t('loginError')
  } finally {
    loginLoading.value = false
  }
}

const logout = () => {
  setAuthToken('')
}

const handleTruckImage = (event) => {
  truckForm.image = event.target.files[0] || null
}

const handleProjectImage = (event) => {
  projectForm.image = event.target.files[0] || null
}

const createTruck = async () => {
  actionStatus.value = ''
  const formData = toFormData(truckForm)
  try {
    await api.post('/trucks/', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    truckForm.title = ''
    truckForm.description = ''
    truckForm.image = null
    await loadDashboard()
    actionStatus.value = props.t('statsSaved')
  } catch (error) {
    actionStatus.value = props.t('loginError')
  }
}

const createProject = async () => {
  actionStatus.value = ''
  const formData = toFormData(projectForm)
  try {
    await api.post('/projects/', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    projectForm.title = ''
    projectForm.description = ''
    projectForm.date = ''
    projectForm.image = null
    await loadDashboard()
    actionStatus.value = props.t('statsSaved')
  } catch (error) {
    actionStatus.value = props.t('loginError')
  }
}

const updateStat = async (stat) => {
  actionStatus.value = ''
  const formData = toFormData({
    key: stat.key,
    value: stat.value,
    suffix: stat.suffix,
    order: stat.order,
  })
  try {
    await api.patch(`/stats/${stat.id}/`, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    actionStatus.value = props.t('statsSaved')
  } catch (error) {
    actionStatus.value = props.t('loginError')
  }
}

const deleteTruck = async (truckId) => {
  actionStatus.value = ''
  try {
    await api.delete(`/trucks/${truckId}/`)
    await loadDashboard()
  } catch (error) {
    actionStatus.value = props.t('loginError')
  }
}

const deleteProject = async (projectId) => {
  actionStatus.value = ''
  try {
    await api.delete(`/projects/${projectId}/`)
    await loadDashboard()
  } catch (error) {
    actionStatus.value = props.t('loginError')
  }
}

onMounted(() => {
  if (token.value) {
    setAuthToken(token.value)
    loadDashboard()
  }
})
</script>

<template>
  <section id="dashboard" class="relative py-16 lg:py-24">
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(212,175,55,0.2),_transparent_60%)]"></div>
    <div class="relative mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col gap-4">
        <p class="text-xs uppercase tracking-[0.4em] text-[#bfa76a]">{{ t('adminSecureNote') }}</p>
        <div class="flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between" :class="isRtl ? 'lg:flex-row-reverse' : ''">
          <div :class="isRtl ? 'text-right' : ''">
            <h2 class="text-3xl font-semibold text-slate-900 dark:text-white">{{ t('adminTitle') }}</h2>
            <p class="mt-2 text-sm text-slate-500 dark:text-slate-300">{{ t('adminSubtitle') }}</p>
          </div>
          <div class="flex items-center gap-3">
            <span
              class="rounded-full border border-[#d4af37]/40 bg-[#f3e2a2]/30 px-4 py-2 text-xs uppercase tracking-[0.35em] text-[#8c774a]"
            >
              {{ isAuthenticated ? t('sessionActive') : t('adminSecureNote') }}
            </span>
            <button
              v-if="isAuthenticated"
              class="rounded-full border border-slate-200/70 bg-white/70 px-4 py-2 text-xs uppercase tracking-[0.3em] text-slate-700 transition hover:border-[#d4af37] dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-200"
              @click="logout"
            >
              {{ t('logoutButton') }}
            </button>
          </div>
        </div>
      </div>

      <div class="mt-10 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
        <div class="space-y-6">
          <div class="rounded-3xl border border-slate-200/70 bg-white/90 p-6 shadow-2xl shadow-slate-900/5 backdrop-blur dark:border-white/10 dark:bg-slate-900/70">
            <div class="flex items-center justify-between">
              <div :class="isRtl ? 'text-right' : ''">
                <p class="text-xs uppercase tracking-[0.3em] text-[#bfa76a]">{{ t('truckFormTitle') }}</p>
                <p class="mt-2 text-sm text-slate-500 dark:text-slate-300">{{ t('truckFormSubtitle') }}</p>
              </div>
              <span class="rounded-full bg-[#d4af37]/15 px-3 py-1 text-xs uppercase tracking-[0.2em] text-[#bfa76a]">
                {{ t('uploading') }}
              </span>
            </div>
            <div class="mt-5 grid gap-4 md:grid-cols-2">
              <input
                v-model="truckForm.title"
                :placeholder="t('truckTitleLabel')"
                class="rounded-2xl border border-slate-200/70 bg-white/80 px-4 py-3 text-sm text-slate-800 shadow-sm outline-none focus:border-[#d4af37] dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-100"
              />
              <input
                v-model="truckForm.description"
                :placeholder="t('truckDescLabel')"
                class="rounded-2xl border border-slate-200/70 bg-white/80 px-4 py-3 text-sm text-slate-800 shadow-sm outline-none focus:border-[#d4af37] dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-100"
              />
              <input
                type="file"
                accept="image/*"
                class="rounded-2xl border border-dashed border-[#d4af37]/40 bg-white/70 px-4 py-3 text-xs uppercase tracking-[0.25em] text-slate-600 dark:bg-slate-900/60 dark:text-slate-300"
                @change="handleTruckImage"
              />
              <button
                class="rounded-2xl bg-slate-900 px-4 py-3 text-xs uppercase tracking-[0.3em] text-white transition hover:bg-slate-800 dark:bg-white dark:text-slate-900"
                @click="createTruck"
              >
                {{ t('truckSubmit') }}
              </button>
            </div>
          </div>

          <div class="rounded-3xl border border-slate-200/70 bg-white/90 p-6 shadow-2xl shadow-slate-900/5 backdrop-blur dark:border-white/10 dark:bg-slate-900/70">
            <div class="flex items-center justify-between">
              <div :class="isRtl ? 'text-right' : ''">
                <p class="text-xs uppercase tracking-[0.3em] text-[#bfa76a]">{{ t('projectFormTitle') }}</p>
                <p class="mt-2 text-sm text-slate-500 dark:text-slate-300">{{ t('projectFormSubtitle') }}</p>
              </div>
              <span class="rounded-full bg-[#d4af37]/15 px-3 py-1 text-xs uppercase tracking-[0.2em] text-[#bfa76a]">
                {{ t('saving') }}
              </span>
            </div>
            <div class="mt-5 grid gap-4 md:grid-cols-2">
              <input
                v-model="projectForm.title"
                :placeholder="t('projectTitleLabel')"
                class="rounded-2xl border border-slate-200/70 bg-white/80 px-4 py-3 text-sm text-slate-800 shadow-sm outline-none focus:border-[#d4af37] dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-100"
              />
              <input
                v-model="projectForm.description"
                :placeholder="t('projectDescLabel')"
                class="rounded-2xl border border-slate-200/70 bg-white/80 px-4 py-3 text-sm text-slate-800 shadow-sm outline-none focus:border-[#d4af37] dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-100"
              />
              <input
                v-model="projectForm.date"
                type="date"
                class="rounded-2xl border border-slate-200/70 bg-white/80 px-4 py-3 text-sm text-slate-800 shadow-sm outline-none focus:border-[#d4af37] dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-100"
              />
              <input
                type="file"
                accept="image/*"
                class="rounded-2xl border border-dashed border-[#d4af37]/40 bg-white/70 px-4 py-3 text-xs uppercase tracking-[0.25em] text-slate-600 dark:bg-slate-900/60 dark:text-slate-300"
                @change="handleProjectImage"
              />
              <button
                class="rounded-2xl bg-slate-900 px-4 py-3 text-xs uppercase tracking-[0.3em] text-white transition hover:bg-slate-800 dark:bg-white dark:text-slate-900 md:col-span-2"
                @click="createProject"
              >
                {{ t('projectSubmit') }}
              </button>
            </div>
          </div>
        </div>

        <div class="space-y-6">
          <div class="rounded-3xl border border-slate-200/70 bg-white/90 p-6 shadow-2xl shadow-slate-900/5 backdrop-blur dark:border-white/10 dark:bg-slate-900/70">
            <div class="flex items-center justify-between">
              <div :class="isRtl ? 'text-right' : ''">
                <p class="text-xs uppercase tracking-[0.3em] text-[#bfa76a]">{{ t('statsTitle') }}</p>
                <p class="mt-2 text-sm text-slate-500 dark:text-slate-300">{{ t('statsSubtitle') }}</p>
              </div>
              <span class="rounded-full bg-[#d4af37]/15 px-3 py-1 text-xs uppercase tracking-[0.2em] text-[#bfa76a]">
                {{ loading ? t('loading') : t('statsSave') }}
              </span>
            </div>
            <div class="mt-5 space-y-4">
              <div
                v-for="stat in stats"
                :key="stat.id"
                class="rounded-2xl border border-slate-200/70 bg-white/70 p-4 dark:border-white/10 dark:bg-slate-900/60"
              >
                <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between" :class="isRtl ? 'sm:flex-row-reverse text-right' : ''">
                  <div>
                    <p class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-300">
                      {{ statLabelMap(stat.key) }}
                    </p>
                  </div>
                  <div class="flex items-center gap-2">
                    <input
                      v-model="stat.value"
                      type="number"
                      class="w-24 rounded-xl border border-slate-200/70 bg-white/80 px-3 py-2 text-sm text-slate-800 outline-none focus:border-[#d4af37] dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-100"
                    />
                    <input
                      v-model="stat.suffix"
                      class="w-16 rounded-xl border border-slate-200/70 bg-white/80 px-3 py-2 text-sm text-slate-800 outline-none focus:border-[#d4af37] dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-100"
                    />
                    <button
                      class="rounded-full border border-[#d4af37]/40 bg-[#f3e2a2]/30 px-3 py-2 text-xs uppercase tracking-[0.3em] text-[#8c774a] transition hover:bg-[#d4af37]/30"
                      @click="updateStat(stat)"
                    >
                      {{ t('statsSave') }}
                    </button>
                  </div>
                </div>
              </div>
              <p v-if="!stats.length" class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">
                {{ t('statsSubtitle') }}
              </p>
            </div>
          </div>

          <div class="rounded-3xl border border-slate-200/70 bg-white/90 p-6 shadow-2xl shadow-slate-900/5 backdrop-blur dark:border-white/10 dark:bg-slate-900/70">
            <div class="flex items-center justify-between">
              <p class="text-xs uppercase tracking-[0.3em] text-[#bfa76a]">{{ t('trucksListTitle') }}</p>
              <span class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">{{ trucks.length }}</span>
            </div>
            <div class="mt-4 space-y-3">
              <div
                v-for="truck in trucks"
                :key="truck.id"
                class="flex items-center justify-between gap-3 rounded-2xl border border-slate-200/70 bg-white/70 p-3 dark:border-white/10 dark:bg-slate-900/60"
              >
                <div :class="isRtl ? 'text-right' : ''">
                  <p class="text-sm font-semibold text-slate-900 dark:text-white">{{ truck.title }}</p>
                  <p class="text-xs text-slate-500 dark:text-slate-400">{{ truck.description }}</p>
                </div>
                <button class="text-xs uppercase tracking-[0.3em] text-rose-500" @click="deleteTruck(truck.id)">
                  {{ t('deleteButton') }}
                </button>
              </div>
              <p v-if="!trucks.length" class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">
                {{ t('trucksEmpty') }}
              </p>
            </div>
          </div>

          <div class="rounded-3xl border border-slate-200/70 bg-white/90 p-6 shadow-2xl shadow-slate-900/5 backdrop-blur dark:border-white/10 dark:bg-slate-900/70">
            <div class="flex items-center justify-between">
              <p class="text-xs uppercase tracking-[0.3em] text-[#bfa76a]">{{ t('projectsListTitle') }}</p>
              <span class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">{{ projects.length }}</span>
            </div>
            <div class="mt-4 space-y-3">
              <div
                v-for="project in projects"
                :key="project.id"
                class="flex items-center justify-between gap-3 rounded-2xl border border-slate-200/70 bg-white/70 p-3 dark:border-white/10 dark:bg-slate-900/60"
              >
                <div :class="isRtl ? 'text-right' : ''">
                  <p class="text-sm font-semibold text-slate-900 dark:text-white">{{ project.title }}</p>
                  <p class="text-xs text-slate-500 dark:text-slate-400">{{ project.date }}</p>
                </div>
                <button class="text-xs uppercase tracking-[0.3em] text-rose-500" @click="deleteProject(project.id)">
                  {{ t('deleteButton') }}
                </button>
              </div>
              <p v-if="!projects.length" class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">
                {{ t('projectsEmpty') }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="!isAuthenticated"
        class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 px-4 backdrop-blur-sm"
      >
        <div class="w-full max-w-md rounded-3xl border border-white/10 bg-white/90 p-6 shadow-2xl shadow-slate-900/30 backdrop-blur dark:bg-slate-900/80">
          <div class="flex flex-col gap-2" :class="isRtl ? 'text-right' : ''">
            <p class="text-xs uppercase tracking-[0.4em] text-[#bfa76a]">{{ t('adminSecureNote') }}</p>
            <h3 class="text-2xl font-semibold text-slate-900 dark:text-white">{{ t('loginTitle') }}</h3>
            <p class="text-sm text-slate-500 dark:text-slate-300">{{ t('loginSubtitle') }}</p>
          </div>
          <div class="mt-6 space-y-4">
            <input
              v-model="loginForm.username"
              :placeholder="t('loginUsername')"
              class="w-full rounded-2xl border border-slate-200/70 bg-white/80 px-4 py-3 text-sm text-slate-800 shadow-sm outline-none focus:border-[#d4af37] dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-100"
            />
            <input
              v-model="loginForm.password"
              type="password"
              :placeholder="t('loginPassword')"
              class="w-full rounded-2xl border border-slate-200/70 bg-white/80 px-4 py-3 text-sm text-slate-800 shadow-sm outline-none focus:border-[#d4af37] dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-100"
            />
            <button
              class="w-full rounded-2xl bg-slate-900 px-4 py-3 text-xs uppercase tracking-[0.35em] text-white transition hover:bg-slate-800 dark:bg-white dark:text-slate-900"
              @click="login"
            >
              {{ loginLoading ? t('loading') : t('loginButton') }}
            </button>
            <p v-if="loginError" class="text-xs uppercase tracking-[0.3em] text-rose-500">
              {{ loginError }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
