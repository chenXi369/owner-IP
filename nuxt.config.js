// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  
  devtools: { enabled: true },
  
  devServer: {
    port: 3001
  },
  
  css: ['~/assets/styles/main.scss'],
  
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
