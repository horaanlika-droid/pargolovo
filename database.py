import aiosqlite
import time

DB_PATH = "koroleva.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # Таблица игроков
        await db.execute('''
            CREATE TABLE IF NOT EXISTS players (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                nickname TEXT,
                current_scene TEXT,
                save_scene TEXT,
                points INTEGER DEFAULT 0,
                dressage_level INTEGER DEFAULT 0,
                sissy_level INTEGER DEFAULT 0,
                adult_level INTEGER DEFAULT 0,
                rolls_left INTEGER DEFAULT 0,
                used_rolls INTEGER DEFAULT 0,
                invites INTEGER DEFAULT 0,
                achievements TEXT DEFAULT '',
                ending TEXT,
                created_at INTEGER
            )
        ''')
        
        # Таблица для хранения прогресса мини-игр
        await db.execute('''
            CREATE TABLE IF NOT EXISTS minigame_progress (
                user_id INTEGER,
                scene_id TEXT,
                progress INTEGER DEFAULT 0,
                start_time REAL,
                data TEXT,
                PRIMARY KEY (user_id, scene_id)
            )
        ''')
        
        await db.commit()

# ========== ИГРОКИ ==========
async def create_player(user_id: int, username: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO players (user_id, username, current_scene, created_at) VALUES (?, ?, ?, ?)",
            (user_id, username, "prolog", int(time.time()))
        )
        await db.commit()

async def get_player(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM players WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchone()

async def get_username(user_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT username FROM players WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else str(user_id)

async def get_all_players():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id, username, points, rolls_left, used_rolls FROM players") as cursor:
            return await cursor.fetchall()

async def get_stats():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM players") as cursor:
            total = (await cursor.fetchone())[0]
        return {"total_players": total}

# ========== ПРОГРЕСС ==========
async def get_current_scene(user_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT current_scene FROM players WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else "prolog"

async def update_current_scene(user_id: int, scene_id: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE players SET current_scene = ? WHERE user_id = ?", (scene_id, user_id))
        await db.commit()

async def reset_player(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE players SET current_scene = 'prolog', save_scene = NULL, points = 0 WHERE user_id = ?",
            (user_id,)
        )
        await db.commit()

# ========== СОХРАНЕНИЯ ==========
async def get_save_point(user_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT save_scene FROM players WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def update_save_point(user_id: int, scene_id: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE players SET save_scene = ? WHERE user_id = ?", (scene_id, user_id))
        await db.commit()

async def has_save(user_id: int) -> bool:
    return await get_save_point(user_id) is not None

async def clear_save(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE players SET save_scene = NULL WHERE user_id = ?", (user_id,))
        await db.commit()

# ========== БАЛЛЫ И ДОСТИЖЕНИЯ ==========
async def get_points(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT points FROM players WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def add_points(user_id: int, points: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE players SET points = points + ? WHERE user_id = ?", (points, user_id))
        await db.commit()

async def get_nickname(user_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT nickname FROM players WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def add_achievement(user_id: int, achievement: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE players SET achievements = CASE WHEN achievements = '' THEN ? ELSE achievements || ',' || ? END WHERE user_id = ?",
            (achievement, achievement, user_id)
        )
        await db.commit()

async def get_achievements(user_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT achievements FROM players WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else ""

async def set_ending(user_id: int, ending: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE players SET ending = ? WHERE user_id = ?", (ending, user_id))
        await db.commit()

async def get_ending(user_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT ending FROM players WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

# ========== МИНИ-ИГРЫ ==========
async def get_minigame_progress(user_id: int, scene_id: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT progress FROM minigame_progress WHERE user_id = ? AND scene_id = ?",
            (user_id, scene_id)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def set_minigame_progress(user_id: int, scene_id: str, progress: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO minigame_progress (user_id, scene_id, progress) VALUES (?, ?, ?)",
            (user_id, scene_id, progress)
        )
        await db.commit()

async def clear_minigame_progress(user_id: int, scene_id: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM minigame_progress WHERE user_id = ? AND scene_id = ?", (user_id, scene_id))
        await db.commit()

async def get_minigame_start(user_id: int, scene_id: str) -> float:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT start_time FROM minigame_progress WHERE user_id = ? AND scene_id = ?",
            (user_id, scene_id)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def set_minigame_start(user_id: int, scene_id: str, start_time: float):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO minigame_progress (user_id, scene_id, start_time) VALUES (?, ?, ?)",
            (user_id, scene_id, start_time)
        )
        await db.commit()

async def set_minigame_data(user_id: int, scene_id: str, data: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO minigame_progress (user_id, scene_id, data) VALUES (?, ?, ?)",
            (user_id, scene_id, data)
        )
        await db.commit()

async def get_minigame_data(user_id: int, scene_id: str) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT data FROM minigame_progress WHERE user_id = ? AND scene_id = ?",
            (user_id, scene_id)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else ""
