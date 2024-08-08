import React from 'react'
import classNames from 'classnames'
import {
  CCard,
  CCardBody,
  CCardFooter,
  CCardHeader,
  CCol,
  CRow,
  CProgress,
  CButton,
  CButtonGroup,
  CFormLabel,
  CInputGroup,
  CFormInput,
  CInputGroupText,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import {
  cilBriefcase,
  cilCheckCircle,
  cilPeople,
  cilCloudDownload,
} from '@coreui/icons'
import MainChart from 'src/views/dashboard/MainChart'
import WidgetsBrand from 'src/views/widgets/WidgetsBrand'

const Dashboard = () => {
  const jobMetrics = [
    { title: 'Jobs Parsed', value: '12,345', change: '+12.5%', icon: cilBriefcase, color: 'info' },
    { title: 'Jobs Applied', value: '3,678', change: '+5.2%', icon: cilCheckCircle, color: 'success' },
    { title: 'Referrals', value: '789', change: '-2.1%', icon: cilPeople, color: 'warning' },
  ]

  const overallStatistics = {
    totalJobsParsed: 12345,
    totalJobsApplied: 3678,
    totalReferrals: 789,
  }

  const progressExample = [
    { title: 'Jobs Parsed', value: '12,345 Jobs', percent: 40, color: 'info' },
    { title: 'Jobs Applied', value: '3,678 Jobs', percent: 20, color: 'success' },
    { title: 'Referrals', value: '789 Users', percent: 60, color: 'warning' },
  ]

  return (
    <>
      <CRow>
        {jobMetrics.map((metric, index) => (
          <CCol sm={4} key={index}>
            <CCard
              className={`text-white bg-${metric.color} mb-4`}
              style={{ height: '150px' }}
            >
              <CCardBody className="pb-0">
                <center>
                  <div className="text-value-lg" style={{ fontSize: '1.5rem' }}>
                    {metric.value}
                  </div>
                  <div className="small">
                    <span>{metric.change}</span> compared to last month
                  </div>
                </center>
              </CCardBody>
              <CCardFooter className="text-center">
                <CIcon icon={metric.icon} size="sm" />
                <div>{metric.title}</div>
              </CCardFooter>
            </CCard>
          </CCol>
        ))}
      </CRow>

      <CCard className="mb-4">
        <CCardBody>
          <CRow>
            <CCol sm={5}>
              <h4 id="traffic" className="card-title mb-0">
                Statistics
              </h4>
              <div className="small text-body-secondary">January - July 2023</div>
            </CCol>
            <CCol sm={7} className="d-none d-md-block">
              <CButton color="primary" className="float-end">
                <CIcon icon={cilCloudDownload} />
              </CButton>
              <CButtonGroup className="float-end me-3">
                {['Day', 'Month', 'Year'].map((value) => (
                  <CButton
                    color="outline-secondary"
                    key={value}
                    className="mx-0"
                    active={value === 'Month'}
                  >
                    {value}
                  </CButton>
                ))}
              </CButtonGroup>
            </CCol>
          </CRow>
          <MainChart />
        </CCardBody>
        <CCardFooter>
          <CRow
            xs={{ cols: 1, gutter: 4 }}
            sm={{ cols: 2 }}
            lg={{ cols: 4 }}
            xl={{ cols: 5 }}
            className="mb-2 text-center"
          >
            {progressExample.map((item, index, items) => (
              <CCol
                className={classNames({
                  'd-none d-xl-block': index + 1 === items.length,
                })}
                key={index}
              >
                <div className="text-body-secondary">{item.title}</div>
                <div className="fw-semibold text-truncate">
                  {item.value} ({item.percent}%)
                </div>
                <CProgress thin className="mt-2" color={item.color} value={item.percent} />
              </CCol>
            ))}
          </CRow>
        </CCardFooter>
      </CCard>

      <CCard className="mb-4">
        <CCardHeader>Referral Link</CCardHeader>
        <CInputGroup>
          <CFormInput type="text" id="referralsLink" readOnly disabled defaultValue="https://example.com" />
          <CInputGroupText>
            <CButton color="primary">Copy</CButton>
          </CInputGroupText>
        </CInputGroup>
      </CCard>

      <CCard className="mb-4">
        <CCardHeader>Social Networks</CCardHeader>
        <CCardBody>
          <WidgetsBrand withCharts />
        </CCardBody>
      </CCard>

      <CCard className="mb-4">
        <CCardHeader>Overall Statistics</CCardHeader>
        <CCardBody>
          <CRow>
            <CCol sm={4}>
              <div className="border-start border-start-4 border-start-info py-1 px-3 mb-3">
                <div className="text-body-secondary text-truncate small">Total Jobs Parsed</div>
                <div className="fs-5 fw-semibold">{overallStatistics.totalJobsParsed}</div>
              </div>
            </CCol>
            <CCol sm={4}>
              <div className="border-start border-start-4 border-start-success py-1 px-3 mb-3">
                <div className="text-body-secondary text-truncate small">Total Jobs Applied</div>
                <div className="fs-5 fw-semibold">{overallStatistics.totalJobsApplied}</div>
              </div>
            </CCol>
            <CCol sm={4}>
              <div className="border-start border-start-4 border-start-warning py-1 px-3 mb-3">
                <div className="text-body-secondary text-truncate small">Total Referrals</div>
                <div className="fs-5 fw-semibold">{overallStatistics.totalReferrals}</div>
              </div>
            </CCol>
          </CRow>
        </CCardBody>
      </CCard>
    </>
  )
}

export default Dashboard
