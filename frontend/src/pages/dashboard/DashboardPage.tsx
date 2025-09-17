import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useDashboardData } from '@/features/interviews/store/interviewsStore'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { 
  Briefcase, 
  TrendingUp, 
  Plus,
  BarChart3,
  Clock,
  Target,
  Activity,
  ArrowUpRight,
  Building
} from 'lucide-react'
import { STATUS_CONFIG } from '@/types/interview'

export function DashboardPage() {
  const { summary, isLoading, error, fetchSummary } = useDashboardData()

  useEffect(() => {
    fetchSummary()
  }, [fetchSummary])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-md mx-auto py-12">
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <div className="text-red-500 text-xl mb-2">⚠️</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">Unable to load dashboard</h3>
              <p className="text-sm text-gray-600 mb-4">{error}</p>
              <Button onClick={fetchSummary} variant="outline">
                Try Again
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  const stats = summary?.summary
  const insights = summary?.insights || []

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-sm text-gray-600 mt-1">
            Track your interview progress and job search analytics
          </p>
        </div>
        <Link to="/interviews/new">
          <Button className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            New Interview
          </Button>
        </Link>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Interviews</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.total_interviews || 0}</p>
              </div>
              <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Briefcase className="h-6 w-6 text-blue-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Conversion Rate</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.conversion_rate || 0}%</p>
              </div>
              <div className="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center">
                <TrendingUp className="h-6 w-6 text-green-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Success Rate</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.success_rate || 0}%</p>
              </div>
              <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <Target className="h-6 w-6 text-purple-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">This Week</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.this_week_applications || 0}</p>
              </div>
              <div className="h-12 w-12 bg-orange-100 rounded-lg flex items-center justify-center">
                <Activity className="h-6 w-6 text-orange-600" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Status Distribution */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-lg font-semibold">Interview Pipeline</CardTitle>
            <BarChart3 className="h-5 w-5 text-gray-400" />
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {summary?.status_distribution && summary.status_distribution.length > 0 ? (
                summary.status_distribution.map((item) => {
                  const statusKey = item.status.replace(' ', '_').toUpperCase() as keyof typeof STATUS_CONFIG
                  const statusConfig = STATUS_CONFIG[statusKey] || { label: item.status, color: 'text-gray-700', bgColor: 'bg-gray-100' }
                  
                  return (
                    <div key={item.status} className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <Badge 
                          variant="secondary"
                          className={`${statusConfig.bgColor} ${statusConfig.color}`}
                        >
                          {statusConfig.label}
                        </Badge>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm font-medium text-gray-900">{item.count}</span>
                        <div className="w-16 bg-gray-200 rounded-full h-2">
                          <div 
                            className="h-2 rounded-full bg-blue-600"
                            style={{ 
                              width: `${stats?.total_interviews ? (item.count / stats.total_interviews) * 100 : 0}%` 
                            }}
                          />
                        </div>
                      </div>
                    </div>
                  )
                })
              ) : (
                <div className="text-center py-8">
                  <Briefcase className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">No interviews yet</p>
                  <p className="text-sm text-gray-400 mb-4">Start tracking your job applications</p>
                  <Link to="/interviews/new">
                    <Button size="sm">Add First Interview</Button>
                  </Link>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Upcoming Interviews */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-lg font-semibold">Upcoming Interviews</CardTitle>
            <Clock className="h-5 w-5 text-gray-400" />
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {summary?.upcoming_interviews && summary.upcoming_interviews.length > 0 ? (
                summary.upcoming_interviews.map((interview) => (
                  <div key={interview.id} className="flex items-start justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        <Building className="h-4 w-4 text-gray-400" />
                        <h4 className="text-sm font-medium text-gray-900">{interview.company_name}</h4>
                      </div>
                      <p className="text-sm text-gray-600">{interview.role_title}</p>
                      {interview.interview_date && (
                        <p className="text-xs text-gray-500 mt-1">
                          {new Date(interview.interview_date).toLocaleDateString('en-US', {
                            weekday: 'short',
                            month: 'short',
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </p>
                      )}
                    </div>
                    <Link to={`/interviews/${interview.id}`}>
                      <Button size="sm" variant="ghost">
                        <ArrowUpRight className="h-4 w-4" />
                      </Button>
                    </Link>
                  </div>
                ))
              ) : (
                <div className="text-center py-8">
                  <Clock className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">No upcoming interviews</p>
                  <p className="text-sm text-gray-400">Schedule your interviews to see them here</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card className="mt-8">
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="text-lg font-semibold">Recent Activity</CardTitle>
          <Activity className="h-5 w-5 text-gray-400" />
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {summary?.recent_activity && summary.recent_activity.length > 0 ? (
              summary.recent_activity.map((activity) => {
                const statusKey = activity.status.replace(' ', '_').toUpperCase() as keyof typeof STATUS_CONFIG
                const statusConfig = STATUS_CONFIG[statusKey] || { label: activity.status, color: 'text-gray-700', bgColor: 'bg-gray-100' }
                
                return (
                  <div key={`${activity.id}-${activity.updated_at}`} className="flex items-center justify-between py-2 border-b last:border-b-0">
                    <div className="flex items-center space-x-3">
                      <div className="h-8 w-8 bg-gray-100 rounded-full flex items-center justify-center">
                        <Building className="h-4 w-4 text-gray-600" />
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {activity.company_name} • {activity.role_title}
                        </p>
                        <p className="text-xs text-gray-500">
                          {new Date(activity.updated_at).toLocaleDateString('en-US', {
                            month: 'short',
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </p>
                      </div>
                    </div>
                    <Badge 
                      variant="secondary"
                      className={`${statusConfig.bgColor} ${statusConfig.color}`}
                    >
                      {statusConfig.label}
                    </Badge>
                  </div>
                )
              })
            ) : (
              <div className="text-center py-8">
                <Activity className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500">No recent activity</p>
                <p className="text-sm text-gray-400">Your interview updates will appear here</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Insights */}
      {insights.length > 0 && (
        <Card className="mt-8">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Insights</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {insights.map((insight, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                  <div className="flex-shrink-0 w-5 h-5 bg-blue-100 rounded-full flex items-center justify-center mt-0.5">
                    <div className="w-2 h-2 bg-blue-600 rounded-full" />
                  </div>
                  <p className="text-sm text-blue-900">{insight}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
