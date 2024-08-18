import React, {useEffect} from 'react'
import {
  CButton,
  CButtonGroup,
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
import { cilLockLocked, cibTelegram, cibGoogle, cibMessenger } from '@coreui/icons'
import { useNavigate } from "react-router-dom"
import jobParserClient from "src/client/Client"
import {getCookies, setCookie} from "src/helpers/_auth"
import UserRegisterDTO from "src/client/DTOs/UserRegisterDTO"

const Register = () => {
  const [email, setEmail] = React.useState('')
  const [password, setPassword] = React.useState('')
  const [confirmPassword, setConfirmPassword] = React.useState('')
  const [error, setError] = React.useState('')
  const [loading, setLoading] = React.useState(false)

  const [refer, setRefer] = React.useState(null)

  const navigate = useNavigate()

  useEffect(() => {
    const getRefer = async () => {
      const cookies = getCookies()
      if (cookies.refer) {
        setRefer(cookies.refer)
      }
    }
    getRefer()
  }, []);

  const getTelegramURL = async () => {
      const data = {
          ref: refer || 0,
          login: null
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
    ).toJSON()

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
      setError(e.response?.message || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  const handleRegisterMethod = async (method) => {
    setLoading(true)
    try {
      let response
      switch (method) {
        case 'telegram':
          const telegramURL = await getTelegramURL()
          window.open(telegramURL, '_blank')
          break
        // case 'google':
        //   response = await jobParserClient.registerByGoogle()
        //   break
        // case 'messenger':
        //   response = await jobParserClient.registerByMessenger()
        //   break
        default:
          setError('Unsupported registration method')
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
                <div className="d-flex justify-content-center mt-3">
                  <CButtonGroup>
                    <CButton
                      color="info"
                      className="px-4"
                      disabled={loading}
                      onClick={() => handleRegisterMethod('telegram')}
                    >
                      <CIcon icon={cibTelegram} size="lg" />
                    </CButton>
                    <CButton
                      color="danger"
                      className="px-4"
                      disabled={loading}
                      onClick={() => handleRegisterMethod('google')}
                    >
                      <CIcon icon={cibGoogle} size="lg" />
                    </CButton>
                    <CButton
                      color="primary"
                      className="px-4"
                      disabled={loading}
                      onClick={() => handleRegisterMethod('messenger')}
                    >
                      <CIcon icon={cibMessenger} size="lg" />
                    </CButton>
                  </CButtonGroup>
                </div>
              </CCardBody>
            </CCard>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default Register
