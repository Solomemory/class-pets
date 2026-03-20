import { http } from './http';
import type { PetTemplate } from '../types';

export const petsApi = {
  listTemplates() {
    return http.get<PetTemplate[]>('/pet-templates').then((res) => res.data);
  },
};
