import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import { authApi } from '../api/auth';

export function LoginPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('teacher');
  const [password, setPassword] = useState('123456');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await authApi.login({ username, password });
      localStorage.setItem('class_pets_token', res.token);
      navigate('/students');
    } catch {
      setError('登录失败，请检查后端服务。');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      minHeight='100vh'
      display='flex'
      alignItems='center'
      justifyContent='center'
      sx={{ px: 2 }}
    >
      <Card sx={{ width: '100%', maxWidth: 480 }}>
        <CardContent>
          <Stack spacing={2.5} component='form' onSubmit={onSubmit}>
            <Typography variant='h3'>宠物课堂登录</Typography>
            <Typography color='text.secondary'>
              进入“课堂表现 x 战宠养成”控制台
            </Typography>
            {error && <Alert severity='error'>{error}</Alert>}
            <TextField label='账号' value={username} onChange={(e) => setUsername(e.target.value)} required />
            <TextField
              label='密码'
              type='password'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <Button type='submit' variant='contained' color='secondary' disabled={loading}>
              {loading ? '登录中...' : '进入系统'}
            </Button>
          </Stack>
        </CardContent>
      </Card>
    </Box>
  );
}
