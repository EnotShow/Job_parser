import React from 'react'
import Settings from "src/views/settings/Settings";
import Applications from "src/views/applications/Applications";
import Searches from "src/views/searches/Searches";

const Dashboard = React.lazy(() => import('./views/dashboard/Dashboard'))

const routes = [
  { path: '/', exact: true, name: 'Home' },
  { path: '/dashboard', name: 'Dashboard', element: Dashboard },

  // searches
  { path: '/searches', name: 'Searches', element: Searches },

  // applications
  { path: '/applications/my-applications', name: 'My Applications', element: Applications },
  { path: '/applications/all-applications', name: 'All Applications', element: Applications },

  { path: '/settings', name: 'Settings', element: Settings },
]

export default routes
