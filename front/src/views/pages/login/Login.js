import React, {useEffect} from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  CButton,
  CButtonGroup,
  CCard,
  CCardBody,
  CCardGroup,
  CCol,
  CContainer,
  CForm,
  CFormInput,
  CInputGroup,
  CInputGroupText,
  CRow,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilLockLocked, cilUser, cibTelegram, cibGoogle, cibMessenger } from '@coreui/icons'
import { setCookie } from 'src/helpers/_auth'
import jobParserClient from "src/client/Client";
import UserLoginDTO from "src/client/DTOs/UserLoginDTO";

const Login = () => {
  const [email, setEmail] = React.useState('')
  const [password, setPassword] = React.useState('')
  const [error, setError] = React.useState('')
  const [loading, setLoading] = React.useState(false)

  const navigate = useNavigate()

  const getTelegramURL = async () => {
      const data = {
          ref: null,
          login: true
      }
      const response = await jobParserClient.telegram.generatePayload(data)
      if (response) {
          return response.start_link
      }
    }

  const validateForm = () => {
    if (!email || !password) {
      setError('Username and password are required')
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

    const formDetails = new UserLoginDTO(
      email,
      password
    ).toJSON();

    try {
      const response = await jobParserClient.authAsUser(formDetails)
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

  const handleLoginMethod = async (method) => {
    setLoading(true)
    try {
      let response
      switch (method) {
        case 'telegram':
          const telegramURL = await getTelegramURL()
          window.open(telegramURL, '_blank')
          break
        // case 'google':
        //   response = await jobParserClient.authByGoogle()
        //   break
        // case 'messenger':
        //   response = await jobParserClient.authByMessenger()
        //   break
        default:
          setError('Unsupported login method')
          setLoading(false)
          return
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-body-tertiary min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md={8}>
            <CCardGroup>
              <CCard className="p-4">
                <CCardBody>
                  <CForm onSubmit={handleSubmit}>
                    <h1>Login</h1>
                    <p className="text-body-secondary">Sign In to your account</p>
                    <CInputGroup className="mb-3">
                      <CInputGroupText>
                        <CIcon icon={cilUser} />
                      </CInputGroupText>
                      <CFormInput
                        placeholder="Email"
                        autoComplete="username"
                        onChange={(e) => setEmail(e.target.value)}
                        value={email}
                      />
                    </CInputGroup>
                    <CInputGroup className="mb-4">
                      <CInputGroupText>
                        <CIcon icon={cilLockLocked} />
                      </CInputGroupText>
                      <CFormInput
                        type="password"
                        placeholder="Password"
                        autoComplete="current-password"
                        onChange={(e) => setPassword(e.target.value)}
                        value={password}
                      />
                    </CInputGroup>
                    <CRow>
                      <CCol xs={6}>
                        <CButton color="primary" className="px-4" disabled={loading} type="submit">
                          {loading ? 'Loading...' : 'Login'}
                        </CButton>
                      </CCol>
                      {error && <p className="text-danger mt-2">{error}</p>}
                      <CCol xs={6} className="text-right">
                        <CButton color="link" className="px-0">
                          Forgot password?
                        </CButton>
                      </CCol>
                    </CRow>
                    <CRow className="mt-3">
                      <CCol xs={12} className="d-flex justify-content-center">
                        <CButtonGroup>
                          <CButton
                            color="info"
                            className="px-4"
                            disabled={loading}
                            onClick={() => handleLoginMethod('telegram')}
                          >
                            <CIcon icon={cibTelegram} size="lg" />
                          </CButton>
                          <CButton
                            color="danger"
                            className="px-4"
                            disabled={loading}
                            onClick={() => handleLoginMethod('google')}
                          >
                            <CIcon icon={cibGoogle} size="lg" />
                          </CButton>
                          <CButton
                            color="primary"
                            className="px-4"
                            disabled={loading}
                            onClick={() => handleLoginMethod('messenger')}
                          >
                            <CIcon icon={cibMessenger} size="lg" />
                          </CButton>
                        </CButtonGroup>
                      </CCol>
                    </CRow>
                  </CForm>
                </CCardBody>
              </CCard>
              <CCard className="text-white bg-primary py-5" style={{ width: '44%' }}>
                <CCardBody className="text-center">
                  <div>
                    <h2>Sign up</h2>
                    <p>
                      Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                      tempor incididunt ut labore et dolore magna aliqua.
                    </p>
                    <Link to="/register">
                      <CButton color="primary" className="mt-3" active tabIndex={-1}>
                        Register Now!
                      </CButton>
                    </Link>
                  </div>
                </CCardBody>
              </CCard>
            </CCardGroup>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default Login
