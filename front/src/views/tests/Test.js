import React from 'react'
import {formatRoute} from "react-router-named-routes/lib";
import dotenv from  'dotenv'
import {
  CAvatar, CButton,
  CCard,
  CCardBody,
  CCol, CForm, CFormCheck, CFormInput, CFormSelect,
  CRow,
} from '@coreui/react'
import {ROUTES} from "src/routes";
import {Link} from "react-router-dom";

const Test = () => {
  const baseUrl = import.meta.env.VITE_BASE_URL
  console.log(baseUrl)

  return (
    <>
      <div>
        <h1>Some title</h1>
        {<div><Link to={formatRoute(ROUTES.HOME)}>Home</Link></div>}
        {<div><Link to={formatRoute(ROUTES.LOGIN)}>Login</Link></div>}
        {<div><Link to={formatRoute(ROUTES.REGISTER)}>Register</Link></div>}
        {<div><Link to={formatRoute(ROUTES.DASHBOARD)}>Dashboard</Link></div>}
        {<div><Link to={formatRoute(ROUTES.APPLICATIONS)}>Applications</Link></div>}
        {<div><Link to={formatRoute(ROUTES.APPLICATION_DETAILS, {application_id: 1})}>Test</Link></div>}


      </div>
    </>
  )
}

export default Test
