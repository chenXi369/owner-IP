import request from './request'

export const getAllExperiences = () => request.get('/experiences')
export const getExperiencesByResume = (resumeId) => request.get(`/experiences/resume/${resumeId}`)
export const createExperience = (data) => request.post('/experiences', data)
export const updateExperience = (id, data) => request.put(`/experiences/${id}`, data)
export const deleteExperience = (id) => request.delete(`/experiences/${id}`)
