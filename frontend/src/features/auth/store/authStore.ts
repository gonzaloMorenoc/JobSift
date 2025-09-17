import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { User } from '@/types/api'
import { apiClient } from '@/lib/api'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, fullName: string) => Promise<void>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (email: string, password: string) => {
        set({ isLoading: true })
        try {
          const response = await apiClient.login({ email, password })
          set({ user: response.user, isAuthenticated: true })
        } catch (error) {
          throw error
        } finally {
          set({ isLoading: false })
        }
      },

      register: async (email: string, password: string, fullName: string) => {
        set({ isLoading: true })
        try {
          const user = await apiClient.register({ email, password, full_name: fullName })
          set({ user, isAuthenticated: true })
        } catch (error) {
          throw error
        } finally {
          set({ isLoading: false })
        }
      },

      logout: async () => {
        try {
          await apiClient.logout()
        } catch (error) {
          console.error('Logout error:', error)
        } finally {
          set({ user: null, isAuthenticated: false })
        }
      },

      refreshUser: async () => {
        try {
          const user = await apiClient.getCurrentUser()
          set({ user, isAuthenticated: true })
        } catch (error) {
          set({ user: null, isAuthenticated: false })
          throw error
        }
      }
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user, isAuthenticated: state.isAuthenticated })
    }
  )
)