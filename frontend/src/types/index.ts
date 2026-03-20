export interface LoginPayload {
  username: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  username: string;
}

export interface PetStageConfig {
  id: number;
  stage_index: number;
  stage_key: string;
  stage_name: string;
  stage_description: string;
  image_prompt: string;
  level_min: number;
  level_max: number | null;
}

export interface PetTemplate {
  id: number;
  name: string;
  pet_type: string;
  lore: string;
  rarity: string;
  image_url: string | null;
  created_at: string;
  stage_configs: PetStageConfig[];
}

export interface PetAttributes {
  wisdom: number;
  focus: number;
  affinity: number;
  resilience: number;
  vitality: number;
  dominant_attribute_key: string;
  dominant_attribute_label: string;
}

export interface PetBadge {
  id: number;
  code: string;
  name: string;
  description: string;
  rarity: string;
  unlocked_at: string;
}

export interface PetTimelineEvent {
  event_code: string;
  event_name: string;
  event_time: string;
  detail: string;
}

export interface StudentPetStatus {
  student_pet_id: number;
  pet_template_id: number;
  pet_name: string;
  pet_type: string;
  rarity: string;
  total_points: number;
  level: number;
  stage_index: number;
  stage_label: string;
  stage_star: number;
  stage_star_label: string;
  route_key: string;
  route_label: string;
  route_theme: string;
  title: string;
  status_key: string;
  status_label: string;
  current_stage_name: string;
  current_stage_description: string;
  current_image_prompt: string;
  points_per_level: number;
  points_to_next_level: number;
  points_to_next_stage: number;
  next_stage_level: number | null;
  evolution_switched: boolean;
  attributes: PetAttributes;
  unlocked_badge_count: number;
  stage_preview: PetStageConfig[];
}

export interface PetArchive {
  student_id: number;
  student_name: string;
  grade_class: string | null;
  pet_status: StudentPetStatus;
  badges: PetBadge[];
  timeline: PetTimelineEvent[];
}

export interface Student {
  id: number;
  name: string;
  grade_class: string | null;
  total_points: number;
  available_points: number;
  created_at: string;
}

export interface StudentListItem extends Student {
  pet_status: StudentPetStatus | null;
}

export interface StudentDetail extends Student {
  pet_status: StudentPetStatus | null;
}

export interface CreateStudentPayload {
  name: string;
  grade_class?: string;
}

export interface SelectPetPayload {
  pet_template_id: number;
}

export interface PointLog {
  id: number;
  student_id: number;
  point_change: number;
  reason: string;
  remark: string | null;
  wisdom_delta: number;
  focus_delta: number;
  affinity_delta: number;
  resilience_delta: number;
  vitality_delta: number;
  created_at: string;
}

export interface AddPointPayload {
  point_change: number;
  reason: string;
  remark?: string;
}

export interface AddPointResponse {
  log: PointLog;
  pet_status: StudentPetStatus | null;
}

export interface GrowthRule {
  points_per_level: number;
  stages: Array<{
    stage_index: number;
    stage_label: string;
    level_min: number;
    level_max: number | null;
  }>;
}
