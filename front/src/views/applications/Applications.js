import React, {useState} from 'react'

import {
  CButton,
  CButtonGroup,
  CCard,
  CCardBody,
  CCol,
  CDropdown,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle, CFormInput, CInputGroup,
  CPagination,
  CPaginationItem,
  CRow,
  CTable,
} from '@coreui/react'

const Applications = () => {
  const columns = [
  {
    key: 'id',
    label: '#',
    _props: { scope: 'col' },
  },
  {
    key: 'title',
    label: 'Title',
    _props: { scope: 'col' },
  },
  {
    key: 'description',
    label: 'Description',
    _props: { scope: 'col' },
  },
  {
    key: 'finded_date',
    label: 'Finded',
    _props: { scope: 'col' },
  },
  {
    key: 'application_date',
    label: 'Application date',
    _props: { scope: 'col' },
  },
  {
    key: 'applied',
    label: 'Applied',
    _props: { scope: 'col' },
  },
  {
    key: 'actions',
    label: 'Actions',
    _props: { scope: 'col' },
  },
]
  const items = [
    {
      id: 1,
      title: 'Title',
      description: 'Description',
      finded_date: '07-01-2004',
      application_date: '07-01-2004',
      applied: 'Applied',
      actions: (
        <>
        <CRow>
        <CButtonGroup>
        <CButton color="primary" onClick={() => alert('Button 2 clicked')}>
        Apply
        </CButton>
        <CButton color="primary" onClick={() => alert('Button 2 clicked')}>
        Details
        </CButton>
        </CButtonGroup>
        </CRow>
        </>
      ),
      _cellProps: {id: {scope: 'row', },},
    },
  ]

  for (let i = 2; i <= 10; i++) {
    let item = { ...items[0] }
    item.id = i
    items.push(item)
  }

  return (
    <>
      <CRow>
        <CCol xs={12}>
          <CCard className="items">
            <CCardBody>
              <CInputGroup className="mb-3">
                <CFormInput placeholder="Recipient's username" aria-label="Recipient's username" aria-describedby="button-addon2"/>
                <CButton type="button" color="secondary" variant="outline" id="button-addon2">Button</CButton>
              </CInputGroup>
              <CRow>
              <CCol xs={3} md={3} style={{ display: 'flex' }}>
              <CDropdown>
                <CDropdownToggle color={'background-color'} style={{ border: '1px solid black' }}>Selected language: English</CDropdownToggle>
                <CDropdownMenu>
                  <CDropdownItem href="#">English</CDropdownItem>
                  <CDropdownItem href="#">Polish</CDropdownItem>
                  <CDropdownItem href="#">Russian</CDropdownItem>
                </CDropdownMenu>
              </CDropdown>

              <CDropdown>
                <CDropdownToggle color={'background-color'} style={{ border: '1px solid black' }}>Selected language: English</CDropdownToggle>
                <CDropdownMenu>
                  <CDropdownItem href="#">English</CDropdownItem>
                  <CDropdownItem href="#">Polish</CDropdownItem>
                  <CDropdownItem href="#">Russian</CDropdownItem>
                </CDropdownMenu>
              </CDropdown>

              <CDropdown>
                <CDropdownToggle color={'background-color'} style={{ border: '1px solid black' }}>Selected language: English</CDropdownToggle>
                <CDropdownMenu>
                  <CDropdownItem href="#">English</CDropdownItem>
                  <CDropdownItem href="#">Polish</CDropdownItem>
                  <CDropdownItem href="#">Russian</CDropdownItem>
                </CDropdownMenu>
              </CDropdown>
              </CCol>
              </CRow>
              <center><h1>Applications</h1></center>
              <CTable columns={columns} items={items} />
              <CPagination aria-label="Page navigation example">
                <CPaginationItem aria-label="Previous" disabled>
                  <span aria-hidden="true">&laquo;</span>
                </CPaginationItem>
                <CPaginationItem active>1</CPaginationItem>
                <CPaginationItem>2</CPaginationItem>
                <CPaginationItem>3</CPaginationItem>
                <CPaginationItem aria-label="Next">
                  <span aria-hidden="true">&raquo;</span>
                </CPaginationItem>
              </CPagination>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  )
}

export default Applications
