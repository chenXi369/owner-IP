import request from './request'

export const getResumes = () => request.get('/resumes')
export const getActiveResume = () => request.get('/resumes/active')
export const getResumeById = (id) => request.get(`/resumes/${id}`)
export const createResume = (data) => request.post('/resumes', data)
export const updateResume = (id, data) => request.put(`/resumes/${id}`, data)
export const deleteResume = (id) => request.delete(`/resumes/${id}`)
export const getPublicResume = (userId, slug) => request.get(`/public/resumes/${userId}/${slug}`)
