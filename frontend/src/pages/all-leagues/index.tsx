// ** React Imports
import { SyntheticEvent, useEffect, useState } from 'react'

// ** MUI Imports
import Box from '@mui/material/Box'
import Card from '@mui/material/Card'
import TabList from '@mui/lab/TabList'
import TabPanel from '@mui/lab/TabPanel'
import TabContext from '@mui/lab/TabContext'
import { styled } from '@mui/material/styles'
import MuiTab, { TabProps } from '@mui/material/Tab'
import Grid from '@mui/material/Grid'

// ** Icons Imports
import AccountOutline from 'mdi-material-ui/AccountOutline'
import LockOpenOutline from 'mdi-material-ui/LockOpenOutline'
import InformationOutline from 'mdi-material-ui/InformationOutline'

// ** Demo Tabs Imports
import TabInfo from 'src/views/account-settings/TabInfo'
import TabAccount from 'src/views/account-settings/TabAccount'
import TabSecurity from 'src/views/account-settings/TabSecurity'

// ** Third Party Styles Imports
import 'react-datepicker/dist/react-datepicker.css'

import { FetchDataFromIpfsLink, GetLeagueDataIpfsLink, GetSquadDataIpfsLink } from 'src/@core/utils/nftStorage'
import { ALL_LEAGUES } from 'src/@core/utils/constants'
import { Button, CardActions, CardContent, CardMedia, Collapse, Divider, FormControl, FormHelperText, IconButton, InputLabel, MenuItem, Modal, Typography } from '@mui/material'
import LoadingButton from '@mui/lab/LoadingButton';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { ChevronDown, ChevronUp } from 'mdi-material-ui'
import { isValidLeadingWildcardRoute } from '@json-rpc-tools/utils'
import { useAuth } from 'src/configs/authProvider'
import { getUserSquadData, ParticipateWithUserAddress } from 'src/@core/utils/api-calls'
import TypographyHeadings from 'src/views/typography/TypographyHeadings'
import TypographyTexts from 'src/views/typography/TypographyTexts'

async function getAllLeaguesData() {
  var allLeaguesLink = FetchDataFromIpfsLink(ALL_LEAGUES)
  var ipfsResp = await fetch(allLeaguesLink)
  var finalResp = await ipfsResp.json()
  return finalResp
}

interface ILeagueData {
  appId: BigInteger,
  leagueName: string,
  leagueImg: string,
  leagueMetadata: string,
  competitionName: string,
  isRunning: boolean,
  isFinished: boolean,
  leaguePrice: string
}

const style = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '60%',
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

const AllLeagues = (props: any) => {
  // ** State
  const [value, setValue] = useState<string>('account')
  const [allLeaguesData, setAllLeaguesData] = useState<ILeagueData[]>([])
  const [showLeaguesData, setShowLeaguesData] = useState<boolean>(false)
  const { currentAccount, setCurrentAccount, disconnectAccount, apiToken, setApiToken } = useAuth()
  const [squadData, setSquadData] = useState<any>([])
  const [selectedLeague, setSelectedLeague] = useState<ILeagueData>()
  const [selectedSquad, setSelectedSquad] = useState<any>()
  const [isLoading, settIsLoading] = useState<boolean>(false)

  const [modalOpen, setModalOpen] = useState(false);
  const handleModalOpen = () => setModalOpen(true);
  const handleModalClose = () => setModalOpen(false);

  const handleModalChange = (event: SelectChangeEvent) => {
    setSelectedSquad(event.target.value)
  };

  useEffect(() => {
    if (props && props.leagues) {
      setAllLeaguesData(props.leagues.leagues)
      setShowLeaguesData(true)
    }

    if (showLeaguesData) {
      (async () => {
        const sqs = await getUserSquadData(apiToken)
        if (sqs) {
          setSquadData(sqs.squads)
        }

      })();
    }
  }, [showLeaguesData, props])

  const [collapse, setCollapse] = useState<boolean>(false)
  const handleClick = () => {
    setCollapse(!collapse)
  }

  async function ParticipateInLeague(selectedLeague: ILeagueData) {
    console.log("participatig in league")
    console.log("----- squad data is:", squadData)
    setSelectedLeague(selectedLeague)
    handleModalOpen()
  }

  async function ConfirmParticipation() {
    settIsLoading(true)
    console.log("confirming participation...", selectedLeague, selectedSquad)

    const l_data = await GetLeagueDataIpfsLink(selectedLeague)
    const sq_data = await GetSquadDataIpfsLink(selectedSquad)

    const participateResp = await ParticipateWithUserAddress(apiToken, l_data, sq_data)
    console.log("participate response in page: ", l_data, sq_data, participateResp)
    settIsLoading(false)
    setModalOpen(false)
    alert("Participation Successful. Please navigate to My-leagues page to see your participation")
  }

  return (
    <div>
      <Modal
        open={modalOpen}
        onClose={handleModalClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <Grid container spacing={6}>
            <Grid item xs={12}>
              <Typography id="modal-modal-title" variant="h6" component="h2">
                Participate in {selectedLeague?.leagueName}
              </Typography>
            </Grid>
            <Grid item xs={12}>
              <FormControl sx={{ m: 1, minWidth: 120, width: '100%' }}>
                <InputLabel id="demo-simple-select-helper-label">Select your Squad</InputLabel>
                <Select
                  labelId="demo-simple-select-helper-label"
                  id="demo-simple-select-helper"
                  defaultValue=""
                  value={selectedSquad}
                  label="My Squads"
                  onChange={handleModalChange}
                >
                  {selectedLeague && squadData.map((sq: any) => {
                    return <MenuItem value={sq}>{sq.squadName}</MenuItem>
                  })}
                </Select>
                <FormHelperText>Select your squad for {selectedLeague?.leagueName}</FormHelperText>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <Button variant='contained' sx={{ py: 2.5, width: '100%', borderTopLeftRadius: 0, borderTopRightRadius: 0 }} onClick={() => ConfirmParticipation()} disabled={isLoading}>
                <LoadingButton loading={isLoading}></LoadingButton>
                Confirm Participation with {selectedLeague?.leaguePrice} ALGO
              </Button>
            </Grid>
          </Grid>
        </Box>
      </Modal>
      {
        allLeaguesData.length > 0 ?
          <Grid container spacing={6}>
            {
              allLeaguesData.map((league: ILeagueData) => {
                return <Grid item xs={12} sm={6} md={4}>
                  <Card key={league.leagueName}>
                    {/* image="https://ipfs.io/ipfs/bafybeihbmt4n5gr6qifjhu6haxrx433rzmvpw4smvywt2xf4nn3gqhvckq" */}
                    <CardMedia sx={{ height: '14.5625rem' }} image={FetchDataFromIpfsLink(league.leagueImg)} />
                    <CardContent>
                      <Typography variant='h6' sx={{ marginBottom: 2 }}>
                        {league.leagueName}
                      </Typography>
                      <Typography variant='body2'>
                        Although cards can support multiple actions, UI controls, and an overflow menu.
                      </Typography>
                    </CardContent>
                    <CardActions className='card-action-dense'>
                      <Box
                        sx={{
                          width: '100%',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between'
                        }}
                      >
                        <Button onClick={handleClick}>Details</Button>
                        <IconButton size='small' onClick={handleClick}>
                          {collapse ? <ChevronUp sx={{ fontSize: '1.875rem' }} /> : <ChevronDown sx={{ fontSize: '1.875rem' }} />}
                        </IconButton>
                      </Box>
                    </CardActions>
                    <Collapse in={collapse}>
                      <Divider sx={{ margin: 0 }} />
                      <CardContent>
                        <Typography variant='body2'>
                          I&prime;m a thing. But, like most politicians, he promised more than he could deliver. You won&prime;t have
                          time for sleeping, soldier, not with all the bed making you&prime;ll be doing. Then we&prime;ll go with that
                          data file! Hey, you add a one and two zeros to that or we walk! You&prime;re going to do his laundry?
                          I&prime;ve got to find a way to escape.
                        </Typography>
                      </CardContent>
                    </Collapse>

                    {league.isFinished ? <Button variant='contained' disabled={true} sx={{ py: 2.5, width: '100%', borderTopLeftRadius: 0, borderTopRightRadius: 0 }}>
                      League Concluded
                    </Button> : <Button variant='contained' sx={{ py: 2.5, width: '100%', borderTopLeftRadius: 0, borderTopRightRadius: 0 }} onClick={() => ParticipateInLeague(league)}>
                      Participate
                    </Button>}

                  </Card>
                </Grid>
              })
            }
          </Grid>
          :
          <div>Loading</div>
      }
    </div >
  )
}

export async function getStaticProps(context: any) {
  var leaguesData = await getAllLeaguesData()
  return {
    props: {
      'leagues': leaguesData
    }
  };
}

export default AllLeagues
