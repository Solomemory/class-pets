import { useEffect, useMemo, useState } from 'react';
import { Alert, Card, CardContent, MenuItem, Stack, TextField, Typography } from '@mui/material';
import { pointsApi } from '../api/points';
import { studentsApi } from '../api/students';
import { PointLogList } from '../components/PointLogList';
import type { PointLog, StudentListItem } from '../types';

export function PointLogsPage() {
  const [logs, setLogs] = useState<PointLog[]>([]);
  const [students, setStudents] = useState<StudentListItem[]>([]);
  const [studentId, setStudentId] = useState<number | ''>('');
  const [error, setError] = useState('');

  const loadStudents = async () => {
    try {
      setStudents(await studentsApi.list());
    } catch {
      setError('学生列表加载失败。');
    }
  };

  const loadLogs = async (id?: number) => {
    try {
      setLogs(await pointsApi.list(id));
    } catch {
      setError('积分日志加载失败。');
    }
  };

  useEffect(() => {
    loadStudents();
    loadLogs();
  }, []);

  useEffect(() => {
    if (studentId === '') {
      loadLogs();
      return;
    }
    loadLogs(studentId);
  }, [studentId]);

  const selectedStudent = useMemo(
    () => students.find((student) => student.id === studentId),
    [students, studentId],
  );

  return (
    <Stack spacing={2.2}>
      <Typography variant='h4'>积分记录</Typography>
      <Typography color='text.secondary'>按学生筛选课堂表现积分流水</Typography>
      {error && <Alert severity='error'>{error}</Alert>}

      <Card>
        <CardContent>
          <Stack spacing={2}>
            <TextField
              select
              label='筛选学生'
              value={studentId}
              onChange={(e) => setStudentId(e.target.value ? Number(e.target.value) : '')}
            >
              <MenuItem value=''>全部学生</MenuItem>
              {students.map((student) => (
                <MenuItem key={student.id} value={student.id}>
                  {student.name}
                </MenuItem>
              ))}
            </TextField>
            {selectedStudent && (
              <Typography color='text.secondary'>
                当前筛选：{selectedStudent.name}（总积分 {selectedStudent.total_points}）
              </Typography>
            )}
          </Stack>
        </CardContent>
      </Card>

      <PointLogList logs={logs} />
    </Stack>
  );
}
