export default defineNuxtConfig({
  devtools: { enabled: true },
  
  devServer: {
    port: 3001
  },
  
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "~/assets/styles/variables.scss" as *;'
        }
      }
    }
  },
  
  css: [
    '~/assets/styles/main.scss'
  ],
  
  modules: [
    '@vueuse/nuxt'
  ],
  
  app: {
    baseURL: process.env.NODE_ENV === 'production' ? '/threejs简历/' : '/',
    buildAssetsDir: '/_nuxt/',
    head: {
      title: '个人简历 - 3D Interactive Resume',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: '专业前端开发工程师个人简历，展示Three.js 3D视觉效果和交互设计能力' }
      ],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap' }
      ]
    },
    pageTransition: { name: 'page', mode: 'out-in' }
  },
  
  nitro: {
    preset: 'github-pages'
  },
  
  build: {
    transpile: ['three']
  },
  
  compatibilityDate: '2024-11-01'
})
