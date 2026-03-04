<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue'
import { messages } from './i18n'

const isDark = ref(false)
const language = ref('en')
const isRtl = computed(() => language.value === 'ar')
const route = useRoute()
const isDashboardRoute = computed(() => route.path.startsWith('/dashboard'))

const t = (key) => messages[language.value]?.[key] ?? key

const applyTheme = (value) => {
  try {
    if (typeof document === 'undefined') return
    const root = document.documentElement
    if (!root || !root.classList) return
    if (value) {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
    root.style.colorScheme = value ? 'dark' : 'light'
  } catch (error) {
    // Never allow theme toggling to crash the app.
  }
}

const applyLanguage = () => {
  try {
    if (typeof document === 'undefined') return
    document.documentElement.setAttribute('dir', isRtl.value ? 'rtl' : 'ltr')
    document.documentElement.setAttribute('lang', language.value)
  } catch (error) {
    // Avoid crashes on constrained browsers.
  }
}

const setTheme = (value) => {
  try {
    isDark.value = Boolean(value)
    applyTheme(isDark.value)
    try {
      localStorage.setItem('khututs-theme', isDark.value ? 'dark' : 'light')
    } catch (error) {
      // Ignore storage errors.
    }
  } catch (error) {
    // Final guard against toggle crashes.
  }
}

onMounted(() => {
  let nextTheme = false
  try {
    const savedTheme = localStorage.getItem('khututs-theme')
    if (savedTheme === 'light' || savedTheme === 'dark') {
      nextTheme = savedTheme === 'dark'
    }
  } catch (error) {
    // Ignore storage errors (e.g., Safari private mode).
  }
  setTheme(nextTheme)

  try {
    const savedLang = localStorage.getItem('khututs-lang')
    if (savedLang === 'en' || savedLang === 'ar') {
      language.value = savedLang
    }
  } catch (error) {
    // Ignore storage errors.
  }
  applyLanguage()
})

watch(language, (value) => {
  applyLanguage()
  try {
    localStorage.setItem('khututs-lang', value)
  } catch (error) {
    // Ignore storage errors.
  }
})

const toggleTheme = () => {
  setTheme(!isDark.value)
}

const setLanguage = (value) => {
  if (value === 'en' || value === 'ar') {
    language.value = value
  }
}
</script>

<template>
  <div
    :dir="isRtl ? 'rtl' : 'ltr'"
    :class="
      isDashboardRoute
        ? 'min-h-screen bg-[#0b0f14] text-slate-100'
        : 'min-h-screen bg-[#f7f2e8] text-slate-900 transition-colors duration-300 dark:bg-[#111827] dark:text-slate-100'
    "
  >
    <Navbar
      v-if="!isDashboardRoute"
      :is-dark="isDark"
      :language="language"
      :is-rtl="isRtl"
      :t="t"
      @toggle-theme="toggleTheme"
      @change-language="setLanguage"
    />

    <main>
      <router-view v-slot="{ Component }">
        <component :is="Component" :t="t" :language="language" :is-rtl="isRtl" />
      </router-view>
    </main>

    <footer
      v-if="!isDashboardRoute"
      class="border-t border-slate-200/60 bg-white/70 py-6 text-center text-xs uppercase tracking-[0.3em] text-slate-500 dark:border-white/10 dark:bg-slate-900/80 dark:text-slate-300"
    >
      {{ t('footerText') }}
    </footer>
  </div>
</template>

<style>

:root {
  color-scheme: light dark;
}

html {
  font-family: 'Manrope', system-ui, -apple-system, sans-serif;
  scroll-behavior: smooth;
}

html[dir='rtl'] {
  font-family: 'Cairo', 'Manrope', system-ui, -apple-system, sans-serif;
}

body {
  margin: 0;
  min-height: 100%;
  background-color: #111827;
  color: inherit;
  display: block;
}

#app {
  max-width: none;
  margin: 0;
  padding: 0;
  text-align: left;
  min-height: 100vh;
}

html[dir='rtl'] #app {
  text-align: right;
}

h1,
h2,
h3,
h4 {
  font-family: 'Marcellus', serif;
}

html[dir='rtl'] h1,
html[dir='rtl'] h2,
html[dir='rtl'] h3,
html[dir='rtl'] h4 {
  font-family: 'Cairo', 'Manrope', system-ui, -apple-system, sans-serif;
}

html[dir='rtl'] [class*='tracking-'] {
  letter-spacing: 0 !important;
}

.dark .text-slate-300,
.dark .text-slate-400 {
  color: #f1f5f9 !important;
}

.dark .text-slate-500 {
  color: #e2e8f0 !important;
}

* {
  box-sizing: border-box;
}
</style>
