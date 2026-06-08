/**
 * 获取用户个人信息的组合式函数
 */
export const useProfile = () => {
  const profile = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchProfile = async (userId = null) => {
    try {
      loading.value = true
      error.value = null

      const apiBase = useRuntimeConfig().public.apiBase || 'http://localhost:8000'
      const url = userId
        ? `${apiBase}/api/public/profile/${userId}`
        : `${apiBase}/api/profile`

      const data = await $fetch(url)

      if (data) {
        profile.value = data
      }
    } catch (err) {
      console.error('获取个人信息失败:', err)
      error.value = err.message || '获取个人信息失败'
    } finally {
      loading.value = false
    }
  }

  // 将 about_text 按段落分割
  const aboutParagraphs = computed(() => {
    if (!profile.value?.about_text) return []
    return profile.value.about_text.split('\n').filter(p => p.trim())
  })

  // 统计数据
  const stats = computed(() => {
    if (!profile.value) return []
    return [
      { number: profile.value.years_exp || '0', label: '年开发经验' },
      { number: profile.value.projects_count || '0', label: '完成项目' },
      { number: profile.value.articles_count || '0', label: '技术文章' },
      { number: profile.value.contributions_count || '0', label: '开源贡献' }
    ]
  })

  return {
    profile,
    aboutParagraphs,
    stats,
    loading,
    error,
    fetchProfile
  }
}
