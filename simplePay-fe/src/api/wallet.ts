import { notify } from '@/service/alert'

export interface DepositRequest {
  amount: number | null
  card_number: string
  card_holder: string
  expiry_month: number | null
  expiry_year: number | null
  cvv: string
}

export interface WithdrawRequest {
  amount: number | null
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
      notify('error', 'Errore durante il recupero del saldo. Riprova più tardi.')
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
      notify(
        'error',
        'Errore durante il deposito. Controlla i dati della tua carta o riprova più tardi.'
      )
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
      notify(
        'error',
        'Errore durante il prelievo. Controlla i dati del tuo conto o riprova più tardi.'
      )
      throw new Error('Withdrawal failed')
    }
    return response.text()
  }
}

export interface Balance {
  balance: string
  currency: string
}
