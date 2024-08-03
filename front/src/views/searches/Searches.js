import React, { useState, useEffect } from 'react';
import {
  CButton, CButtonGroup,
  CCard,
  CCardBody,
  CCol, CFormInput, CInputGroup, CPagination, CPaginationItem,
  CRow, CTable,
} from '@coreui/react';
import DeleteModal from 'src/views/_DeleteModal';
import jobParserClient from 'src/client/BaseClient';
import {useNavigate} from "react-router-dom";

const Searches = () => {
  const navigate = useNavigate();
  const [visible, setVisible] = useState(false);
  const [items, setItems] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = await jobParserClient.searches.getSearches();
      setItems(generateItems(data.items));
    };

    fetchData();
  }, []);

  const generateItems = (data) => {
    return data.map((item) => ({
      id: item.id,
      title: item.title,
      url: item.url,
      created_at: item.created_at,
      actions: (
        <>
          <CRow>
            <CButtonGroup>
              <CButton color="primary" onClick={(event) => navigate(event.id)}>
                Details
              </CButton>
              <CButton color="primary" onClick={() => alert('Edit clicked')}>
                Edit
              </CButton>
              <CButton color="danger" onClick={() => setVisible(true)}>
                Delete
              </CButton>
            </CButtonGroup>
          </CRow>
        </>
      ),
      _cellProps: { id: { scope: 'row' } },
    }));
  };

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
  ];

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
              <CInputGroup className="mb-3">
                <CFormInput placeholder="Recipient's username" aria-label="Recipient's username" aria-describedby="button-addon2" />
                <CButton type="button" color="secondary" variant="outline" id="button-addon2">Button</CButton>
              </CInputGroup>
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
  );
};

export default Searches;
