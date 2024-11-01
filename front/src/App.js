import React, { Suspense, useEffect } from 'react'
import {BrowserRouter, Route, Routes} from 'react-router-dom'
import { useSelector } from 'react-redux'

import { CSpinner, useColorModes } from '@coreui/react'
import './scss/style.scss'
import ProtectedRoute from "src/helpers/ProtectedRouter";
import {ROUTES} from "src/routes";
import LoginByHash from "src/views/pages/login/LoginByHash";

// Containers
const DefaultLayout = React.lazy(() => import('./layout/DefaultLayout'))

// Pages
const Login = React.lazy(() => import('./views/pages/login/Login'))
const Register = React.lazy(() => import('./views/pages/register/Register'))
const Page404 = React.lazy(() => import('./views/pages/page404/Page404'))
const Page500 = React.lazy(() => import('./views/pages/page500/Page500'))

const App = () => {
  const { isColorModeSet, setColorMode } = useColorModes('coreui-free-react-admin-template-theme')
  const storedTheme = useSelector((state) => state.theme)

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.href.split('?')[1])
    const theme = urlParams.get('theme') && urlParams.get('theme').match(/^[A-Za-z0-9\s]+/)[0]
    if (theme) {
      setColorMode(theme)
    }

    if (isColorModeSet()) {
      return
    }

    setColorMode(storedTheme)
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <BrowserRouter>
      <Suspense
        fallback={
          <div className="pt-3 text-center">
            <CSpinner color="primary" variant="grow" />
          </div>
        }
      >
        <Routes>
          <Route exact path={ROUTES.LOGIN_BY_HASH} name="Login By Hash" element={<LoginByHash />} />
          <Route exact path={ROUTES.LOGIN} name="Login Page" element={<Login />} />

          <Route exact path={ROUTES.REGISTER} name="Register Page" element={<Register />} />
          <Route exact path={ROUTES.NOT_FOUND} name="Page 404" element={<Page404 />} />
          <Route exact path={ROUTES.SERVER_ERROR} name="Page 500" element={<Page500 />} />
          <Route path="*" name="Home" element={<ProtectedRoute element={<DefaultLayout />} />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}

export default App
