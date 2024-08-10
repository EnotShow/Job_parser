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
import { ROUTES } from 'src/routes'; // Assuming you have defined your routes

const SearchEdit = () => {
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

  const handleSave = async () => {
    try {
      await jobParserClient.searches.updateSearch(searchDetails, id);
      navigate(ROUTES.SEARCH_DETAILS.replace(':id', id));
    } catch (error) {
      console.error('Error updating search:', error);
    }
  };

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
              <center><h1>Edit Search</h1></center>
              <CForm className="row g-3">
                <CRow className="mb-3">
                  <CFormLabel htmlFor="title" className="col-sm-2 col-form-label">Title</CFormLabel>
                  <CCol sm={10}>
                    <CFormInput
                      type="text"
                      id="title"
                      value={searchDetails.title}
                      onChange={(e) => setSearchDetails({ ...searchDetails, title: e.target.value })}
                    />
                  </CCol>
                </CRow>
                <CRow className="mb-3">
                  <CFormLabel htmlFor="url" className="col-sm-2 col-form-label">Url</CFormLabel>
                  <CCol sm={10}>
                    <CFormInput
                      type="text"
                      id="url"
                      value={searchDetails.url}
                      onChange={(e) => setSearchDetails({ ...searchDetails, url: e.target.value })}
                    />
                  </CCol>
                </CRow>
                <CCol xs={12}>
                  <CButtonGroup>
                    <CButton color="primary" onClick={handleSave}>Save</CButton>
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

export default SearchEdit;
