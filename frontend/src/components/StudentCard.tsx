import { Button, Card, CardContent, Chip, Stack, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import type { StudentListItem } from '../types';

interface StudentCardProps {
  student: StudentListItem;
}

export function StudentCard({ student }: StudentCardProps) {
  const navigate = useNavigate();

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Stack spacing={1.2}>
          <Typography variant='h6'>{student.name}</Typography>
          <Typography variant='body2' color='text.secondary'>
            班级：{student.grade_class || '未填写'}
          </Typography>
          <Stack direction='row' spacing={1} alignItems='center' flexWrap='wrap'>
            <Chip label={`总积分 ${student.total_points}`} color='secondary' size='small' />
            {student.pet_status ? (
              <>
                <Chip label={`${student.pet_status.pet_name} · Lv.${student.pet_status.level}`} color='primary' size='small' />
                <Chip label={`${student.pet_status.route_label} · ${student.pet_status.stage_star}★`} size='small' variant='outlined' />
              </>
            ) : (
              <Chip label='未绑定宠物' size='small' />
            )}
          </Stack>
          {student.pet_status && (
            <Typography variant='caption' sx={{ color: student.pet_status.route_theme }}>
              {student.pet_status.title}
            </Typography>
          )}
          <Stack direction='row' spacing={1}>
            <Button variant='outlined' onClick={() => navigate(`/students/${student.id}`)}>
              查看详情
            </Button>
            {!student.pet_status && (
              <Button variant='contained' color='secondary' onClick={() => navigate(`/students/${student.id}/select-pet`)}>
                立即选宠
              </Button>
            )}
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
}
