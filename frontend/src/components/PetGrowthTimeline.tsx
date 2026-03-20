import dayjs from 'dayjs';
import { Card, CardContent, Stack, Typography } from '@mui/material';
import type { PetTimelineEvent } from '../types';

interface PetGrowthTimelineProps {
  events: PetTimelineEvent[];
}

export function PetGrowthTimeline({ events }: PetGrowthTimelineProps) {
  return (
    <Card>
      <CardContent>
        <Stack spacing={1.1}>
          <Typography variant='h6'>成长时间线</Typography>
          {events.map((event) => (
            <Stack
              key={`${event.event_code}_${event.event_time}`}
              spacing={0.3}
              sx={{
                borderLeft: '2px solid rgba(78,208,255,0.35)',
                pl: 1,
                py: 0.2,
              }}
            >
              <Typography variant='subtitle2'>{event.event_name}</Typography>
              <Typography variant='caption' color='text.secondary'>
                {dayjs(event.event_time).format('YYYY-MM-DD HH:mm')}
              </Typography>
              <Typography variant='body2' color='text.secondary'>
                {event.detail}
              </Typography>
            </Stack>
          ))}
        </Stack>
      </CardContent>
    </Card>
  );
}
