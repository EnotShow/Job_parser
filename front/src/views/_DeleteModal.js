import {CButton, CModal, CModalBody, CModalFooter, CModalHeader, CModalTitle} from "@coreui/react";
import React from "react";

const DeleteModal = ({ visible, setVisible, model, onDelete }) => {
  return (
      <CModal visible={visible} onClose={() => setVisible(false)} aria-labelledby="DeleteWarning">
      <CModalHeader>
        <CModalTitle>Warning!</CModalTitle>
      </CModalHeader>
      <CModalBody>
        <p>Are you sure you want to delete {model}?</p>
      </CModalBody>
      <CModalFooter>
        <CButton color="secondary" onClick={() => setVisible(false)}>Close</CButton>
        <CButton color="danger" onClick={() => { onDelete(); setVisible(false); }}>Delete anyway</CButton>
      </CModalFooter>
    </CModal>
  );
};

export default DeleteModal
