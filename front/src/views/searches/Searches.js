import React, {useState} from 'react'

import {
  CButton, CButtonGroup,
  CCard,
  CCardBody,
  CCol, CPagination, CPaginationItem,
  CRow, CTable,
} from '@coreui/react'
import DeleteModal from "src/views/_DeleteModal";

const Searches = () => {
  const [visible, setVisible] = useState(false)

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
    key: 'url',
    label: 'URL',
    _props: { scope: 'col' },
  },
  {
    key: 'created_at',
    label: 'Created at',
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
      url: 'https://google.com',
      created_at: '2022-01-01',
      actions: (
        <>
        <CRow>
        <CButtonGroup>
        <CButton color="primary" onClick={() => alert('Button 2 clicked')}>
        Edit
        </CButton>
        <CButton color="primary" onClick={() => alert('Button 2 clicked')}>
        Details
        </CButton>
        <CButton color="danger" onClick={() => setVisible(true)}>
        Delete
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

  const handleDelete = () => {
    console.log("Item deleted");
  };

  return (
    <>
      <DeleteModal model="search" visible={visible} setVisible={setVisible} onDelete={handleDelete} />

      <CRow>
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardBody>
              <center><h1>Searches</h1></center>
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

export default Searches
