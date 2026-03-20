import dayjs from 'dayjs';
import { Card, CardContent, Chip, Grid, Stack, Typography } from '@mui/material';
import type { PetBadge } from '../types';
import { rarityPalette } from '../theme/tokens';

interface PetBadgeListProps {
  badges: PetBadge[];
}

export function PetBadgeList({ badges }: PetBadgeListProps) {
  if (!badges.length) {
    return (
      <Card>
        <CardContent>
          <Typography variant='h6'>成就徽章</Typography>
          <Typography color='text.secondary'>暂无徽章，继续培养可解锁更多成就。</Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Stack spacing={1.3}>
          <Typography variant='h6'>成就徽章（{badges.length}）</Typography>
          <Grid container spacing={1}>
            {badges.map((badge) => {
              const rarity = rarityPalette[badge.rarity] ?? rarityPalette['普通'];
              return (
                <Grid key={badge.id} size={{ xs: 12, sm: 6, lg: 4 }}>
                  <Stack
                    spacing={0.5}
                    sx={{
                      p: 1,
                      border: `1px solid ${rarity.border}`,
                      background: 'rgba(18, 28, 40, 0.6)',
                    }}
                  >
                    <Stack direction='row' justifyContent='space-between' alignItems='center'>
                      <Typography variant='subtitle2'>{badge.name}</Typography>
                      <Chip size='small' label={badge.rarity} sx={{ bgcolor: rarity.chip, border: `1px solid ${rarity.border}` }} />
                    </Stack>
                    <Typography variant='caption' color='text.secondary'>
                      {badge.description}
                    </Typography>
                    <Typography variant='caption' color='text.secondary'>
                      解锁时间：{dayjs(badge.unlocked_at).format('YYYY-MM-DD HH:mm')}
                    </Typography>
                  </Stack>
                </Grid>
              );
            })}
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}
