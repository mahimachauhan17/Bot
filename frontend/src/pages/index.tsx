import Head from 'next/head'
import Link from 'next/link'
import { useRouter } from 'next/router'

export default function Home() {
  const router = useRouter()

  return (
    <>
      <Head>
        <title>Interviewer AI Agent</title>
        <meta name="description" content="AI-powered interview platform" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Navigation */}
        <nav className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16 items-center">
              <div className="flex-shrink-0 flex items-center">
                <h1 className="text-2xl font-bold text-blue-600">Interviewer AI</h1>
              </div>
              <div className="flex space-x-4">
                <Link href="/login" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md">
                  Login
                </Link>
                <Link href="/signup" className="bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded-md">
                  Sign Up
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h1 className="text-5xl font-extrabold text-gray-900 sm:text-6xl">
              AI-Powered Interview Platform
            </h1>
            <p className="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
              Automate your interview process with AI. Generate job descriptions, parse CVs,
              conduct live video interviews, and get comprehensive candidate evaluations.
            </p>
            
            <div className="mt-10 flex justify-center space-x-4">
              <Link
                href="/recruiter/dashboard"
                className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition"
              >
                Recruiter Dashboard
              </Link>
              <Link
                href="/candidate/join"
                className="bg-white text-blue-600 px-8 py-3 rounded-lg text-lg font-semibold border-2 border-blue-600 hover:bg-blue-50 transition"
              >
                Join Interview
              </Link>
            </div>
          </div>

          {/* Features Grid */}
          <div className="mt-24 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <FeatureCard
              title="AI Job Descriptions"
              description="Generate comprehensive JDs from just a job title using GPT-4"
              icon="📝"
            />
            <FeatureCard
              title="Smart CV Parsing"
              description="Automatically extract skills, experience, and education from CVs"
              icon="📄"
            />
            <FeatureCard
              title="Live AI Interviews"
              description="Conduct video interviews where AI speaks and listens in real-time"
              icon="🎥"
            />
            <FeatureCard
              title="Intelligent Questions"
              description="Generate role-specific questions tailored to candidate profiles"
              icon="❓"
            />
            <FeatureCard
              title="Body Language Analysis"
              description="Analyze facial expressions and body language during video interviews"
              icon="👤"
            />
            <FeatureCard
              title="Comprehensive Reports"
              description="Get detailed scores, insights, and hiring recommendations"
              icon="📊"
            />
          </div>
        </main>
      </div>
    </>
  )
}

function FeatureCard({ title, description, icon }: { title: string; description: string; icon: string }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}
