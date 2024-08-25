import React, { useState } from 'react';
import {
  CAlert,
  CButton,
  CCard,
  CCardBody,
  CCardTitle,
  CCol,
  CRow,
  CFormCheck,
} from '@coreui/react';
import CIcon from '@coreui/icons-react';
import { cilCheckCircle } from '@coreui/icons';

const SubscriptionPage = () => {
  const oneMonthPrice = 9.99;

  const subscriptionOptions = [
    { id: '1', duration: '1 Month', price: 9.99, discount: 0 },
    { id: '3', duration: '3 Months', price: 27.99, discount: ((1 - 27.99 / (3 * oneMonthPrice)) * 100).toFixed(2) },
    { id: '6', duration: '6 Months', price: 49.99, discount: ((1 - 49.99 / (6 * oneMonthPrice)) * 100).toFixed(2) },
    { id: '12', duration: '12 Months', price: 89.99, discount: ((1 - 89.99 / (12 * oneMonthPrice)) * 100).toFixed(2) },
  ];

  const [selectedSubscription, setSelectedSubscription] = useState('1');

  const handleSubscriptionChange = (id) => {
    setSelectedSubscription(id);
  };

  const handleSubscribe = () => {
    alert(`Subscribed to ${subscriptionOptions.find(option => option.id === selectedSubscription).duration} plan`);
  };

  return (
    <CRow className="justify-content-center">
      <CCol xs={12} md={6}>
        <CCard className="mb-4">
          <CCardBody>
            <center><h1>Subscription Plans</h1></center>
            <CAlert color="info">
              Select a subscription plan that suits you best.
            </CAlert>

            {subscriptionOptions.map((option) => (
              <CCard
                key={option.id}
                className={`mb-3 ${selectedSubscription === option.id ? 'border-primary' : ''}`}
                onClick={() => handleSubscriptionChange(option.id)}
                style={{ height: '150px', cursor: 'pointer' }}
              >
                <CCardBody className="d-flex align-items-center">
                  <CFormCheck
                    type="radio"
                    id={`subscription-${option.id}`}
                    name="subscription"
                    value={option.id}
                    checked={selectedSubscription === option.id}
                    onChange={() => handleSubscriptionChange(option.id)}
                    hidden
                  />
                  <CIcon icon={cilCheckCircle} size="2xl" className={`me-3 ${selectedSubscription === option.id ? 'text-primary' : 'text-muted'}`} />
                  <div className="d-flex flex-column justify-content-center w-100">
                    <CCardTitle>{option.duration}</CCardTitle>
                    <h2>${option.price.toFixed(2)}</h2>
                    {option.id !== '1' && (
                      <>
                        <p className="mb-1">(${(option.price / parseInt(option.duration)).toFixed(2)} per month)</p>
                        <p className="text-success">{option.discount}% off</p>
                      </>
                    )}
                  </div>
                </CCardBody>
              </CCard>
            ))}

            <CCol xs={12} className="d-flex justify-content-center mt-4">
              <CButton color="primary" onClick={handleSubscribe}>
                Subscribe
              </CButton>
            </CCol>

            <CCol xs={12} className="d-flex justify-content-center mt-2">
              <CButton color="secondary">
                Back
              </CButton>
            </CCol>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  );
};

export default SubscriptionPage;
