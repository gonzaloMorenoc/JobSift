import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useEffect } from 'react'
import { useAuthStore } from '@/features/auth/store/authStore'
import { AppLayout } from '@/components/layout/AppLayout'

// Pages
import { LoginPage } from '@/pages/auth/LoginPage'
import { DashboardPage } from '@/pages/dashboard/DashboardPage'

import './styles/globals.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore(state => state.isAuthenticated)
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />
}

function PublicRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore(state => state.isAuthenticated)
  return !isAuthenticated ? <>{children}</> : <Navigate to="/dashboard" replace />
}

// Placeholder components for routes not yet implemented
const InterviewsPage = () => (
  <AppLayout>
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-8">Interviews</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🚀</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Interviews Page Coming Soon!</h3>
          <p className="text-gray-600 mb-4">
            This page will show all your interviews with filtering, search, and management capabilities.
          </p>
          <div className="text-sm text-gray-500">
            <p className="mb-2">Planned features:</p>
            <ul className="list-disc list-inside space-y-1">
              <li>Interview list with status filtering</li>
              <li>Create and edit interview forms</li>
              <li>Search and sort functionality</li>
              <li>Bulk actions and export</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
)

const NewInterviewPage = () => (
  <AppLayout>
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-8">Add New Interview</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📝</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Interview Form Coming Soon!</h3>
          <p className="text-gray-600 mb-4">
            This page will have a comprehensive form to add new interviews to your tracking system.
          </p>
          <div className="text-sm text-gray-500">
            <p className="mb-2">Form will include:</p>
            <ul className="list-disc list-inside space-y-1">
              <li>Company information and role details</li>
              <li>Contact information and salary range</li>
              <li>Interview status and scheduling</li>
              <li>Notes and file attachments</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
)

const InterviewDetailsPage = () => (
  <AppLayout>
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-8">Interview Details</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📊</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Interview Details Page Coming Soon!</h3>
          <p className="text-gray-600 mb-4">
            This page will show detailed information about a specific interview with editing capabilities.
          </p>
          <div className="text-sm text-gray-500">
            <p className="mb-2">Features will include:</p>
            <ul className="list-disc list-inside space-y-1">
              <li>Complete interview timeline and history</li>
              <li>Status updates and milestone tracking</li>
              <li>Calendar integration and reminders</li>
              <li>Document storage and notes</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
)

const CalendarPage = () => (
  <AppLayout>
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-8">Calendar</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📅</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Calendar Integration Coming Soon!</h3>
          <p className="text-gray-600 mb-4">
            This page will show your interview schedule and provide calendar integrations.
          </p>
          <div className="text-sm text-gray-500">
            <p className="mb-2">Calendar features:</p>
            <ul className="list-disc list-inside space-y-1">
              <li>Visual calendar view of interviews</li>
              <li>Google Calendar sync integration</li>
              <li>ICS feed export for Apple/Outlook</li>
              <li>Reminder notifications</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
)

function AppContent() {
  const { isAuthenticated, refreshUser, user } = useAuthStore()

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token && !isAuthenticated && !user) {
      refreshUser().catch(() => {
        localStorage.removeItem('access_token')
      })
    }
  }, [isAuthenticated, refreshUser, user])

  return (
    <Routes>
      {/* Public Routes */}
      <Route
        path="/login"
        element={
          <PublicRoute>
            <LoginPage />
          </PublicRoute>
        }
      />
      
      {/* Protected Routes */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <AppLayout>
              <DashboardPage />
            </AppLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/interviews"
        element={
          <ProtectedRoute>
            <InterviewsPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/interviews/new"
        element={
          <ProtectedRoute>
            <NewInterviewPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/interviews/:id"
        element={
          <ProtectedRoute>
            <InterviewDetailsPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/calendar"
        element={
          <ProtectedRoute>
            <CalendarPage />
          </ProtectedRoute>
        }
      />

      {/* Default redirects */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AppContent />
      </Router>
    </QueryClientProvider>
  )
}

export default App
