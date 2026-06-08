import request from './request'

export const getAllSkills = () => request.get('/skills')
export const getSkillsByResume = (resumeId) => request.get(`/skills/resume/${resumeId}`)
export const createSkill = (data) => request.post('/skills', data)
export const updateSkill = (id, data) => request.put(`/skills/${id}`, data)
export const deleteSkill = (id) => request.delete(`/skills/${id}`)
