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
const authDisabled = false
const loginError = ref('')
const loginLoading = ref(false)
const loginForm = reactive({
  username: '',
  password: '',
})

const vehicles = ref([])
const statistics = ref([])
const siteSetting = ref(null)

const vehicleForm = reactive({
  id: null,
  title: '',
  description: '',
  image: null,
})
const vehicleImagePreview = ref('')
const vehicleSaving = ref(false)

const statForm = reactive({
  key: '',
  label_en: '',
  label_ar: '',
  caption_en: '',
  caption_ar: '',
  value: 0,
  suffix: '',
  order: 0,
})
const statSaving = ref(false)

const siteForm = reactive({
  site_name_en: '',
  site_name_ar: '',
  hero_title_en: '',
  hero_title_ar: '',
  hero_desc_en: '',
  hero_desc_ar: '',
  address_en: '',
  address_ar: '',
  contact_phone: '',
  contact_email: '',
  logo: null,
  hero_image: null,
})
const siteSaving = ref(false)
const siteLogoPreview = ref('')
const siteHeroPreview = ref('')

const loading = reactive({
  vehicles: false,
  statistics: false,
  settings: false,
})

const status = reactive({
  message: '',
  type: 'neutral',
})

const apiOnline = ref(true)

const isAuthenticated = computed(() => authDisabled || Boolean(token.value))
const showLogout = computed(() => !authDisabled && Boolean(token.value))

const statusClass = computed(() => {
  if (!status.message) return ''
  if (status.type === 'success') return 'border-emerald-400/60 text-emerald-200 bg-emerald-500/10'
  if (status.type === 'error') return 'border-rose-400/60 text-rose-200 bg-rose-500/10'
  return 'border-slate-500/60 text-slate-200 bg-slate-800/60'
})

const setStatus = (type, message) => {
  status.type = type
  status.message = message
}

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

const resolveImage = (item, key = 'image') => {
  if (!item) return ''
  const rawUrl = item[`${key}_url`] || item[key] || ''
  if (!rawUrl) return ''
  if (rawUrl.startsWith('http')) return rawUrl
  return `${API_BASE}${rawUrl}`
}

const formatDate = (value) => {
  if (!value) return '--'
  try {
    return new Date(value).toLocaleString(props.language === 'ar' ? 'ar' : 'en')
  } catch (error) {
    return value
  }
}

const applySiteForm = (setting) => {
  siteForm.site_name_en = setting?.site_name_en || ''
  siteForm.site_name_ar = setting?.site_name_ar || ''
  siteForm.hero_title_en = setting?.hero_title_en || ''
  siteForm.hero_title_ar = setting?.hero_title_ar || ''
  siteForm.hero_desc_en = setting?.hero_desc_en || ''
  siteForm.hero_desc_ar = setting?.hero_desc_ar || ''
  siteForm.address_en = setting?.address_en || ''
  siteForm.address_ar = setting?.address_ar || ''
  siteForm.contact_phone = setting?.contact_phone || ''
  siteForm.contact_email = setting?.contact_email || ''
  siteForm.logo = null
  siteForm.hero_image = null
  siteLogoPreview.value = resolveImage(setting, 'logo')
  siteHeroPreview.value = resolveImage(setting, 'hero_image')
}

const fetchVehicles = async () => {
  loading.vehicles = true
  try {
    const { data } = await api.get('/vehicles/')
    vehicles.value = Array.isArray(data) ? data : []
  } catch (error) {
    apiOnline.value = false
    vehicles.value = []
  } finally {
    loading.vehicles = false
  }
}

const fetchStatistics = async () => {
  loading.statistics = true
  try {
    const { data } = await api.get('/statistics/')
    statistics.value = Array.isArray(data) ? data : []
  } catch (error) {
    apiOnline.value = false
    statistics.value = []
  } finally {
    loading.statistics = false
  }
}

const fetchSiteSettings = async () => {
  loading.settings = true
  try {
    const { data } = await api.get('/site-settings/')
    const setting = Array.isArray(data) ? data[0] : data
    siteSetting.value = setting || null
    applySiteForm(setting)
  } catch (error) {
    apiOnline.value = false
    siteSetting.value = null
    applySiteForm(null)
  } finally {
    loading.settings = false
  }
}

const loadDashboard = async () => {
  apiOnline.value = true
  await Promise.all([fetchVehicles(), fetchStatistics(), fetchSiteSettings()])
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

const resetVehicleForm = () => {
  vehicleForm.id = null
  vehicleForm.title = ''
  vehicleForm.description = ''
  vehicleForm.image = null
  vehicleImagePreview.value = ''
}

const startEditVehicle = (vehicle) => {
  vehicleForm.id = vehicle.id
  vehicleForm.title = vehicle.title
  vehicleForm.description = vehicle.description
  vehicleForm.image = null
  vehicleImagePreview.value = resolveImage(vehicle)
}

const handleVehicleImage = (event) => {
  const file = event.target.files[0]
  vehicleForm.image = file || null
  vehicleImagePreview.value = file ? URL.createObjectURL(file) : vehicleImagePreview.value
}

const saveVehicle = async () => {
  if (!vehicleForm.title) {
    setStatus('error', props.t('statusMissing'))
    return
  }
  vehicleSaving.value = true
  const payload = {
    title: vehicleForm.title,
    description: vehicleForm.description,
    image: vehicleForm.image,
  }
  const formData = toFormData(payload)

  if (vehicleForm.id) {
    const index = vehicles.value.findIndex((item) => item.id === vehicleForm.id)
    const previous = index >= 0 ? { ...vehicles.value[index] } : null
    if (index >= 0) {
      vehicles.value[index] = {
        ...vehicles.value[index],
        title: vehicleForm.title,
        description: vehicleForm.description,
        image_url: vehicleImagePreview.value || vehicles.value[index]?.image_url,
      }
    }
    try {
      const { data } = await api.patch(`/vehicles/${vehicleForm.id}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      if (index >= 0) {
        vehicles.value[index] = data
      }
      setStatus('success', props.t('statusSaved'))
      resetVehicleForm()
    } catch (error) {
      if (index >= 0 && previous) {
        vehicles.value[index] = previous
      }
      setStatus('error', props.t('statusError'))
    } finally {
      vehicleSaving.value = false
    }
    return
  }

  const tempId = `tmp-${Date.now()}`
  const optimistic = {
    id: tempId,
    title: vehicleForm.title,
    description: vehicleForm.description,
    image_url: vehicleImagePreview.value,
    updated_at: new Date().toISOString(),
  }
  vehicles.value = [optimistic, ...vehicles.value]

  try {
    const { data } = await api.post('/vehicles/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    const index = vehicles.value.findIndex((item) => item.id === tempId)
    if (index >= 0) {
      vehicles.value[index] = data
    }
    setStatus('success', props.t('statusSaved'))
    resetVehicleForm()
  } catch (error) {
    vehicles.value = vehicles.value.filter((item) => item.id !== tempId)
    setStatus('error', props.t('statusError'))
  } finally {
    vehicleSaving.value = false
  }
}

const deleteVehicle = async (vehicle) => {
  const snapshot = [...vehicles.value]
  vehicles.value = vehicles.value.filter((item) => item.id !== vehicle.id)
  try {
    await api.delete(`/vehicles/${vehicle.id}/`)
    setStatus('success', props.t('statusDeleted'))
  } catch (error) {
    vehicles.value = snapshot
    setStatus('error', props.t('statusError'))
  }
}

const resetStatForm = () => {
  statForm.key = ''
  statForm.label_en = ''
  statForm.label_ar = ''
  statForm.caption_en = ''
  statForm.caption_ar = ''
  statForm.value = 0
  statForm.suffix = ''
  statForm.order = 0
}

const createStatistic = async () => {
  if (!statForm.key || !statForm.label_en) {
    setStatus('error', props.t('statusMissing'))
    return
  }
  statSaving.value = true
  const payload = { ...statForm }
  const formData = toFormData(payload)
  const tempId = `tmp-${Date.now()}`
  const optimistic = {
    id: tempId,
    ...payload,
    updated_at: new Date().toISOString(),
  }
  statistics.value = [...statistics.value, optimistic]

  try {
    const { data } = await api.post('/statistics/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    const index = statistics.value.findIndex((item) => item.id === tempId)
    if (index >= 0) {
      statistics.value[index] = data
    }
    setStatus('success', props.t('statusSaved'))
    resetStatForm()
  } catch (error) {
    statistics.value = statistics.value.filter((item) => item.id !== tempId)
    setStatus('error', props.t('statusError'))
  } finally {
    statSaving.value = false
  }
}

const updateStatistic = async (stat) => {
  const previous = { ...stat }
  const payload = {
    key: stat.key,
    label_en: stat.label_en,
    label_ar: stat.label_ar,
    caption_en: stat.caption_en,
    caption_ar: stat.caption_ar,
    value: stat.value,
    suffix: stat.suffix,
    order: stat.order,
  }
  const formData = toFormData(payload)
  try {
    const { data } = await api.patch(`/statistics/${stat.id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    const index = statistics.value.findIndex((item) => item.id === stat.id)
    if (index >= 0) {
      statistics.value[index] = data
    }
    setStatus('success', props.t('statusSaved'))
  } catch (error) {
    const index = statistics.value.findIndex((item) => item.id === stat.id)
    if (index >= 0) {
      statistics.value[index] = previous
    }
    setStatus('error', props.t('statusError'))
  }
}

const deleteStatistic = async (stat) => {
  const snapshot = [...statistics.value]
  statistics.value = statistics.value.filter((item) => item.id !== stat.id)
  try {
    await api.delete(`/statistics/${stat.id}/`)
    setStatus('success', props.t('statusDeleted'))
  } catch (error) {
    statistics.value = snapshot
    setStatus('error', props.t('statusError'))
  }
}

const handleSiteLogo = (event) => {
  const file = event.target.files[0]
  siteForm.logo = file || null
  siteLogoPreview.value = file ? URL.createObjectURL(file) : siteLogoPreview.value
}

const handleSiteHero = (event) => {
  const file = event.target.files[0]
  siteForm.hero_image = file || null
  siteHeroPreview.value = file ? URL.createObjectURL(file) : siteHeroPreview.value
}

const saveSiteSettings = async () => {
  siteSaving.value = true
  const payload = {
    site_name_en: siteForm.site_name_en,
    site_name_ar: siteForm.site_name_ar,
    hero_title_en: siteForm.hero_title_en,
    hero_title_ar: siteForm.hero_title_ar,
    hero_desc_en: siteForm.hero_desc_en,
    hero_desc_ar: siteForm.hero_desc_ar,
    address_en: siteForm.address_en,
    address_ar: siteForm.address_ar,
    contact_phone: siteForm.contact_phone,
    contact_email: siteForm.contact_email,
    logo: siteForm.logo,
    hero_image: siteForm.hero_image,
  }
  const formData = toFormData(payload)

  try {
    if (siteSetting.value?.id) {
      const { data } = await api.patch(`/site-settings/${siteSetting.value.id}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      siteSetting.value = data
      applySiteForm(data)
      setStatus('success', props.t('settingsSaved'))
    } else {
      const { data } = await api.post('/site-settings/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      siteSetting.value = data
      applySiteForm(data)
      setStatus('success', props.t('settingsSaved'))
    }
  } catch (error) {
    setStatus('error', props.t('statusError'))
  } finally {
    siteSaving.value = false
  }
}

const refreshPublic = async () => {
  try {
    const { data } = await api.post('/site-settings/refresh/', null, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    siteSetting.value = data
    applySiteForm(data)
    setStatus('success', props.t('consoleRefreshSuccess'))
  } catch (error) {
    setStatus('error', props.t('consoleRefreshError'))
  }
}

onMounted(() => {
  if (authDisabled) {
    setAuthToken('')
    loadDashboard()
    return
  }
  if (token.value) {
    setAuthToken(token.value)
    loadDashboard()
  }
})
</script>

<template>
  <section class="min-h-screen bg-[#0b0f14] text-slate-100">
    <div class="mx-auto w-full max-w-7xl px-4 pb-16 pt-10 sm:px-6 lg:px-8">
      <header class="border border-[#1f2a37] bg-[#0f172a]/80 p-6">
        <div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between" :class="isRtl ? 'lg:flex-row-reverse' : ''">
          <div :class="isRtl ? 'text-right' : ''">
            <p class="text-xs uppercase tracking-[0.35em] text-[#d4af37]">{{ t('consoleOverline') }}</p>
            <h1 class="mt-3 text-3xl font-semibold text-white">{{ t('consoleTitle') }}</h1>
            <p class="mt-2 max-w-2xl text-sm text-slate-300">{{ t('consoleSubtitle') }}</p>
          </div>
          <div class="flex flex-wrap items-center gap-3" :class="isRtl ? 'justify-end' : ''">
            <div class="border border-[#1f2a37] bg-[#0b1220] px-4 py-2 text-xs uppercase tracking-[0.3em] text-slate-300">
              {{ t('consoleStatusLabel') }}: <span class="text-white">{{ apiOnline ? t('consoleStatusOnline') : t('consoleStatusOffline') }}</span>
            </div>
            <div class="border border-[#1f2a37] bg-[#0b1220] px-4 py-2 text-xs uppercase tracking-[0.3em] text-slate-300">
              {{ t('consoleAuthLabel') }}: <span class="text-white">{{ isAuthenticated ? t('consoleAuthGranted') : t('consoleAuthRequired') }}</span>
            </div>
            <button
              class="border border-[#d4af37] bg-[#d4af37] px-4 py-2 text-xs font-semibold uppercase tracking-[0.3em] text-slate-900 transition hover:bg-[#f3e2a2]"
              @click="refreshPublic"
            >
              {{ t('consoleInstantUpdate') }}
            </button>
            <button
              v-if="showLogout"
              class="border border-[#1f2a37] bg-transparent px-4 py-2 text-xs uppercase tracking-[0.3em] text-slate-200 transition hover:border-[#d4af37]"
              @click="logout"
            >
              {{ t('logoutButton') }}
            </button>
          </div>
        </div>
        <p class="mt-4 text-xs uppercase tracking-[0.3em] text-slate-400" :class="isRtl ? 'text-right' : ''">
          {{ t('consoleInstantHint') }}
        </p>
      </header>

      <div v-if="status.message" class="mt-4 border px-4 py-3 text-xs uppercase tracking-[0.3em]" :class="statusClass">
        {{ status.message }}
      </div>

      <div class="mt-6 grid gap-6 lg:grid-cols-[240px_1fr]">
        <aside class="border border-[#1f2a37] bg-[#0f172a]/70 p-5" :class="isRtl ? 'text-right' : ''">
          <p class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('dashboardOverline') }}</p>
          <h2 class="mt-2 text-lg font-semibold text-white">{{ t('dashboardTitle') }}</h2>
          <nav class="mt-6 space-y-3 text-sm">
            <a href="#overview" class="block border border-transparent px-3 py-2 text-slate-300 transition hover:border-[#d4af37] hover:text-white">
              {{ t('navOverview') }}
            </a>
            <a href="#vehicles" class="block border border-transparent px-3 py-2 text-slate-300 transition hover:border-[#d4af37] hover:text-white">
              {{ t('navVehicles') }}
            </a>
            <a href="#statistics" class="block border border-transparent px-3 py-2 text-slate-300 transition hover:border-[#d4af37] hover:text-white">
              {{ t('navStatistics') }}
            </a>
            <a href="#settings" class="block border border-transparent px-3 py-2 text-slate-300 transition hover:border-[#d4af37] hover:text-white">
              {{ t('navSettings') }}
            </a>
          </nav>
        </aside>

        <main class="space-y-10">
          <section id="overview" class="border border-[#1f2a37] bg-[#0f172a]/70 p-6" :class="isRtl ? 'text-right' : ''">
            <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between" :class="isRtl ? 'lg:flex-row-reverse' : ''">
              <div>
                <p class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('consoleLastSync') }}</p>
                <p class="mt-2 text-sm text-white">{{ formatDate(siteSetting?.updated_at) }}</p>
              </div>
              <div class="grid gap-4 sm:grid-cols-3">
                <div class="border border-[#1f2a37] bg-[#0b1220] px-4 py-3">
                  <p class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('overviewVehicles') }}</p>
                  <p class="mt-2 text-2xl font-semibold text-white">{{ vehicles.length }}</p>
                </div>
                <div class="border border-[#1f2a37] bg-[#0b1220] px-4 py-3">
                  <p class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('overviewStatistics') }}</p>
                  <p class="mt-2 text-2xl font-semibold text-white">{{ statistics.length }}</p>
                </div>
                <div class="border border-[#1f2a37] bg-[#0b1220] px-4 py-3">
                  <p class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('overviewSettings') }}</p>
                  <p class="mt-2 text-2xl font-semibold text-white">{{ siteSetting ? 1 : 0 }}</p>
                </div>
              </div>
            </div>
          </section>

          <section id="vehicles" class="border border-[#1f2a37] bg-[#0f172a]/70 p-6">
            <div class="flex flex-col gap-2" :class="isRtl ? 'text-right' : ''">
              <p class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('vehiclesTitle') }}</p>
              <h3 class="text-2xl font-semibold text-white">{{ t('vehicleFormTitle') }}</h3>
              <p class="text-sm text-slate-400">{{ t('vehiclesSubtitle') }}</p>
            </div>

            <div class="mt-6 grid gap-4 lg:grid-cols-[1fr_260px]">
              <div class="grid gap-4">
                <input
                  v-model="vehicleForm.title"
                  :placeholder="t('vehicleFieldTitle')"
                  class="w-full border border-[#1f2a37] bg-[#0b1220] px-4 py-3 text-sm text-slate-200 outline-none"
                  :class="isRtl ? 'text-right' : ''"
                />
                <textarea
                  v-model="vehicleForm.description"
                  :placeholder="t('vehicleFieldDescription')"
                  rows="3"
                  class="w-full border border-[#1f2a37] bg-[#0b1220] px-4 py-3 text-sm text-slate-200 outline-none"
                  :class="isRtl ? 'text-right' : ''"
                ></textarea>
                <input
                  type="file"
                  accept="image/*"
                  class="w-full border border-dashed border-[#d4af37]/60 bg-[#0b1220] px-4 py-3 text-xs uppercase tracking-[0.3em] text-slate-300"
                  @change="handleVehicleImage"
                />
                <div class="flex flex-wrap items-center gap-3">
                  <button
                    class="border border-[#d4af37] bg-[#d4af37] px-4 py-2 text-xs font-semibold uppercase tracking-[0.3em] text-slate-900"
                    @click="saveVehicle"
                  >
                    {{ vehicleForm.id ? t('vehicleUpdate') : t('vehicleCreate') }}
                  </button>
                  <button
                    v-if="vehicleForm.id"
                    class="border border-[#1f2a37] bg-transparent px-4 py-2 text-xs uppercase tracking-[0.3em] text-slate-200"
                    @click="resetVehicleForm"
                  >
                    {{ t('vehicleCancel') }}
                  </button>
                  <span v-if="vehicleSaving" class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('saving') }}</span>
                </div>
              </div>
              <div class="border border-[#1f2a37] bg-[#0b1220] p-4">
                <p class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('vehicleFieldImage') }}</p>
                <div class="mt-4 aspect-[4/3] w-full overflow-hidden border border-[#1f2a37] bg-[#0f172a]">
                  <img v-if="vehicleImagePreview" :src="vehicleImagePreview" :alt="vehicleForm.title" class="h-full w-full object-cover" />
                  <div v-else class="flex h-full w-full items-center justify-center text-xs uppercase tracking-[0.3em] text-slate-500">
                    {{ t('vehicleFieldImage') }}
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-8 border border-[#1f2a37]">
              <div class="flex items-center justify-between border-b border-[#1f2a37] bg-[#0b1220] px-4 py-3">
                <p class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('vehicleTableTitle') }}</p>
                <span class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ vehicles.length }}</span>
              </div>
              <div class="overflow-x-auto">
                <table class="w-full text-sm">
                  <thead class="bg-[#0f172a] text-xs uppercase tracking-[0.3em] text-slate-400">
                    <tr>
                      <th class="px-4 py-3 text-left" :class="isRtl ? 'text-right' : ''">{{ t('vehicleTableHeaderTitle') }}</th>
                      <th class="px-4 py-3 text-left" :class="isRtl ? 'text-right' : ''">{{ t('vehicleTableHeaderDescription') }}</th>
                      <th class="px-4 py-3 text-left" :class="isRtl ? 'text-right' : ''">{{ t('vehicleTableHeaderUpdated') }}</th>
                      <th class="px-4 py-3 text-left" :class="isRtl ? 'text-right' : ''">{{ t('vehicleTableHeaderActions') }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="vehicle in vehicles"
                      :key="vehicle.id"
                      class="border-t border-[#1f2a37] text-slate-200 hover:bg-[#0b1220]"
                    >
                      <td class="px-4 py-3">
                        <div class="flex items-center gap-3" :class="isRtl ? 'flex-row-reverse' : ''">
                          <div class="h-10 w-14 overflow-hidden border border-[#1f2a37] bg-[#0f172a]">
                            <img v-if="resolveImage(vehicle)" :src="resolveImage(vehicle)" :alt="vehicle.title" class="h-full w-full object-cover" />
                          </div>
                          <div :class="isRtl ? 'text-right' : ''">
                            <p class="text-sm font-semibold text-white">{{ vehicle.title }}</p>
                          </div>
                        </div>
                      </td>
                      <td class="px-4 py-3 text-slate-400">{{ vehicle.description }}</td>
                      <td class="px-4 py-3 text-slate-400">{{ formatDate(vehicle.updated_at) }}</td>
                      <td class="px-4 py-3">
                        <div class="flex items-center gap-3" :class="isRtl ? 'flex-row-reverse' : ''">
                          <button class="text-xs uppercase tracking-[0.3em] text-[#d4af37]" @click="startEditVehicle(vehicle)">
                            {{ t('editButton') }}
                          </button>
                          <button class="text-xs uppercase tracking-[0.3em] text-rose-300" @click="deleteVehicle(vehicle)">
                            {{ t('deleteButton') }}
                          </button>
                        </div>
                      </td>
                    </tr>
                    <tr v-if="!vehicles.length && !loading.vehicles">
                      <td colspan="4" class="px-4 py-6 text-center text-xs uppercase tracking-[0.3em] text-slate-500">
                        {{ t('vehicleEmpty') }}
                      </td>
                    </tr>
                    <tr v-if="loading.vehicles">
                      <td colspan="4" class="px-4 py-6 text-center text-xs uppercase tracking-[0.3em] text-slate-500">
                        {{ t('loading') }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </section>

          <section id="statistics" class="border border-[#1f2a37] bg-[#0f172a]/70 p-6">
            <div class="flex flex-col gap-2" :class="isRtl ? 'text-right' : ''">
              <p class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('statisticsTitle') }}</p>
              <h3 class="text-2xl font-semibold text-white">{{ t('statsTitle') }}</h3>
              <p class="text-sm text-slate-400">{{ t('statisticsSubtitle') }}</p>
            </div>

            <div class="mt-6 grid gap-4 lg:grid-cols-2">
              <div class="grid gap-3 border border-[#1f2a37] bg-[#0b1220] p-4">
                <p class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('statFormTitle') }}</p>
                <input v-model="statForm.key" :placeholder="t('statKeyLabel')" class="border border-[#1f2a37] bg-[#0f172a] px-3 py-2 text-sm text-slate-200" />
                <input v-model="statForm.label_en" :placeholder="t('statLabelEn')" class="border border-[#1f2a37] bg-[#0f172a] px-3 py-2 text-sm text-slate-200" />
                <input v-model="statForm.label_ar" :placeholder="t('statLabelAr')" class="border border-[#1f2a37] bg-[#0f172a] px-3 py-2 text-sm text-slate-200" />
                <input v-model="statForm.caption_en" :placeholder="t('statCaptionEn')" class="border border-[#1f2a37] bg-[#0f172a] px-3 py-2 text-sm text-slate-200" />
                <input v-model="statForm.caption_ar" :placeholder="t('statCaptionAr')" class="border border-[#1f2a37] bg-[#0f172a] px-3 py-2 text-sm text-slate-200" />
                <div class="grid gap-3 sm:grid-cols-3">
                  <input v-model.number="statForm.value" type="number" :placeholder="t('statValueLabel')" class="border border-[#1f2a37] bg-[#0f172a] px-3 py-2 text-sm text-slate-200" />
                  <input v-model="statForm.suffix" :placeholder="t('statSuffixLabel')" class="border border-[#1f2a37] bg-[#0f172a] px-3 py-2 text-sm text-slate-200" />
                  <input v-model.number="statForm.order" type="number" :placeholder="t('statOrderLabel')" class="border border-[#1f2a37] bg-[#0f172a] px-3 py-2 text-sm text-slate-200" />
                </div>
                <div class="flex items-center gap-3">
                  <button class="border border-[#d4af37] bg-[#d4af37] px-4 py-2 text-xs font-semibold uppercase tracking-[0.3em] text-slate-900" @click="createStatistic">
                    {{ t('statCreateButton') }}
                  </button>
                  <span v-if="statSaving" class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('saving') }}</span>
                </div>
              </div>

              <div class="border border-[#1f2a37]">
                <div class="flex items-center justify-between border-b border-[#1f2a37] bg-[#0b1220] px-4 py-3">
                  <p class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('statsTitle') }}</p>
                  <span class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ statistics.length }}</span>
                </div>
                <div class="overflow-x-auto">
                  <table class="w-full text-sm">
                    <thead class="bg-[#0f172a] text-xs uppercase tracking-[0.3em] text-slate-400">
                      <tr>
                        <th class="px-4 py-3 text-left" :class="isRtl ? 'text-right' : ''">{{ t('statTableHeaderKey') }}</th>
                        <th class="px-4 py-3 text-left" :class="isRtl ? 'text-right' : ''">{{ t('statTableHeaderLabel') }}</th>
                        <th class="px-4 py-3 text-left" :class="isRtl ? 'text-right' : ''">{{ t('statTableHeaderValue') }}</th>
                        <th class="px-4 py-3 text-left" :class="isRtl ? 'text-right' : ''">{{ t('statTableHeaderOrder') }}</th>
                        <th class="px-4 py-3 text-left" :class="isRtl ? 'text-right' : ''">{{ t('statTableHeaderActions') }}</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="stat in statistics"
                        :key="stat.id"
                        class="border-t border-[#1f2a37] text-slate-200 hover:bg-[#0b1220]"
                      >
                        <td class="px-4 py-3">
                          <input v-model="stat.key" class="w-32 border border-[#1f2a37] bg-[#0f172a] px-2 py-1 text-xs text-slate-200" />
                        </td>
                        <td class="px-4 py-3">
                          <div class="grid gap-2">
                            <input v-model="stat.label_en" class="border border-[#1f2a37] bg-[#0f172a] px-2 py-1 text-xs text-slate-200" />
                            <input v-model="stat.label_ar" class="border border-[#1f2a37] bg-[#0f172a] px-2 py-1 text-xs text-slate-200" />
                          </div>
                        </td>
                        <td class="px-4 py-3">
                          <div class="grid gap-2">
                            <input v-model.number="stat.value" type="number" class="w-24 border border-[#1f2a37] bg-[#0f172a] px-2 py-1 text-xs text-slate-200" />
                            <input v-model="stat.suffix" class="w-20 border border-[#1f2a37] bg-[#0f172a] px-2 py-1 text-xs text-slate-200" />
                          </div>
                        </td>
                        <td class="px-4 py-3">
                          <input v-model.number="stat.order" type="number" class="w-20 border border-[#1f2a37] bg-[#0f172a] px-2 py-1 text-xs text-slate-200" />
                        </td>
                        <td class="px-4 py-3">
                          <div class="flex items-center gap-3" :class="isRtl ? 'flex-row-reverse' : ''">
                            <button class="text-xs uppercase tracking-[0.3em] text-[#d4af37]" @click="updateStatistic(stat)">
                              {{ t('statUpdateButton') }}
                            </button>
                            <button class="text-xs uppercase tracking-[0.3em] text-rose-300" @click="deleteStatistic(stat)">
                              {{ t('deleteButton') }}
                            </button>
                          </div>
                        </td>
                      </tr>
                      <tr v-if="!statistics.length && !loading.statistics">
                        <td colspan="5" class="px-4 py-6 text-center text-xs uppercase tracking-[0.3em] text-slate-500">
                          {{ t('statEmpty') }}
                        </td>
                      </tr>
                      <tr v-if="loading.statistics">
                        <td colspan="5" class="px-4 py-6 text-center text-xs uppercase tracking-[0.3em] text-slate-500">
                          {{ t('loading') }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </section>

          <section id="settings" class="border border-[#1f2a37] bg-[#0f172a]/70 p-6">
            <div class="flex flex-col gap-2" :class="isRtl ? 'text-right' : ''">
              <p class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('settingsTitle') }}</p>
              <h3 class="text-2xl font-semibold text-white">{{ t('settingsTitle') }}</h3>
              <p class="text-sm text-slate-400">{{ t('settingsSubtitle') }}</p>
            </div>

            <div class="mt-6 grid gap-6 lg:grid-cols-[1fr_320px]">
              <div class="grid gap-4">
                <div class="grid gap-4 sm:grid-cols-2">
                  <input v-model="siteForm.site_name_en" :placeholder="t('settingsSiteNameEn')" class="border border-[#1f2a37] bg-[#0b1220] px-4 py-3 text-sm text-slate-200" />
                  <input v-model="siteForm.site_name_ar" :placeholder="t('settingsSiteNameAr')" class="border border-[#1f2a37] bg-[#0b1220] px-4 py-3 text-sm text-slate-200" />
                </div>
                <div class="grid gap-4 sm:grid-cols-2">
                  <input v-model="siteForm.hero_title_en" :placeholder="t('settingsHeroTitleEn')" class="border border-[#1f2a37] bg-[#0b1220] px-4 py-3 text-sm text-slate-200" />
                  <input v-model="siteForm.hero_title_ar" :placeholder="t('settingsHeroTitleAr')" class="border border-[#1f2a37] bg-[#0b1220] px-4 py-3 text-sm text-slate-200" />
                </div>
                <div class="grid gap-4 sm:grid-cols-2">
                  <textarea v-model="siteForm.hero_desc_en" rows="3" :placeholder="t('settingsHeroDescEn')" class="border border-[#1f2a37] bg-[#0b1220] px-4 py-3 text-sm text-slate-200"></textarea>
                  <textarea v-model="siteForm.hero_desc_ar" rows="3" :placeholder="t('settingsHeroDescAr')" class="border border-[#1f2a37] bg-[#0b1220] px-4 py-3 text-sm text-slate-200"></textarea>
                </div>
                <div class="grid gap-4 sm:grid-cols-2">
                  <input v-model="siteForm.address_en" :placeholder="t('settingsAddressEn')" class="border border-[#1f2a37] bg-[#0b1220] px-4 py-3 text-sm text-slate-200" />
                  <input v-model="siteForm.address_ar" :placeholder="t('settingsAddressAr')" class="border border-[#1f2a37] bg-[#0b1220] px-4 py-3 text-sm text-slate-200" />
                </div>
                <div class="grid gap-4 sm:grid-cols-2">
                  <input v-model="siteForm.contact_phone" :placeholder="t('settingsContactPhone')" class="border border-[#1f2a37] bg-[#0b1220] px-4 py-3 text-sm text-slate-200" />
                  <input v-model="siteForm.contact_email" :placeholder="t('settingsContactEmail')" class="border border-[#1f2a37] bg-[#0b1220] px-4 py-3 text-sm text-slate-200" />
                </div>
                <div class="flex flex-wrap items-center gap-3">
                  <button class="border border-[#d4af37] bg-[#d4af37] px-4 py-2 text-xs font-semibold uppercase tracking-[0.3em] text-slate-900" @click="saveSiteSettings">
                    {{ siteSetting ? t('settingsUpdate') : t('settingsCreate') }}
                  </button>
                  <button class="border border-[#1f2a37] bg-transparent px-4 py-2 text-xs uppercase tracking-[0.3em] text-slate-200" @click="refreshPublic">
                    {{ t('consoleInstantUpdate') }}
                  </button>
                  <span v-if="siteSaving" class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('saving') }}</span>
                </div>
              </div>

              <div class="grid gap-4">
                <div class="border border-[#1f2a37] bg-[#0b1220] p-4">
                  <p class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('settingsLogo') }}</p>
                  <input type="file" accept="image/*" class="mt-3 w-full border border-dashed border-[#d4af37]/60 bg-[#0f172a] px-3 py-2 text-xs uppercase tracking-[0.3em] text-slate-300" @change="handleSiteLogo" />
                  <div class="mt-3 aspect-[4/3] w-full overflow-hidden border border-[#1f2a37] bg-[#0f172a]">
                    <img v-if="siteLogoPreview" :src="siteLogoPreview" alt="logo" class="h-full w-full object-cover" />
                    <div v-else class="flex h-full w-full items-center justify-center text-xs uppercase tracking-[0.3em] text-slate-500">
                      {{ t('settingsLogo') }}
                    </div>
                  </div>
                </div>
                <div class="border border-[#1f2a37] bg-[#0b1220] p-4">
                  <p class="text-xs uppercase tracking-[0.3em] text-slate-400">{{ t('settingsHeroImage') }}</p>
                  <input type="file" accept="image/*" class="mt-3 w-full border border-dashed border-[#d4af37]/60 bg-[#0f172a] px-3 py-2 text-xs uppercase tracking-[0.3em] text-slate-300" @change="handleSiteHero" />
                  <div class="mt-3 aspect-[4/3] w-full overflow-hidden border border-[#1f2a37] bg-[#0f172a]">
                    <img v-if="siteHeroPreview" :src="siteHeroPreview" alt="hero" class="h-full w-full object-cover" />
                    <div v-else class="flex h-full w-full items-center justify-center text-xs uppercase tracking-[0.3em] text-slate-500">
                      {{ t('settingsHeroImage') }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </main>
      </div>

      <div v-if="!isAuthenticated" class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4 backdrop-blur-sm">
        <div class="w-full max-w-md border border-[#1f2a37] bg-[#0f172a] p-6">
          <div class="flex flex-col gap-2" :class="isRtl ? 'text-right' : ''">
            <p class="text-xs uppercase tracking-[0.35em] text-slate-400">{{ t('adminSecureNote') }}</p>
            <h3 class="text-2xl font-semibold text-white">{{ t('loginTitle') }}</h3>
            <p class="text-sm text-slate-400">{{ t('loginSubtitle') }}</p>
          </div>
          <div class="mt-6 space-y-4">
            <input v-model="loginForm.username" :placeholder="t('loginUsername')" class="w-full border border-[#1f2a37] bg-[#0b1220] px-4 py-3 text-sm text-slate-200" />
            <input v-model="loginForm.password" type="password" :placeholder="t('loginPassword')" class="w-full border border-[#1f2a37] bg-[#0b1220] px-4 py-3 text-sm text-slate-200" />
            <button class="w-full border border-[#d4af37] bg-[#d4af37] px-4 py-3 text-xs font-semibold uppercase tracking-[0.3em] text-slate-900" @click="login">
              {{ loginLoading ? t('loading') : t('loginButton') }}
            </button>
            <p v-if="loginError" class="text-xs uppercase tracking-[0.3em] text-rose-300">
              {{ loginError }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
