<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  isDark: {
    type: Boolean,
    default: false,
  },
  language: {
    type: String,
    default: 'en',
  },
  isRtl: {
    type: Boolean,
    default: false,
  },
  t: {
    type: Function,
    required: true,
  },
})

const emit = defineEmits(['toggle-theme', 'change-language'])

const mobileOpen = ref(false)

const links = computed(() => {
  props.language
  return [
    { label: props.t('navHome'), href: '/#home' },
    { label: props.t('navServices'), href: '/#services' },
    { label: props.t('navProjects'), href: '/#projects' },
    { label: props.t('navAbout'), href: '/#about' },
    { label: props.t('navContact'), href: '/#contact' },
  ]
})

const setLanguage = (value) => {
  emit('change-language', value)
}
</script>

<template>
  <header class="sticky top-0 z-50 border-b border-slate-200/60 bg-white/80 backdrop-blur dark:border-white/10 dark:bg-slate-900/80">
    <div class="mx-auto flex h-16 w-full max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
      <div class="flex items-center gap-3" :class="isRtl ? 'flex-row-reverse text-right' : ''">
        <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-[#f3e2a2] to-[#d4af37] text-sm font-semibold text-slate-900 shadow-lg shadow-[#d4af37]/30">
          KA
        </div>
        <div class="leading-tight">
          <p class="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-300">{{ t('brandUpper') }}</p>
          <p class="text-sm font-semibold text-slate-900 dark:text-white">{{ t('brandSub') }}</p>
        </div>
      </div>

      <nav class="hidden items-center gap-8 md:flex">
        <a
          v-for="link in links"
          :key="link.label"
          :href="link.href"
          class="text-xs uppercase tracking-[0.25em] text-slate-600 transition hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
        >
          {{ link.label }}
        </a>
      </nav>

      <div class="flex items-center gap-2">
        <div class="flex items-center rounded-full border border-slate-200/70 bg-white/70 p-1 text-xs uppercase tracking-[0.25em] text-slate-600 shadow-sm dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-200 sm:hidden">
          <button
            type="button"
            class="rounded-full px-2 py-1 transition"
            :class="
              language === 'en'
                ? 'bg-[#d4af37] text-slate-900 dark:bg-slate-700 dark:text-white'
                : 'hover:text-slate-900 dark:hover:text-white'
            "
            @click="setLanguage('en')"
          >
            EN
          </button>
          <button
            type="button"
            class="rounded-full px-2 py-1 transition"
            :class="
              language === 'ar'
                ? 'bg-[#d4af37] text-slate-900 dark:bg-slate-700 dark:text-white'
                : 'hover:text-slate-900 dark:hover:text-white'
            "
            @click="setLanguage('ar')"
          >
            AR
          </button>
        </div>
        <div class="hidden items-center rounded-full border border-slate-200/70 bg-white/70 p-1 text-xs uppercase tracking-[0.25em] text-slate-600 shadow-sm dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-200 sm:flex">
          <button
            type="button"
            class="rounded-full px-3 py-1 transition"
            :class="
              language === 'en'
                ? 'bg-[#d4af37] text-slate-900 dark:bg-slate-700 dark:text-white'
                : 'hover:text-slate-900 dark:hover:text-white'
            "
            @click="setLanguage('en')"
          >
            EN
          </button>
          <button
            type="button"
            class="rounded-full px-3 py-1 transition"
            :class="
              language === 'ar'
                ? 'bg-[#d4af37] text-slate-900 dark:bg-slate-700 dark:text-white'
                : 'hover:text-slate-900 dark:hover:text-white'
            "
            @click="setLanguage('ar')"
          >
            AR
          </button>
        </div>

        <button
          type="button"
          class="inline-flex h-10 w-10 items-center justify-center rounded-full border border-slate-200/70 bg-white/70 text-slate-700 shadow-sm transition hover:border-[#d4af37] hover:text-slate-900 dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-200 dark:hover:border-slate-400"
          @click="emit('toggle-theme')"
        >
          <span class="sr-only">{{ t('toggleTheme') }}</span>
          <svg v-if="props.isDark" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <circle cx="12" cy="12" r="4"></circle>
            <path d="M12 3v2M12 19v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M3 12h2M19 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"></path>
          </svg>
          <svg v-else class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"></path>
          </svg>
        </button>

        <button
          type="button"
          class="inline-flex h-10 w-10 items-center justify-center rounded-full border border-slate-200/70 bg-white/70 text-slate-700 shadow-sm transition hover:border-[#d4af37] hover:text-slate-900 dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-200 dark:hover:border-slate-400 md:hidden"
          @click="mobileOpen = !mobileOpen"
        >
          <span class="sr-only">{{ t('toggleMenu') }}</span>
          <div class="flex flex-col gap-1">
            <span class="h-0.5 w-4 rounded-full bg-current"></span>
            <span class="h-0.5 w-4 rounded-full bg-current"></span>
            <span class="h-0.5 w-4 rounded-full bg-current"></span>
          </div>
        </button>
      </div>
    </div>

    <div
      v-show="mobileOpen"
      class="border-t border-slate-200/60 bg-white/95 px-4 py-4 shadow-lg shadow-slate-900/5 backdrop-blur dark:border-white/10 dark:bg-slate-900/90 md:hidden"
    >
      <div class="flex flex-col gap-3">
        <div class="flex items-center justify-between rounded-xl border border-slate-200/60 bg-white/80 px-4 py-2 text-xs uppercase tracking-[0.25em] text-slate-700 dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-200">
          <span>{{ t('languageLabel') }}</span>
          <div class="flex items-center gap-2">
            <button
              type="button"
              class="rounded-full px-2 py-1"
              :class="language === 'en' ? 'bg-[#d4af37] text-slate-900 dark:bg-slate-700 dark:text-white' : ''"
              @click="setLanguage('en')"
            >
              EN
            </button>
            <button
              type="button"
              class="rounded-full px-2 py-1"
              :class="language === 'ar' ? 'bg-[#d4af37] text-slate-900 dark:bg-slate-700 dark:text-white' : ''"
              @click="setLanguage('ar')"
            >
              AR
            </button>
          </div>
        </div>

        <a
          v-for="link in links"
          :key="link.label"
          :href="link.href"
          class="rounded-xl border border-slate-200/60 bg-white/80 px-4 py-2 text-xs uppercase tracking-[0.25em] text-slate-700 transition hover:border-[#d4af37] hover:text-slate-900 dark:border-white/10 dark:bg-slate-900/60 dark:text-slate-200 dark:hover:border-slate-400"
          @click="mobileOpen = false"
        >
          {{ link.label }}
        </a>
      </div>
    </div>
  </header>
</template>
