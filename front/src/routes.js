import React from 'react'

const Dashboard = React.lazy(() => import('./views/dashboard/Dashboard'))

const Searches = React.lazy(() => import('./views/searches/Searches'))
const SearchDetails = React.lazy(() => import('./views/searches/SearchDetails'))
const SearchEdit = React.lazy(() => import('./views/searches/SearchEdit'))

const Applications = React.lazy(() => import('./views/applications/Applications'))
const ApplicationDetails = React.lazy(() => import('./views/applications/ApplicationDetails'))
const ApplicationEdit = React.lazy(() => import('./views/applications/ApplicationEdit'))

const Settings = React.lazy(() => import('./views/settings/Settings'))



const routes = [
  { path: '/', exact: true, name: 'Home' },
  { path: '/dashboard', name: 'Dashboard', element: Dashboard },

  // searches
  { path: '/searches', name: 'Searches', element: Searches },
  { path: '/searches/{search_id}', name: 'Searches', element: SearchDetails },
  { path: '/searches/{search_id}/edit', name: 'Searches', element: SearchEdit },

  // applications
  { path: '/applications/my-applications', name: 'My Applications', element: Applications },
  { path: '/applications/all-applications', name: 'All Applications', element: Applications },
  { path: '/applications/{application_id}', name: 'Applications', element: ApplicationDetails },
  { path: '/applications/{application_id}/edit', name: 'Applications', element: ApplicationEdit },

  { path: '/settings', name: 'Settings', element: Settings },
]

export default routes
