import React, {useState} from 'react'

import {
  CAvatar, CButton,
  CCard,
  CCardBody,
  CCol, CForm, CFormCheck, CFormInput, CFormSelect,
  CRow,
} from '@coreui/react'

const Profile = () => {

  return (
    <>
  <CRow>
    <CCol xs={12}>
      <CCard className="mb-4">
        <CCardBody>
          <CRow>
            <CCol>
              <center><h1>Profile</h1></center>
            </CCol>
          </CRow>
          <CRow className="justify-content-center my-3">
            <CAvatar color="primary" textColor="white" shape="rounded" size="xl">IK</CAvatar>
          </CRow>
          <CRow className="justify-content-center my-2">
            <CCol xs="auto">
              <CButton color="primary">Change Picture</CButton>
            </CCol>
          </CRow>
          <CForm className="row g-3">
            <CCol md={6}>
              <CFormInput type="name" id="inputName" label="Name" />
            </CCol>
            <CCol md={6}>
              <CFormInput type="lastname" id="inputLastname" label="Lastname" />
            </CCol>
            <CCol xs={12}>
              <CFormInput id="inputEmail" label="Email" placeholder="example@mail.com"/>
            </CCol>
            <CCol xs={12}>
              <CButton color="primary" type="submit">Save Changes</CButton>
            </CCol>
          </CForm>
        </CCardBody>
      </CCard>
    </CCol>
  </CRow>
</>

  )
}

export default Profile
