import React, {useState} from 'react'

import {
  CButton,
  CButtonGroup,
  CCard,
  CCardBody,
  CCol,
  CForm,
  CFormInput, CFormLabel,
  CRow,
} from '@coreui/react'
import DeleteModal from "src/views/_DeleteModal";

const ApplicationEdit = () => {
  const [visible, setVisible] = useState(false)

  const handleDelete = () => {
    console.log("Item deleted");
  };

  return (
    <>
      <DeleteModal model="application" visible={visible} setVisible={setVisible} onDelete={handleDelete} />

      <CRow>
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardBody>
              <center><h1>Search Details</h1></center>
              <CForm className="row g-3">
                <CRow className="mb-3">
                <CFormLabel htmlFor="staticTitle" className="col-sm-2 col-form-label">Title</CFormLabel>
                <CCol sm={10}>
                  <CFormInput type="text" id="staticTitle" defaultValue="Some search title"/>
                </CCol>
              </CRow>
              <CRow className="mb-3">
                <CFormLabel htmlFor="staticUrl" className="col-sm-2 col-form-label">Url</CFormLabel>
                <CCol sm={10}>
                  <CFormInput type="text" id="staticUrl" defaultValue="https://searchurl.com/jobs"/>
                </CCol>
              </CRow>
              <CRow className="mb-3">
                <CFormLabel htmlFor="staticCreatedAt" className="col-sm-2 col-form-label">Created at</CFormLabel>
                <CCol sm={10}>
                  <CFormInput type="text" id="staticCreatedAt" defaultValue="2022-01-01"/>
                </CCol>
              </CRow>
              <CCol xs={12}>
              <CButtonGroup>
                <CButton color="primary" type="submit">Save</CButton>
                <CButton color="secondary">Back</CButton>
                <CButton color="danger" onClick={() => setVisible(true)}>Delete</CButton>
              </CButtonGroup>
              </CCol>
              </CForm>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  )
}

export default ApplicationEdit
