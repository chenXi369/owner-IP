import request from './request'

export const getAllEducations = () => request.get('/educations')
export const getEducationsByResume = (resumeId) => request.get(`/educations/resume/${resumeId}`)
export const createEducation = (data) => request.post('/educations', data)
export const updateEducation = (id, data) => request.put(`/educations/${id}`, data)
export const deleteEducation = (id) => request.delete(`/educations/${id}`)
