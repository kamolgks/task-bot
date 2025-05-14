import sqlite3
import aiosqlite
import logging
from datetime import datetime
from config import DB_NAME


class Database:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.logger = logging.getLogger(__name__)

    async def create_database(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    timezone TEXT DEFAULT '+0'
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    notified INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
                """
            )
            await db.commit()
            self.logger.info("Таблицы tasks и users созданы или уже существуют")

    async def create_tables(self):
        await self.create_database()

    async def add_task(self, user_id, name, description, date, time):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "INSERT INTO tasks (user_id, name, description, date, time) VALUES (?, ?, ?, ?, ?)",
                (user_id, name, description, date, time),
            )
            await db.commit()
            self.logger.info(
                f"Добавлена новая задача для пользователя {user_id}: {name}"
            )
            return True

    async def get_tasks(self, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = sqlite3.Row
            cursor = await db.execute(
                "SELECT * FROM tasks WHERE user_id = ? ORDER BY date, time", (user_id,)
            )
            tasks = await cursor.fetchall()
            return [dict(task) for task in tasks]
            
    async def get_today_tasks(self, user_id):
        today = datetime.now().strftime("%d.%m.%Y")
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = sqlite3.Row
            cursor = await db.execute(
                "SELECT * FROM tasks WHERE user_id = ? AND date = ? ORDER BY time",
                (user_id, today),
            )
            tasks = await cursor.fetchall()
            return [dict(task) for task in tasks]
        
    async def get_future_tasks(self, user_id):
        today = datetime.now().strftime("%d.%m.%Y")
        current_time = datetime.now().strftime("%H:%M")
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = sqlite3.Row
            cursor = await db.execute(
                """
                SELECT * FROM tasks 
                WHERE user_id = ? 
                AND (
                    strftime('%Y%m%d', substr(date, 7, 4) || '-' || substr(date, 4, 2) || '-' || substr(date, 1, 2)) > 
                    strftime('%Y%m%d', substr(?, 7, 4) || '-' || substr(?, 4, 2) || '-' || substr(?, 1, 2))
                    OR 
                    (date = ? AND time > ?)
                )
                ORDER BY date, time
                """,
                (user_id, today, today, today, today, current_time),
            )
            tasks = await cursor.fetchall()
            return [dict(task) for task in tasks]

    async def delete_task(self, task_id, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id)
            )
            await db.commit()
            self.logger.info(f"Задача {task_id} пользователя {user_id} была удалена")
            return True

    async def get_task(self, task_id, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = sqlite3.Row
            cursor = await db.execute(
                "SELECT * FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id)
            )
            task = await cursor.fetchone()
            return dict(task) if task else None

    async def get_tasks_by_datetime(self, date, time):
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = sqlite3.Row
            cursor = await db.execute(
                "SELECT * FROM tasks WHERE date = ? AND time = ?", (date, time)
            )
            tasks = await cursor.fetchall()
            return [dict(task) for task in tasks]

    async def get_user_timezone(self, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute(
                "SELECT timezone FROM users WHERE user_id = ?", (user_id,)
            )
            result = await cursor.fetchone()
            return result[0] if result else '+0'

    async def set_user_timezone(self, user_id, timezone):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                """
                INSERT INTO users (user_id, timezone) 
                VALUES (?, ?) 
                ON CONFLICT(user_id) 
                DO UPDATE SET timezone = ?
                """,
                (user_id, timezone, timezone)
            )
            await db.commit()
            self.logger.info(f"Обновлен часовой пояс для пользователя {user_id}: {timezone}")
            return True

    async def mark_task_as_notified(self, task_id):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "UPDATE tasks SET notified = 1 WHERE id = ?",
                (task_id,)
            )
            await db.commit()
            return True


