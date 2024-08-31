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
import jobParserClient from 'src/client/Client';
import { useNavigate, useLocation } from 'react-router-dom';
import { formatRoute } from 'react-router-named-routes/lib';
import { ROUTES } from 'src/routes';

const Applications = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const queryParams = new URLSearchParams(location.search);
  const initialPage = parseInt(queryParams.get('page'), 10) || 1;

  const [items, setItems] = useState([]);
  const [paginationLimit, setPaginationLimit] = useState(10);
  const [currentPage, setCurrentPage] = useState(initialPage);
  const [totalItems, setTotalItems] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await jobParserClient.applications.getApplications(
          paginationLimit,
          currentPage,
          searchTerm // include search term in the request
        );
        setItems(generateItems(data.items));
        setTotalItems(data.total);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [paginationLimit, currentPage, searchTerm]);

  useEffect(() => {
    if (currentPage > 1) {
      navigate(`?page=${currentPage}`, { replace: true });
    }
  }, [currentPage, navigate]);

  const generateItems = (data) => {
    let index = currentPage === 1 ? 1 : (currentPage - 1) * paginationLimit + 1;
    return data.map((item) => {
      const row = {
        id: index,
        title: item.title,
        finded_date: item.created_at,
        application_date: item.application_date,
        applied: item.applied ? 'Yes' : 'No',
        actions: (
          <CButtonGroup>
            <CButton
              color="primary"
              onClick={() =>
                navigate(formatRoute(ROUTES.APPLICATION_DETAILS, { id: item.id }))
              }
            >
              Details
            </CButton>
            <CButton color="primary" href={jobParserClient.applications.getApplyLink(item.short_id)}>
              Apply
            </CButton>
          </CButtonGroup>
        ),
        _cellProps: { id: { scope: 'row' } },
      };
      index += 1;
      return row;
    });
  };

  const columns = [
    { key: 'id', label: '#', _props: { scope: 'col' } },
    { key: 'title', label: 'Title', _props: { scope: 'col' } },
    { key: 'finded_date', label: 'Finded', _props: { scope: 'col' } },
    { key: 'application_date', label: 'Application date', _props: { scope: 'col' } },
    { key: 'applied', label: 'Applied', _props: { scope: 'col' } },
    { key: 'actions', label: 'Actions', _props: { scope: 'col' } },
  ];

  const handlePaginationChange = (e) => {
    setPaginationLimit(parseInt(e.target.value, 10));
    setCurrentPage(1);
  };

  const handleSearch = async () => {
    setCurrentPage(1); // reset to first page after search
    try {
      const data = await jobParserClient.applications.getApplications(paginationLimit, currentPage, searchTerm);
      setItems(generateItems(data.items));
      setTotalItems(data.total);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const totalPages = Math.ceil(totalItems / paginationLimit);

  return (
    <>
      <CRow>
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardBody>
              <CInputGroup className="mb-3">
                <CFormInput
                  placeholder="Search..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  aria-label="Search"
                  aria-describedby="button-addon2"
                />
                <CButton
                  type="button"
                  color="secondary"
                  variant="outline"
                  id="button-addon2"
                  onClick={handleSearch}
                >
                  Search
                </CButton>
              </CInputGroup>
              <center><h1>Applications</h1></center>
              {items.length > 0 ? (
                <CTable columns={columns} items={items} />
              ) : (
                <p>No applications found.</p>
              )}
              <div className="d-flex justify-content-between align-items-center">
                <CPagination aria-label="Page navigation example">
                  <CPaginationItem
                    aria-label="Previous"
                    disabled={currentPage === 1}
                    onClick={() => setCurrentPage(currentPage - 1)}
                  >
                    <span aria-hidden="true">&laquo;</span>
                  </CPaginationItem>
                  {[...Array(totalPages).keys()].map((page) => (
                    <CPaginationItem
                      key={page}
                      active={currentPage === page + 1}
                      onClick={() => setCurrentPage(page + 1)}
                    >
                      {page + 1}
                    </CPaginationItem>
                  ))}
                  <CPaginationItem
                    aria-label="Next"
                    disabled={currentPage === totalPages}
                    onClick={() => setCurrentPage(currentPage + 1)}
                  >
                    <span aria-hidden="true">&raquo;</span>
                  </CPaginationItem>
                </CPagination>
                <CFormSelect
                  className="ms-3"
                  aria-label="Select pagination limit"
                  onChange={handlePaginationChange}
                  style={{ width: 'auto' }}
                >
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

export default Applications;
