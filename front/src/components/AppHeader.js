import React, { useState, useEffect, useRef } from 'react';
import { NavLink } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import {
  CContainer,
  CDropdown,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
  CHeader,
  CHeaderNav,
  CHeaderToggler,
  CNavLink,
  CNavItem,
  useColorModes,
  CBadge,
} from '@coreui/react';
import CIcon from '@coreui/icons-react';
import {
  cilBell,
  cilContrast,
  cilEnvelopeOpen,
  cilList,
  cilMenu,
  cilMoon,
  cilSun,
} from '@coreui/icons';

import { AppBreadcrumb } from './index';
import { AppHeaderDropdown } from './header/index';
import { formatRoute } from "react-router-named-routes/lib";
import { ROUTES } from "src/routes";

const AppHeader = () => {
  const headerRef = useRef();
  const { colorMode, setColorMode } = useColorModes('coreui-free-react-admin-template-theme');
  const dispatch = useDispatch();
  const sidebarShow = useSelector((state) => state.sidebarShow);

  const [unreadNotifications, setUnreadNotifications] = useState([
    { id: 1, type: 'success', title: 'New Comment', message: 'You have a new comment on your post.', time: '5 mins ago' },
    { id: 2, type: 'warning', title: 'New Like', message: 'Someone liked your post.', time: '10 mins ago' },
    { id: 3, type: 'danger', title: 'New Follower', message: 'You have a new follower.', time: '15 mins ago' },
    // Add more notifications as needed
  ]);

  useEffect(() => {
    document.addEventListener('scroll', () => {
      headerRef.current &&
        headerRef.current.classList.toggle('shadow-sm', document.documentElement.scrollTop > 0);
    });
  }, []);

  const borderClasses = {
    success: 'border-success',
    warning: 'border-warning',
    danger: 'border-danger',
    info: 'border-info',
    primary: 'border-primary',
  };

  return (
    <CHeader position="sticky" className="mb-4 p-0" ref={headerRef}>
      <CContainer className="border-bottom px-4" fluid>
        <CHeaderToggler
          onClick={() => dispatch({ type: 'set', sidebarShow: !sidebarShow })}
          style={{ marginInlineStart: '-14px' }}
        >
          <CIcon icon={cilMenu} size="lg" />
        </CHeaderToggler>
        <CHeaderNav className="d-none d-md-flex">
          <CNavItem>
            <CNavLink to={formatRoute(ROUTES.DASHBOARD)} as={NavLink}>
              Dashboard
            </CNavLink>
          </CNavItem>
          <CNavItem>
            <CNavLink to={formatRoute(ROUTES.PROFILE)} as={NavLink}>
              Profile
            </CNavLink>
          </CNavItem>
          <CNavItem>
            <CNavLink to={formatRoute(ROUTES.SETTINGS)} as={NavLink}>
              Settings
            </CNavLink>
          </CNavItem>
        </CHeaderNav>
        <CHeaderNav className="ms-auto">
          <CNavItem>
            <CDropdown variant="nav-item" placement="bottom-end">
              <CDropdownToggle caret={false}>
                <CIcon icon={cilBell} size="lg" />
                {unreadNotifications.length > 0 && (
                  <CBadge color="danger" shape="rounded-pill">
                    {unreadNotifications.length}
                  </CBadge>
                )}
              </CDropdownToggle>
              <CDropdownMenu>
                {unreadNotifications.length === 0 ? (
                  <CDropdownItem disabled>No new notifications</CDropdownItem>
                ) : (
                  unreadNotifications.map((notification) => (
                    <CDropdownItem
                      key={notification.id}
                      className={`border ${borderClasses[notification.type]} mb-2`}
                      style={{ transition: 'border-color 0.3s ease' }}
                      onMouseEnter={(e) => e.currentTarget.classList.add('shadow-sm')}
                      onMouseLeave={(e) => e.currentTarget.classList.remove('shadow-sm')}
                    >
                      <strong>{notification.title}</strong>
                      <div className="small text-muted">{notification.message}</div>
                      <div className="small text-muted">{notification.time}</div>
                    </CDropdownItem>
                  ))
                )}
                <CDropdownItem to={formatRoute(ROUTES.NOTIFICATIONS)} as={NavLink}>See all notifications</CDropdownItem>
              </CDropdownMenu>
            </CDropdown>
          </CNavItem>
        </CHeaderNav>
        <CHeaderNav>
          <li className="nav-item py-1">
            <div className="vr h-100 mx-2 text-body text-opacity-75"></div>
          </li>
          <CDropdown variant="nav-item" placement="bottom-end">
            <CDropdownToggle caret={false}>
              {colorMode === 'dark' ? (
                <CIcon icon={cilMoon} size="lg" />
              ) : colorMode === 'auto' ? (
                <CIcon icon={cilContrast} size="lg" />
              ) : (
                <CIcon icon={cilSun} size="lg" />
              )}
            </CDropdownToggle>
            <CDropdownMenu>
              <CDropdownItem
                active={colorMode === 'light'}
                className="d-flex align-items-center"
                as="button"
                type="button"
                onClick={() => setColorMode('light')}
              >
                <CIcon className="me-2" icon={cilSun} size="lg" /> Light
              </CDropdownItem>
              <CDropdownItem
                active={colorMode === 'dark'}
                className="d-flex align-items-center"
                as="button"
                type="button"
                onClick={() => setColorMode('dark')}
              >
                <CIcon className="me-2" icon={cilMoon} size="lg" /> Dark
              </CDropdownItem>
              <CDropdownItem
                active={colorMode === 'auto'}
                className="d-flex align-items-center"
                as="button"
                type="button"
                onClick={() => setColorMode('auto')}
              >
                <CIcon className="me-2" icon={cilContrast} size="lg" /> Auto
              </CDropdownItem>
            </CDropdownMenu>
          </CDropdown>
          <li className="nav-item py-1">
            <div className="vr h-100 mx-2 text-body text-opacity-75"></div>
          </li>
          <AppHeaderDropdown />
        </CHeaderNav>
      </CContainer>
      <CContainer className="px-4" fluid>
        <AppBreadcrumb />
      </CContainer>
    </CHeader>
  );
};

export default AppHeader;
