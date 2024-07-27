import React from 'react'
import Settings from "src/views/settings/Settings";

const Dashboard = React.lazy(() => import('./views/dashboard/Dashboard'))

const routes = [
  { path: '/', exact: true, name: 'Home' },
  { path: '/dashboard', name: 'Dashboard', element: Dashboard },
  { path: '/settings', name: 'Settings', element: Settings },
]

export default routes
