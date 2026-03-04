<script setup>
import { computed, ref } from 'vue'

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

const isOpen = ref(false)

const navItems = computed(() => {
  props.language
  return [
    {
      label: props.t('sidebarNavOverview'),
      sub: props.t('sidebarNavOverviewSub'),
      icon: 'M4 4h6v6H4V4Zm0 10h6v6H4v-6Zm10-10h6v10h-6V4Zm0 12h6v4h-6v-4Z',
    },
    {
      label: props.t('sidebarNavProjects'),
      sub: props.t('sidebarNavProjectsSub'),
      icon: 'M4 7h16M4 12h16M4 17h10',
    },
    {
      label: props.t('sidebarNavFleet'),
      sub: props.t('sidebarNavFleetSub'),
      icon: 'M3 14l2-5h14l2 5M7 14v4M17 14v4M7 18h10',
    },
    {
      label: props.t('sidebarNavInvoices'),
      sub: props.t('sidebarNavInvoicesSub'),
      icon: 'M6 3h12v18l-3-2-3 2-3-2-3 2V3Z',
    },
    {
      label: props.t('sidebarNavReports'),
      sub: props.t('sidebarNavReportsSub'),
      icon: 'M4 19h16M6 16V8M12 16V5M18 16v-7',
    },
    {
      label: props.t('sidebarNavSettings'),
      sub: props.t('sidebarNavSettingsSub'),
      icon: 'M12 8.5a3.5 3.5 0 1 0 0 7a3.5 3.5 0 0 0 0-7ZM4 12h2M18 12h2M6.5 6.5l1.4 1.4M16.1 16.1l1.4 1.4M6.5 17.5l1.4-1.4M16.1 7.9l1.4-1.4',
    },
  ]
})
</script>

<template>
  <div class="relative">
    <button
      type="button"
      class="fixed top-24 z-40 flex h-10 w-10 items-center justify-center rounded-full border border-slate-200/70 bg-white/90 text-slate-700 shadow-lg shadow-slate-900/10 backdrop-blur transition hover:border-[#d4af37] dark:border-white/10 dark:bg-slate-900/70 dark:text-slate-200 md:hidden"
      :class="isRtl ? 'right-4' : 'left-4'"
      @click="isOpen = true"
    >
      <span class="sr-only">Open sidebar</span>
      <div class="flex flex-col gap-1">
        <span class="h-0.5 w-4 rounded-full bg-current"></span>
        <span class="h-0.5 w-4 rounded-full bg-current"></span>
        <span class="h-0.5 w-4 rounded-full bg-current"></span>
      </div>
    </button>

    <div v-if="isOpen" class="fixed inset-0 z-40 bg-slate-950/60 backdrop-blur-sm md:hidden" @click="isOpen = false"></div>

    <aside
      class="fixed inset-y-0 z-50 w-72 bg-white/95 p-6 shadow-2xl shadow-slate-900/20 backdrop-blur transition-transform duration-300 dark:bg-slate-900/90 md:static md:translate-x-0 md:rounded-3xl md:border md:shadow-xl"
      :class="[
        isRtl ? 'right-0 border-l border-slate-200/70 dark:border-white/10' : 'left-0 border-r border-slate-200/70 dark:border-white/10',
        isOpen ? 'translate-x-0' : isRtl ? 'translate-x-full md:translate-x-0' : '-translate-x-full md:translate-x-0',
      ]"
    >
      <div class="flex items-center justify-between" :class="isRtl ? 'flex-row-reverse text-right' : ''">
        <div>
          <p class="text-xs uppercase tracking-[0.3em] text-[#bfa76a]">{{ t('dashboardOverline') }}</p>
          <h3 class="text-lg font-semibold text-slate-900 dark:text-white">{{ t('sidebarTitle') }}</h3>
        </div>
        <button
          type="button"
          class="rounded-full border border-slate-200/70 p-2 text-slate-600 transition hover:border-[#d4af37] dark:border-white/10 dark:text-slate-300 md:hidden"
          @click="isOpen = false"
        >
          <span class="sr-only">Close sidebar</span>
          <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M6 6l12 12M18 6l-12 12"></path>
          </svg>
        </button>
      </div>

      <div class="mt-6 space-y-3">
        <div class="rounded-2xl border border-[#d4af37]/20 bg-gradient-to-r from-[#f3e2a2]/30 to-transparent p-4" :class="isRtl ? 'text-right' : ''">
          <p class="text-xs uppercase tracking-[0.3em] text-[#bfa76a]">{{ t('sidebarPrimaryOverline') }}</p>
          <p class="mt-2 text-sm font-semibold text-slate-900 dark:text-white">{{ t('sidebarPrimaryName') }}</p>
          <p class="text-xs text-slate-500 dark:text-slate-400">{{ t('sidebarPrimaryScore') }}</p>
        </div>

        <nav class="space-y-2">
          <a
            v-for="item in navItems"
            :key="item.label"
            href="#"
            class="group flex items-start gap-3 rounded-2xl border border-transparent px-3 py-3 transition hover:border-[#d4af37]/40 hover:bg-[#f3e2a2]/20 dark:hover:bg-white/5"
            :class="isRtl ? 'flex-row-reverse text-right' : ''"
          >
            <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-[#f3e2a2]/40 text-[#bfa76a] transition group-hover:bg-[#d4af37] group-hover:text-slate-900">
              <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path :d="item.icon"></path>
              </svg>
            </span>
            <span class="flex-1">
              <span class="block text-sm font-semibold text-slate-900 dark:text-white">{{ item.label }}</span>
              <span class="block text-xs text-slate-500 dark:text-slate-400">{{ item.sub }}</span>
            </span>
          </a>
        </nav>
      </div>

      <div class="mt-8 rounded-2xl border border-slate-200/70 bg-white/80 p-4 dark:border-white/10 dark:bg-slate-900/60" :class="isRtl ? 'text-right' : ''">
        <p class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-300">{{ t('sidebarSupportOverline') }}</p>
        <p class="mt-2 text-sm font-semibold text-slate-900 dark:text-white">{{ t('sidebarSupportTitle') }}</p>
        <p class="text-xs text-slate-500 dark:text-slate-400">{{ t('sidebarSupportPhone') }}</p>
        <button class="mt-3 w-full rounded-full border border-[#d4af37]/50 bg-[#d4af37]/10 px-3 py-2 text-xs uppercase tracking-[0.3em] text-[#bfa76a] transition hover:bg-[#d4af37]/20">
          {{ t('sidebarSupportCta') }}
        </button>
      </div>
    </aside>
  </div>
</template>
