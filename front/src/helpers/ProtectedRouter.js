import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import {verifyToken} from "src/helpers/_auth";
import {CSpinner} from "@coreui/react";

const ProtectedRoute = ({ element }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(() => {
    const checkAuth = async () => {
      const authenticated = await verifyToken();
      setIsAuthenticated(authenticated);
    };
    checkAuth();
  }, []);

  if (isAuthenticated === null) {
    return <div className="pt-3 text-center">
      <CSpinner color="primary" variant="grow"/>
    </div>;
  }

  return isAuthenticated ? element : <Navigate to="/login" />;
};

export default ProtectedRoute;
