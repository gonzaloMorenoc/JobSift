import { ReactNode } from 'react'
import { Header } from './Header'

interface AppLayoutProps {
  children: ReactNode
  showHeader?: boolean
}

export function AppLayout({ children, showHeader = true }: AppLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      {showHeader && <Header />}
      <main className="flex-1">
        {children}
      </main>
    </div>
  )
}

// Page wrapper for consistent padding and max-width
interface PageWrapperProps {
  children: ReactNode
  className?: string
}

export function PageWrapper({ children, className = '' }: PageWrapperProps) {
  return (
    <div className={`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 ${className}`}>
      {children}
    </div>
  )
}

// Page header component for consistent page titles
interface PageHeaderProps {
  title: string
  description?: string
  action?: ReactNode
}

export function PageHeader({ title, description, action }: PageHeaderProps) {
  return (
    <div className="flex justify-between items-start mb-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
        {description && (
          <p className="text-sm text-gray-600 mt-1">{description}</p>
        )}
      </div>
      {action && <div>{action}</div>}
    </div>
  )
}

// Content container for cards and sections
interface ContentSectionProps {
  children: ReactNode
  className?: string
}

export function ContentSection({ children, className = '' }: ContentSectionProps) {
  return (
    <div className={`bg-white rounded-lg shadow p-6 ${className}`}>
      {children}
    </div>
  )
}
