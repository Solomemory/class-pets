import { useState } from 'react';
import PetsIcon from '@mui/icons-material/Pets';
import ReceiptLongIcon from '@mui/icons-material/ReceiptLong';
import LogoutIcon from '@mui/icons-material/Logout';
import MenuIcon from '@mui/icons-material/Menu';
import {
  AppBar,
  Box,
  Button,
  Container,
  Drawer,
  IconButton,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Stack,
  Toolbar,
  Typography,
} from '@mui/material';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';

const navItems = [
  { label: '学生列表', path: '/students', icon: <PetsIcon fontSize='small' /> },
  { label: '积分记录', path: '/points', icon: <ReceiptLongIcon fontSize='small' /> },
];

export function AppLayout() {
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const logout = () => {
    localStorage.removeItem('class_pets_token');
    navigate('/login');
  };

  return (
    <Box minHeight='100vh'>
      <AppBar
        position='sticky'
        elevation={0}
        sx={{
          background: 'linear-gradient(90deg, rgba(11,17,26,0.95), rgba(20,31,46,0.95))',
          borderBottom: '1px solid rgba(78,208,255,0.25)',
          backdropFilter: 'blur(12px)',
        }}
      >
        <Toolbar sx={{ display: { xs: 'flex', sm: 'none' }, minHeight: '56px !important', px: 1.2, gap: 1 }}>
          <Typography variant='h6' sx={{ flex: 1 }}>
            宠物课堂
          </Typography>
          <IconButton color='inherit' onClick={() => setMobileMenuOpen(true)} aria-label='打开菜单'>
            <MenuIcon />
          </IconButton>
        </Toolbar>

        <Toolbar sx={{ display: { xs: 'none', sm: 'flex' }, minHeight: '64px !important', gap: 1.2 }}>
          <Typography variant='h5' sx={{ mr: 1, whiteSpace: 'nowrap' }}>
            宠物课堂
          </Typography>

          <Stack direction='row' spacing={0.8} sx={{ flex: 1, minWidth: 0 }}>
            {navItems.map((item) => (
              <Button
                key={item.path}
                component={NavLink}
                to={item.path}
                startIcon={item.icon}
                color='inherit'
                sx={{
                  whiteSpace: 'nowrap',
                  borderRadius: 1,
                  px: 1.25,
                  '&.active': {
                    color: '#0b111a',
                    bgcolor: '#f0c768',
                  },
                }}
              >
                {item.label}
              </Button>
            ))}
          </Stack>

          <Button
            variant='outlined'
            color='inherit'
            startIcon={<LogoutIcon />}
            sx={{ borderRadius: 1, minWidth: 84 }}
            onClick={logout}
          >
            退出
          </Button>
        </Toolbar>
      </AppBar>

      <Drawer
        anchor='right'
        open={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
        PaperProps={{
          sx: {
            width: 258,
            background: 'linear-gradient(180deg, rgba(13,20,30,0.98), rgba(17,28,40,0.98))',
            borderLeft: '1px solid rgba(78,208,255,0.22)',
            borderRadius: 0,
          },
        }}
      >
        <Box sx={{ p: 1.4, borderBottom: '1px solid rgba(78,208,255,0.2)' }}>
          <Typography variant='h6'>导航</Typography>
        </Box>

        <List sx={{ py: 0.6 }}>
          {navItems.map((item) => (
            <ListItemButton
              key={item.path}
              component={NavLink}
              to={item.path}
              onClick={() => setMobileMenuOpen(false)}
              sx={{
                borderRadius: 1,
                mx: 0.8,
                my: 0.25,
                '&.active': {
                  bgcolor: 'rgba(240,199,104,0.9)',
                  color: '#0b111a',
                },
                '&.active .MuiListItemIcon-root': {
                  color: '#0b111a',
                },
              }}
            >
              <ListItemIcon sx={{ minWidth: 34, color: 'inherit' }}>{item.icon}</ListItemIcon>
              <ListItemText primary={item.label} />
            </ListItemButton>
          ))}
        </List>

        <Box sx={{ mt: 'auto', p: 1.2, borderTop: '1px solid rgba(78,208,255,0.16)' }}>
          <Button fullWidth variant='outlined' color='inherit' startIcon={<LogoutIcon />} sx={{ borderRadius: 1 }} onClick={logout}>
            退出登录
          </Button>
        </Box>
      </Drawer>

      <Container maxWidth='xl' sx={{ py: { xs: 2, md: 3 } }}>
        <Outlet />
      </Container>
    </Box>
  );
}

