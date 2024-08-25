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
  CFormSelect,
} from '@coreui/react';
import DeleteModal from 'src/views/_DeleteModal';
import jobParserClient from 'src/client/Client';
import { useNavigate } from 'react-router-dom';
import { formatRoute } from 'react-router-named-routes/lib';
import { ROUTES } from 'src/routes';

const truncateUrl = (url, maxLength = 30) => {
  if (url.length > maxLength) {
    return url.slice(0, maxLength) + '...';
  }
  return url;
};

const Searches = () => {
  const navigate = useNavigate();
  const [visible, setVisible] = useState(false);
  const [items, setItems] = useState([]);
  const [itemDelete, setItemDelete] = useState(null);
  const [paginationLimit, setPaginationLimit] = useState(10);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalItems, setTotalItems] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await jobParserClient.searches.getSearches(
          paginationLimit,
          currentPage
        );
        setItems(generateItems(data.items));
        setTotalItems(data.total);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [paginationLimit, currentPage]);

  useEffect(() => {
    if (currentPage > 1) {
      navigate(`?page=${currentPage}`, { replace: true });
    }
  }, [currentPage, navigate]);

  const generateItems = (data) => {
    return data.map((item) => ({
      id: item.id,
      title: item.title,
      url: truncateUrl(item.url),
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

  const handlePaginationChange = (e) => {
    setPaginationLimit(parseInt(e.target.value, 10));
    setCurrentPage(1);
  };

  const totalPages = Math.ceil(totalItems / paginationLimit);

  return (
    <>
      <DeleteModal model="search" visible={visible} setVisible={setVisible} onDelete={handleDelete} />

      {/* Smart Editor Card */}
      <CRow className="mb-4">
        <CCol xs={12}>
          <CCard>
            <CCardBody className="d-flex justify-content-between align-items-center">
              <div>
                <h5>You can automate adding requests using Smart Editor</h5>
                <p>Click the button below to start automating your requests.</p>
              </div>
              <CButton color="primary" onClick={() => navigate(ROUTES.SMART_EDITOR)}>
                Go to Smart Editor
              </CButton>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>

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
              <CButton color="primary" className="mb-3" onClick={() => navigate(ROUTES.SEARCH_CREATE)}>
                Create Search
              </CButton>
              <center><h1>Searches</h1></center>
              <CTable columns={columns} items={items} />
              <div className="d-flex justify-content-between align-items-center">
                <CPagination aria-label="Page navigation example">
                  <CPaginationItem aria-label="Previous" disabled={currentPage === 1} onClick={() => setCurrentPage(currentPage - 1)}>
                    <span aria-hidden="true">&laquo;</span>
                  </CPaginationItem>
                  {[...Array(totalPages).keys()].map((page) => (
                    <CPaginationItem key={page} active={currentPage === page + 1} onClick={() => setCurrentPage(page + 1)}>
                      {page + 1}
                    </CPaginationItem>
                  ))}
                  <CPaginationItem aria-label="Next" disabled={currentPage === totalPages} onClick={() => setCurrentPage(currentPage + 1)}>
                    <span aria-hidden="true">&raquo;</span>
                  </CPaginationItem>
                </CPagination>
                <CFormSelect className="ms-3" aria-label="Select pagination limit" onChange={handlePaginationChange} style={{ width: 'auto' }}>
                  <option value="10">10</option>
                  <option value="20">20</option>
                  <option value="30">30</option>
                </CFormSelect>
              </div>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  );
};

export default Searches;
