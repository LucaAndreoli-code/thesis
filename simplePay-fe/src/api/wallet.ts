export interface DepositRequest {
  amount: number
  card_number: string
  card_holder: string
  expiry_month: number
  expiry_year: number
  cvv: string
}

export interface WithdrawRequest {
  amount: number
  bank_account: string
  back_account_name: string
}

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
  },
  async deposit(body: DepositRequest) {
    const response = await fetch(`${import.meta.env.VITE_APP_BASE_URL}/wallet/deposit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('userToken') ?? ''}`
      },
      body: JSON.stringify(body)
    })
    if (!response.ok) {
      throw new Error('Deposit failed')
    }
    return response.text()
  },
  async withdraw(body: WithdrawRequest) {
    const response = await fetch(`${import.meta.env.VITE_APP_BASE_URL}/wallet/withdraw`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('userToken') ?? ''}`
      },
      body: JSON.stringify(body)
    })
    if (!response.ok) {
      throw new Error('Withdrawal failed')
    }
    return response.text()
  }
}

export interface Balance {
  balance: string
  currency: string
}
