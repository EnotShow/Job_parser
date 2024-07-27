import React from 'react'

import {
  CButton,
  CCard,
  CCardBody,
  CCardHeader,
  CCol, CDropdown, CDropdownItem, CDropdownMenu, CDropdownToggle, CFormCheck, CFormSwitch,
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
              <CDropdown>
              <CDropdownToggle color={'background-color'} style={{ border: '1px solid black' }}>Selected language: English</CDropdownToggle>
              <CDropdownMenu>
                <CDropdownItem href="#">English</CDropdownItem>
                <CDropdownItem href="#">Polish</CDropdownItem>
                <CDropdownItem href="#">Russian</CDropdownItem>
              </CDropdownMenu>
            </CDropdown>
            </CCardBody>
          </CCard>
            <CButton color="primary">Save</CButton>
        </CCol>
      </CRow>
    </>
  )
}

export default Settings
