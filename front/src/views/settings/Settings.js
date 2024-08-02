import React from 'react'

import {
  CButton,
  CCard,
  CCardBody,
  CCardHeader,
  CCol, CDropdown, CDropdownItem, CDropdownMenu, CDropdownToggle, CFormCheck, CFormSelect, CFormSwitch,
  CRow,
} from '@coreui/react'

const Settings = () => {

  return (
    <>
      <CRow>
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardHeader>Settings</CCardHeader>
            <CCardBody>
              <CFormCheck id="flexCheckDefault" label="Default checkbox"/>
              <CFormCheck id="flexCheckChecked" label="Checked checkbox" defaultChecked />
              <CFormSwitch label="Default switch checkbox input" id="formSwitchCheckDefault"/>
              <CFormSwitch label="Checked switch checkbox input" id="formSwitchCheckChecked" defaultChecked/>
              <CFormSelect id="inputState" label="State">
                <option>Choose...</option>
                <option>...</option>
              </CFormSelect>
              <CRow>
                <CCol>
                  <CButton color="primary">Save</CButton>
                </CCol>
              </CRow>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  )
}

export default Settings
