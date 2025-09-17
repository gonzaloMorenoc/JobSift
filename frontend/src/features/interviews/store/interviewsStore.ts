import { create } from 'zustand'
import { Interview, InterviewCreate, InterviewUpdate, InterviewFilters, InterviewsResponse, DashboardSummary } from '@/types/interview'
import { apiClient } from '@/lib/api'

interface InterviewsState {
  // State
  interviews: Interview[]
  currentInterview: Interview | null
  dashboardSummary: DashboardSummary | null
  total: number
  isLoading: boolean
  error: string | null

  // Filters and pagination
  filters: InterviewFilters
  currentPage: number
  pageSize: number

  // Actions
  fetchInterviews: (page?: number, filters?: InterviewFilters) => Promise<void>
  createInterview: (data: InterviewCreate) => Promise<Interview>
  updateInterview: (id: string, data: InterviewUpdate) => Promise<Interview>
  deleteInterview: (id: string) => Promise<void>
  fetchInterview: (id: string) => Promise<Interview>
  fetchDashboardSummary: () => Promise<void>
  setFilters: (filters: Partial<InterviewFilters>) => void
  clearFilters: () => void
  setCurrentPage: (page: number) => void
  clearError: () => void
}

export const useInterviewsStore = create<InterviewsState>((set, get) => ({
  // Initial state
  interviews: [],
  currentInterview: null,
  dashboardSummary: null,
  total: 0,
  isLoading: false,
  error: null,

  // Filters and pagination
  filters: {},
  currentPage: 1,
  pageSize: 20,

  // Actions
  fetchInterviews: async (page = 1, filters) => {
    set({ isLoading: true, error: null })
    
    try {
      const state = get()
      const currentFilters = filters || state.filters
      const skip = (page - 1) * state.pageSize

      const response: InterviewsResponse = await apiClient.getInterviews({
        ...currentFilters,
        limit: state.pageSize,
        offset: skip
      })

      set({
        interviews: response.interviews,
        total: response.total,
        currentPage: page,
        filters: currentFilters,
        isLoading: false
      })
    } catch (error: any) {
      set({
        error: error.response?.data?.message || 'Failed to fetch interviews',
        isLoading: false
      })
      throw error
    }
  },

  createInterview: async (data: InterviewCreate) => {
    set({ isLoading: true, error: null })
    
    try {
      const interview = await apiClient.createInterview(data)
      
      // Add to the beginning of the current list
      set(state => ({
        interviews: [interview, ...state.interviews],
        total: state.total + 1,
        isLoading: false
      }))
      
      return interview
    } catch (error: any) {
      set({
        error: error.response?.data?.message || 'Failed to create interview',
        isLoading: false
      })
      throw error
    }
  },

  updateInterview: async (id: string, data: InterviewUpdate) => {
    set({ isLoading: true, error: null })
    
    try {
      const updatedInterview = await apiClient.updateInterview(id, data)
      
      // Update in the current list
      set(state => ({
        interviews: state.interviews.map(interview =>
          interview.id === id ? updatedInterview : interview
        ),
        currentInterview: state.currentInterview?.id === id ? updatedInterview : state.currentInterview,
        isLoading: false
      }))
      
      return updatedInterview
    } catch (error: any) {
      set({
        error: error.response?.data?.message || 'Failed to update interview',
        isLoading: false
      })
      throw error
    }
  },

  deleteInterview: async (id: string) => {
    set({ isLoading: true, error: null })
    
    try {
      await apiClient.deleteInterview(id)
      
      // Remove from the current list
      set(state => ({
        interviews: state.interviews.filter(interview => interview.id !== id),
        total: state.total - 1,
        currentInterview: state.currentInterview?.id === id ? null : state.currentInterview,
        isLoading: false
      }))
    } catch (error: any) {
      set({
        error: error.response?.data?.message || 'Failed to delete interview',
        isLoading: false
      })
      throw error
    }
  },

  fetchInterview: async (id: string) => {
    set({ isLoading: true, error: null })
    
    try {
      const interview = await apiClient.getInterview(id)
      
      set({
        currentInterview: interview,
        isLoading: false
      })
      
      return interview
    } catch (error: any) {
      set({
        error: error.response?.data?.message || 'Failed to fetch interview',
        isLoading: false
      })
      throw error
    }
  },

  fetchDashboardSummary: async () => {
    try {
      const summary = await apiClient.getDashboardSummary()
      set({ dashboardSummary: summary })
    } catch (error: any) {
      set({
        error: error.response?.data?.message || 'Failed to fetch dashboard summary'
      })
      throw error
    }
  },

  setFilters: (newFilters: Partial<InterviewFilters>) => {
    set(state => ({
      filters: { ...state.filters, ...newFilters },
      currentPage: 1 // Reset to first page when filters change
    }))
  },

  clearFilters: () => {
    set({
      filters: {},
      currentPage: 1
    })
  },

  setCurrentPage: (page: number) => {
    set({ currentPage: page })
  },

  clearError: () => {
    set({ error: null })
  }
}))

// Selector hooks for easier access to computed values
export const useInterviewsData = () => {
  const store = useInterviewsStore()
  return {
    interviews: store.interviews,
    total: store.total,
    isLoading: store.isLoading,
    error: store.error,
    hasInterviews: store.interviews.length > 0,
    totalPages: Math.ceil(store.total / store.pageSize),
    currentPage: store.currentPage
  }
}

export const useDashboardData = () => {
  const store = useInterviewsStore()
  return {
    summary: store.dashboardSummary,
    isLoading: store.isLoading,
    error: store.error,
    fetchSummary: store.fetchDashboardSummary
  }
}

export const useInterviewFilters = () => {
  const store = useInterviewsStore()
  return {
    filters: store.filters,
    setFilters: store.setFilters,
    clearFilters: store.clearFilters,
    hasActiveFilters: Object.keys(store.filters).length > 0
  }
}
