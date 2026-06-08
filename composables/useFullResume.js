/**
 * 获取完整简历数据的组合式函数
 */
export const useFullResume = () => {
  const resume = ref(null)
  const skills = ref([])
  const projects = ref([])
  const experiences = ref([])
  const educations = ref([])
  const contacts = ref([])
  const loading = ref(true)
  const error = ref(null)
  
  const fetchFullResume = async (userId = null) => {
    try {
      loading.value = true
      error.value = null
      
      // 使用 $fetch 手动获取数据（可在异步函数中使用）
      const apiBase = useRuntimeConfig().public.apiBase || 'http://localhost:8000'
      let url = `${apiBase}/api/resumes/active`
      if (userId) {
        url += `?user_id=${userId}`
      }
      const data = await $fetch(url)
      
      if (data) {
        resume.value = data.resume
        skills.value = data.skills || []
        projects.value = data.projects || []
        experiences.value = data.experiences || []
        educations.value = data.educations || []
        contacts.value = data.contacts || []
      }
    } catch (err) {
      console.error('获取简历数据失败:', err)
      error.value = err.message || '获取数据失败'
    } finally {
      loading.value = false
    }
  }
  
  return {
    resume,
    skills,
    projects,
    experiences,
    educations,
    contacts,
    loading,
    error,
    fetchFullResume
  }
}
