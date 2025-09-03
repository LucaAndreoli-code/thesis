import router from '@/router'
import { notify } from './alert'
import { getTokenInfo } from './jwt'

const { fetch: originalFetch } = window

const checkIfTokenExpired = () => {
  const token = getTokenInfo()
  if (!token) return false
  const currentTime = Math.floor(Date.now() / 1000)
  if (token.exp < currentTime) {
    localStorage.removeItem('userToken')
    return true
  }
  return false
}

window.fetch = async (...args) => {
  let [resource, config] = args

  const token = localStorage.getItem('userToken')
  if (token) {
    if (checkIfTokenExpired()) {
      localStorage.removeItem('userToken')
      setTimeout(() => {
        notify('warning', 'La sessione è scaduta. Effettua nuovamente il login.')
      }, 100)
      router.push('/login')
    }
    const headers = new Headers(config?.headers || {})
    headers.set('Authorization', `Bearer ${token}`)
    config = { ...config, headers }
  }

  return originalFetch(resource, config)
}
