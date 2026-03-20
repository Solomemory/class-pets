import { Card, CardContent, LinearProgress, Stack, Typography } from '@mui/material';

interface ProgressInfoCardProps {
  title: string;
  value: string;
  helper?: string;
  progress?: number;
}

export function ProgressInfoCard({ title, value, helper, progress }: ProgressInfoCardProps) {
  return (
    <Card sx={{ minWidth: 200 }}>
      <CardContent>
        <Stack spacing={1}>
          <Typography variant='caption' color='text.secondary'>
            {title}
          </Typography>
          <Typography variant='h5'>{value}</Typography>
          {typeof progress === 'number' && (
            <LinearProgress
              variant='determinate'
              value={Math.max(0, Math.min(100, progress))}
              sx={{
                height: 9,
                borderRadius: 4,
                backgroundColor: 'rgba(255,255,255,0.12)',
                '& .MuiLinearProgress-bar': {
                  background: 'linear-gradient(90deg, #4ed0ff 0%, #f0c768 100%)',
                },
              }}
            />
          )}
          {helper && (
            <Typography variant='body2' color='text.secondary'>
              {helper}
            </Typography>
          )}
        </Stack>
      </CardContent>
    </Card>
  );
}

