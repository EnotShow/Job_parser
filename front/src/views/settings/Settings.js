import React, { useEffect, useState } from 'react';
import {
  CButton, CButtonGroup,
  CCard,
  CCardBody,
  CCol,
  CForm,
  CFormInput,
  CFormLabel,
  CFormSelect,
  CInputGroup, CInputGroupText,
  CRow,
} from '@coreui/react';
import jobParserClient from 'src/client/Client';

const Settings = () => {
  const [linksLimit, setLinksLimit] = useState('');
  const [searchDetails, setSearchDetails] = useState({
    id: 0,
    selected_language: '',
    paused: false,
  });

  useEffect(() => {
    const getUserSettings = async () => {
      try {
        const user_settings = await jobParserClient.users.getSettings();
        setLinksLimit(user_settings.links_limit);
        setSearchDetails((prevDetails) => ({
          ...prevDetails,
          id: user_settings.id,
          selected_language: user_settings.selected_language,
          paused: user_settings.paused,
        }));
      } catch (error) {
        console.error('Error getting user settings:', error);
      }
    };
    getUserSettings();
  }, []);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSearchDetails((prevDetails) => ({
      ...prevDetails,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handlePauseToggle = (isPaused) => {
    setSearchDetails((prevDetails) => ({
      ...prevDetails,
      paused: isPaused,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await jobParserClient.users.updateMe(searchDetails);
  };

  return (
    <>
      <CRow>
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardBody>
              <CRow>
                <CCol>
                  <center><h1>Settings</h1></center>
                </CCol>
              </CRow>
              <CForm className="row g-3 mt-4" onSubmit={handleSubmit}>
                <CCol md={12}>
                  <CFormLabel htmlFor="languageSelect">Language</CFormLabel>
                  <CFormSelect
                    id="languageSelect"
                    name="selected_language"
                    value={searchDetails.selected_language}
                    onChange={handleInputChange}
                    aria-label="Language select"
                  >
                    <option value="en">English</option>
                    <option value="pl">Polish</option>
                    <option value="ua">Ukrainian</option>
                    <option value="ru">Russian</option>
                  </CFormSelect>
                </CCol>

                <CCol md={12} className="d-flex align-items-center">
                  <CFormLabel htmlFor="pauseParsingButton" className="me-4" style={{ fontSize: '1.25rem' }}>Pause Parsing</CFormLabel>
                  <CButtonGroup>
                    <CButton
                      color={searchDetails.paused ? "primary" : "secondary"}
                      variant="outline"
                      id="pauseParsingButton"
                      active={searchDetails.paused}
                      onClick={() => handlePauseToggle(true)}
                    >
                      Pause
                    </CButton>
                    <CButton
                      color={!searchDetails.paused ? "primary" : "secondary"}
                      variant="outline"
                      active={!searchDetails.paused}
                      onClick={() => handlePauseToggle(false)}
                    >
                      Resume
                    </CButton>
                  </CButtonGroup>
                </CCol>

                <CCol md={12}>
                  <CFormLabel htmlFor="linksLimit">Links Limit</CFormLabel>
                  <CInputGroup>
                    <CFormInput
                      type="number"
                      id="linksLimit"
                      name="links_limit"
                      value={linksLimit}
                      disabled
                      readOnly
                    />
                    <CInputGroupText>
                      <CButton color="primary">Increase</CButton>
                    </CInputGroupText>
                  </CInputGroup>
                </CCol>

                <CCol xs={12} className="mt-4">
                  <CButton color="primary" type="submit">Save Settings</CButton>
                </CCol>
              </CForm>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  );
};

export default Settings;
