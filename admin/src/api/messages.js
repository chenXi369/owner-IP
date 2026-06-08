import request from './request'

export const getMessages = () => request.get('/messages')
export const deleteMessage = (id) => request.delete(`/messages/${id}`)
export const markMessageRead = (id) => request.put(`/messages/${id}/read`)
