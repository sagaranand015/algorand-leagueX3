// ** MUI Imports
import Grid from '@mui/material/Grid'

// ** Icons Imports
import Poll from 'mdi-material-ui/Poll'
import CurrencyUsd from 'mdi-material-ui/CurrencyUsd'
import HelpCircleOutline from 'mdi-material-ui/HelpCircleOutline'
import BriefcaseVariantOutline from 'mdi-material-ui/BriefcaseVariantOutline'

// ** Custom Components Imports
import CardStatisticsVerticalComponent from 'src/@core/components/card-statistics/card-stats-vertical'

// ** Styled Component Import
import ApexChartWrapper from 'src/@core/styles/libs/react-apexcharts'

// ** Demo Components Imports
import Table from 'src/views/dashboard/Table'
import Trophy from 'src/views/dashboard/Trophy'
import TotalEarning from 'src/views/dashboard/TotalEarning'
import StatisticsCard from 'src/views/dashboard/StatisticsCard'
import WeeklyOverview from 'src/views/dashboard/WeeklyOverview'
import DepositWithdraw from 'src/views/dashboard/DepositWithdraw'
import SalesByCountries from 'src/views/dashboard/SalesByCountries'
import { useAuth } from 'src/configs/authProvider'
import { useEffect, useState } from 'react'
import algosdk from 'algosdk'
import { METHODS } from 'http'
import HelpNotificationCard from 'src/views/cards/HelpNotificationCard'

const Dashboard = (props: any) => {
  const { currentAccount, setCurrentAccount, disconnectAccount, apiToken, setApiToken } = useAuth()
  const [accountConnected, setAccountConnected] = useState(false)

  useEffect(() => {
    console.log("current account on dashboard page is: ", currentAccount)
    if (currentAccount) {
      setAccountConnected(true)
    } else {
      setAccountConnected(false)
    }
  }, [currentAccount])

  useEffect(() => {
    console.log("current apiToken on dashboard page is: ", apiToken)
    if (currentAccount) {
      setApiToken(currentAccount)
    } else {
      setApiToken(null)
    }
  }, [accountConnected])

  return (
    <div>
      {accountConnected && apiToken ? (
        <ApexChartWrapper>
          <Grid container spacing={6}>
            <Grid item xs={12} md={4}>
              <Trophy />
            </Grid>
            <Grid item xs={12} md={8}>
              <StatisticsCard />
            </Grid>
            <Grid item xs={12} md={6} lg={6}>
              <TotalEarning />
            </Grid>
            <Grid item xs={12} md={6} lg={6}>
              <SalesByCountries />
            </Grid>
          </Grid>
        </ApexChartWrapper>
      ) :
        (
          <HelpNotificationCard heading='Connect Wallet' content='Please connect your wallet to continue!' clickButtonText='Connect Wallet' clickButton={setCurrentAccount} />
        )
      }
    </div >
  )
}

export async function getServerSideProps(context: any) {
  // fetch the blog posts from the mock API
  return {
    props: {}
  };
}

export default Dashboard
