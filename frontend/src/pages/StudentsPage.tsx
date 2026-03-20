import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Alert, Button, Grid, Stack, Typography } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { studentsApi } from '../api/students';
import { StudentCard } from '../components/StudentCard';
import type { StudentListItem } from '../types';

export function StudentsPage() {
  const navigate = useNavigate();
  const [students, setStudents] = useState<StudentListItem[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    studentsApi
      .list()
      .then(setStudents)
      .catch(() => setError('加载学生列表失败，请确认后端服务与数据库状态。'));
  }, []);

  return (
    <Stack spacing={2.5}>
      <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent='space-between' spacing={1.2}>
        <div>
          <Typography variant='h4'>学生总览</Typography>
          <Typography color='text.secondary'>查看每位学生的主宠物成长状态</Typography>
        </div>
        <Button variant='contained' color='secondary' startIcon={<AddIcon />} onClick={() => navigate('/students/create')}>
          创建学生
        </Button>
      </Stack>

      {error && <Alert severity='error'>{error}</Alert>}

      <Grid container spacing={2}>
        {students.map((student) => (
          <Grid key={student.id} size={{ xs: 12, sm: 6, md: 4 }}>
            <StudentCard student={student} />
          </Grid>
        ))}
      </Grid>
    </Stack>
  );
}



