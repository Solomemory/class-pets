import { Card, CardContent, LinearProgress, Stack, Typography } from '@mui/material';
import type { PetAttributes } from '../types';

interface PetAttributePanelProps {
  attributes: PetAttributes;
}

const ATTR_ORDER: Array<{ key: keyof Pick<PetAttributes, 'wisdom' | 'focus' | 'affinity' | 'resilience' | 'vitality'>; label: string }> = [
  { key: 'wisdom', label: '智慧' },
  { key: 'focus', label: '专注' },
  { key: 'affinity', label: '亲和' },
  { key: 'resilience', label: '毅力' },
  { key: 'vitality', label: '活力' },
];

export function PetAttributePanel({ attributes }: PetAttributePanelProps) {
  const values = ATTR_ORDER.map((item) => Number(attributes[item.key]));
  const maxValue = Math.max(120, ...values);

  return (
    <Card>
      <CardContent>
        <Stack spacing={1.2}>
          <Typography variant='h6'>属性面板</Typography>
          <Typography variant='body2' color='text.secondary'>
            主属性：{attributes.dominant_attribute_label}
          </Typography>

          {ATTR_ORDER.map((item) => {
            const value = Number(attributes[item.key]);
            return (
              <Stack key={item.key} spacing={0.4}>
                <Stack direction='row' justifyContent='space-between'>
                  <Typography variant='body2'>{item.label}</Typography>
                  <Typography variant='body2' color='text.secondary'>
                    {value}
                  </Typography>
                </Stack>
                <LinearProgress
                  variant='determinate'
                  value={Math.min(100, (value / maxValue) * 100)}
                  sx={{
                    height: 8,
                    borderRadius: 3,
                    backgroundColor: 'rgba(255,255,255,0.08)',
                    '& .MuiLinearProgress-bar': {
                      background: 'linear-gradient(90deg, #4ed0ff 0%, #f0c768 100%)',
                    },
                  }}
                />
              </Stack>
            );
          })}
        </Stack>
      </CardContent>
    </Card>
  );
}
