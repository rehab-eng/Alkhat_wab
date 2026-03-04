import { createApp } from 'vue'
import inlineCss from './style.css?inline'
import App from './App.vue'
import router from './router'

if (typeof document !== 'undefined') {
  const style = document.createElement('style')
  style.setAttribute('data-inline', 'true')
  style.textContent = inlineCss
  document.head.appendChild(style)
}

createApp(App).use(router).mount('#app')
