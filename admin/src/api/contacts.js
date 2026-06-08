import request from './request'

export const getAllContacts = () => request.get('/contacts')
export const getContactsByResume = (resumeId) => request.get(`/contacts/resume/${resumeId}`)
export const getMyContacts = () => request.get('/my/contacts')
export const getMyActiveResume = () => request.get('/my/active-resume')
export const createContact = (data) => request.post('/contacts', data)
export const updateContact = (id, data) => request.put(`/contacts/${id}`, data)
export const deleteContact = (id) => request.delete(`/contacts/${id}`)
