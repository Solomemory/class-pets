import { useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams, useSearchParams } from 'react-router-dom';
import { Alert, Grid, Stack, Typography } from '@mui/material';
import { petsApi } from '../api/pets';
import { studentsApi } from '../api/students';
import { PetCard } from '../components/PetCard';
import type { PetTemplate } from '../types';

export function PetSelectPage() {
  const { studentId } = useParams();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [pets, setPets] = useState<PetTemplate[]>([]);
  const [error, setError] = useState('');

  const isReselectMode = useMemo(() => searchParams.get('mode') === 'reselect', [searchParams]);

  useEffect(() => {
    petsApi
      .listTemplates()
      .then(setPets)
      .catch(() => setError('宠物模板加载失败。'));
  }, []);

  const handleSelect = async (petTemplateId: number) => {
    if (!studentId) return;
    setError('');
    try {
      if (isReselectMode) {
        await studentsApi.reselectPet(Number(studentId), { pet_template_id: petTemplateId });
      } else {
        await studentsApi.selectPet(Number(studentId), { pet_template_id: petTemplateId });
      }
      navigate(`/students/${studentId}`);
    } catch {
      setError(isReselectMode ? '重选宠物失败，请稍后重试。' : '绑定宠物失败，该学生可能已绑定主宠物。');
    }
  };

  return (
    <Stack spacing={2.2}>
      <Typography variant='h4'>{isReselectMode ? '重选契约战宠' : '选择你的契约战宠'}</Typography>
      <Typography color='text.secondary'>
        {isReselectMode
          ? '重选将清空该学生当前积分与积分日志，新的宠物将从 Lv.1 开始培养。'
          : '每位学生当前仅可绑定 1 个主宠物。'}
      </Typography>
      {error && <Alert severity='error'>{error}</Alert>}
      <Grid container spacing={2}>
        {pets.map((pet) => (
          <Grid key={pet.id} size={{ xs: 12, sm: 6, lg: 4 }}>
            <PetCard pet={pet} selectable onSelect={handleSelect} />
          </Grid>
        ))}
      </Grid>
    </Stack>
  );
}
