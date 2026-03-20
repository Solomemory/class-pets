# 1. 项目整体架构说明

- 架构：前后端分离。
- 前端（React）负责页面渲染、交互和展示游戏化养成反馈。
- 后端（FastAPI）提供 RESTful API、成长规则计算、积分日志记录。
- MySQL 存储学生、宠物模板、阶段配置、学生宠物状态、积分流水。
- 核心闭环：创建学生 -> 选择主宠物 -> 增加积分 -> 自动升级与阶段切换 -> 页面实时展示。

# 2. 技术选型说明（UI 组件库）

- 前端框架：React + TypeScript + React Router + Axios
- 后端框架：FastAPI + SQLAlchemy + Pydantic
- 数据库：MySQL 8
- UI 组件库：MUI（Material UI）
- 选择 MUI 的理由：
  1. Web 与移动端响应式成熟：内置断点系统、栅格布局、弹窗/抽屉等组件在不同屏宽表现稳定。
  2. 常用组件完整：卡片、列表、弹窗、表单、标签、进度条、导航组件可直接覆盖 MVP 需求。
  3. 易于二次封装：主题系统（`createTheme`）和样式覆写机制适合做“游戏化皮肤”与稀有度边框等扩展。
  4. 与 React 生态兼容好，工程可维护性高。

# 3. 数据库表设计

- `students`
  - 主键：`id`
  - 字段：`name`, `grade_class`, `total_points`, `available_points`, `created_at`
- `pet_templates`
  - 主键：`id`
  - 唯一约束：`name`
  - 字段：`name`, `pet_type`, `lore`, `rarity`, `image_url`, `created_at`
- `pet_stage_configs`
  - 主键：`id`
  - 外键：`pet_template_id -> pet_templates.id`
  - 唯一约束：`(pet_template_id, stage_index)`
  - 字段：`stage_key`, `stage_name`, `stage_description`, `image_prompt`, `level_min`, `level_max`
- `student_pets`
  - 主键：`id`
  - 外键：`student_id -> students.id`，`pet_template_id -> pet_templates.id`
  - 唯一约束：`student_id`（一个学生一个主宠）
  - 字段：`level`, `stage_index`, `current_stage_name`, `current_stage_description`, `current_image_prompt`, `points_to_next_level`, `points_to_next_stage`, `next_stage_level`, `created_at`, `updated_at`
- `point_logs`
  - 主键：`id`
  - 外键：`student_id -> students.id`
  - 字段：`point_change`, `reason`, `remark`, `created_at`

关系说明：

- 学生与主宠：`students 1 - 1 student_pets`
- 宠物模板与阶段：`pet_templates 1 - N pet_stage_configs`
- 学生主宠关联模板：`student_pets N - 1 pet_templates`
- 学生与积分日志：`students 1 - N point_logs`

# 4. 核心业务规则说明

- 每累计 `100` 积分升 `1` 级，公式：`level = total_points // 100 + 1`
- 阶段规则：
  - `1~9` 级：初始形态
  - `10~19` 级：进化形态
  - `20~29` 级：超进化形态
  - `30+` 级：究极进化形态
- 当积分变化时自动执行：
  1. 计算新等级
  2. 计算当前阶段
  3. 更新 `student_pets` 当前形态字段
  4. 计算距离下一级/下一阶段所需积分
  5. 标记是否发生形态切换 `evolution_switched`

# 5. 后端目录结构

```text
backend/
  app/
    api/
      v1/
        routes/
          auth.py
          students.py
          pets.py
          points.py
          rules.py
        router.py
    core/config.py
    db/session.py
    models/
      student.py
      pet.py
      point_log.py
    schemas/
      auth.py
      student.py
      pet.py
      point.py
    services/
      growth_service.py
      student_service.py
      pet_service.py
      point_service.py
    seeds/
      pet_templates.py
      seed_data.py
    main.py
  sql/init_schema.sql
  seed.py
  requirements.txt
```

# 6. 前端目录结构

```text
frontend/
  src/
    api/
      http.ts
      auth.ts
      students.ts
      pets.ts
      points.ts
      rules.ts
    components/
      StudentCard.tsx
      PetCard.tsx
      PetStageTimeline.tsx
      PetStatusPanel.tsx
      PointLogList.tsx
      ProgressInfoCard.tsx
    layout/AppLayout.tsx
    pages/
      LoginPage.tsx
      StudentsPage.tsx
      CreateStudentPage.tsx
      PetSelectPage.tsx
      StudentDetailPage.tsx
      PetHomePage.tsx
      PointLogsPage.tsx
    router/
      index.tsx
      RequireAuth.tsx
    theme/
      tokens.ts
      theme.ts
    types/index.ts
    styles/global.css
    App.tsx
    main.tsx
  package.json
```

# 7. 后端主要代码

- 应用入口：[main.py](backend/app/main.py)
- 配置与数据库连接：[config.py](backend/app/core/config.py), [session.py](backend/app/db/session.py)
- 业务模型：[student.py](backend/app/models/student.py), [pet.py](backend/app/models/pet.py), [point_log.py](backend/app/models/point_log.py)
- 核心成长规则服务：[growth_service.py](backend/app/services/growth_service.py)
- 学生/选宠业务：[student_service.py](backend/app/services/student_service.py)
- 积分业务：[point_service.py](backend/app/services/point_service.py)
- API 路由：[students.py](backend/app/api/v1/routes/students.py), [pets.py](backend/app/api/v1/routes/pets.py), [points.py](backend/app/api/v1/routes/points.py)

# 8. 前端主要代码

- 应用与路由：[App.tsx](frontend/src/App.tsx), [router/index.tsx](frontend/src/router/index.tsx)
- 全局主题变量：[tokens.ts](frontend/src/theme/tokens.ts), [theme.ts](frontend/src/theme/theme.ts), [global.css](frontend/src/styles/global.css)
- 复用组件：
  - [StudentCard.tsx](frontend/src/components/StudentCard.tsx)
  - [PetCard.tsx](frontend/src/components/PetCard.tsx)
  - [PetStageTimeline.tsx](frontend/src/components/PetStageTimeline.tsx)
  - [PetStatusPanel.tsx](frontend/src/components/PetStatusPanel.tsx)
  - [PointLogList.tsx](frontend/src/components/PointLogList.tsx)
  - [ProgressInfoCard.tsx](frontend/src/components/ProgressInfoCard.tsx)
- 页面实现：`Login / Students / CreateStudent / PetSelect / StudentDetail / PetHome / PointLogs`

# 9. 初始化 SQL 或种子数据

- 建表 SQL：`backend/sql/init_schema.sql`
- 宠物种子脚本：`backend/seed.py`
- 10 条完整宠物模板数据：`backend/app/seeds/pet_templates.py`

# 10. 10 个宠物模板完整数据

已完整内置（含：名称、类型、简介、稀有度、四阶段名称、四阶段描述、四阶段图片提示词、等级区间）：

- 霆曜狮鹫
- 玄潮鲸灵
- 灰烬翼龙
- 星穹狐
- 岩誓巨犀
- 影缚夜鸦
- 苍岚鹿
- 霜烬白虎
- 曜金机甲狼
- 天谕圣蛇

完整字段请查看：`backend/app/seeds/pet_templates.py`

# 11. 示例 API 请求与返回

1. 创建学生

```http
POST /api/v1/students
Content-Type: application/json

{
  "name": "林岚",
  "grade_class": "高一(2)班"
}
```

```json
{
  "id": 1,
  "name": "林岚",
  "grade_class": "高一(2)班",
  "total_points": 0,
  "available_points": 0,
  "created_at": "2026-03-19T09:30:00"
}
```

2. 选择宠物

```http
POST /api/v1/students/1/select-pet
Content-Type: application/json

{
  "pet_template_id": 8
}
```

```json
{
  "student_pet_id": 1,
  "pet_template_id": 8,
  "pet_name": "霜烬白虎",
  "pet_type": "冰炎双生",
  "rarity": "传说",
  "total_points": 0,
  "level": 1,
  "stage_index": 1,
  "stage_label": "初始形态",
  "current_stage_name": "霜纹幼虎",
  "current_stage_description": "...",
  "current_image_prompt": "...",
  "points_per_level": 100,
  "points_to_next_level": 100,
  "points_to_next_stage": 900,
  "next_stage_level": 10,
  "evolution_switched": false,
  "stage_preview": []
}
```

3. 增加积分

```http
POST /api/v1/students/1/points
Content-Type: application/json

{
  "point_change": 250,
  "reason": "课堂挑战完成",
  "remark": "解题速度优秀"
}
```

```json
{
  "log": {
    "id": 1,
    "student_id": 1,
    "point_change": 250,
    "reason": "课堂挑战完成",
    "remark": "解题速度优秀",
    "created_at": "2026-03-19T10:10:00"
  },
  "pet_status": {
    "level": 3,
    "stage_index": 1,
    "points_to_next_level": 50,
    "points_to_next_stage": 650
  }
}
```

4. 获取宠物模板

```http
GET /api/v1/pet-templates
```

5. 获取积分日志

```http
GET /api/v1/point-logs?student_id=1
```

# 12. 启动步骤

1. 配置后端环境变量

```bash
cd backend
cp .env.example .env
```

2. 安装并启动后端

```bash
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload --port 8000
```

3. 安装并启动前端

```bash
cd ../frontend
cp .env.example .env
npm install
npm run dev
```

5. 访问

- 前端：`http://localhost:5173`
- 后端接口文档：`http://localhost:8000/docs`

# 13. 后续扩展建议

- 多宠物系统：`students 1 - N student_pets`，增加主宠切换。
- 宠物技能树：技能表 + 学习条件 + 冷却机制。
- 装备系统：装备位与属性加成。
- 宠物属性战斗值：攻击/防御/速度/元素抗性。
- 排行榜：按积分、等级、阶段、连续成长天数排序。
- 徽章系统：行为成就触发与称号展示。
- 事件系统：周挑战、赛季任务、阶段奖励。
