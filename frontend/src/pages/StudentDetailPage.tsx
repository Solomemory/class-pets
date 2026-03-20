import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Alert,
  Button,
  Card,
  CardContent,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import { studentsApi } from '../api/students';
import { pointsApi } from '../api/points';
import { PetStatusPanel } from '../components/PetStatusPanel';
import type { StudentDetail } from '../types';

const POINT_REASONS = ['回答问题', '完成作业', '课堂纪律优秀', '小组协作', '课堂挑战完成'];

export function StudentDetailPage() {
  const { studentId } = useParams();
  const navigate = useNavigate();
  const [student, setStudent] = useState<StudentDetail | null>(null);
  const [error, setError] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [pointChange, setPointChange] = useState(20);
  const [reason, setReason] = useState(POINT_REASONS[0]);
  const [remark, setRemark] = useState('');

  const load = async () => {
    if (!studentId) return;
    try {
      const detail = await studentsApi.detail(Number(studentId));
      setStudent(detail);
    } catch {
      setError('加载学生详情失败。');
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [studentId]);

  const submitPoint = async () => {
    if (!studentId) return;
    try {
      await pointsApi.add(Number(studentId), { point_change: pointChange, reason, remark: remark || undefined });
      setDialogOpen(false);
      setRemark('');
      await load();
    } catch {
      setError('积分添加失败。');
    }
  };

  const handleDeleteStudent = async () => {
    if (!studentId) return;
    const confirmed = window.confirm('确认删除该学生？该学生及其宠物与积分记录将被永久删除。');
    if (!confirmed) return;

    try {
      await studentsApi.delete(Number(studentId));
      navigate('/students');
    } catch {
      setError('删除学生失败，请稍后重试。');
    }
  };

  const handleReselectPet = () => {
    if (!studentId) return;
    navigate(`/students/${studentId}/select-pet?mode=reselect`);
  };

  if (!student) {
    return <Typography color='text.secondary'>加载中...</Typography>;
  }

  return (
    <Stack spacing={2.2}>
      {error && <Alert severity='error'>{error}</Alert>}
      <Card>
        <CardContent>
          <Grid container spacing={2} alignItems='center'>
            <Grid size={{ xs: 12, md: 6 }}>
              <Typography variant='h4'>{student.name}</Typography>
              <Typography color='text.secondary'>班级：{student.grade_class || '未填写'}</Typography>
              <Typography sx={{ mt: 1 }}>总积分：{student.total_points}</Typography>
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} justifyContent='flex-end'>
                <Button variant='contained' color='secondary' onClick={() => setDialogOpen(true)}>
                  添加积分
                </Button>
                {student.pet_status ? (
                  <>
                    <Button variant='outlined' startIcon={<AutoAwesomeIcon />} onClick={() => navigate(`/students/${student.id}/pet`)}>
                      进入宠物主页
                    </Button>
                    <Button variant='outlined' color='warning' startIcon={<AutorenewIcon />} onClick={handleReselectPet}>
                      重选宠物
                    </Button>
                  </>
                ) : (
                  <Button variant='outlined' onClick={() => navigate(`/students/${student.id}/select-pet`)}>
                    选择宠物
                  </Button>
                )}
                <Button variant='outlined' color='error' startIcon={<DeleteOutlineIcon />} onClick={handleDeleteStudent}>
                  删除学生
                </Button>
              </Stack>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {student.pet_status ? (
        <>
          <Alert severity='warning'>重选宠物将清空该学生当前积分与积分日志，并从 Lv.1 重新培养。</Alert>
          <PetStatusPanel petStatus={student.pet_status} />
        </>
      ) : (
        <Alert severity='warning'>该学生尚未绑定主宠物，请先完成宠物选择。</Alert>
      )}

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} fullWidth maxWidth='sm'>
        <DialogTitle>添加课堂积分</DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ mt: 1 }}>
            <TextField
              label='积分值'
              type='number'
              value={pointChange}
              onChange={(e) => setPointChange(Number(e.target.value))}
            />
            <TextField select label='积分原因' value={reason} onChange={(e) => setReason(e.target.value)}>
              {POINT_REASONS.map((item) => (
                <MenuItem key={item} value={item}>
                  {item}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              label='备注（可选）'
              multiline
              minRows={2}
              value={remark}
              onChange={(e) => setRemark(e.target.value)}
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>取消</Button>
          <Button variant='contained' color='secondary' onClick={submitPoint}>
            确认增加
          </Button>
        </DialogActions>
      </Dialog>
    </Stack>
  );
}
