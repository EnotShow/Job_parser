import React, { useState, useEffect } from 'react';
import {
  CButton,
  CButtonGroup,
  CCard,
  CCardBody,
  CCol,
  CForm,
  CFormInput,
  CFormLabel,
  CRow,
} from '@coreui/react';
import DeleteModal from 'src/views/_DeleteModal';
import { useParams, useNavigate } from 'react-router-dom';
import jobParserClient from 'src/client/Client'; // Assuming you have a client for API calls
import { ROUTES } from 'src/routes';
import {formatRoute} from "react-router-named-routes/lib"; // Assuming you have defined your routes

const SearchDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [visible, setVisible] = useState(false);
  const [searchDetails, setSearchDetails] = useState({
    title: '',
    url: '',
    created_at: ''
  });

  useEffect(() => {
    const fetchSearchDetails = async () => {
      try {
        const data = await jobParserClient.searches.getSearchById(id);
        setSearchDetails(data);
      } catch (error) {
        console.error('Error fetching search details:', error);
      }
    };

    fetchSearchDetails();
  }, [id]);

  const handleDelete = async () => {
    try {
      await jobParserClient.searches.deleteSearch(id);
      setVisible(false);
      navigate(ROUTES.SEARCHES);
    } catch (error) {
      console.error('Error deleting search:', error);
    }
  };

  return (
    <>
      <DeleteModal model="search" visible={visible} setVisible={setVisible} onDelete={handleDelete} />

      <CRow>
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardBody>
              <center><h1>Search Details</h1></center>
              <CForm className="row g-3">
                <CRow className="mb-3">
                  <CFormLabel htmlFor="staticTitle" className="col-sm-2 col-form-label">Title</CFormLabel>
                  <CCol sm={10}>
                    <CFormInput type="text" id="staticTitle" value={searchDetails.title} readOnly plainText />
                  </CCol>
                </CRow>
                <CRow className="mb-3">
                  <CFormLabel htmlFor="staticUrl" className="col-sm-2 col-form-label">Url</CFormLabel>
                  <CCol sm={10}>
                    <CFormInput type="text" id="staticUrl" value={searchDetails.url} readOnly plainText />
                  </CCol>
                </CRow>
                <CRow className="mb-3">
                  <CFormLabel htmlFor="staticCreatedAt" className="col-sm-2 col-form-label">Created at</CFormLabel>
                  <CCol sm={10}>
                    <CFormInput type="text" id="staticCreatedAt" value={searchDetails.created_at} readOnly plainText />
                  </CCol>
                </CRow>
                <CCol xs={12}>
                  <CButtonGroup>
                    <CButton color="primary" onClick={() => navigate(formatRoute(ROUTES.SEARCH_EDIT, { id: id }))}>Edit</CButton>
                    <CButton color="secondary" onClick={() => navigate(-1)}>Back</CButton>
                    <CButton color="danger" onClick={() => setVisible(true)}>Delete</CButton>
                  </CButtonGroup>
                </CCol>
              </CForm>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  );
};

export default SearchDetails;
