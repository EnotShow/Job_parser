import React, { useState } from 'react';
import {
  CAlert,
  CButton,
  CCard,
  CCardBody,
  CCol,
  CForm,
  CFormInput,
  CFormLabel,
  CFormCheck,
  CRow,
} from '@coreui/react';
import CIcon from '@coreui/icons-react';
import { cilPlus, cilTrash } from '@coreui/icons';

const SmartEditor = () => {
  const serviceOptions = [
    { id: '1', name: 'OLX.pl' },
    { id: '2', name: 'Pracuj.pl' },
    { id: '3', name: 'Praca.pl' },
  ];

  const [formObjects, setFormObjects] = useState([
    { kwords: '', location: '', salary: '', services: [] } // services is now an array
  ]);

  const handleChange = (index, field, value) => {
    const newFormObjects = [...formObjects];
    newFormObjects[index][field] = value;
    setFormObjects(newFormObjects);
  };

  const handleServiceChange = (index, service) => {
    const newFormObjects = [...formObjects];
    const serviceIndex = newFormObjects[index].services.indexOf(service);

    if (serviceIndex === -1) {
      newFormObjects[index].services.push(service); // Add service if not already selected
    } else {
      newFormObjects[index].services.splice(serviceIndex, 1); // Remove service if already selected
    }

    setFormObjects(newFormObjects);
  };

  const addNewObject = () => {
    setFormObjects([...formObjects, { kwords: '', location: '', salary: '', services: [] }]);
  };

  const deleteObject = (index) => {
    const newFormObjects = [...formObjects];
    newFormObjects.splice(index, 1);
    setFormObjects(newFormObjects);
  };

  return (
    <CRow>
      <CCol xs={12}>
        <CCard className="mb-4">
          <CCardBody>
            <center><h1>Smart Editor</h1></center>
            <CAlert color="warning">
              Smart Editor already processing. We are informing you once it is complete.
            </CAlert>

            {/* Object Cards */}
            {formObjects.map((formObject, index) => (
              <CCard className="mb-3" key={index}>
                <CCardBody>
                  <CForm className="row mb-3">
                    {/* Keywords Field */}
                    <CRow className="mb-3">
                      <CFormLabel htmlFor={`kwords-${index}`} className="col-sm-2 col-form-label">Keywords</CFormLabel>
                      <CCol sm={10}>
                        <CFormInput
                          required
                          type="text"
                          id={`kwords-${index}`}
                          value={formObject.kwords}
                          onChange={(e) => handleChange(index, 'kwords', e.target.value)}
                        />
                      </CCol>
                    </CRow>

                    <CRow className="mb-3">
                      <CFormLabel htmlFor={`location-${index}`} className="col-sm-2 col-form-label">Location</CFormLabel>
                      <CCol sm={10}>
                        <CFormInput
                          required
                          type="text"
                          id={`location-${index}`}
                          value={formObject.location}
                          onChange={(e) => handleChange(index, 'location', e.target.value)}
                        />
                      </CCol>
                    </CRow>

                    <CRow className="mb-3">
                      <CFormLabel htmlFor={`salary-${index}`} className="col-sm-2 col-form-label">Salary</CFormLabel>
                      <CCol sm={10}>
                        <CFormInput
                          required
                          type="text"
                          id={`salary-${index}`}
                          value={formObject.salary}
                          onChange={(e) => handleChange(index, 'salary', e.target.value)}
                        />
                      </CCol>
                    </CRow>

                    <CRow className="mb-3">
                      <CFormLabel htmlFor={`services-${index}`} className="col-sm-2 col-form-label">Services</CFormLabel>
                      <CCol sm={10}>
                        {serviceOptions.map(service => (
                          <CFormCheck
                            required
                            key={service.id}
                            type="checkbox"
                            id={`service-${index}-${service.id}`}
                            label={service.name}
                            checked={formObject.services.includes(service.name)} // Check if service is selected
                            onChange={() => handleServiceChange(index, service.name)} // Toggle service selection
                          />
                        ))}
                      </CCol>
                    </CRow>

                    {formObjects.length > 1 && (
                      <CRow>
                        <CCol className="d-flex justify-content-end">
                          <CButton color="danger" onClick={() => deleteObject(index)}>
                            <CIcon icon={cilTrash} />
                          </CButton>
                        </CCol>
                      </CRow>
                    )}
                  </CForm>
                </CCardBody>
              </CCard>
            ))}

            <CCol xs={12} className="d-flex justify-content-end mb-3">
              <CButton color="secondary" onClick={addNewObject}>
                <CIcon icon={cilPlus} />
              </CButton>
            </CCol>

            <CCol xs={12}>
              <CButton color="primary">Save</CButton>
              <CButton color="secondary" className="ms-2">Back</CButton>
            </CCol>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  );
};

export default SmartEditor;
