import { useState } from 'react'
import Head from 'next/head'
import Link from 'next/link'
import DashboardLayout from '@/components/layouts/DashboardLayout'

export default function RecruiterDashboard() {
  const [activeTab, setActiveTab] = useState<'overview' | 'jobs' | 'candidates' | 'interviews'>('overview')

  return (
    <>
      <Head>
        <title>Recruiter Dashboard | Interviewer AI</title>
      </Head>

      <DashboardLayout>
        <div className="space-y-6">
          {/* Header */}
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
              <p className="text-gray-600 mt-1">Manage your interviews and candidates</p>
            </div>
            <div className="flex space-x-3">
              <Link
                href="/recruiter/jobs/create"
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
              >
                + Create Job
              </Link>
              <Link
                href="/recruiter/candidates/upload"
                className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition"
              >
                + Upload CV
              </Link>
            </div>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatCard title="Active Jobs" value="12" change="+2 this week" />
            <StatCard title="Total Candidates" value="48" change="+8 this week" />
            <StatCard title="Interviews Scheduled" value="15" change="+5 today" />
            <StatCard title="Completed" value="32" change="90% completion" />
          </div>

          {/* Tabs */}
          <div className="bg-white rounded-lg shadow">
            <div className="border-b border-gray-200">
              <nav className="flex space-x-8 px-6" aria-label="Tabs">
                <TabButton
                  active={activeTab === 'overview'}
                  onClick={() => setActiveTab('overview')}
                  label="Overview"
                />
                <TabButton
                  active={activeTab === 'jobs'}
                  onClick={() => setActiveTab('jobs')}
                  label="Jobs"
                />
                <TabButton
                  active={activeTab === 'candidates'}
                  onClick={() => setActiveTab('candidates')}
                  label="Candidates"
                />
                <TabButton
                  active={activeTab === 'interviews'}
                  onClick={() => setActiveTab('interviews')}
                  label="Interviews"
                />
              </nav>
            </div>

            <div className="p-6">
              {activeTab === 'overview' && <OverviewTab />}
              {activeTab === 'jobs' && <JobsTab />}
              {activeTab === 'candidates' && <CandidatesTab />}
              {activeTab === 'interviews' && <InterviewsTab />}
            </div>
          </div>
        </div>
      </DashboardLayout>
    </>
  )
}

function StatCard({ title, value, change }: { title: string; value: string; change: string }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <div className="text-gray-600 text-sm font-medium">{title}</div>
      <div className="mt-2 text-3xl font-bold text-gray-900">{value}</div>
      <div className="mt-2 text-sm text-green-600">{change}</div>
    </div>
  )
}

function TabButton({ active, onClick, label }: { active: boolean; onClick: () => void; label: string }) {
  return (
    <button
      onClick={onClick}
      className={`py-4 px-1 border-b-2 font-medium text-sm ${
        active
          ? 'border-blue-500 text-blue-600'
          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
      }`}
    >
      {label}
    </button>
  )
}

function OverviewTab() {
  return (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold">Recent Activity</h3>
      <div className="space-y-4">
        <ActivityItem
          title="New candidate: John Doe applied for Senior Developer"
          time="2 hours ago"
          type="candidate"
        />
        <ActivityItem
          title="Interview completed: Sarah Smith - Frontend Developer"
          time="5 hours ago"
          type="interview"
        />
        <ActivityItem
          title="New job posted: Full Stack Developer"
          time="1 day ago"
          type="job"
        />
      </div>
    </div>
  )
}

function JobsTab() {
  const jobs = [
    { id: 1, title: 'Senior Java Developer', candidates: 12, status: 'Active' },
    { id: 2, title: 'Frontend React Developer', candidates: 8, status: 'Active' },
    { id: 3, title: 'DevOps Engineer', candidates: 15, status: 'Active' },
  ]

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Active Jobs</h3>
        <Link href="/recruiter/jobs/create" className="text-blue-600 hover:text-blue-700">
          + Add New
        </Link>
      </div>
      <div className="space-y-2">
        {jobs.map((job) => (
          <div key={job.id} className="border rounded-lg p-4 hover:bg-gray-50 cursor-pointer">
            <div className="flex justify-between items-start">
              <div>
                <h4 className="font-semibold text-gray-900">{job.title}</h4>
                <p className="text-sm text-gray-600 mt-1">{job.candidates} candidates</p>
              </div>
              <span className="px-3 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                {job.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function CandidatesTab() {
  const candidates = [
    { id: 1, name: 'John Doe', email: 'john@example.com', job: 'Senior Java Developer', score: 8.5 },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', job: 'Frontend Developer', score: 7.2 },
    { id: 3, name: 'Bob Wilson', email: 'bob@example.com', job: 'DevOps Engineer', score: 9.1 },
  ]

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Recent Candidates</h3>
        <Link href="/recruiter/candidates" className="text-blue-600 hover:text-blue-700">
          View All
        </Link>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Job</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Score</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {candidates.map((candidate) => (
              <tr key={candidate.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-sm font-medium text-gray-900">{candidate.name}</td>
                <td className="px-4 py-3 text-sm text-gray-600">{candidate.email}</td>
                <td className="px-4 py-3 text-sm text-gray-600">{candidate.job}</td>
                <td className="px-4 py-3 text-sm">
                  <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded">{candidate.score}/10</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function InterviewsTab() {
  const interviews = [
    { id: 1, candidate: 'John Doe', date: '2024-01-15 10:00', type: 'Video', status: 'Scheduled' },
    { id: 2, candidate: 'Jane Smith', date: '2024-01-15 14:00', type: 'Chat', status: 'Completed' },
    { id: 3, candidate: 'Bob Wilson', date: '2024-01-16 09:00', type: 'Video', status: 'Scheduled' },
  ]

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">Upcoming Interviews</h3>
      <div className="space-y-2">
        {interviews.map((interview) => (
          <div key={interview.id} className="border rounded-lg p-4 hover:bg-gray-50">
            <div className="flex justify-between items-center">
              <div>
                <h4 className="font-semibold text-gray-900">{interview.candidate}</h4>
                <p className="text-sm text-gray-600 mt-1">
                  {interview.date} • {interview.type}
                </p>
              </div>
              <span
                className={`px-3 py-1 text-xs font-medium rounded-full ${
                  interview.status === 'Completed'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'
                }`}
              >
                {interview.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function ActivityItem({ title, time, type }: { title: string; time: string; type: string }) {
  const icons = {
    candidate: '👤',
    interview: '🎥',
    job: '💼',
  }

  return (
    <div className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50">
      <div className="text-2xl">{icons[type as keyof typeof icons]}</div>
      <div>
        <p className="text-sm text-gray-900">{title}</p>
        <p className="text-xs text-gray-500 mt-1">{time}</p>
      </div>
    </div>
  )
}
