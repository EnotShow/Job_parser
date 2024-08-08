import React from 'react'

import {
  CButton, CButtonGroup,
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CDropdown,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
  CForm,
  CFormCheck, CFormInput,
  CFormLabel,
  CFormSelect,
  CFormSwitch, CInputGroup, CInputGroupText,
  CRow,
} from '@coreui/react'

const Settings = () => {

  return (
    <>
      <CRow>
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardBody>
              <CRow>
                <CCol>
                  <center><h1>Settings</h1></center>
                </CCol>
              </CRow>
              <CForm className="row g-3 mt-4">
                {/* Language Selector */}
                <CCol md={12}>
                  <CFormLabel htmlFor="languageSelect">Language</CFormLabel>
                  <CFormSelect id="languageSelect" aria-label="Language select">
                    <option value="en">English</option>
                    <option value="pl">Polish</option>
                    <option value="ua">Ukrainian</option>
                    <option value="ru">Russian</option>
                  </CFormSelect>
                </CCol>

                {/* Pause Parsing Switch */}
                <CCol md={12} className="d-flex align-items-center">
                  <CFormLabel htmlFor="pauseParsingButton" className="me-4" style={{ fontSize: '1.25rem' }}>Pause Parsing</CFormLabel>
                  <CButtonGroup>
                    <CButton
                      color="primary"
                      variant="outline"
                      id="pauseParsingButton"
                      active
                      onClick={() => console.log('Parsing Paused')}
                    >
                      Pause
                    </CButton>
                    <CButton
                      color="secondary"
                      variant="outline"
                      onClick={() => console.log('Parsing Resumed')}
                    >
                      Resume
                    </CButton>
                  </CButtonGroup>
                </CCol>

                {/* Links Limit with Increase Button */}
                <CCol md={12}>
                  <CFormLabel htmlFor="linksLimit">Links Limit</CFormLabel>
                  <CInputGroup>
                    <CFormInput type="number" id="linksLimit" disabled defaultValue="25" />
                    <CInputGroupText>
                      <CButton color="primary">Increase</CButton>
                    </CInputGroupText>
                  </CInputGroup>
                </CCol>

                <CCol xs={12} className="mt-4">
                  <CButton color="primary" type="submit">Save Settings</CButton>
                </CCol>
              </CForm>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  )
}

export default Settings
