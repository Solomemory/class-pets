import dayjs from 'dayjs';
import { Card, CardContent, Chip, Stack, Typography } from '@mui/material';
import type { PointLog } from '../types';

interface PointLogListProps {
  logs: PointLog[];
}

export function PointLogList({ logs }: PointLogListProps) {
  if (!logs.length) {
    return <Typography color='text.secondary'>暂无积分记录。</Typography>;
  }

  return (
    <Stack spacing={1.5}>
      {logs.map((log) => (
        <Card key={log.id}>
          <CardContent>
            <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent='space-between' spacing={1.2}>
              <Stack spacing={0.5}>
                <Typography variant='subtitle1'>{log.reason}</Typography>
                <Typography variant='body2' color='text.secondary'>
                  {log.remark || '无备注'}
                </Typography>
                <Typography variant='caption' color='text.secondary'>
                  属性增量：智{log.wisdom_delta >= 0 ? '+' : ''}{log.wisdom_delta} / 专{log.focus_delta >= 0 ? '+' : ''}{log.focus_delta} / 亲{log.affinity_delta >= 0 ? '+' : ''}{log.affinity_delta} / 毅{log.resilience_delta >= 0 ? '+' : ''}{log.resilience_delta} / 活{log.vitality_delta >= 0 ? '+' : ''}{log.vitality_delta}
                </Typography>
                <Typography variant='caption' color='text.secondary'>
                  {dayjs(log.created_at).format('YYYY-MM-DD HH:mm:ss')}
                </Typography>
              </Stack>
              <Stack alignItems={{ xs: 'flex-start', sm: 'flex-end' }} spacing={0.8}>
                <Chip
                  label={`${log.point_change > 0 ? '+' : ''}${log.point_change}`}
                  color={log.point_change >= 0 ? 'success' : 'error'}
                  sx={{ minWidth: 74 }}
                />
                <Typography variant='caption' color='text.secondary'>
                  学生 ID: {log.student_id}
                </Typography>
              </Stack>
            </Stack>
          </CardContent>
        </Card>
      ))}
    </Stack>
  );
}
