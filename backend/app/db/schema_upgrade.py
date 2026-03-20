from collections.abc import Mapping

from sqlalchemy import Engine, text


SCHEMA_PATCHES: Mapping[str, Mapping[str, str]] = {
    'student_pets': {
        'stage_star': 'INT NOT NULL DEFAULT 1',
        'wisdom': 'INT NOT NULL DEFAULT 0',
        'focus': 'INT NOT NULL DEFAULT 0',
        'affinity': 'INT NOT NULL DEFAULT 0',
        'resilience': 'INT NOT NULL DEFAULT 0',
        'vitality': 'INT NOT NULL DEFAULT 0',
        "growth_route": "VARCHAR(30) NOT NULL DEFAULT 'starlight'",
        "growth_title": "VARCHAR(100) NOT NULL DEFAULT '星辉执律者'",
        "current_status": "VARCHAR(30) NOT NULL DEFAULT 'stable'",
        'first_level_up_at': 'DATETIME NULL',
        'first_evolution_at': 'DATETIME NULL',
        'first_super_evolution_at': 'DATETIME NULL',
        'ultimate_evolution_at': 'DATETIME NULL',
    },
    'point_logs': {
        'wisdom_delta': 'INT NOT NULL DEFAULT 0',
        'focus_delta': 'INT NOT NULL DEFAULT 0',
        'affinity_delta': 'INT NOT NULL DEFAULT 0',
        'resilience_delta': 'INT NOT NULL DEFAULT 0',
        'vitality_delta': 'INT NOT NULL DEFAULT 0',
    },
}


def _column_exists(conn, table_name: str, column_name: str) -> bool:
    result = conn.execute(
        text(
            '''
            SELECT COUNT(*)
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table_name
              AND COLUMN_NAME = :column_name
            '''
        ),
        {'table_name': table_name, 'column_name': column_name},
    )
    return int(result.scalar_one()) > 0


def apply_schema_upgrade(engine: Engine) -> None:
    # 兼容已有旧库：只在字段缺失时执行 ALTER，避免重复执行报错。
    with engine.begin() as conn:
        for table_name, columns in SCHEMA_PATCHES.items():
            for column_name, column_ddl in columns.items():
                if _column_exists(conn, table_name, column_name):
                    continue
                conn.execute(text(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_ddl}'))
