import React, { useState } from 'react';
import {
  CAlert,
  CButton,
  CCard,
  CCardBody,
  CCardTitle,
  CCol,
  CRow,
  CPagination,
  CPaginationItem,
  CFormSelect,
} from '@coreui/react';

const NotificationPage = () => {
  const notifications = [
    { id: 1, type: 'success', title: 'Success', message: 'Your subscription has been successfully updated!' },
    { id: 2, type: 'warning', title: 'Warning', message: 'Your subscription is about to expire in 7 days. Please renew to avoid interruption.' },
    { id: 3, type: 'danger', title: 'Error', message: 'There was an error processing your payment. Please try again or contact support.' },
    { id: 4, type: 'info', title: 'Information', message: 'A new version of the app is available. Update to the latest version to enjoy new features.' },
    { id: 5, type: 'secondary', title: 'Neutral', message: 'Your profile information has been updated.' },
    // Add more notifications as needed
  ];

  const [currentPage, setCurrentPage] = useState(1);
  const [paginationLimit, setPaginationLimit] = useState(5);

  const totalItems = notifications.length;
  const totalPages = Math.ceil(totalItems / paginationLimit);

  const paginatedNotifications = notifications.slice(
    (currentPage - 1) * paginationLimit,
    currentPage * paginationLimit
  );

  const handlePaginationChange = (e) => {
    setPaginationLimit(parseInt(e.target.value, 10));
    setCurrentPage(1); // Reset to first page on limit change
  };

  return (
    <CRow className="justify-content-center">
      <CCol xs={12}>
        <CCard className="mb-4">
          <CCardBody>
            <center><h1>Notifications</h1></center>
          </CCardBody>
        </CCard>

        {/* Display paginated notifications */}
        {paginatedNotifications.map((notification) => (
          <CCard className={`mb-3 border-${notification.type}`} key={notification.id}>
            <CCardBody>
              <CCardTitle className={`text-${notification.type}`}>{notification.title}</CCardTitle>
              <CAlert color={notification.type}>
                {notification.message}
              </CAlert>
              <CButton color={notification.type}>View Details</CButton>
            </CCardBody>
          </CCard>
        ))}

        {/* Pagination Controls */}
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
            <CFormSelect className="ms-3" aria-label="Select pagination limit" onChange={handlePaginationChange}
                         style={{width: 'auto'}}>
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="20">20</option>
            </CFormSelect>
        </div>
      </CCol>
    </CRow>
  );
};

export default NotificationPage;
