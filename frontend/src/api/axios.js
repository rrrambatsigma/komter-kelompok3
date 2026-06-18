import axios from 'axios'
import toast from 'react-hot-toast'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.message || error.message || 'Terjadi kesalahan'
    toast.error(message)
    return Promise.reject(error)
  },
)

export const fetchAll = (endpoint) => api.get(endpoint).then((r) => r.data)

export const createItem = (endpoint, data) =>
  api.post(endpoint, data).then((r) => r.data)

export const updateItem = (endpoint, id, data) =>
  api.put(`${endpoint}/${id}`, data).then((r) => r.data)

export const deleteItem = (endpoint, id) =>
  api.delete(`${endpoint}/${id}`).then((r) => r.data)

export default api
