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

export interface Balance {
  balance: string
  currency: string
}

export default {
  async getBalance() {
    const response = await fetch(`${import.meta.env.VITE_APP_BASE_URL}/wallet/balance`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
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
        'Content-Type': 'application/json'
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
    return
  },
  async withdraw(body: WithdrawRequest) {
    const response = await fetch(`${import.meta.env.VITE_APP_BASE_URL}/wallet/withdraw`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })
    if (!response.ok) {
      notify(
        'error',
        `Errore durante l'operazione di bonifico. Controlla i dati del tuo conto o riprova più tardi.`
      )
      throw new Error('Withdrawal failed')
    }
    return
  }
}
