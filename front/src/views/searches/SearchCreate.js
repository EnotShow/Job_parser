import React, { useEffect, useState } from 'react';
import {
  CButton,
  CCard,
  CCardBody,
  CCol,
  CForm,
  CFormInput,
  CFormLabel,
  CRow,
} from '@coreui/react';
import { useNavigate } from 'react-router-dom';
import jobParserClient from 'src/client/Client'; // Assuming you have a client for API calls
import { ROUTES } from 'src/routes'; // Assuming you have defined your routes

const SearchCreate = () => {
  const navigate = useNavigate();
  const [searchDetails, setSearchDetails] = useState({
    title: '',
    url: '',
    owner_id: '',
  });
  const [userId, setUserId] = useState('');

  useEffect(() => {
    const getUserId = async () => {
      try {
        const user = await jobParserClient.users.getMe();
        setUserId(user.id);
        setSearchDetails((prevDetails) => ({ ...prevDetails, owner_id: user.id }));
      } catch (error) {
        console.error('Error getting user ID:', error);
      }
    };
    getUserId();
  }, []);

  const handleChange = (e) => {
    const { id, value } = e.target;
    setSearchDetails((prevDetails) => ({ ...prevDetails, [id]: value }));
  };

  const handleSave = async () => {
    try {
      await jobParserClient.searches.createSearch(searchDetails);
      navigate(ROUTES.SEARCHES); // Redirect to the searches list or wherever appropriate
    } catch (error) {
      console.error('Error creating search:', error);
    }
  };

  return (
    <CRow>
      <CCol xs={12}>
        <CCard className="mb-4">
          <CCardBody>
            <center><h1>Create New Search</h1></center>
            <CForm className="row g-3">
              <CRow className="mb-3">
                <CFormLabel htmlFor="title" className="col-sm-2 col-form-label">Title</CFormLabel>
                <CCol sm={10}>
                  <CFormInput
                    type="text"
                    id="title"
                    value={searchDetails.title}
                    onChange={handleChange}
                  />
                </CCol>
              </CRow>
              <CRow className="mb-3">
                <CFormLabel htmlFor="url" className="col-sm-2 col-form-label">URL</CFormLabel>
                <CCol sm={10}>
                  <CFormInput
                    type="text"
                    id="url"
                    value={searchDetails.url}
                    onChange={handleChange}
                  />
                </CCol>
              </CRow>
              <CCol xs={12}>
                <CButton color="primary" onClick={handleSave}>Save</CButton>
                <CButton color="secondary" onClick={() => navigate(-1)}>Back</CButton>
              </CCol>
            </CForm>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  );
};

export default SearchCreate;
