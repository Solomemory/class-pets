import { Box, Chip, Grid, Stack, Typography } from '@mui/material';
import type { StudentPetStatus } from '../types';
import { ProgressInfoCard } from './ProgressInfoCard';
import { PetStageTimeline } from './PetStageTimeline';
import { PetAttributePanel } from './PetAttributePanel';
import { PetStageMedia } from './PetStageMedia';
import { rarityPalette } from '../theme/tokens';

interface PetStatusPanelProps {
  petStatus: StudentPetStatus;
}

export function PetStatusPanel({ petStatus }: PetStatusPanelProps) {
  const rarity = rarityPalette[petStatus.rarity] ?? rarityPalette['普通'];
  const nextLevelProgress = ((petStatus.points_per_level - petStatus.points_to_next_level) / petStatus.points_per_level) * 100;

  return (
    <Stack spacing={2}>
      <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} alignItems={{ xs: 'flex-start', sm: 'center' }} flexWrap='wrap'>
        <Typography variant='h4'>{petStatus.pet_name}</Typography>
        <Chip label={petStatus.rarity} sx={{ border: `1px solid ${rarity.border}`, bgcolor: rarity.chip }} />
        <Chip label={petStatus.stage_label} color='secondary' variant='outlined' />
        <Chip label={`阶段星级 ${petStatus.stage_star}★`} color='primary' variant='outlined' />
        <Chip label={`路线 ${petStatus.route_label}`} sx={{ borderColor: petStatus.route_theme, color: petStatus.route_theme }} variant='outlined' />
        <Chip label={`状态 ${petStatus.status_label}`} variant='outlined' />
      </Stack>

      <Typography variant='h6' sx={{ color: petStatus.route_theme }}>
        称号：{petStatus.title}
      </Typography>

      <Grid container spacing={2}>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <ProgressInfoCard title='当前等级' value={`Lv.${petStatus.level}`} helper='每 100 积分升 1 级' />
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <ProgressInfoCard
            title='下一级进度'
            value={`${petStatus.points_per_level - petStatus.points_to_next_level}/${petStatus.points_per_level}`}
            helper={`还需 ${petStatus.points_to_next_level} 积分`}
            progress={nextLevelProgress}
          />
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <ProgressInfoCard
            title='下一阶段'
            value={petStatus.next_stage_level ? `Lv.${petStatus.next_stage_level}` : '已达究极'}
            helper={petStatus.next_stage_level ? `还需 ${petStatus.points_to_next_stage} 积分` : '已解锁全部形态'}
          />
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <ProgressInfoCard title='已解锁徽章' value={`${petStatus.unlocked_badge_count}`} helper='长期成长成就' />
        </Grid>
      </Grid>

      <Grid container spacing={2} alignItems='stretch'>
        <Grid size={{ xs: 12, lg: 7 }}>
          <Stack spacing={1.2}>
            <Box
              sx={{
                width: '100%',
                maxWidth: { xs: '100%', md: 520 },
                aspectRatio: '1 / 1',
                borderRadius: 1,
                border: `1px solid ${rarity.border}`,
                boxShadow: '0 0 28px rgba(240, 199, 104, 0.2)',
                background:
                  'radial-gradient(circle at 50% 35%, rgba(240,199,104,0.16), transparent 62%), linear-gradient(180deg, rgba(10,16,25,0.92), rgba(18,27,39,0.82))',
                p: 2,
                overflow: 'hidden',
                mx: { xs: 0, md: 'auto' },
              }}
            >
              <PetStageMedia
                petTemplateId={petStatus.pet_template_id}
                stageIndex={petStatus.stage_index}
                alt={`${petStatus.pet_name} ${petStatus.current_stage_name}`}
              />
            </Box>

            <Typography variant='h6'>当前形态：{petStatus.current_stage_name}</Typography>
            <Typography color='text.secondary'>{petStatus.current_stage_description}</Typography>
          </Stack>
        </Grid>
        <Grid size={{ xs: 12, lg: 5 }}>
          <PetAttributePanel attributes={petStatus.attributes} />
        </Grid>
      </Grid>

      <PetStageTimeline
        stages={petStatus.stage_preview}
        currentStageIndex={petStatus.stage_index}
        petTemplateId={petStatus.pet_template_id}
      />
    </Stack>
  );
}
