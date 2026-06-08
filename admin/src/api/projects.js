import request from './request'

export const getAllProjects = () => request.get('/projects')
export const getProjectsByResume = (resumeId) => request.get(`/projects/resume/${resumeId}`)
export const createProject = (data) => request.post('/projects', data)
export const updateProject = (id, data) => request.put(`/projects/${id}`, data)
export const deleteProject = (id) => request.delete(`/projects/${id}`)
