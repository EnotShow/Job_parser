import React from 'react'
import CIcon from '@coreui/icons-react'
import {
  cilSettings,
  cilSearch,
  cilPencil,
  cilNotes,
  cilSpeedometer,
  cilStar, cilCreditCard, cilBell,
} from '@coreui/icons'
import { CNavGroup, CNavItem, CNavTitle } from '@coreui/react'

const _nav = [
  {
    component: CNavItem,
    name: 'Dashboard',
    to: '/dashboard',
    icon: <CIcon icon={cilSpeedometer} customClassName="nav-icon" />,
    // badge: {
    //   color: 'info',
    //   text: 'NEW',
    // },
  },
  {
    component: CNavItem,
    name: 'AdminDashboard',
    to: '/admin/dashboard',
    icon: <CIcon icon={cilSpeedometer} customClassName="nav-icon" />,
    badge: {
      color: 'info',
      text: 'NEW',
    },
  },
  {
    component: CNavItem,
    name: 'My Searches',
    to: '/searches',
    icon: <CIcon icon={cilSearch} customClassName="nav-icon" />,
  },
  {
    component: CNavGroup,
    name: 'Applications',
    to: '/applications',
    icon: <CIcon icon={cilNotes} customClassName="nav-icon" />,
    items: [
      {
        component: CNavItem,
        name: 'My Applications',
        to: '/applications/my-applications',
        icon: <CIcon icon={cilStar} customClassName="nav-icon" />,
      },
      {
        component: CNavItem,
        name: 'All Applications',
        to: '/applications/all-applications',
        icon: <CIcon icon={cilPencil} customClassName="nav-icon" />,
      },
    ],
  },
  {
    component: CNavTitle,
    name: 'Settings',
  },
  {
    component: CNavItem,
    name: 'Profile',
    to: '/profile',
    icon: <CIcon icon={cilPencil} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Settings',
    to: '/settings',
    icon: <CIcon icon={cilSettings} customClassName="nav-icon" />,
  },

  {
    component: CNavTitle,
    name: 'Temporary',
  },
  {
    component: CNavItem,
    name: 'Subscriptions',
    to: '/subscriptions',
    icon: <CIcon icon={cilCreditCard} customClassName="nav-icon" />,
  },
  {
    component: CNavGroup,
    name: 'Temporary Applications',
    to: '/applications',
    icon: <CIcon icon={cilNotes} customClassName="nav-icon" />,
    items: [
      {
        component: CNavItem,
        name: 'Notifications',
        to: '/notifications',
        icon: <CIcon icon={cilBell} customClassName="nav-icon" />,
      },
      {
        component: CNavItem,
        name: 'Application Details',
        to: '/applications/{application_id}',
        icon: <CIcon icon={cilPencil} customClassName="nav-icon" />,
      },
      {
        component: CNavItem,
        name: 'Application Edit',
        to: '/applications/{application_id}/edit',
        icon: <CIcon icon={cilPencil} customClassName="nav-icon" />
      }
    ],
  },
  {
    component: CNavGroup,
    name: 'Temporary Searches',
    to: '/searches',
    icon: <CIcon icon={cilNotes} customClassName="nav-icon" />,
    items: [
      {
        component: CNavItem,
        name: 'Search Details',
        to: '/searches/{search_id}',
        icon: <CIcon icon={cilPencil} customClassName="nav-icon" />,
      },
      {
        component: CNavItem,
        name: 'Search Edit',
        to: '/searches/{search_id}/edit',
        icon: <CIcon icon={cilPencil} customClassName="nav-icon" />
      }
    ],
  },
  {
    component: CNavItem,
    name: 'Login',
    to: '/login',
    icon: <CIcon icon={cilStar} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Sign Up',
    to: '/register',
    icon: <CIcon icon={cilStar} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: '404',
    to: '/404',
    icon: <CIcon icon={cilStar} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: '500',
    to: '/500',
    icon: <CIcon icon={cilStar} customClassName="nav-icon" />,
  }
]

export default _nav
