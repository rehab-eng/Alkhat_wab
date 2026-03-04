<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
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
const API_ENABLED = import.meta.env.VITE_ENABLE_API === 'true' || import.meta.env.DEV
const SITE_URL = import.meta.env.VITE_SITE_URL || 'https://khututalrimal.ly'
const heroFallback = '/ssss.webp'

const vehicles = ref([])
const statistics = ref([])
const siteSettings = ref(null)
const refreshToken = ref('')

const vehiclesLoading = ref(true)
const statsLoading = ref(true)
const settingsLoading = ref(true)

const statsRef = ref(null)
const displayValues = ref([])
const hasAnimated = ref(false)
let observer
let refreshInterval
const ENABLE_ANIMATION = false

const fallbackStats = [
  {
    labelKey: 'statYears',
    captionKey: 'statYearsCaption',
    value: 560,
    suffix: '+',
  },
  {
    labelKey: 'statProjects',
    captionKey: 'statProjectsCaption',
    value: 20,
    suffix: '+',
  },
  {
    labelKey: 'statFleet',
    captionKey: 'statFleetCaption',
    value: 24,
    suffix: '/7',
  },
  {
    labelKey: 'statSafety',
    captionKey: 'statSafetyCaption',
    value: 50000,
    suffix: '',
  },
]

const displayStats = computed(() => {
  if (!statistics.value.length) {
    return fallbackStats.map((stat) => ({
      label: props.t(stat.labelKey),
      caption: props.t(stat.captionKey),
      value: stat.value,
      suffix: stat.suffix,
    }))
  }
  return statistics.value.map((stat) => ({
    label: props.language === 'ar' ? stat.label_ar || stat.label_en : stat.label_en || stat.label_ar,
    caption: props.language === 'ar' ? stat.caption_ar || stat.caption_en : stat.caption_en || stat.caption_ar,
    value: stat.value,
    suffix: stat.suffix,
  }))
})

const setDisplayValues = () => {
  displayValues.value = displayStats.value.map((stat) => (ENABLE_ANIMATION ? 0 : stat.value))
}

watch(displayStats, () => {
  setDisplayValues()
  hasAnimated.value = false
})

watch(
  () => props.language,
  () => {
    if (siteSettings.value) {
      updateStructuredData()
    }
  }
)

const animateStats = () => {
  if (!ENABLE_ANIMATION) {
    displayValues.value = displayStats.value.map((stat) => stat.value)
    return
  }
  const nowFn =
    typeof performance !== 'undefined' && typeof performance.now === 'function' ? () => performance.now() : () => Date.now()
  const raf =
    typeof requestAnimationFrame === 'function'
      ? requestAnimationFrame
      : (cb) => setTimeout(() => cb(nowFn()), 16)

  displayStats.value.forEach((stat, index) => {
    const duration = 1400 + index * 180
    const start = nowFn()

    const step = (now) => {
      const progress = Math.min((now - start) / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      displayValues.value[index] = Math.floor(eased * stat.value)
      if (progress < 1) {
        raf(step)
      } else {
        displayValues.value[index] = stat.value
      }
    }

    raf(step)
  })
}

const formatStat = (index) => {
  const value = displayValues.value[index] ?? 0
  const suffix = displayStats.value[index]?.suffix || ''
  let formatted = value
  if (Number.isFinite(value)) {
    try {
      if (typeof Intl !== 'undefined') {
        formatted = new Intl.NumberFormat(props.language === 'ar' ? 'ar-LY' : 'en-US').format(value)
      } else {
        formatted = value
      }
    } catch (error) {
      formatted = value
    }
  }
  return `${formatted}${suffix}`
}

const resolveImage = (item, key = 'image') => {
  if (!item) return ''
  let rawUrl = item[`${key}_url`] || item[key] || ''
  if (!rawUrl) return ''
  if (typeof rawUrl !== 'string') {
    rawUrl = rawUrl?.url || rawUrl?.path || ''
  }
  if (!rawUrl || typeof rawUrl !== 'string') return ''
  if (rawUrl.startsWith('http')) return rawUrl
  return `${API_BASE}${rawUrl}`
}

const heroImage = computed(() => {
  if (siteSettings.value?.hero_image_url || siteSettings.value?.hero_image) {
    return resolveImage(siteSettings.value, 'hero_image')
  }
  const vehicleImage = resolveImage(vehicles.value[0])
  return vehicleImage || heroFallback
})

const getSetting = (field) => {
  const locale = props.language === 'ar' ? 'ar' : 'en'
  return siteSettings.value?.[`${field}_${locale}`] || ''
}

const heroBadge = computed(() => getSetting('site_name') || props.t('heroBadge'))
const heroTitle = computed(() => getSetting('hero_title') || props.t('heroTitle'))
const heroDesc = computed(() => getSetting('hero_desc') || props.t('heroDesc'))
const contactPhone = computed(() => siteSettings.value?.contact_phone || '')
const contactEmail = computed(() => siteSettings.value?.contact_email || '')
const contactNumbers = ['091-5320462', '092-5256275']

const fetchVehicles = async () => {
  vehiclesLoading.value = true
  try {
    const { data } = await axios.get(`${API_BASE}/api/vehicles/`)
    vehicles.value = Array.isArray(data) ? data : []
  } catch (error) {
    vehicles.value = []
  } finally {
    vehiclesLoading.value = false
  }
}

const fetchStatistics = async () => {
  statsLoading.value = true
  try {
    const { data } = await axios.get(`${API_BASE}/api/statistics/`)
    statistics.value = Array.isArray(data) ? data : []
  } catch (error) {
    statistics.value = []
  } finally {
    statsLoading.value = false
  }
}

const updateStructuredData = () => {
  if (typeof document === 'undefined') return
  const name = siteSettings.value?.site_name_ar || siteSettings.value?.site_name_en || 'KHUTUT ALRIMAL'
  const phone = siteSettings.value?.contact_phone || ''
  const email = siteSettings.value?.contact_email || ''
  const addressText =
    (props.language === 'ar' ? siteSettings.value?.address_ar : siteSettings.value?.address_en) ||
    'Tripoli, Libya'
  const logoUrl = siteSettings.value?.logo ? resolveImage(siteSettings.value, 'logo') : `${SITE_URL}/vite.svg`

  const clean = (obj) => {
    Object.keys(obj).forEach((key) => {
      const value = obj[key]
      if (value === '' || value === null || value === undefined) {
        delete obj[key]
      } else if (typeof value === 'object' && !Array.isArray(value)) {
        clean(value)
        if (!Object.keys(value).length) {
          delete obj[key]
        }
      }
    })
    return obj
  }

  const services = [
    '??? ????',
    '????? ????',
    '??? ???? ????',
    '??? ????',
    '??? ??????',
    '??? ????',
    '????? ?????? 6x4',
    '????? ??? ??????',
    '????? ?????',
  ]

  const organization = clean({
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name,
    url: SITE_URL,
    logo: logoUrl,
    telephone: phone,
    email,
    areaServed: 'Libya',
    knowsAbout: services,
  })

  const localBusiness = clean({
    '@context': 'https://schema.org',
    '@type': 'LocalBusiness',
    name,
    url: SITE_URL,
    image: logoUrl,
    telephone: phone,
    email,
    address: {
      '@type': 'PostalAddress',
      addressLocality: 'Tripoli',
      addressCountry: 'LY',
      streetAddress: addressText,
    },
    areaServed: 'Tripoli, Libya',
    serviceType: services,
  })

  const upsert = (id, data) => {
    let script = document.getElementById(id)
    if (!script) {
      script = document.createElement('script')
      script.type = 'application/ld+json'
      script.id = id
      document.head.appendChild(script)
    }
    script.textContent = JSON.stringify(data)
  }

  try {
    upsert('org-schema', organization)
    upsert('local-schema', localBusiness)
  } catch (error) {
    // Prevent structured data failures from breaking the UI.
  }
}

const fetchSiteSettings = async () => {
  settingsLoading.value = true
  try {
    const { data } = await axios.get(`${API_BASE}/api/site-settings/`)
    const setting = Array.isArray(data) ? data[0] : data
    siteSettings.value = setting || null
    updateStructuredData()
    return setting
  } catch (error) {
    siteSettings.value = null
    return null
  } finally {
    settingsLoading.value = false
  }
}

const syncPublicData = async (force = false) => {
  if (!API_ENABLED) return
  try {
    const setting = await fetchSiteSettings()
    const token = setting?.refresh_token || ''
    if (force || (token && token !== refreshToken.value)) {
      refreshToken.value = token
      await Promise.all([fetchVehicles(), fetchStatistics()])
    }
  } catch (error) {
    // Never allow sync errors to break mounting.
  }
}

onMounted(() => {
  try {
    setDisplayValues()

    if (ENABLE_ANIMATION && typeof window !== 'undefined' && 'IntersectionObserver' in window) {
      observer = new IntersectionObserver(
        (entries) => {
          if (entries[0].isIntersecting && !hasAnimated.value) {
            hasAnimated.value = true
            animateStats()
          }
        },
        { threshold: 0.35 }
      )

      if (statsRef.value) {
        observer.observe(statsRef.value)
      }
    } else if (ENABLE_ANIMATION) {
      hasAnimated.value = true
      animateStats()
    }

    if (API_ENABLED) {
      syncPublicData(true)
      if (typeof window !== 'undefined') {
        refreshInterval = setInterval(() => syncPublicData(false), 5000)
      }
    } else {
      vehiclesLoading.value = false
      statsLoading.value = false
      settingsLoading.value = false
    }
  } catch (error) {
    // Never allow runtime errors to block rendering.
  }
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<template>
  <section id="home" class="relative overflow-hidden">
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(212,175,55,0.18),_transparent_60%)]"></div>
    <div class="absolute -right-32 top-12 h-72 w-72 rounded-full bg-[#d4af37]/20 blur-3xl dark:opacity-0"></div>
    <div class="absolute -left-20 bottom-10 h-60 w-60 rounded-full bg-[#111827]/20 blur-3xl dark:bg-[#f3e2a2]/10"></div>
    <div class="stardust-layer"></div>

    <div class="relative mx-auto w-full max-w-7xl px-4 pb-16 pt-16 sm:px-6 lg:px-8 lg:pt-24">
      <div class="grid items-center gap-10 lg:grid-cols-[1.05fr_0.95fr]">
        <div class="space-y-6" :class="isRtl ? 'text-right' : ''">
          <div class="inline-flex items-center gap-3 rounded-full border border-[#d4af37]/40 bg-[#f3e2a2]/30 px-4 py-2 text-xs uppercase tracking-[0.35em] text-[#7a5a1f] dark:border-transparent dark:bg-slate-900/60 dark:text-slate-200">
            {{ heroBadge }}
          </div>
          <h1
            class="hero-slide break-words text-2xl font-semibold leading-tight text-slate-900 dark:text-white sm:text-3xl lg:text-5xl"
            :class="isRtl ? 'hero-slide-rtl' : 'hero-slide-ltr'"
          >
            {{ heroTitle }}
          </h1>
          <h2
            class="hero-slide break-words text-base font-semibold text-slate-700 dark:text-slate-300 sm:text-lg"
            :class="isRtl ? 'hero-slide-rtl' : 'hero-slide-ltr'"
          >
            {{ t('heroSeoSubheading') }}
          </h2>
          <p class="text-sm text-slate-600 dark:text-slate-300 sm:text-base">
            {{ heroDesc }}
          </p>
          <div class="flex flex-wrap items-center gap-3" :class="isRtl ? 'justify-end' : ''">
            <button class="rounded-full bg-slate-900 px-5 py-2 text-xs uppercase tracking-[0.35em] text-white transition hover:bg-slate-800 dark:bg-white dark:text-slate-900">
              {{ t('ctaProposal') }}
            </button>
            <button class="rounded-full border border-slate-300/70 px-5 py-2 text-xs uppercase tracking-[0.35em] text-slate-700 transition hover:border-[#d4af37] dark:border-white/20 dark:text-slate-200 dark:hover:border-slate-400">
              {{ t('ctaPortfolio') }}
            </button>
          </div>
          <div class="flex flex-wrap gap-6 text-xs uppercase tracking-[0.25em] text-slate-500 dark:text-slate-400" :class="isRtl ? 'justify-end' : ''">
            <div class="flex items-center gap-2" :class="isRtl ? 'flex-row-reverse' : ''">
              <span class="h-2 w-2 rounded-full bg-[#d4af37] dark:bg-slate-500"></span>
              {{ t('highlightIso') }}
            </div>
            <div class="flex items-center gap-2" :class="isRtl ? 'flex-row-reverse' : ''">
              <span class="h-2 w-2 rounded-full bg-[#d4af37] dark:bg-slate-500"></span>
              {{ t('highlightOps') }}
            </div>
            <div class="flex items-center gap-2" :class="isRtl ? 'flex-row-reverse' : ''">
              <span class="h-2 w-2 rounded-full bg-[#d4af37] dark:bg-slate-500"></span>
              {{ t('highlightCoverage') }}
            </div>
          </div>
        </div>

        <div class="relative">
          <div class="relative overflow-hidden rounded-3xl border border-slate-200/70 bg-gradient-to-br from-slate-900 via-[#1d2b40] to-slate-900 p-6 shadow-2xl shadow-slate-900/30">
            <div class="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(212,175,55,0.25),_transparent_60%)]"></div>
            <div class="relative z-10 flex flex-col gap-4">
              <div class="aspect-[4/3] w-full overflow-hidden rounded-2xl border border-white/10 bg-[linear-gradient(120deg,_rgba(243,226,162,0.22),_rgba(15,23,42,0.85))]">
                <img
                  v-if="heroImage"
                  :src="heroImage"
                  :alt="language === 'ar' ? '????? ??? ????' : t('heroCardTitle')"
                  width="800"
                  height="600"
                  loading="eager"
                  fetchpriority="high"
                  class="h-full w-full object-cover"
                />
                <div v-else class="flex h-full w-full items-center justify-center text-center text-sm uppercase tracking-[0.4em] text-[#f3e2a2]">
                  {{ t('heroCardTitle') }}
                </div>
              </div>
              <div class="grid gap-3 sm:grid-cols-2">
                <div class="rounded-2xl border border-white/10 bg-white/5 p-4" :class="isRtl ? 'text-right' : ''">
                  <p class="text-xs uppercase tracking-[0.25em] text-slate-300">{{ t('payloadLabel') }}</p>
                  <p class="mt-2 text-2xl font-semibold text-white">{{ t('payloadValue') }}</p>
                </div>
                <div class="rounded-2xl border border-white/10 bg-white/5 p-4" :class="isRtl ? 'text-right' : ''">
                  <p class="text-xs uppercase tracking-[0.25em] text-slate-300">{{ t('fleetRangeLabel') }}</p>
                  <p class="mt-2 text-2xl font-semibold text-white">{{ t('fleetRangeValue') }}</p>
                </div>
              </div>

            </div>
          </div>
          <div class="absolute -bottom-6 -left-6 hidden h-24 w-24 rounded-2xl border border-[#d4af37]/50 bg-[#f3e2a2]/30 sm:block dark:opacity-0"></div>
          <div class="absolute -right-6 -top-6 hidden h-20 w-20 rounded-full border border-white/20 bg-white/10 sm:block"></div>
        </div>
      </div>
    </div>
  </section>

  <section class="border-y border-slate-200/60 bg-white/70 py-4 dark:border-white/10 dark:bg-slate-900/70">
    <div class="overflow-hidden">
      <div class="marquee-track">
        <span class="marquee-item">{{ t('marqueeText') }}</span>
        <span class="marquee-item">{{ t('marqueeText') }}</span>
      </div>
    </div>
  </section>

  <section ref="statsRef" class="relative py-16 lg:py-20" id="services">
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(15,23,42,0.08),_transparent_60%)] dark:bg-[radial-gradient(circle_at_top,_rgba(212,175,55,0.1),_transparent_60%)]"></div>
    <div class="relative mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col gap-3" :class="isRtl ? 'text-right' : ''">
        <p class="text-xs uppercase tracking-[0.35em] text-[#8a6a2f] dark:text-slate-300">{{ t('statsOverline') }}</p>
        <h2 class="text-2xl font-semibold text-slate-900 dark:text-white sm:text-3xl">{{ t('statsTitle') }}</h2>
        <p class="text-sm text-slate-500 dark:text-slate-300">{{ t('statsSubtitle') }}</p>
      </div>

      <div class="mt-10 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <div
          v-for="(stat, index) in displayStats"
          :key="`${stat.label}-${index}`"
          class="rounded-3xl border border-slate-200/70 bg-white/90 p-5 shadow-lg shadow-slate-900/5 backdrop-blur dark:border-white/10 dark:bg-slate-900/70"
        >
          <p class="text-2xl font-semibold text-slate-900 dark:text-white sm:text-3xl">
            {{ formatStat(index) }}
          </p>
          <p class="mt-2 text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-300">{{ stat.label }}</p>
          <p v-if="stat.caption" class="mt-3 text-xs text-slate-500 dark:text-slate-400">{{ stat.caption }}</p>
        </div>
      </div>
    </div>
  </section>

  <section id="projects" class="py-16 lg:py-20">
    <div class="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
        <div class="rounded-3xl border border-slate-200/70 bg-white/90 p-6 shadow-xl shadow-slate-900/5 backdrop-blur dark:border-white/10 dark:bg-slate-900/70">
          <p class="text-xs uppercase tracking-[0.35em] text-[#8a6a2f] dark:text-slate-300">{{ t('featuredOverline') }}</p>
          <h3 class="mt-3 text-lg font-semibold text-slate-900 dark:text-white sm:text-2xl">{{ t('featuredTitle') }}</h3>
          <p class="mt-3 text-sm text-slate-500 dark:text-slate-300 sm:text-base">
            {{ t('featuredDesc') }}
          </p>
          <div class="mt-6 grid gap-4 sm:grid-cols-2">
            <div class="rounded-2xl border border-slate-200/70 bg-white/70 p-4 dark:border-white/10 dark:bg-slate-900/60" :class="isRtl ? 'text-right' : ''">
              <p class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-300">{{ t('feature1Title') }}</p>
              <p class="mt-2 text-sm font-semibold text-slate-900 dark:text-white">{{ t('feature1Desc') }}</p>
            </div>
            <div class="rounded-2xl border border-slate-200/70 bg-white/70 p-4 dark:border-white/10 dark:bg-slate-900/60" :class="isRtl ? 'text-right' : ''">
              <p class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-300">{{ t('feature2Title') }}</p>
              <p class="mt-2 text-sm font-semibold text-slate-900 dark:text-white">{{ t('feature2Desc') }}</p>
            </div>
            <div class="rounded-2xl border border-slate-200/70 bg-white/70 p-4 dark:border-white/10 dark:bg-slate-900/60" :class="isRtl ? 'text-right' : ''">
              <p class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-300">{{ t('feature3Title') }}</p>
              <p class="mt-2 text-sm font-semibold text-slate-900 dark:text-white">{{ t('feature3Desc') }}</p>
            </div>
            <div class="rounded-2xl border border-slate-200/70 bg-white/70 p-4 dark:border-white/10 dark:bg-slate-900/60" :class="isRtl ? 'text-right' : ''">
              <p class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-300">{{ t('feature4Title') }}</p>
              <p class="mt-2 text-sm font-semibold text-slate-900 dark:text-white">{{ t('feature4Desc') }}</p>
            </div>
          </div>
        </div>

        <div class="rounded-3xl border border-slate-200/70 bg-gradient-to-br from-[#111827] via-[#1f2a44] to-[#111827] p-6 text-white shadow-xl shadow-slate-900/25">
          <p class="text-xs uppercase tracking-[0.35em] text-[#f3e2a2]">{{ t('liveFleetOverline') }}</p>
          <h3 class="mt-3 text-lg font-semibold sm:text-2xl">{{ t('liveFleetTitle') }}</h3>
          <p class="mt-2 text-sm text-slate-200 sm:text-base">{{ t('liveFleetDesc') }}</p>
          <div class="mt-6 space-y-3">
            <div class="rounded-2xl border border-white/10 bg-white/5 p-4" :class="isRtl ? 'text-right' : ''">
              <p class="text-xs uppercase tracking-[0.3em] text-slate-300">{{ t('liveFleetOnRouteLabel') }}</p>
              <p class="mt-2 text-2xl font-semibold">{{ t('liveFleetOnRouteValue') }}</p>
            </div>
            <div class="rounded-2xl border border-white/10 bg-white/5 p-4" :class="isRtl ? 'text-right' : ''">
              <p class="text-xs uppercase tracking-[0.3em] text-slate-300">{{ t('liveFleetStagedLabel') }}</p>
              <p class="mt-2 text-2xl font-semibold">{{ t('liveFleetStagedValue') }}</p>
            </div>
            <div class="rounded-2xl border border-white/10 bg-white/5 p-4" :class="isRtl ? 'text-right' : ''">
              <p class="text-xs uppercase tracking-[0.3em] text-slate-300">{{ t('liveFleetCompletedLabel') }}</p>
              <p class="mt-2 text-2xl font-semibold">{{ t('liveFleetCompletedValue') }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section id="about" class="py-16 lg:py-20">
    <div class="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="rounded-3xl border border-slate-200/70 bg-white/90 p-8 shadow-xl shadow-slate-900/5 backdrop-blur dark:border-white/10 dark:bg-slate-900/70">
        <div class="grid gap-8 lg:grid-cols-2">
          <div :class="isRtl ? 'text-right' : ''">
            <p class="text-xs uppercase tracking-[0.35em] text-[#8a6a2f] dark:text-slate-300">{{ t('aboutOverline') }}</p>
            <h3 class="mt-3 text-xl font-semibold text-slate-900 dark:text-white sm:text-3xl">{{ t('aboutTitle') }}</h3>
            <p class="mt-3 text-sm text-slate-500 dark:text-slate-300 sm:text-base">
              {{ t('aboutDesc') }}
            </p>
          </div>
          <div class="grid gap-4 sm:grid-cols-2">
            <div class="rounded-2xl border border-slate-200/70 bg-white/70 p-4 dark:border-white/10 dark:bg-slate-900/60" :class="isRtl ? 'text-right' : ''">
              <p class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-300">{{ t('about1Title') }}</p>
              <p class="mt-2 text-sm font-semibold text-slate-900 dark:text-white">{{ t('about1Desc') }}</p>
            </div>
            <div class="rounded-2xl border border-slate-200/70 bg-white/70 p-4 dark:border-white/10 dark:bg-slate-900/60" :class="isRtl ? 'text-right' : ''">
              <p class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-300">{{ t('about2Title') }}</p>
              <p class="mt-2 text-sm font-semibold text-slate-900 dark:text-white">{{ t('about2Desc') }}</p>
            </div>
            <div class="rounded-2xl border border-slate-200/70 bg-white/70 p-4 dark:border-white/10 dark:bg-slate-900/60" :class="isRtl ? 'text-right' : ''">
              <p class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-300">{{ t('about3Title') }}</p>
              <p class="mt-2 text-sm font-semibold text-slate-900 dark:text-white">{{ t('about3Desc') }}</p>
            </div>
            <div class="rounded-2xl border border-slate-200/70 bg-white/70 p-4 dark:border-white/10 dark:bg-slate-900/60" :class="isRtl ? 'text-right' : ''">
              <p class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-300">{{ t('about4Title') }}</p>
              <p class="mt-2 text-sm font-semibold text-slate-900 dark:text-white">{{ t('about4Desc') }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section id="contact" class="py-16 lg:py-20">
    <div class="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="rounded-3xl border border-slate-200/70 bg-gradient-to-r from-[#f3e2a2]/40 to-white/90 p-8 shadow-xl shadow-slate-900/5 backdrop-blur dark:border-white/10 dark:from-[#1b2333] dark:to-[#111827]">
        <div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between" :class="isRtl ? 'lg:flex-row-reverse' : ''">
          <div :class="isRtl ? 'text-right' : ''">
            <p class="text-xs uppercase tracking-[0.35em] text-[#8a6a2f] dark:text-slate-300">{{ t('contactOverline') }}</p>
            <h3 class="mt-2 text-xl font-semibold text-slate-900 dark:text-white sm:text-3xl">{{ t('contactTitle') }}</h3>
            <p class="mt-3 text-sm text-slate-600 dark:text-slate-300 sm:text-base">{{ t('contactDesc') }}</p>
            <div
              v-if="contactPhone || contactEmail || contactNumbers.length"
              class="mt-4 space-y-1 text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-300"
            >
              <p v-if="contactPhone">{{ contactPhone }}</p>
              <p v-if="contactEmail">{{ contactEmail }}</p>
              <p v-for="number in contactNumbers" :key="number">{{ number }}</p>
            </div>
          </div>
          <a
            href="https://wa.me/218915320462"
            target="_blank"
            rel="noopener"
            class="rounded-full bg-slate-900 px-6 py-3 text-xs uppercase tracking-[0.35em] text-white transition hover:bg-slate-800 dark:bg-white dark:text-slate-900"
          >
            {{ t('contactCta') }}
          </a>
        </div>
      </div>
    </div>
  </section>
</template>
