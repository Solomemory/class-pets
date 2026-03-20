import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Alert, Card, CardContent, Grid, Stack, Typography } from '@mui/material';
import { studentsApi } from '../api/students';
import { PetStatusPanel } from '../components/PetStatusPanel';
import { PetBadgeList } from '../components/PetBadgeList';
import { PetGrowthTimeline } from '../components/PetGrowthTimeline';
import type { PetArchive } from '../types';

export function PetHomePage() {
  const { studentId } = useParams();
  const [archive, setArchive] = useState<PetArchive | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!studentId) return;
    studentsApi
      .petArchive(Number(studentId))
      .then(setArchive)
      .catch(() => setError('获取宠物档案数据失败。'));
  }, [studentId]);

  if (error) return <Alert severity='error'>{error}</Alert>;
  if (!archive) return <Typography color='text.secondary'>加载中...</Typography>;

  return (
    <Stack spacing={2.2}>
      <Card>
        <CardContent>
          <Typography variant='h4'>宠物档案中枢</Typography>
          <Typography color='text.secondary'>
            学生：{archive.student_name} · 当前主宠：{archive.pet_status.pet_name} · {archive.pet_status.stage_label} · Lv.{archive.pet_status.level}
          </Typography>
        </CardContent>
      </Card>

      <PetStatusPanel petStatus={archive.pet_status} />

      <Grid container spacing={2}>
        <Grid size={{ xs: 12, lg: 7 }}>
          <PetBadgeList badges={archive.badges} />
        </Grid>
        <Grid size={{ xs: 12, lg: 5 }}>
          <PetGrowthTimeline events={archive.timeline} />
        </Grid>
      </Grid>
    </Stack>
  );
}
