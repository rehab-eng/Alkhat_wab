import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    {
      name: 'defer-css',
      transformIndexHtml(html) {
        return html.replace(/<link[^>]+rel=["']stylesheet["'][^>]*>/g, (tag) => {
          const hrefMatch = tag.match(/href=["']([^"']+)["']/)
          if (!hrefMatch) return tag
          const href = hrefMatch[1]
          if (href.startsWith('http')) {
            return tag
          }
          return (
            `<link rel="preload" as="style" href="${href}" onload="this.onload=null;this.rel='stylesheet'">` +
            `<noscript><link rel="stylesheet" href="${href}"></noscript>`
          )
        })
      },
    },
  ],
})
