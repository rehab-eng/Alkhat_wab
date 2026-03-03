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
  document.documentElement.classList.toggle('dark', value)
}

const applyLanguage = () => {
  document.documentElement.setAttribute('dir', isRtl.value ? 'rtl' : 'ltr')
  document.documentElement.setAttribute('lang', language.value)
}

onMounted(() => {
  const savedTheme = localStorage.getItem('khututs-theme')
  if (savedTheme === 'light' || savedTheme === 'dark') {
    isDark.value = savedTheme === 'dark'
  } else if (window.matchMedia) {
    isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  applyTheme(isDark.value)

  const savedLang = localStorage.getItem('khututs-lang')
  if (savedLang === 'en' || savedLang === 'ar') {
    language.value = savedLang
  }
  applyLanguage()
})

watch(isDark, (value) => {
  applyTheme(value)
  localStorage.setItem('khututs-theme', value ? 'dark' : 'light')
})

watch(language, (value) => {
  applyLanguage()
  localStorage.setItem('khututs-lang', value)
})

const toggleTheme = () => {
  isDark.value = !isDark.value
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
        : 'min-h-screen bg-[#f7f2e8] text-slate-900 transition-colors duration-300 dark:bg-[#0b121c] dark:text-slate-100'
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
      class="border-t border-slate-200/60 bg-white/70 py-6 text-center text-xs uppercase tracking-[0.3em] text-slate-500 dark:border-white/10 dark:bg-slate-950/60 dark:text-slate-400"
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
  background-color: #0b121c;
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

* {
  box-sizing: border-box;
}
</style>
