export interface SendMoneyRequest {
  to_user_email: string
  amount: number
  description: string
}

export interface Paginated<T> {
  pagination: {
    page: number
    limit: number
    total: number
    total_pages: number
  }
  data: T[]
}

export interface Transaction {
  pagination: {
    page: number
    limit: number
    total: number
    total_pages: number
  }
  transactions: {
    id: number
    amount: number
    currency: string
    description: string
    reference_code: string
    status: string
    type: 'send' | 'receive' | 'withdraw' | 'deposit'
    created_at: string
    processed_at: string | null
  }[]
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
      throw new Error('Payment failed')
    }
    return response.text()
  },
  async getTransactions(page: number, pageSize: number): Promise<Transaction> {
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
      throw new Error('Fetching transactions failed')
    }
    return response.json() as Promise<Transaction>
  }
}
