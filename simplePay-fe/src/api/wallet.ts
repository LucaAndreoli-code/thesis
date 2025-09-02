export default {
  async getBalance() {
    const response = await fetch(`${import.meta.env.VITE_APP_BASE_URL}/wallet/balance`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('userToken') ?? ''}`
      }
    })
    if (!response.ok) {
      throw new Error('Fetching balance failed')
    }
    return response.json() as Promise<Balance>
  }
}

export interface Balance {
  balance: string
  currency: string
}
