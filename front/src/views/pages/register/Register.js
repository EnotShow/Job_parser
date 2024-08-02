import React from 'react'
import {
  CButton,
  CCard,
  CCardBody,
  CCol,
  CContainer,
  CForm,
  CFormInput,
  CInputGroup,
  CInputGroupText,
  CRow,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilLockLocked, cilUser } from '@coreui/icons'
import {useNavigate} from "react-router-dom";
import jobParserClient from "src/client/BaseClient";
import {setCookie} from "src/helpers/_auth";
import UserRegisterDTO from "src/client/DTOs/UserRegisterDTO";

const Register = () => {
  const [email, setEmail] = React.useState('')
  const [password, setPassword] = React.useState('')
  const [confirmPassword, setConfirmPassword] = React.useState('')
  const [error, setError] = React.useState('')
  const [loading, setLoading] = React.useState(false)

  const navigate = useNavigate()

  const validateForm = () => {
    if (!email || !password) {
      setError('Username and password are required')
      return false
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return false
    }
    setError('')
    return true
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!validateForm()) {
      return
    }
    setLoading(true)

    const formDetails = new UserRegisterDTO(
      email,
      password,
      "en",
      0
    ).toJSON();

    try {

      const response = await jobParserClient.register(formDetails)

      if (response) {
        setCookie('accessToken', response.access_token, 1)
        setCookie('refreshToken', response.refresh_token, 1)
        navigate('/')
      } else {
        setError(response.details || 'Unexpected error occurred')
      }
    } catch (e) {
      setError(e.response?.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-body-tertiary min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md={9} lg={7} xl={6}>
            <CCard className="mx-4">
              <CCardBody className="p-4">
                <CForm onSubmit={handleSubmit}>
                  <h1>Register</h1>
                  <p className="text-body-secondary">Create your account</p>
                  <CInputGroup className="mb-3">
                    <CInputGroupText>@</CInputGroupText>
                    <CFormInput
                      placeholder="Email"
                      autoComplete="email"
                      onChange={(e) => setEmail(e.target.value)}
                      value={email}
                    />
                  </CInputGroup>
                  <CInputGroup className="mb-3">
                    <CInputGroupText>
                      <CIcon icon={cilLockLocked} />
                    </CInputGroupText>
                    <CFormInput
                      type="password"
                      placeholder="Password"
                      autoComplete="new-password"
                      onChange={(e) => setPassword(e.target.value)}
                      value={password}
                    />
                  </CInputGroup>
                  <CInputGroup className="mb-4">
                    <CInputGroupText>
                      <CIcon icon={cilLockLocked} />
                    </CInputGroupText>
                    <CFormInput
                      type="password"
                      placeholder="Repeat password"
                      autoComplete="new-password"
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      value={confirmPassword}
                    />
                  </CInputGroup>
                  <div className="d-grid">
                    <CButton color="primary" className="px-4" disabled={loading} type="submit">
                          {loading ? 'Loading...' : 'Create account'}
                    </CButton>
                  </div>
                    {error && <p className="text-danger mt-2">{error}</p>}
                </CForm>
              </CCardBody>
            </CCard>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default Register
