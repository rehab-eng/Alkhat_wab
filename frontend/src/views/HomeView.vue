<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
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

const stats = ref([
  {
    key: 'years',
    labelKey: 'statYears',
    captionKey: 'statYearsCaption',
    value: 16,
    suffix: '+',
  },
  {
    key: 'projects',
    labelKey: 'statProjects',
    captionKey: 'statProjectsCaption',
    value: 240,
    suffix: '+',
  },
  {
    key: 'fleet',
    labelKey: 'statFleet',
    captionKey: 'statFleetCaption',
    value: 38,
    suffix: '+',
  },
  {
    key: 'safety',
    labelKey: 'statSafety',
    captionKey: 'statSafetyCaption',
    value: 98,
    suffix: '%',
  },
])

const statsRef = ref(null)
const displayValues = ref(stats.value.map(() => 0))
const hasAnimated = ref(false)
let observer

const animateStats = () => {
  stats.value.forEach((stat, index) => {
    const duration = 1400 + index * 180
    const start = performance.now()

    const step = (now) => {
      const progress = Math.min((now - start) / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      displayValues.value[index] = Math.floor(eased * stat.value)
      if (progress < 1) {
        requestAnimationFrame(step)
      } else {
        displayValues.value[index] = stat.value
      }
    }

    requestAnimationFrame(step)
  })
}

const formatStat = (index) => {
  const value = displayValues.value[index] ?? 0
  const suffix = stats.value[index].suffix
  return `${value}${suffix}`
}

const trucks = ref([])
const trucksLoading = ref(true)
const trucksError = ref(false)
const statsLoading = ref(true)

const resolveImage = (truck) => {
  if (!truck) return ''
  const rawUrl = truck.image_url || truck.image || ''
  if (!rawUrl) return ''
  if (rawUrl.startsWith('http')) return rawUrl
  return `${API_BASE}${rawUrl}`
}

const heroImage = computed(() => resolveImage(trucks.value[0]))

const fetchTrucks = async () => {
  trucksLoading.value = true
  trucksError.value = false
  try {
    const { data } = await axios.get(`${API_BASE}/api/trucks/`)
    trucks.value = Array.isArray(data) ? data : []
  } catch (error) {
    trucksError.value = true
  } finally {
    trucksLoading.value = false
  }
}

const fetchStats = async () => {
  statsLoading.value = true
  try {
    const { data } = await axios.get(`${API_BASE}/api/stats/`)
    if (Array.isArray(data) && data.length) {
      const statMap = new Map(data.map((item) => [item.key, item]))
      stats.value = stats.value.map((stat) => {
        const remote = statMap.get(stat.key)
        if (!remote) return stat
        return {
          ...stat,
          value: Number(remote.value) || stat.value,
          suffix: remote.suffix || stat.suffix,
        }
      })
      displayValues.value = stats.value.map(() => 0)
      hasAnimated.value = false
      if (statsRef.value && statsRef.value.getBoundingClientRect().top < window.innerHeight) {
        hasAnimated.value = true
        animateStats()
      }
    }
  } catch (error) {
    // Keep fallback values
  } finally {
    statsLoading.value = false
  }
}

onMounted(() => {
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

  fetchTrucks()
  fetchStats()
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
})
</script>

<template>
  <section id="home" class="relative overflow-hidden">
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(212,175,55,0.18),_transparent_60%)]"></div>
    <div class="absolute -right-32 top-12 h-72 w-72 rounded-full bg-[#d4af37]/20 blur-3xl"></div>
    <div class="absolute -left-20 bottom-10 h-60 w-60 rounded-full bg-[#0b121c]/20 blur-3xl dark:bg-[#f3e2a2]/10"></div>

    <div class="relative mx-auto w-full max-w-7xl px-4 pb-16 pt-16 sm:px-6 lg:px-8 lg:pt-24">
      <div class="grid items-center gap-10 lg:grid-cols-[1.05fr_0.95fr]">
        <div class="space-y-6" :class="isRtl ? 'text-right' : ''">
          <div class="inline-flex items-center gap-3 rounded-full border border-[#d4af37]/40 bg-[#f3e2a2]/30 px-4 py-2 text-xs uppercase tracking-[0.35em] text-[#8c774a]">
            {{ t('heroBadge') }}
          </div>
          <h1 class="text-4xl font-semibold leading-tight text-slate-900 dark:text-white lg:text-5xl">
            {{ t('heroTitle') }}
          </h1>
          <p class="text-base text-slate-600 dark:text-slate-300">
            {{ t('heroDesc') }}
          </p>
          <div class="flex flex-wrap items-center gap-3" :class="isRtl ? 'justify-end' : ''">
            <button class="rounded-full bg-slate-900 px-5 py-2 text-xs uppercase tracking-[0.35em] text-white transition hover:bg-slate-800 dark:bg-white dark:text-slate-900">
              {{ t('ctaProposal') }}
            </button>
            <button class="rounded-full border border-slate-300/70 px-5 py-2 text-xs uppercase tracking-[0.35em] text-slate-700 transition hover:border-[#d4af37] dark:border-white/20 dark:text-slate-200">
              {{ t('ctaPortfolio') }}
            </button>
          </div>
          <div class="flex flex-wrap gap-6 text-xs uppercase tracking-[0.25em] text-slate-500 dark:text-slate-400" :class="isRtl ? 'justify-end' : ''">
            <div class="flex items-center gap-2" :class="isRtl ? 'flex-row-reverse' : ''">
              <span class="h-2 w-2 rounded-full bg-[#d4af37]"></span>
              {{ t('highlightIso') }}
            </div>
            <div class="flex items-center gap-2" :class="isRtl ? 'flex-row-reverse' : ''">
              <span class="h-2 w-2 rounded-full bg-[#d4af37]"></span>
              {{ t('highlightOps') }}
            </div>
            <div class="flex items-center gap-2" :class="isRtl ? 'flex-row-reverse' : ''">
              <span class="h-2 w-2 rounded-full bg-[#d4af37]"></span>
              {{ t('highlightCoverage') }}
            </div>
          </div>
        </div>

        <div class="relative">
          <div class="relative overflow-hidden rounded-3xl border border-slate-200/70 bg-gradient-to-br from-slate-900 via-[#1d2b40] to-slate-900 p-6 shadow-2xl shadow-slate-900/30">
            <div class="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(212,175,55,0.25),_transparent_60%)]"></div>
            <div class="relative z-10 flex flex-col gap-4">
              <div class="aspect-[4/3] w-full overflow-hidden rounded-2xl border border-white/10 bg-[linear-gradient(120deg,_rgba(243,226,162,0.22),_rgba(15,23,42,0.85))]">
                <img v-if="heroImage" :src="heroImage" :alt="t('heroCardTitle')" class="h-full w-full object-cover" />
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

              <div class="rounded-2xl border border-white/10 bg-white/5 p-4" :class="isRtl ? 'text-right' : ''">
                <div class="flex items-start justify-between gap-4" :class="isRtl ? 'flex-row-reverse' : ''">
                  <div>
                    <p class="text-xs uppercase tracking-[0.3em] text-slate-300">{{ t('fleetGalleryTitle') }}</p>
                    <p class="mt-2 text-sm text-slate-200">{{ t('fleetGallerySubtitle') }}</p>
                  </div>
                  <span class="rounded-full border border-white/10 px-3 py-1 text-xs uppercase tracking-[0.3em] text-slate-300">
                    {{ trucks.length }}
                  </span>
                </div>

                <div class="mt-4 flex gap-3 overflow-x-auto pb-2">
                  <div
                    v-if="trucksLoading"
                    class="min-w-[200px] rounded-2xl border border-white/10 bg-white/5 p-4 text-xs uppercase tracking-[0.3em] text-slate-300"
                  >
                    {{ t('trucksLoading') }}
                  </div>
                  <div
                    v-else-if="trucksError"
                    class="min-w-[200px] rounded-2xl border border-white/10 bg-white/5 p-4 text-xs uppercase tracking-[0.3em] text-amber-200"
                  >
                    {{ t('trucksError') }}
                  </div>
                  <div
                    v-else-if="!trucks.length"
                    class="min-w-[200px] rounded-2xl border border-white/10 bg-white/5 p-4 text-xs uppercase tracking-[0.3em] text-slate-300"
                  >
                    {{ t('trucksEmpty') }}
                  </div>
                  <div
                    v-for="truck in trucks"
                    :key="truck.id"
                    class="min-w-[220px] overflow-hidden rounded-2xl border border-white/10 bg-white/5"
                  >
                    <div class="aspect-[4/3] w-full overflow-hidden">
                      <img
                        v-if="resolveImage(truck)"
                        :src="resolveImage(truck)"
                        :alt="truck.title"
                        class="h-full w-full object-cover"
                      />
                      <div v-else class="flex h-full items-center justify-center text-xs uppercase tracking-[0.3em] text-slate-300">
                        {{ t('heroCardTitle') }}
                      </div>
                    </div>
                    <div class="p-3" :class="isRtl ? 'text-right' : ''">
                      <p class="text-xs uppercase tracking-[0.25em] text-slate-200">{{ truck.title }}</p>
                      <p class="mt-2 text-xs text-slate-300">{{ truck.description }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="absolute -bottom-6 -left-6 hidden h-24 w-24 rounded-2xl border border-[#d4af37]/50 bg-[#f3e2a2]/30 sm:block"></div>
          <div class="absolute -right-6 -top-6 hidden h-20 w-20 rounded-full border border-white/20 bg-white/10 sm:block"></div>
        </div>
      </div>
    </div>
  </section>

  <section class="border-y border-slate-200/60 bg-white/70 py-4 dark:border-white/10 dark:bg-slate-950/60">
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
        <p class="text-xs uppercase tracking-[0.35em] text-[#bfa76a]">{{ t('statsOverline') }}</p>
        <h2 class="text-3xl font-semibold text-slate-900 dark:text-white">{{ t('statsTitle') }}</h2>
        <p class="text-sm text-slate-500 dark:text-slate-300">{{ t('statsSubtitle') }}</p>
      </div>

      <div class="mt-10 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <div
          v-for="(stat, index) in stats"
          :key="stat.labelKey"
          class="rounded-3xl border border-slate-200/70 bg-white/90 p-5 shadow-lg shadow-slate-900/5 backdrop-blur dark:border-white/10 dark:bg-slate-900/70"
        >
          <p class="text-3xl font-semibold text-slate-900 dark:text-white">
            {{ formatStat(index) }}
          </p>
          <p class="mt-2 text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-300">{{ t(stat.labelKey) }}</p>
          <p class="mt-3 text-xs text-slate-500 dark:text-slate-400">{{ t(stat.captionKey) }}</p>
        </div>
      </div>
    </div>
  </section>

  <section id="projects" class="py-16 lg:py-20">
    <div class="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
        <div class="rounded-3xl border border-slate-200/70 bg-white/90 p-6 shadow-xl shadow-slate-900/5 backdrop-blur dark:border-white/10 dark:bg-slate-900/70">
          <p class="text-xs uppercase tracking-[0.35em] text-[#bfa76a]">{{ t('featuredOverline') }}</p>
          <h3 class="mt-3 text-2xl font-semibold text-slate-900 dark:text-white">{{ t('featuredTitle') }}</h3>
          <p class="mt-3 text-sm text-slate-500 dark:text-slate-300">
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

        <div class="rounded-3xl border border-slate-200/70 bg-gradient-to-br from-[#0b121c] via-[#182233] to-[#0b121c] p-6 text-white shadow-xl shadow-slate-900/25">
          <p class="text-xs uppercase tracking-[0.35em] text-[#f3e2a2]">{{ t('liveFleetOverline') }}</p>
          <h3 class="mt-3 text-2xl font-semibold">{{ t('liveFleetTitle') }}</h3>
          <p class="mt-2 text-sm text-slate-200">{{ t('liveFleetDesc') }}</p>
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
            <p class="text-xs uppercase tracking-[0.35em] text-[#bfa76a]">{{ t('aboutOverline') }}</p>
            <h3 class="mt-3 text-3xl font-semibold text-slate-900 dark:text-white">{{ t('aboutTitle') }}</h3>
            <p class="mt-3 text-sm text-slate-500 dark:text-slate-300">
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
      <div class="rounded-3xl border border-slate-200/70 bg-gradient-to-r from-[#f3e2a2]/40 to-white/90 p-8 shadow-xl shadow-slate-900/5 backdrop-blur dark:border-white/10 dark:from-[#1b2333] dark:to-[#0b121c]">
        <div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between" :class="isRtl ? 'lg:flex-row-reverse' : ''">
          <div :class="isRtl ? 'text-right' : ''">
            <p class="text-xs uppercase tracking-[0.35em] text-[#bfa76a]">{{ t('contactOverline') }}</p>
            <h3 class="mt-2 text-3xl font-semibold text-slate-900 dark:text-white">{{ t('contactTitle') }}</h3>
            <p class="mt-3 text-sm text-slate-600 dark:text-slate-300">{{ t('contactDesc') }}</p>
          </div>
          <button class="rounded-full bg-slate-900 px-6 py-3 text-xs uppercase tracking-[0.35em] text-white transition hover:bg-slate-800 dark:bg-white dark:text-slate-900">
            {{ t('contactCta') }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.marquee-track {
  display: inline-flex;
  align-items: center;
  gap: 3rem;
  white-space: nowrap;
  animation: marquee 18s linear infinite;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.4em;
  color: #8c774a;
}

.marquee-item {
  padding-right: 3rem;
}

@keyframes marquee {
  0% {
    transform: translateX(0%);
  }
  100% {
    transform: translateX(-50%);
  }
}

@media (max-width: 768px) {
  .marquee-track {
    font-size: 0.65rem;
    letter-spacing: 0.3em;
  }
}
</style>
