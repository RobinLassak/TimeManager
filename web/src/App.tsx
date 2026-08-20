import { useState } from 'react'

import Dashboard from './pages/Dashboard'
import Customers from './pages/Customers'
import Projects from './pages/Projects'
import Works from './pages/Works'

function App() {
  const [page, setPage] = useState('dashboard')

  return (
    <div className="flex h-screen flex-col">
      <header className="h-14 shrink-0 border-b border-slate-200 bg-gray-300">
        {/* Zatim prazdny navbar */}
      </header>
      <div className="flex min-h-0 flex-1 bg-gray-200">
        <aside className="w-64 shrink-0 border-r border-slate-200">
          <nav className="flex flex-col gap-2 mt-6 ml-3 mr-3">
            <button
            type='button'
            onClick={() => setPage('dashboard')}
            className={`rounded px-3 py-2 text-left ${
                page === 'dashboard' ? 'bg-white font-semibold' : ''
              }`}
            >
              Dashboard
            </button>
            <button
            type='button'
            onClick={() => setPage('customers')}
            className={`rounded px-3 py-2 text-left ${
                page === 'customers' ? 'bg-white font-semibold' : ''
              }`}
            >
              Customers
            </button>
            <button
            type='button'
            onClick={() => setPage('projects')}
            className={`rounded px-3 py-2 text-left ${
                page === 'projects' ? 'bg-white font-semibold' : ''
              }`}
            >
              Projects
            </button>
            <button
            type='button'
            onClick={() => setPage('works')}
            className={`rounded px-3 py-2 text-left ${
                page === 'works' ? 'bg-white font-semibold' : ''
              }`}
            >
              Works
            </button>
          </nav>
        </aside>
        <main className="flex-1 overflow-auto bg-slate-100 p-6 bg-white">
          {page === 'dashboard' && <Dashboard />}
          {page === 'customers' && <Customers />}
          {page === 'projects' && <Projects />}
          {page === 'works' && <Works />}
        </main>
      </div>
    </div>
  )
}

export default App
