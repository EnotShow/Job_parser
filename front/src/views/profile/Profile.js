import React, { useState, useEffect } from 'react';
import jobParserClient from 'src/client/Client';
import {
  CButton,
  CCard,
  CCardBody,
  CCol,
  CForm,
  CFormInput,
  CRow,
} from '@coreui/react';
import { cibMessenger, cibTelegram, cibWhatsapp } from '@coreui/icons';
import CIcon from '@coreui/icons-react';

const Profile = () => {
  const [profileData, setProfileData] = useState({
    id: null,
    first_name: '',
    last_name: '',
    email: '',
  });

  // Fetch profile data from the server when the component mounts
  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const response = await jobParserClient.users.getMe(); // Assume this API fetches the user's profile
        setProfileData((prevData) => ({
          ...prevData,
          ...response, // Merge response data with current state
        }));
      } catch (error) {
        console.error('Error fetching profile data:', error);
      }
    };

    fetchProfileData();
  }, []);

  // Handler for input changes
  const handleInputChange = (e) => {
    const { id, value } = e.target;
    setProfileData((prevData) => ({
      ...prevData,
      [id]: value,
    }));
  };

  // Handler for form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await jobParserClient.users.updateMe(profileData); // Assume this API updates the user's profile
      console.log('Profile data submitted:', profileData);
    } catch (error) {
      console.error('Error submitting profile data:', error);
    }
  };

  return (
    <>
      <CRow>
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardBody>
              <CRow>
                <CCol>
                  <center><h1>Profile</h1></center>
                </CCol>
              </CRow>
              <CForm className="row g-3" onSubmit={handleSubmit}>
                <CCol md={6}>
                  <CFormInput
                    type="text"
                    id="first_name"
                    label="Name"
                    value={profileData.first_name}
                    onChange={handleInputChange}
                  />
                </CCol>
                <CCol md={6}>
                  <CFormInput
                    type="text"
                    id="last_name"
                    label="Lastname"
                    value={profileData.last_name}
                    onChange={handleInputChange}
                  />
                </CCol>
                <CCol xs={12}>
                  <CFormInput
                    type="email"
                    id="email"
                    label="Email"
                    placeholder="example@mail.com"
                    value={profileData.email}
                    onChange={handleInputChange}
                  />
                </CCol>
                <CCol xs={12}>
                  <CRow>
                    <center><h2>Social networks</h2></center>
                  </CRow>
                </CCol>
                <CCol xs={12} className="my-3">
                  <CRow className="align-items-center">
                    <CCol xs="auto">
                      <CIcon icon={cibTelegram} size="xl" />
                    </CCol>
                    <CCol xs="auto">
                      <h5>Telegram</h5>
                    </CCol>
                    <CCol xs="auto">
                      <CButton color="primary">Connect</CButton>
                    </CCol>
                  </CRow>
                </CCol>
                <CCol xs={12} className="my-3">
                  <CRow className="align-items-center">
                    <CCol xs="auto">
                      <CIcon icon={cibWhatsapp} size="xl" />
                    </CCol>
                    <CCol xs="auto">
                      <h5>WhatsApp</h5>
                    </CCol>
                    <CCol xs="auto">
                      <CButton color="primary">Connect</CButton>
                    </CCol>
                  </CRow>
                </CCol>
                <CCol xs={12} className="my-3">
                  <CRow className="align-items-center">
                    <CCol xs="auto">
                      <CIcon icon={cibMessenger} size="xl" />
                    </CCol>
                    <CCol xs="auto">
                      <h5>Messenger</h5>
                    </CCol>
                    <CCol xs="auto">
                      <CButton color="success" disabled>Connected</CButton>
                    </CCol>
                  </CRow>
                </CCol>
                <CCol xs={12}>
                  <CButton color="primary" type="submit">Save Changes</CButton>
                </CCol>
              </CForm>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  );
};

export default Profile;
