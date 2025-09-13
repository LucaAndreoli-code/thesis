import { notify } from '@/service/alert'

export default {
  async deleteAccount() {
    const response = await fetch(`${import.meta.env.VITE_APP_BASE_URL}/user/delete`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    if (!response.ok) {
      notify('error', `Errore durante l'eliminazione dell'account. Riprovare piú tardi.`)
      throw new Error('Failed to delete account')
    }
    return response.json()
  }
}

export interface LoginResponse {
  access_token: string
  token_type: string
}
