import { notify } from '@/service/alert'

export interface SendMoneyRequest {
  to_user_email: string
  amount: number | null
  description: string
}

export interface Paginated<T> {
  page: number
  page_size: number
  total: number
  total_pages: number
  data: T[]
}

export interface Transaction {
  id: number
  amount: number
  currency: string
  description: string
  reference_code: string
  status: string
  transaction_type: 'send' | 'receive' | 'withdraw' | 'deposit'
  created_at: string
}

export default {
  async sendMoney(body: SendMoneyRequest) {
    const response = await fetch(`${import.meta.env.VITE_APP_BASE_URL}/payments/send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('userToken') ?? ''}`
      },
      body: JSON.stringify(body)
    })
    if (!response.ok) {
      notify('error', 'Errore durante il pagamento. Controlla i dati inseriti o riprova più tardi.')
      throw new Error('Payment failed')
    }
    return response.text()
  },
  async getTransactions(page: number, pageSize: number): Promise<Paginated<Transaction>> {
    const response = await fetch(
      `${
        import.meta.env.VITE_APP_BASE_URL
      }/payments/transactions?page=${page}&pageSize=${pageSize}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('userToken') ?? ''}`
        }
      }
    )
    if (!response.ok) {
      notify('error', 'Errore durante il recupero delle transazioni. Riprova più tardi.')
      throw new Error('Fetching transactions failed')
    }
    return response.json() as Promise<Paginated<Transaction>>
  }
}
