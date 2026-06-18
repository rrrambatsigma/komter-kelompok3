import axios from 'axios'
import toast from 'react-hot-toast'

const isDev = import.meta.env.DEV

function createApi(backend, tailscaleUrl) {
  const baseURL = isDev ? `/api/${backend}` : tailscaleUrl

  const api = axios.create({
    baseURL,
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

  return api
}

export const rambatApi = createApi('rambat', import.meta.env.VITE_RAMBAT_URL)
export const meivaApi = createApi('meiva', import.meta.env.VITE_MEIVA_URL)

export const fetchAll = (api, endpoint) => api.get(endpoint).then((r) => r.data)

export const createItem = (api, endpoint, data) =>
  api.post(endpoint, data).then((r) => r.data)

export const updateItem = (api, endpoint, id, data) =>
  api.put(`${endpoint}/${id}`, data).then((r) => r.data)

export const deleteItem = (api, endpoint, id) =>
  api.delete(`${endpoint}/${id}`).then((r) => r.data)
