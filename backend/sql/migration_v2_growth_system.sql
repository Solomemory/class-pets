USE class_pets;

ALTER TABLE student_pets
  ADD COLUMN IF NOT EXISTS stage_star INT NOT NULL DEFAULT 1,
  ADD COLUMN IF NOT EXISTS wisdom INT NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS focus INT NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS affinity INT NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS resilience INT NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS vitality INT NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS growth_route VARCHAR(30) NOT NULL DEFAULT 'starlight',
  ADD COLUMN IF NOT EXISTS growth_title VARCHAR(100) NOT NULL DEFAULT '星辉执律者',
  ADD COLUMN IF NOT EXISTS current_status VARCHAR(30) NOT NULL DEFAULT 'stable',
  ADD COLUMN IF NOT EXISTS first_level_up_at DATETIME NULL,
  ADD COLUMN IF NOT EXISTS first_evolution_at DATETIME NULL,
  ADD COLUMN IF NOT EXISTS first_super_evolution_at DATETIME NULL,
  ADD COLUMN IF NOT EXISTS ultimate_evolution_at DATETIME NULL;

ALTER TABLE point_logs
  ADD COLUMN IF NOT EXISTS wisdom_delta INT NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS focus_delta INT NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS affinity_delta INT NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS resilience_delta INT NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS vitality_delta INT NOT NULL DEFAULT 0;

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

INSERT INTO badges(code, name, description, rarity)
VALUES
  ('stage_first_evolution', '初次蜕变', '宠物首次达到进化形态。', '稀有'),
  ('stage_super_evolution', '超进化觉醒', '宠物首次达到超进化形态。', '史诗'),
  ('stage_ultimate_evolution', '究极降临', '宠物成功达成究极进化。', '传说'),
  ('level_10', '十级试炼', '宠物达到 10 级。', '稀有'),
  ('level_20', '二十级征途', '宠物达到 20 级。', '史诗'),
  ('level_30', '三十级王冠', '宠物达到 30 级。', '传说'),
  ('streak_3', '连成长三日', '连续 3 天获得积分。', '稀有'),
  ('streak_7', '连成长七日', '连续 7 天获得积分。', '史诗'),
  ('attr_wisdom_120', '睿识铭印', '智慧属性达到 120。', '史诗'),
  ('attr_focus_120', '凝神铭印', '专注属性达到 120。', '史诗'),
  ('attr_affinity_120', '共鸣铭印', '亲和属性达到 120。', '史诗'),
  ('attr_resilience_120', '坚毅铭印', '毅力属性达到 120。', '史诗'),
  ('attr_vitality_120', '活力铭印', '活力属性达到 120。', '史诗')
ON DUPLICATE KEY UPDATE
  name = VALUES(name),
  description = VALUES(description),
  rarity = VALUES(rarity);
