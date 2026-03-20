import { http } from './http';
import type { GrowthRule } from '../types';

export const rulesApi = {
  get() {
    return http.get<GrowthRule>('/growth-rules').then((res) => res.data);
  },
};
