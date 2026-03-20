import { http } from './http';
import type { AddPointPayload, AddPointResponse, PointLog } from '../types';

export const pointsApi = {
  add(studentId: number, payload: AddPointPayload) {
    return http.post<AddPointResponse>(`/students/${studentId}/points`, payload).then((res) => res.data);
  },
  list(studentId?: number) {
    return http
      .get<PointLog[]>('/point-logs', {
        params: studentId ? { student_id: studentId } : undefined,
      })
      .then((res) => res.data);
  },
};
