import { jwtDecode } from 'jwt-decode'

export interface TokenInformations {
  email: string
  exp: number
  first_name: string
  iat: number
  last_name: string
  user_id: number
  username: string
}

export function getTokenInfo() {
  const decoded = jwtDecode(localStorage.getItem('userToken') ?? '')
  if (!decoded) return null

  return decoded as TokenInformations
}
