import React from 'react';
import SearchCreate from "src/views/searches/SearchCreate";
import AdminDashboard from "src/views/dashboard/AdminDashboard";

const Dashboard = React.lazy(() => import('./views/dashboard/Dashboard'));

const Searches = React.lazy(() => import('./views/searches/Searches'));
const SearchDetails = React.lazy(() => import('./views/searches/SearchDetails'));
const SearchEdit = React.lazy(() => import('./views/searches/SearchEdit'));

const SmartEditor = React.lazy(() => import('./views/smart_editor/SmartEditor'));

const Applications = React.lazy(() => import('./views/applications/Applications'));
const ApplicationDetails = React.lazy(() => import('./views/applications/ApplicationDetails'));

const Profile = React.lazy(() => import('./views/profile/Profile'));
const Settings = React.lazy(() => import('./views/settings/Settings'));
const Subscriptions = React.lazy(() => import('./views/subscriptions/Subscriptions'));
const Notifications = React.lazy(() => import('./views/notifications/Notifications'));

const Login = React.lazy(() => import('./views/pages/login/Login'));
const LoginByHash = React.lazy(() => import('./views/pages/login/LoginByHash'));
const Register = React.lazy(() => import('./views/pages/register/Register'));
const NotFound = React.lazy(() => import('./views/pages/page404/Page404'));
const Page500 = React.lazy(() => import('./views/pages/page500/Page500'));

const ROUTES = {
  HOME: "/",

  DASHBOARD: "/dashboard",
  ADMIN_DASHBOARD: "/admin/dashboard",

  SEARCHES: "/searches",
  SEARCH_DETAILS: "/searches/:id",
  SEARCH_EDIT: "/searches/:id/edit",
  SEARCH_CREATE: "/searches/create",

  SMART_EDITOR: "/smart-editor",

  APPLICATIONS: "/applications",
  APPLICATIONS_LIST: "/applications/all-applications",
  APPLICATIONS_SELF_LIST: "/applications/my-applications",
  APPLICATION_DETAILS: "/applications/:id",

  PROFILE: "/profile",
  SETTINGS: "/settings",
  SUBSCRIPTIONS: "/subscriptions",
  NOTIFICATIONS: "/notifications",

  LOGIN: "/login",
  LOGIN_BY_HASH: "/login/:hash",
  REGISTER: "/register",
  NOT_FOUND: "/404",
  SERVER_ERROR: "/500",
};

const routeConfig = [
  { path: ROUTES.HOME, exact: true, name: 'Home' },

  { path: ROUTES.DASHBOARD, name: 'Dashboard', element: Dashboard, protected: true },
  { path: ROUTES.ADMIN_DASHBOARD, name: 'Admin Dashboard', element: AdminDashboard, protected: true },

  // searches
  { path: ROUTES.SEARCHES, name: 'Searches', element: Searches },
  { path: ROUTES.SEARCH_DETAILS, name: 'Get Search', element: SearchDetails, protected: true },
  { path: ROUTES.SEARCH_EDIT, name: 'Edit Searches', element: SearchEdit, protected: true },
  { path: ROUTES.SEARCH_CREATE, name: 'Create Search', element: SearchCreate, protected: true },

  // smart editor
  { path: ROUTES.SMART_EDITOR, name: 'Smart Editor', element: SmartEditor, protected: true },

  // applications
  { path: ROUTES.APPLICATIONS_SELF_LIST, name: 'User Applications', element: Applications, protected: true },
  { path: ROUTES.APPLICATIONS_LIST, name: 'Applications', element: Applications, protected: true },
  { path: ROUTES.APPLICATION_DETAILS, name: 'Get Application', element: ApplicationDetails, protected: true },

  { path: ROUTES.PROFILE, name: 'Profile', element: Profile, protected: true },
  { path: ROUTES.SETTINGS, name: 'Settings', element: Settings, protected: true },
  { path: ROUTES.SUBSCRIPTIONS, name: 'Subscriptions', element: Subscriptions, protected: true },
  { path: ROUTES.NOTIFICATIONS, name: 'Notifications', element: Notifications, protected: true },

  { path: ROUTES.LOGIN, name: 'Login', element: Login },
  { path: ROUTES.LOGIN_BY_HASH, name: 'LoginByHash', element: LoginByHash },
  { path: ROUTES.REGISTER, name: 'Register', element: Register },
  { path: ROUTES.NOT_FOUND, name: 'Page404', element: NotFound },
  { path: ROUTES.SERVER_ERROR, name: 'Page500', element: Page500 },

];

export { ROUTES, routeConfig as default };

