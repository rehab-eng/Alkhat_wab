<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue'
import { messages } from './i18n'

const language = ref('en')
const isRtl = computed(() => language.value === 'ar')
const route = useRoute()
const isDashboardRoute = computed(() => route.path.startsWith('/dashboard'))

const t = (key) => messages[language.value]?.[key] ?? key

const LANG_KEY = 'khututs-lang'

const applyLanguage = () => {
  try {
    if (typeof document === 'undefined') return
    document.documentElement.setAttribute('dir', isRtl.value ? 'rtl' : 'ltr')
    document.documentElement.setAttribute('lang', language.value)
  } catch (error) {
    // Avoid crashes on constrained browsers.
  }
}

onMounted(() => {
  try {
    if (typeof document !== 'undefined') {
      document.documentElement.classList.remove('dark')
      document.documentElement.style.colorScheme = 'light'
      document.documentElement.removeAttribute('data-theme')
      if (document.body && document.body.style) {
        document.body.style.backgroundColor = '#f7f2e8'
      }
    }
  } catch (error) {
    // Ignore DOM errors.
  }
  try {
    localStorage.removeItem('khututs-theme')
    localStorage.removeItem('khututs-theme-v2')
  } catch (error) {
    // Ignore storage errors.
  }
  try {
    const savedLang = localStorage.getItem(LANG_KEY)
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
    localStorage.setItem(LANG_KEY, value)
  } catch (error) {
    // Ignore storage errors.
  }
})

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
        : 'min-h-screen bg-[#f7f2e8] text-slate-900 transition-colors duration-300'
    "
  >
    <Navbar
      v-if="!isDashboardRoute"
      :language="language"
      :is-rtl="isRtl"
      :t="t"
      @change-language="setLanguage"
    />

    <main>
      <router-view v-slot="{ Component }">
        <component :is="Component" :t="t" :language="language" :is-rtl="isRtl" />
      </router-view>
    </main>

    <footer
      v-if="!isDashboardRoute"
      class="border-t border-slate-200/60 bg-white/70 py-6 text-center text-xs uppercase tracking-[0.3em] text-slate-500"
    >
      {{ t('footerText') }}
    </footer>
  </div>
</template>

<style>

:root {
  color-scheme: light;
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
  background-color: #f7f2e8;
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

* {
  box-sizing: border-box;
}
</style>
