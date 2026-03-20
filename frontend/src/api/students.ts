import { http } from './http';
import type {
  CreateStudentPayload,
  PetArchive,
  PetBadge,
  SelectPetPayload,
  StudentDetail,
  StudentListItem,
  StudentPetStatus,
  Student,
} from '../types';

export const studentsApi = {
  create(payload: CreateStudentPayload) {
    return http.post<Student>('/students', payload).then((res) => res.data);
  },
  list() {
    return http.get<StudentListItem[]>('/students').then((res) => res.data);
  },
  detail(studentId: number) {
    return http.get<StudentDetail>(`/students/${studentId}`).then((res) => res.data);
  },
  delete(studentId: number) {
    return http.delete(`/students/${studentId}`);
  },
  selectPet(studentId: number, payload: SelectPetPayload) {
    return http.post<StudentPetStatus>(`/students/${studentId}/select-pet`, payload).then((res) => res.data);
  },
  reselectPet(studentId: number, payload: SelectPetPayload) {
    return http.post<StudentPetStatus>(`/students/${studentId}/reselect-pet`, payload).then((res) => res.data);
  },
  currentPet(studentId: number) {
    return http.get<StudentPetStatus>(`/students/${studentId}/pet`).then((res) => res.data);
  },
  petBadges(studentId: number) {
    return http.get<PetBadge[]>(`/students/${studentId}/pet/badges`).then((res) => res.data);
  },
  petArchive(studentId: number) {
    return http.get<PetArchive>(`/students/${studentId}/pet-archive`).then((res) => res.data);
  },
  recalculate(studentId: number) {
    return http.post<StudentPetStatus>(`/students/${studentId}/recalculate`).then((res) => res.data);
  },
};
