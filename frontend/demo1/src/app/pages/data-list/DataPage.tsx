/* eslint-disable jsx-a11y/anchor-is-valid */
import React, {useEffect, useState} from 'react'
import {DummyDataItem, useAuth} from '../../modules/auth'
import {getData} from '../../modules/data-list/requests.ts'

const DataPage: React.FC = () => {
  const {auth} = useAuth()
  const [data, setData] = useState<DummyDataItem[]>([])

  async function fetchData() {
    try {
      const token = auth?.api_token ?? ''
      const data = await getData(token)
      setData(data)
    } catch (error) {
      console.log('Error fetching data:', error)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  return (
    <>
      <div className={`card `}>
        {/* begin::Header */}
        <div className='card-header border-0 pt-5'>
          <h3 className='card-title align-items-start flex-column'>
            <span className='card-label fw-bold fs-3 mb-1'>Dummy Data</span>
            {/* <span className='text-muted mt-1 fw-semibold fs-7'>Over 500 members</span> */}
          </h3>
          <div
            className='card-toolbar'
            data-bs-toggle='tooltip'
            data-bs-placement='top'
            data-bs-trigger='hover'
            title='Click to add a user'
          ></div>
        </div>
        {/* end::Header */}
        {/* begin::Body */}
        <div className='card-body py-3'>
          {/* begin::Table container */}
          <div className='table-responsive'>
            {/* begin::Table */}
            <table className='table table-row-dashed table-row-gray-300 align-middle gs-0 gy-4'>
              {/* begin::Table head */}
              <thead>
                <tr className='fw-bold text-muted'>
                  <th className='w-25px'>
                    <div className='form-check form-check-sm form-check-custom form-check-solid'>
                      <input
                        className='form-check-input'
                        type='checkbox'
                        value='1'
                        data-kt-check='true'
                        data-kt-check-target='.widget-9-check'
                      />
                    </div>
                  </th>
                  <th className='min-w-140px'>First Name</th>
                  <th className='min-w-120px'>Last Name</th>
                  <th className='min-w-100px '>Phone</th>
                </tr>
              </thead>
              {/* end::Table head */}
              {/* begin::Table body */}
              <tbody>
                {data.length > 0 ? (
                  data.map((item, index) => (
                    <tr key={index}>
                      <td>
                        <div className='form-check form-check-sm form-check-custom form-check-solid'>
                          <input
                            className='form-check-input widget-9-check'
                            type='checkbox'
                            value=''
                          />
                        </div>
                      </td>
                      <td>
                        <div className='text-muted fw-bold text-muted d-block fs-7'>
                          {item.first_name || ''}
                        </div>
                      </td>
                      <td className='text-end'>
                        <div className='d-flex flex-column w-100 me-2'>
                          <div className='d-flex flex-stack mb-2'>
                            <div className='text-muted fw-bold text-muted d-block fs-7'>
                              {item.last_name || ''}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td>
                        <div className='d-flex  flex-shrink-0'>
                          <div className='text-muted fw-bold text-muted d-block fs-7'>
                            {item.phone || ''}
                          </div>
                        </div>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={4} className='text-center'>
                      <span>No data available</span>
                    </td>
                  </tr>
                )}
              </tbody>
              {/* end::Table body */}
            </table>
            {/* end::Table */}
          </div>
          {/* end::Table container */}
        </div>
        {/* begin::Body */}
      </div>
    </>
  )
}

export default DataPage
