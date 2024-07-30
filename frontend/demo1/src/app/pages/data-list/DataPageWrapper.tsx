import React from 'react'
import {PageTitle} from '../../../_metronic/layout/core'
import DataPage from './DataPage'

const DummyDataPageWrapper: React.FC = () => {
  return (
    <>
      <PageTitle breadcrumbs={[]}>Dummy Data Table</PageTitle>
      <DataPage />
    </>
  )
}

export default DummyDataPageWrapper;
