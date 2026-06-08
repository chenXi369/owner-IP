/**
 * API 请求工具
 * 封装所有与后端 API 的交互
 */

// API 基础地址
const getApiBase = () => {
  return useRuntimeConfig().public.apiBase || 'http://localhost:8000'
}

/**
 * 获取激活的简历数据
 */
export const useResumeApi = () => {
  const getActiveResume = async () => {
    const { data, error } = await useFetch(`${getApiBase()}/api/resumes/active`, {
      key: 'active-resume',
      // 服务端渲染时也获取数据
      server: true,
      // 客户端也获取数据
      lazy: false
    })
    
    if (error.value) {
      console.error('获取简历数据失败:', error.value)
      return null
    }
    
    return data.value
  }
  
  const getResumeById = async (id) => {
    const { data, error } = await useFetch(`${getApiBase()}/api/resumes/${id}`, {
      key: `resume-${id}`
    })
    
    if (error.value) {
      console.error('获取简历数据失败:', error.value)
      return null
    }
    
    return data.value
  }
  
  return {
    getActiveResume,
    getResumeById
  }
}

/**
 * 提交联系消息
 */
export const useMessageApi = () => {
  const submitMessage = async (messageData) => {
    try {
      const response = await $fetch(`${getApiBase()}/api/messages`, {
        method: 'POST',
        body: messageData,
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      return { success: true, data: response }
    } catch (error) {
      console.error('提交消息失败:', error)
      return { success: false, error: error.message || '提交失败,请稍后重试' }
    }
  }
  
  return {
    submitMessage
  }
}

/**
 * 技能相关 API
 */
export const useSkillApi = () => {
  const getSkillsByResume = async (resumeId) => {
    const { data, error } = await useFetch(`${getApiBase()}/api/skills/resume/${resumeId}`, {
      key: `skills-${resumeId}`
    })
    
    if (error.value) {
      console.error('获取技能数据失败:', error.value)
      return []
    }
    
    return data.value || []
  }
  
  return {
    getSkillsByResume
  }
}

/**
 * 项目相关 API
 */
export const useProjectApi = () => {
  const getProjectsByResume = async (resumeId) => {
    const { data, error } = await useFetch(`${getApiBase()}/api/projects/resume/${resumeId}`, {
      key: `projects-${resumeId}`
    })
    
    if (error.value) {
      console.error('获取项目数据失败:', error.value)
      return []
    }
    
    return data.value || []
  }
  
  return {
    getProjectsByResume
  }
}

/**
 * 工作经历相关 API
 */
export const useExperienceApi = () => {
  const getExperiencesByResume = async (resumeId) => {
    const { data, error } = await useFetch(`${getApiBase()}/api/experiences/resume/${resumeId}`, {
      key: `experiences-${resumeId}`
    })
    
    if (error.value) {
      console.error('获取工作经历数据失败:', error.value)
      return []
    }
    
    return data.value || []
  }
  
  return {
    getExperiencesByResume
  }
}

/**
 * 教育背景相关 API
 */
export const useEducationApi = () => {
  const getEducationsByResume = async (resumeId) => {
    const { data, error } = await useFetch(`${getApiBase()}/api/educations/resume/${resumeId}`, {
      key: `educations-${resumeId}`
    })
    
    if (error.value) {
      console.error('获取教育背景数据失败:', error.value)
      return []
    }
    
    return data.value || []
  }
  
  return {
    getEducationsByResume
  }
}

/**
 * 联系方式相关 API
 */
export const useContactApi = () => {
  const getContactsByResume = async (resumeId) => {
    const { data, error } = await useFetch(`${getApiBase()}/api/contacts/resume/${resumeId}`, {
      key: `contacts-${resumeId}`
    })
    
    if (error.value) {
      console.error('获取联系方式数据失败:', error.value)
      return []
    }
    
    return data.value || []
  }
  
  return {
    getContactsByResume
  }
}
