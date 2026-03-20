import { http } from './http';
import type { LoginPayload, LoginResponse } from '../types';

export const authApi = {
  login(payload: LoginPayload) {
    return http.post<LoginResponse>('/auth/login', payload).then((res) => res.data);
  },
};
