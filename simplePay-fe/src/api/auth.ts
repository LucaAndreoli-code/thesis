import { notify } from '@/service/alert'

export default {
  async login(email: string, password: string) {
    const response = await fetch(`${import.meta.env.VITE_APP_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    })
    if (!response.ok) {
      notify('error', 'Errore durante il login. Controlla le tue credenziali.')
      throw new Error('Login failed')
    }
    return response.json() as Promise<LoginResponse>
  },
  async register(first_name: string, last_name: string, email: string, password: string) {
    const username = `${first_name.toLowerCase()}_${last_name.toLowerCase()}`
    const response = await fetch(`${import.meta.env.VITE_APP_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ first_name, last_name, email, password, username })
    })
    if (!response.ok) {
      notify('error', 'Errore durante la registrazione. Riprova più tardi.')
      throw new Error('Registration failed')
    }
    return
  }
}

export interface LoginResponse {
  access_token: string
  token_type: string
}
