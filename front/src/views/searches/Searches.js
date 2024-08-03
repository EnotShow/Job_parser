import React, { useState, useEffect } from 'react';
import {
  CButton,
  CButtonGroup,
  CCard,
  CCardBody,
  CCol,
  CFormInput,
  CInputGroup,
  CPagination,
  CPaginationItem,
  CRow,
  CTable,
} from '@coreui/react';
import DeleteModal from 'src/views/_DeleteModal';
import jobParserClient from 'src/client/BaseClient';
import { useNavigate } from 'react-router-dom';
import { formatRoute } from 'react-router-named-routes/lib';
import { ROUTES } from 'src/routes';

const Searches = () => {
  const navigate = useNavigate();
  const [visible, setVisible] = useState(false);
  const [items, setItems] = useState([]);
  const [itemDelete, setItemDelete] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await jobParserClient.searches.getSearches();
        setItems(generateItems(data.items));
      } catch (error) {
        console.error('Error fetching data:', error);
      }
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
        <CButtonGroup>
          <CButton color="primary" onClick={() => navigate(formatRoute(ROUTES.SEARCH_DETAILS, { id: item.id }))}>
            Details
          </CButton>
          <CButton color="primary" onClick={() => navigate(formatRoute(ROUTES.SEARCH_EDIT, { id: item.id }))}>
            Edit
          </CButton>
          <CButton color="danger" onClick={() => { setItemDelete(item.id); setVisible(true); }}>
            Delete
          </CButton>
        </CButtonGroup>
      ),
      _cellProps: { id: { scope: 'row' } },
    }));
  };

  const handleDelete = async () => {
    try {
      await jobParserClient.searches.deleteSearch(itemDelete);
      setItems(items.filter(item => item.id !== itemDelete));
      setVisible(false);
    } catch (error) {
      console.error('Error deleting item:', error);
    }
  };

  const columns = [
    { key: 'id', label: '#', _props: { scope: 'col' } },
    { key: 'title', label: 'Title', _props: { scope: 'col' } },
    { key: 'url', label: 'URL', _props: { scope: 'col' } },
    { key: 'created_at', label: 'Created at', _props: { scope: 'col' } },
    { key: 'actions', label: 'Actions', _props: { scope: 'col' } },
  ];

  return (
    <>
      <DeleteModal model="search" visible={visible} setVisible={setVisible} onDelete={handleDelete} />

      <CRow>
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardBody>
              <CInputGroup className="mb-3">
                <CFormInput placeholder="Search..." aria-label="Search" aria-describedby="button-addon2" />
                <CButton type="button" color="secondary" variant="outline" id="button-addon2">
                  Search
                </CButton>
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
}

export default Searches;
