import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // If 401 and not already retried, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        })

        const { access } = response.data
        localStorage.setItem('access_token', access)

        originalRequest.headers.Authorization = `Bearer ${access}`
        return api(originalRequest)
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// API methods
export const jobsAPI = {
  list: () => api.get('/jobs/'),
  get: (id: string) => api.get(`/jobs/${id}/`),
  create: (data: any) => api.post('/jobs/', data),
  update: (id: string, data: any) => api.put(`/jobs/${id}/`, data),
  delete: (id: string) => api.delete(`/jobs/${id}/`),
  generateFromTitle: (title: string, company: string) =>
    api.post('/jobs/generate_from_title/', { title, company }),
}

export const candidatesAPI = {
  list: () => api.get('/candidates/'),
  get: (id: string) => api.get(`/candidates/${id}/`),
  uploadCV: (file: File) => {
    const formData = new FormData()
    formData.append('cv_file', file)
    return api.post('/candidates/upload_cv/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  addNote: (id: string, content: string) =>
    api.post(`/candidates/${id}/add_note/`, { content }),
}

export const interviewsAPI = {
  list: () => api.get('/interviews/'),
  get: (id: string) => api.get(`/interviews/${id}/`),
  create: (data: any) => api.post('/interviews/', data),
  update: (id: string, data: any) => api.put(`/interviews/${id}/`, data),
  delete: (id: string) => api.delete(`/interviews/${id}/`),
}

export const reportsAPI = {
  get: (id: string) => api.get(`/reports/${id}/`),
  export: (id: string) => api.get(`/reports/${id}/export/`, { responseType: 'blob' }),
}

export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login/', { email, password }),
  logout: () => api.post('/auth/logout/'),
  register: (data: any) => api.post('/auth/register/', data),
}

export default api
