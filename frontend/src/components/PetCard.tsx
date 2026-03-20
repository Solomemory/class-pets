import { Box, Button, Card, CardContent, Chip, Stack, Typography } from '@mui/material';
import type { PetTemplate } from '../types';
import { rarityPalette } from '../theme/tokens';
import { PetStageMedia } from './PetStageMedia';

interface PetCardProps {
  pet: PetTemplate;
  onSelect?: (petTemplateId: number) => void;
  selectable?: boolean;
}

export function PetCard({ pet, onSelect, selectable }: PetCardProps) {
  const rarity = rarityPalette[pet.rarity] ?? rarityPalette['普通'];
  const baseStage = [...pet.stage_configs].sort((a, b) => a.stage_index - b.stage_index)[0];

  return (
    <Card
      sx={{
        height: '100%',
        border: `1px solid ${rarity.border}`,
        background:
          'linear-gradient(155deg, rgba(35,50,69,0.9) 0%, rgba(15,23,34,0.95) 65%, rgba(10,16,25,0.97) 100%)',
      }}
    >
      <CardContent>
        <Stack spacing={1.3}>
          <Box
            sx={{
              width: '100%',
              aspectRatio: '1 / 1',
              borderRadius: 1,
              border: `1px solid ${rarity.border}`,
              boxShadow: '0 0 20px rgba(78, 208, 255, 0.2)',
              background:
                'radial-gradient(circle at 50% 35%, rgba(78,208,255,0.14), transparent 62%), linear-gradient(180deg, rgba(10,16,25,0.92), rgba(18,27,39,0.82))',
              p: 1.5,
              overflow: 'hidden',
            }}
          >
            <PetStageMedia petTemplateId={pet.id} stageIndex={1} alt={`${pet.name} 初始形态`} />
          </Box>

          <Stack direction='row' justifyContent='space-between' alignItems='center'>
            <Typography variant='h6'>{pet.name}</Typography>
            <Chip label={pet.rarity} size='small' sx={{ bgcolor: rarity.chip, border: `1px solid ${rarity.border}` }} />
          </Stack>
          <Chip label={pet.pet_type} size='small' variant='outlined' sx={{ width: 'fit-content' }} />
          <Typography variant='body2' color='text.secondary'>
            {pet.lore}
          </Typography>
          <Typography variant='body2'>初始形态：{baseStage?.stage_name}</Typography>
          {selectable && (
            <Button variant='contained' color='secondary' onClick={() => onSelect?.(pet.id)}>
              选择此契约兽
            </Button>
          )}
        </Stack>
      </CardContent>
    </Card>
  );
}
