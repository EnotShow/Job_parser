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

const Test = React.lazy(() => import('./views/tests/Test'))

const routes = [
  { path: '/', exact: true, name: 'Home' },

  { path: '/dashboard', name: 'Dashboard', element: Dashboard, protected: true },

  // searches
  { path: '/searches', name: 'Searches', element: Searches },
  { path: '/searches/:id', name: 'Get_Search', element: SearchDetails, protected: true },
  { path: '/searches/:id/edit', name: 'Edit_Searches', element: SearchEdit, protected: true },

  // applications
  { path: '/applications/my-applications', name: 'User_Applications', element: Applications, protected: true },
  { path: '/applications/all-applications', name: 'Applications', element: Applications, protected: true },
  { path: '/applications/:id', name: 'Get_Application', element: ApplicationDetails, protected: true },
  { path: '/applications/:id/edit', name: 'Edit_Application', element: ApplicationEdit, protected: true },

  { path: '/profile', name: 'Profile', element: Profile, protected: true },
  { path: '/settings', name: 'Settings', element: Settings, protected: true },

  { path: '/login', name: 'Login', element: Login },
  { path: '/register', name: 'Register', element: Register },
  { path: '/404', name: 'Page404', element: NotFound },
  { path: '/500', name: 'Page500', element: Page500 },

  { path: '/test', name: 'Test', element: Test },
]

export const ROUTES = {
  HOME : "/",

  DASHBOARD : "/dashboard",

  SEARCHES : "/searches",
  SEARCH_DETAILS : "/searches/:id",
  SEARCH_EDIT : "/searches/:id/edit",

  APPLICATIONS : "/applications",
  APPLICATION_DETAILS : "/applications/:id",
  APPLICATION_EDIT : "/applications/:id/edit",

  PROFILE : "/profile",
  SETTINGS : "/settings",

  LOGIN : "/login",
  REGISTER : "/register",
  NOT_FOUND : "/404",
  SERVER_ERROR : "/500",
}

export default routes
