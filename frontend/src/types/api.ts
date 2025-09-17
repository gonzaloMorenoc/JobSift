export interface User {
  id: string
  email: string
  full_name: string
  locale: string
  is_verified: boolean
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  full_name: string
  locale?: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export interface RefreshResponse {
  access_token: string
  token_type: string
}