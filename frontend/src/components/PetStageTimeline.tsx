import { Box, Chip, Paper, Stack, Typography } from '@mui/material';
import type { PetStageConfig } from '../types';
import { PetStageMedia } from './PetStageMedia';

interface PetStageTimelineProps {
  stages: PetStageConfig[];
  currentStageIndex: number;
  petTemplateId?: number;
}

export function PetStageTimeline({ stages, currentStageIndex, petTemplateId }: PetStageTimelineProps) {
  return (
    <Stack spacing={1.5}>
      {stages
        .sort((a, b) => a.stage_index - b.stage_index)
        .map((stage) => {
          const active = stage.stage_index === currentStageIndex;
          const unlocked = stage.stage_index < currentStageIndex;

          return (
            <Paper
              key={stage.id}
              sx={{
                p: 1.5,
                border: active ? '1px solid #f0c768' : '1px solid rgba(157,178,205,0.25)',
                background: active
                  ? 'linear-gradient(120deg, rgba(240,199,104,0.16), rgba(78,208,255,0.12))'
                  : 'rgba(20,30,44,0.7)',
              }}
            >
              <Stack direction='row' justifyContent='space-between' alignItems='center'>
                <Typography variant='subtitle1'>
                  {stage.stage_index}. {stage.stage_name}
                </Typography>
                <Chip
                  size='small'
                  label={active ? '当前阶段' : unlocked ? '已解锁' : '未解锁'}
                  color={active ? 'secondary' : unlocked ? 'success' : 'default'}
                />
              </Stack>

              <Stack direction={{ xs: 'column', md: 'row' }} spacing={1.4} sx={{ mt: 1.2 }}>
                {petTemplateId && (
                  <Box
                    sx={{
                      width: { xs: '100%', md: 170 },
                      minWidth: { xs: '100%', md: 170 },
                      aspectRatio: '1 / 1',
                      borderRadius: 1,
                      background:
                        'radial-gradient(circle at 50% 35%, rgba(78,208,255,0.12), transparent 62%), linear-gradient(180deg, rgba(12,18,27,0.9), rgba(22,30,43,0.62))',
                      border: '1px solid rgba(157,178,205,0.22)',
                      p: 1,
                      overflow: 'hidden',
                      alignSelf: { xs: 'stretch', md: 'flex-start' },
                    }}
                  >
                    <PetStageMedia petTemplateId={petTemplateId} stageIndex={stage.stage_index} alt={stage.stage_name} />
                  </Box>
                )}

                <Typography variant='body2' color='text.secondary' sx={{ mt: { xs: 0, md: 0.6 } }}>
                  {stage.stage_description}
                </Typography>
              </Stack>
            </Paper>
          );
        })}
    </Stack>
  );
}
