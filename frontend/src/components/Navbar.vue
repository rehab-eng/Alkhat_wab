<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
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

const emit = defineEmits(['change-language'])

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
  <header class="sticky top-0 z-50 border-b border-slate-200/60 bg-white/80 backdrop-blur">
    <div class="mx-auto flex h-16 w-full max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
      <div class="flex items-center gap-3" :class="isRtl ? 'flex-row-reverse text-right' : ''">
        <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-[#f3e2a2] to-[#d4af37] text-sm font-semibold text-slate-900 shadow-lg shadow-[#d4af37]/30">
          KA
        </div>
        <div class="leading-tight">
          <p class="text-xs uppercase tracking-[0.3em] text-slate-500">{{ t('brandUpper') }}</p>
          <p class="text-sm font-semibold text-slate-900">{{ t('brandSub') }}</p>
        </div>
      </div>

      <nav class="hidden items-center gap-8 md:flex">
        <a
          v-for="link in links"
          :key="link.label"
          :href="link.href"
          class="text-xs uppercase tracking-[0.25em] text-slate-600 transition hover:text-slate-900"
        >
          {{ link.label }}
        </a>
      </nav>

      <div class="flex items-center gap-2">
        <div class="flex items-center rounded-full border border-slate-200/70 bg-white/70 p-1 text-xs uppercase tracking-[0.25em] text-slate-600 shadow-sm sm:hidden">
          <button
            type="button"
            class="rounded-full px-2 py-1 transition"
            :class="
              language === 'en'
                ? 'bg-[#d4af37] text-slate-900'
                : 'hover:text-slate-900'
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
                ? 'bg-[#d4af37] text-slate-900'
                : 'hover:text-slate-900'
            "
            @click="setLanguage('ar')"
          >
            AR
          </button>
        </div>
        <div class="hidden items-center rounded-full border border-slate-200/70 bg-white/70 p-1 text-xs uppercase tracking-[0.25em] text-slate-600 shadow-sm sm:flex">
          <button
            type="button"
            class="rounded-full px-3 py-1 transition"
            :class="
              language === 'en'
                ? 'bg-[#d4af37] text-slate-900'
                : 'hover:text-slate-900'
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
                ? 'bg-[#d4af37] text-slate-900'
                : 'hover:text-slate-900'
            "
            @click="setLanguage('ar')"
          >
            AR
          </button>
        </div>

        <button
          type="button"
          class="inline-flex h-10 w-10 items-center justify-center rounded-full border border-slate-200/70 bg-white/70 text-slate-700 shadow-sm transition hover:border-[#d4af37] hover:text-slate-900 md:hidden"
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
      class="border-t border-slate-200/60 bg-white/95 px-4 py-4 shadow-lg shadow-slate-900/5 backdrop-blur md:hidden"
    >
      <div class="flex flex-col gap-3">
        <div class="flex items-center justify-between rounded-xl border border-slate-200/60 bg-white/80 px-4 py-2 text-xs uppercase tracking-[0.25em] text-slate-700">
          <span>{{ t('languageLabel') }}</span>
          <div class="flex items-center gap-2">
            <button
              type="button"
              class="rounded-full px-2 py-1"
              :class="language === 'en' ? 'bg-[#d4af37] text-slate-900' : ''"
              @click="setLanguage('en')"
            >
              EN
            </button>
            <button
              type="button"
              class="rounded-full px-2 py-1"
              :class="language === 'ar' ? 'bg-[#d4af37] text-slate-900' : ''"
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
          class="rounded-xl border border-slate-200/60 bg-white/80 px-4 py-2 text-xs uppercase tracking-[0.25em] text-slate-700 transition hover:border-[#d4af37] hover:text-slate-900"
          @click="mobileOpen = false"
        >
          {{ link.label }}
        </a>
      </div>
    </div>
  </header>
</template>
