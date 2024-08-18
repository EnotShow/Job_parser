import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import jobParserClient from "src/client/Client";
import { setCookie } from "src/helpers/_auth";
import {CAlert, CSpinner} from "@coreui/react";

const LoginByHash = () => {
  const { hash: _hash } = useParams();
  const navigate = useNavigate();

  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const authenticate = async () => {
      try {
        setLoading(true);
        if (_hash) {
          const tokens = await jobParserClient.authByHash(_hash);

          if (tokens) {
            setCookie("accessToken", tokens.access_token, 1);
            setCookie("refreshToken", tokens.refresh_token, 1);
            navigate("/");
          } else {
            setError("Unexpected error occurred");
          }
        }
      } catch (e) {
        setError(e.response?.message || "Login failed");
      } finally {
        setLoading(false);
      }
    };

    authenticate();
  }, [_hash, navigate]);

  if (loading) return <CSpinner color="primary" variant="grow" />;
  if (error) return (
  <CAlert color="danger">
    Error: {error}
  </CAlert>
);

};

export default LoginByHash;
