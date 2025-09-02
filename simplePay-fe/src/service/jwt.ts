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
  const token = localStorage.getItem('userToken')
  if (!token) return null
  const decoded = jwtDecode(token)
  if (!decoded) return null

  return decoded as TokenInformations
}
