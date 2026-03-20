import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Alert, Button, Card, CardContent, Stack, TextField, Typography } from '@mui/material';
import { studentsApi } from '../api/students';

export function CreateStudentPage() {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [gradeClass, setGradeClass] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const student = await studentsApi.create({ name, grade_class: gradeClass || undefined });
      navigate(`/students/${student.id}/select-pet`);
    } catch {
      setError('创建失败，请检查参数后重试。');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{ maxWidth: 680 }}>
      <CardContent>
        <Stack spacing={2.2} component='form' onSubmit={onSubmit}>
          <Typography variant='h4'>创建学生</Typography>
          <Typography color='text.secondary'>创建完成后将立即进入宠物选择流程</Typography>
          {error && <Alert severity='error'>{error}</Alert>}
          <TextField label='姓名' required value={name} onChange={(e) => setName(e.target.value)} />
          <TextField label='年级/班级（可选）' value={gradeClass} onChange={(e) => setGradeClass(e.target.value)} />
          <Button type='submit' variant='contained' color='secondary' disabled={loading}>
            {loading ? '创建中...' : '创建并选择宠物'}
          </Button>
        </Stack>
      </CardContent>
    </Card>
  );
}
