import React from 'react'

const Dashboard = React.lazy(() => import('./views/dashboard/Dashboard'))

const Searches = React.lazy(() => import('./views/searches/Searches'))
const SearchDetails = React.lazy(() => import('./views/searches/SearchDetails'))
const SearchEdit = React.lazy(() => import('./views/searches/SearchEdit'))

const Applications = React.lazy(() => import('./views/applications/Applications'))
const ApplicationDetails = React.lazy(() => import('./views/applications/ApplicationDetails'))
const ApplicationEdit = React.lazy(() => import('./views/applications/ApplicationEdit'))

const Profile = React.lazy(() => import('./views/profile/Profile'))
const Settings = React.lazy(() => import('./views/settings/Settings'))

const Login = React.lazy(() => import('./views/pages/login/Login'))
const Register = React.lazy(() => import('./views/pages/register/Register'))
const NotFound = React.lazy(() => import('./views/pages/page404/Page404'))
const Page500 = React.lazy(() => import('./views/pages/page500/Page500'))



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

  { path: '/profile', name: 'Profile', element: Profile },
  { path: '/settings', name: 'Settings', element: Settings },

  { path: '/login', name: 'Login', element: Login },
  { path: '/register', name: 'Register', element: Register },
  { path: '/404', name: 'Page404', element: NotFound },
  { path: '/500', name: 'Page500', element: Page500 },
]

export default routes
