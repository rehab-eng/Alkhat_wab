import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    {
      name: 'defer-css',
      transformIndexHtml(html) {
        const re = new RegExp('<link rel="stylesheet" href="([^"]+\\\\.css)"(?![^>]*onload)[^>]*>', 'g')
        return html.replace(re, (_match, href) => {
          return (
            `<link rel="preload" as="style" href="${href}" onload="this.onload=null;this.rel='stylesheet'">` +
            `<noscript><link rel="stylesheet" href="${href}"></noscript>`
          )
        })
      },
    },
  ],
})
