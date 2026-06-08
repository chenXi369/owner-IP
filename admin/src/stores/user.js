import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getMe } from '../api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => ['admin', 'super_admin'].includes(userInfo.value?.role))
  const isSuperAdmin = computed(() => userInfo.value?.role === 'super_admin')

  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setUserInfo = (info) => {
    userInfo.value = info
    localStorage.setItem('userInfo', JSON.stringify(info))
  }

  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  const fetchUserInfo = async () => {
    try {
      const data = await getMe()
      setUserInfo(data)
      return data
    } catch {
      logout()
      return null
    }
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    isAdmin,
    setToken,
    setUserInfo,
    logout,
    fetchUserInfo
  }
})
