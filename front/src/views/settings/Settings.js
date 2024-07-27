import React from 'react'
import classNames from 'classnames'

import {
  CAvatar,
  CButton,
  CButtonGroup,
  CCard,
  CCardBody,
  CCardFooter,
  CCardHeader,
  CCol, CDropdown, CDropdownItem, CDropdownMenu, CDropdownToggle, CFormCheck, CFormSwitch,
  CProgress,
  CRow,
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import {
  cibCcAmex,
  cibCcApplePay,
  cibCcMastercard,
  cibCcPaypal,
  cibCcStripe,
  cibCcVisa,
  cibGoogle,
  cibFacebook,
  cibLinkedin,
  cifBr,
  cifEs,
  cifFr,
  cifIn,
  cifPl,
  cifUs,
  cibTwitter,
  cilCloudDownload,
  cilPeople,
  cilUser,
  cilUserFemale,
} from '@coreui/icons'

import avatar1 from 'src/assets/images/avatars/1.jpg'
import avatar2 from 'src/assets/images/avatars/2.jpg'
import avatar3 from 'src/assets/images/avatars/3.jpg'
import avatar4 from 'src/assets/images/avatars/4.jpg'
import avatar5 from 'src/assets/images/avatars/5.jpg'

import WidgetsBrand from '../widgets/WidgetsBrand'
import WidgetsDropdown from '../widgets/WidgetsDropdown'

const Dashboard = () => {

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

export default Dashboard
