// ** MUI Imports
import Box from '@mui/material/Box'
import { Theme } from '@mui/material/styles'
import TextField from '@mui/material/TextField'
import IconButton from '@mui/material/IconButton'
import useMediaQuery from '@mui/material/useMediaQuery'
import InputAdornment from '@mui/material/InputAdornment'

// ** Icons Imports
import Menu from 'mdi-material-ui/Menu'
import Magnify from 'mdi-material-ui/Magnify'

// ** Type Import
import { Settings } from 'src/@core/context/settingsContext'

// ** Components
import ModeToggler from 'src/@core/layouts/components/shared-components/ModeToggler'
import UserDropdown from 'src/@core/layouts/components/shared-components/UserDropdown'
import NotificationDropdown from 'src/@core/layouts/components/shared-components/NotificationDropdown'
import { useAuth } from 'src/configs/authProvider'
import { useEffect, useState } from 'react'
import algosdk from 'algosdk'

interface Props {
  hidden: boolean
  settings: Settings
  toggleNavVisibility: () => void
  saveSettings: (values: Settings) => void
}

const shortenAddress = (address: string) => {
  if (address)
    return address.substring(0, 6) + "..." + address.substring(address.length - 4, address.length)
}

const AppBarContent = (props: Props) => {
  // ** Props
  const { hidden, settings, saveSettings, toggleNavVisibility } = props

  const client = new algosdk.Algodv2("", "https://testnet-api.algonode.cloud", "");

  const { currentAccount, setCurrentAccount, disconnectAccount } = useAuth()
  const [accountBalance, setAccountBalance] = useState(0)

  useEffect(() => {
    const fetchAccountBalance = async (account: any) => {
      const accountInfo = await client
        .accountInformation(account)
        .setIntDecoding(algosdk.IntDecoding.BIGINT)
        .do();

      setAccountBalance(Number(accountInfo.amount))
    }

    if (currentAccount) {
      fetchAccountBalance(currentAccount)
    }
  }, [currentAccount])

  // ** Hook
  const hiddenSm = useMediaQuery((theme: Theme) => theme.breakpoints.down('sm'))

  return (
    <Box sx={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
      <Box className='actions-left' sx={{ mr: 2, display: 'flex', alignItems: 'center' }}>
      </Box>
      <Box className='actions-right' sx={{ display: 'flex', alignItems: 'center' }}>
        <ModeToggler settings={settings} saveSettings={saveSettings} />
        {currentAccount ? (
          <div className="flex items-center">
            <p className="mr-6 border px-4 py-2">{accountBalance} ALGO</p>
            <h4 onClick={disconnectAccount} className="cursor-pointer">{shortenAddress(currentAccount)}</h4>
          </div>

        ) : (
          <button className="px-4 py-2 text-lg border border-orange-600 text-orange-600" onClick={setCurrentAccount}>Connect Wallet</button>
        )}
      </Box>
    </Box>
  )
}

export default AppBarContent
