import React, { useState, useEffect } from 'react';
import {
  CButton,
  CButtonGroup,
  CCard,
  CCardBody,
  CCol,
  CForm,
  CFormInput,
  CFormLabel, CFormTextarea,
  CRow,
} from '@coreui/react';
import { useParams, useNavigate } from 'react-router-dom';
import jobParserClient from 'src/client/Client'; // Assuming you have a client for API calls
import { ROUTES } from 'src/routes'; // Assuming you have defined your routes

const ApplicationDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [applicationDetails, setApplicationDetails] = useState({
    title: '',
    description: '',
    finded_date: '',
    application_date: '',
    applied: '',
    short_id: ''
  });

  useEffect(() => {
    const fetchApplicationDetails = async () => {
      try {
        const data = await jobParserClient.applications.getApplicationById(id);
        console.log(data);
        console.log("title", data.title, "applied", data.applied, "application_date", data.application_date, "finded_date", data.finded_date, "description", data.description);
        setApplicationDetails({
          title: data.title, // Ensure values are never undefined
          description: data.description,
          finded_date: data.created_at,
          application_date: data.application_date || 'Not applied',
          applied: data.applied ? 'Yes' : 'No',
          short_id: data.short_id
        });
      } catch (error) {
        console.error('Error fetching application details:', error);
      }
    };

    fetchApplicationDetails();
  }, [id]);

  return (
    <>
      <CRow>
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardBody>
              <center><h1>Application Details</h1></center>
              <CForm className="row g-3">
                <CRow className="mb-3">
                  <CFormLabel htmlFor="staticTitle" className="col-sm-2 col-form-label">Title</CFormLabel>
                  <CCol sm={10}>
                    <CFormInput
                      type="text"
                      id="staticTitle"
                      value={applicationDetails.title}
                      readOnly
                      plainText
                    />
                  </CCol>
                </CRow>
                <CRow className="mb-3">
                  <CFormLabel htmlFor="staticDescription" className="col-sm-2 col-form-label">Description</CFormLabel>
                  <CCol sm={10}>
                    <CFormTextarea
                      type="text"
                      id="staticDescription"
                      value={applicationDetails.description}
                      readOnly
                      plainText
                      style={{
                        resize: 'none', // Prevent manual resizing
                        overflow: 'hidden' // Hide scrollbar
                      }}
                    />
                  </CCol>
                </CRow>
                <CRow className="mb-3">
                  <CFormLabel htmlFor="staticFindedDate" className="col-sm-2 col-form-label">Finded Date</CFormLabel>
                  <CCol sm={10}>
                    <CFormInput
                      type="text"
                      id="staticFindedDate"
                      value={applicationDetails.finded_date}
                      readOnly
                      plainText
                    />
                  </CCol>
                </CRow>
                <CRow className="mb-3">
                  <CFormLabel htmlFor="staticApplicationDate" className="col-sm-2 col-form-label">Application Date</CFormLabel>
                  <CCol sm={10}>
                    <CFormInput
                      type="text"
                      id="staticApplicationDate"
                      value={applicationDetails.application_date}
                      readOnly
                      plainText
                    />
                  </CCol>
                </CRow>
                <CRow className="mb-3">
                  <CFormLabel htmlFor="staticApplied" className="col-sm-2 col-form-label">Applied</CFormLabel>
                  <CCol sm={10}>
                    <CFormInput
                      type="text"
                      id="staticApplied"
                      value={applicationDetails.applied}
                      readOnly
                      plainText
                    />
                  </CCol>
                </CRow>
                <CCol xs={12}>
                  <CButtonGroup>
                    <CButton color="primary" href={jobParserClient.applications.getApplyLink(applicationDetails.short_id)}>Apply</CButton>
                    <CButton color="secondary" onClick={() => navigate(-1)}>Back</CButton>
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

export default ApplicationDetails;
