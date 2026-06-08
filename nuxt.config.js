// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  
  // 运行时配置
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
    }
  },
  
  css: ['~/assets/styles/main.scss'],
  
  components: [
    {
      path: '~/components',
      pathPrefix: false
    }
  ],
  
  nitro: {
    preset: 'github-pages'
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
  
  build: {
    transpile: ['three']
  }
})
