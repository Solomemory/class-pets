CREATE DATABASE IF NOT EXISTS class_pets CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE class_pets;

CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  grade_class VARCHAR(50) NULL,
  total_points INT NOT NULL DEFAULT 0,
  available_points INT NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_students_name (name)
);

CREATE TABLE IF NOT EXISTS pet_templates (
  id INT PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  pet_type VARCHAR(50) NOT NULL,
  lore TEXT NOT NULL,
  rarity VARCHAR(20) NOT NULL,
  image_url VARCHAR(255) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pet_stage_configs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  pet_template_id INT NOT NULL,
  stage_index INT NOT NULL,
  stage_key VARCHAR(30) NOT NULL,
  stage_name VARCHAR(100) NOT NULL,
  stage_description TEXT NOT NULL,
  image_prompt TEXT NOT NULL,
  level_min INT NOT NULL,
  level_max INT NULL,
  CONSTRAINT fk_pet_stage_template FOREIGN KEY (pet_template_id) REFERENCES pet_templates(id) ON DELETE CASCADE,
  CONSTRAINT uq_pet_stage UNIQUE (pet_template_id, stage_index)
);

CREATE TABLE IF NOT EXISTS student_pets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  pet_template_id INT NOT NULL,
  level INT NOT NULL DEFAULT 1,
  stage_index INT NOT NULL DEFAULT 1,
  stage_star INT NOT NULL DEFAULT 1,

  wisdom INT NOT NULL DEFAULT 0,
  focus INT NOT NULL DEFAULT 0,
  affinity INT NOT NULL DEFAULT 0,
  resilience INT NOT NULL DEFAULT 0,
  vitality INT NOT NULL DEFAULT 0,

  growth_route VARCHAR(30) NOT NULL DEFAULT 'starlight',
  growth_title VARCHAR(100) NOT NULL DEFAULT '星辉执律者',
  current_status VARCHAR(30) NOT NULL DEFAULT 'stable',

  current_stage_name VARCHAR(100) NOT NULL,
  current_stage_description TEXT NOT NULL,
  current_image_prompt TEXT NOT NULL,
  points_to_next_level INT NOT NULL DEFAULT 100,
  points_to_next_stage INT NOT NULL DEFAULT 900,
  next_stage_level INT NULL,

  first_level_up_at DATETIME NULL,
  first_evolution_at DATETIME NULL,
  first_super_evolution_at DATETIME NULL,
  ultimate_evolution_at DATETIME NULL,

  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_student_pet_student FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
  CONSTRAINT fk_student_pet_template FOREIGN KEY (pet_template_id) REFERENCES pet_templates(id) ON DELETE RESTRICT,
  CONSTRAINT uq_student_main_pet UNIQUE (student_id)
);

CREATE TABLE IF NOT EXISTS point_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  point_change INT NOT NULL,
  reason VARCHAR(50) NOT NULL,
  remark TEXT NULL,

  wisdom_delta INT NOT NULL DEFAULT 0,
  focus_delta INT NOT NULL DEFAULT 0,
  affinity_delta INT NOT NULL DEFAULT 0,
  resilience_delta INT NOT NULL DEFAULT 0,
  vitality_delta INT NOT NULL DEFAULT 0,

  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_point_log_student FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
  INDEX idx_point_logs_student_id (student_id),
  INDEX idx_point_logs_created_at (created_at)
);

CREATE TABLE IF NOT EXISTS badges (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) NOT NULL UNIQUE,
  name VARCHAR(50) NOT NULL,
  description TEXT NOT NULL,
  rarity VARCHAR(20) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS student_pet_badges (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_pet_id INT NOT NULL,
  badge_id INT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_student_pet_badges_pet FOREIGN KEY (student_pet_id) REFERENCES student_pets(id) ON DELETE CASCADE,
  CONSTRAINT fk_student_pet_badges_badge FOREIGN KEY (badge_id) REFERENCES badges(id) ON DELETE CASCADE,
  CONSTRAINT uq_student_pet_badge UNIQUE (student_pet_id, badge_id)
);
