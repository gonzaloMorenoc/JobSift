export type ApplicationStatus = 
  | 'APPLIED'
  | 'SCREENING'
  | 'HR_INTERVIEW'
  | 'TECH_INTERVIEW'
  | 'MANAGER_INTERVIEW'
  | 'OFFER'
  | 'REJECTED'
  | 'ON_HOLD'

export type WorkMode = 'REMOTE' | 'HYBRID' | 'ONSITE'

export interface Interview {
  id: string
  user_id: string
  company_name: string
  company_description?: string
  role_title: string
  work_mode: WorkMode
  location?: string
  application_status: ApplicationStatus
  next_milestone?: string
  contact_name?: string
  contact_email?: string
  contact_phone?: string
  salary_range_min?: number
  salary_range_max?: number
  currency?: string
  language?: string
  travel_requirements?: string
  notes?: string
  interview_date?: string
  created_at: string
  updated_at: string
}

export interface InterviewCreate {
  company_name: string
  company_description?: string
  role_title: string
  work_mode: WorkMode
  location?: string
  application_status?: ApplicationStatus
  next_milestone?: string
  contact_name?: string
  contact_email?: string
  contact_phone?: string
  salary_range_min?: number
  salary_range_max?: number
  currency?: string
  language?: string
  travel_requirements?: string
  notes?: string
  interview_date?: string
}

export interface InterviewUpdate {
  company_name?: string
  company_description?: string
  role_title?: string
  work_mode?: WorkMode
  location?: string
  application_status?: ApplicationStatus
  next_milestone?: string
  contact_name?: string
  contact_email?: string
  contact_phone?: string
  salary_range_min?: number
  salary_range_max?: number
  currency?: string
  language?: string
  travel_requirements?: string
  notes?: string
  interview_date?: string
}

export interface InterviewsResponse {
  interviews: Interview[]
  total: number
  skip: number
  limit: number
}

// Dashboard types
export interface StatusDistributionItem {
  status: string
  count: number
}

export interface UpcomingInterview {
  id: string
  company_name: string
  role_title: string
  interview_date?: string
  status: string
}

export interface RecentActivity {
  id: string
  company_name: string
  role_title: string
  status: string
  updated_at: string
}

export interface DashboardSummaryStats {
  total_interviews: number
  conversion_rate: number
  success_rate: number
  this_week_applications: number
}

export interface DashboardSummary {
  summary: DashboardSummaryStats
  status_distribution: StatusDistributionItem[]
  upcoming_interviews: UpcomingInterview[]
  recent_activity: RecentActivity[]
  insights: string[]
}

// Metadata types
export interface InterviewStatusInfo {
  value: ApplicationStatus
  label: string
  color: string
}

export interface WorkModeInfo {
  value: WorkMode
  label: string
  icon: string
}

export interface InterviewMetadata {
  statuses: InterviewStatusInfo[]
  work_modes: WorkModeInfo[]
  currencies: string[]
}

// Filter types
export interface InterviewFilters {
  status?: ApplicationStatus
  company?: string
  from_date?: string
  to_date?: string
}

// Form types
export interface InterviewFormData extends InterviewCreate {}

// Status colors and labels
export const STATUS_CONFIG: Record<ApplicationStatus, { label: string; color: string; bgColor: string }> = {
  APPLIED: { label: 'Applied', color: 'text-blue-700', bgColor: 'bg-blue-100' },
  SCREENING: { label: 'Screening', color: 'text-yellow-700', bgColor: 'bg-yellow-100' },
  HR_INTERVIEW: { label: 'HR Interview', color: 'text-orange-700', bgColor: 'bg-orange-100' },
  TECH_INTERVIEW: { label: 'Technical Interview', color: 'text-purple-700', bgColor: 'bg-purple-100' },
  MANAGER_INTERVIEW: { label: 'Manager Interview', color: 'text-indigo-700', bgColor: 'bg-indigo-100' },
  OFFER: { label: 'Offer', color: 'text-green-700', bgColor: 'bg-green-100' },
  REJECTED: { label: 'Rejected', color: 'text-red-700', bgColor: 'bg-red-100' },
  ON_HOLD: { label: 'On Hold', color: 'text-gray-700', bgColor: 'bg-gray-100' }
}

export const WORK_MODE_CONFIG: Record<WorkMode, { label: string; icon: string }> = {
  REMOTE: { label: 'Remote', icon: '🏠' },
  HYBRID: { label: 'Hybrid', icon: '🏢' },
  ONSITE: { label: 'On-site', icon: '🏬' }
}
