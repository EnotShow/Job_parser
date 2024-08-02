import React from 'react'
import dotenv from  'dotenv'
import {
  CAvatar, CButton,
  CCard,
  CCardBody,
  CCol, CForm, CFormCheck, CFormInput, CFormSelect,
  CRow,
} from '@coreui/react'

const Test = () => {
  const baseUrl = import.meta.env.VITE_BASE_URL
  console.log(baseUrl)

  return (
    <>
      <h1>Some title</h1>
      {baseUrl}

    </>
  )
}

export default Test
