import React from 'react'
import {
  CCard,
  CCardBody,
  CCardFooter,
  CCardHeader,
  CCol,
  CRow,
  CButton,
  CButtonGroup,
  CInputGroup,
  CFormInput,
  CInputGroupText, CProgress,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilBriefcase, cilCheckCircle, cilPeople, cilCloudDownload } from '@coreui/icons'
import MainChart from 'src/views/dashboard/MainChart'
import WidgetsBrand from 'src/views/widgets/WidgetsBrand'
import {getStyle} from "@coreui/utils";
import classNames from "classnames";

const random = (min, max) => {
  return Math.floor(Math.random() * (max - min + 1)) + min;
};

const Dashboard = () => {
  // Job Metrics Data
  const jobMetrics = {
    jobsParsed: { title: 'Jobs Parsed', value: 12345, change: '+12.5%', icon: cilBriefcase, color: 'info' },
    jobsApplied: { title: 'Jobs Applied', value: 3678, change: '+5.2%', icon: cilCheckCircle, color: 'success' },
    referrals: { title: 'Referrals', value: 789, change: '-2.1%', icon: cilPeople, color: 'warning' },
  };

  // Chart Data
  const chartData = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [
      {
        label: 'My First dataset',
        backgroundColor: `rgba(${getStyle('--cui-info-rgb')}, .1)`,
        borderColor: getStyle('--cui-info'),
        pointHoverBackgroundColor: getStyle('--cui-info'),
        borderWidth: 2,
        data: [
          random(50, 200),
          random(50, 200),
          random(50, 200),
          random(50, 200),
          random(50, 200),
          random(50, 200),
          random(50, 200),
        ],
        fill: true,
      },
      {
        label: 'My Second dataset',
        backgroundColor: 'transparent',
        borderColor: getStyle('--cui-success'),
        pointHoverBackgroundColor: getStyle('--cui-success'),
        borderWidth: 2,
        data: [
          random(50, 200),
          random(50, 200),
          random(50, 200),
          random(50, 200),
          random(50, 200),
          random(50, 200),
          random(50, 200),
        ],
      },
      {
        label: 'My Third dataset',
        backgroundColor: 'transparent',
        borderColor: getStyle('--cui-danger'),
        pointHoverBackgroundColor: getStyle('--cui-danger'),
        borderWidth: 1,
        borderDash: [8, 5],
        data: [65, 65, 65, 65, 65, 65, 65],
      },
    ],
  };

  return (
    <>
      <CRow>
        {Object.keys(jobMetrics).map((key, index) => {
          const metric = jobMetrics[key];
          return (
            <CCol sm={4} key={index}>
              <CCard
                className={`text-white bg-${metric.color} mb-4`}
                style={{ height: '150px' }}
              >
                <CCardBody className="pb-0">
                  <center>
                    <div className="text-value-lg" style={{ fontSize: '1.5rem' }}>
                      {metric.value.toLocaleString()}
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
          );
        })}
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
          <MainChart data={chartData} /> {/* Pass chartData to MainChart */}
        </CCardBody>
        <CCardFooter>
          <CRow md={{ cols: 3 }} className="mb-2 text-center">
            {Object.keys(jobMetrics).map((key, index) => {
              const metric = jobMetrics[key];
              return (
                <CCol
                  key={index}
                  className={classNames({
                    'd-none d-xl-block': key === 'someOtherMetricToHide',
                  })}
                >
                  <div className="text-body-secondary">{metric.title}</div>
                  <div className="fw-semibold text-truncate">
                    {metric.value.toLocaleString()}
                  </div>
                  <CProgress thin className="mt-2" color={metric.color} value={100} />
                </CCol>
              );
            })}
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
                <div className="fs-5 fw-semibold">{jobMetrics.jobsParsed.value.toLocaleString()}</div>
              </div>
            </CCol>
            <CCol sm={4}>
              <div className="border-start border-start-4 border-start-success py-1 px-3 mb-3">
                <div className="text-body-secondary text-truncate small">Total Jobs Applied</div>
                <div className="fs-5 fw-semibold">{jobMetrics.jobsApplied.value.toLocaleString()}</div>
              </div>
            </CCol>
            <CCol sm={4}>
              <div className="border-start border-start-4 border-start-warning py-1 px-3 mb-3">
                <div className="text-body-secondary text-truncate small">Total Referrals</div>
                <div className="fs-5 fw-semibold">{jobMetrics.referrals.value.toLocaleString()}</div>
              </div>
            </CCol>
          </CRow>
        </CCardBody>
      </CCard>
    </>
  );
};

export default Dashboard;
