import { createTheme } from '@mui/material/styles';
import { themeTokens } from './tokens';

export const appTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: themeTokens.color.accentCyan,
    },
    secondary: {
      main: themeTokens.color.accentGold,
    },
    background: {
      default: themeTokens.color.bgPrimary,
      paper: themeTokens.color.surface,
    },
    text: {
      primary: themeTokens.color.textPrimary,
      secondary: themeTokens.color.textSecondary,
    },
    success: {
      main: themeTokens.color.success,
    },
  },
  shape: {
    borderRadius: 8,
  },
  typography: {
    fontFamily: '"Noto Sans SC", sans-serif',
    h1: { fontFamily: '"Rajdhani", sans-serif', fontWeight: 700 },
    h2: { fontFamily: '"Rajdhani", sans-serif', fontWeight: 700 },
    h3: { fontFamily: '"Rajdhani", sans-serif', fontWeight: 700 },
    h4: { fontFamily: '"Rajdhani", sans-serif', fontWeight: 700 },
    h5: { fontFamily: '"Rajdhani", sans-serif', fontWeight: 700 },
    h6: { fontFamily: '"Rajdhani", sans-serif', fontWeight: 700 },
    button: { fontFamily: '"Rajdhani", sans-serif', fontWeight: 700, letterSpacing: 0.4 },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          background: 'linear-gradient(165deg, rgba(30,44,63,0.85) 0%, rgba(17,26,37,0.88) 100%)',
          border: `1px solid ${themeTokens.color.line}`,
          boxShadow: themeTokens.shadow.glow,
          backdropFilter: 'blur(8px)',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 6,
          textTransform: 'none',
        },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          borderRadius: 6,
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          fontWeight: 700,
          letterSpacing: 0.3,
        },
      },
    },
  },
});
