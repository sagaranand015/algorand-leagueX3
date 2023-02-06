// ** MUI Imports
import Box from '@mui/material/Box'
import Link from '@mui/material/Link'
import { Theme } from '@mui/material/styles'
import Typography from '@mui/material/Typography'
import useMediaQuery from '@mui/material/useMediaQuery'

const FooterContent = () => {
  // ** Var
  const hidden = useMediaQuery((theme: Theme) => theme.breakpoints.down('md'))

  return (
    <Box sx={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between' }}>
      <Typography sx={{ mr: 2 }}>
        {`© ${new Date().getFullYear()}, Made with `}
        <Box component='span' sx={{ color: 'error.main' }}>
          ❤️
        </Box>
        {` for `}
        <Link target='_blank' href='https://themeselection.com/'>
          Algorand Gitcoin
        </Link>
      </Typography>
      {hidden ? null : (
        <Box sx={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', '& :not(:last-child)': { mr: 4 } }}>
          <Link
            target='_blank'
            href='https://github.com/themeselection/materio-mui-react-nextjs-admin-template-free/blob/main/LICENSE'
          >
            MIT License
          </Link>
          <Link
            target='_blank'
            href='https://github.com/sagaranand015/algorand-leagueX3/blob/main/README.md'
          >
            Project Documentation
          </Link>
          <Link
            target='_blank'
            href='https://twitter.com/sagaranand015'
          >
            Support
          </Link>
        </Box>
      )}
    </Box>
  )
}

export default FooterContent
