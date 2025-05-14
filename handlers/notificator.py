import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot
from database.database import Database
from config import MESSAGES

logger = logging.getLogger(__name__)

async def notificator(bot: Bot, db: Database):
    while True:
        try:
            now = datetime.now()
            current_date = now.strftime("%d.%m.%Y")
            current_time = now.strftime("%H:%M")

            tasks = await db.get_tasks_by_datetime(current_date, current_time)

            for task in tasks:
                user_id = task["user_id"]
                name = task["name"]
                description = task["description"]
                user_timezone = await db.get_user_timezone(user_id)
                
                tz_offset = int(user_timezone)
                user_time = (now + timedelta(hours=tz_offset)).strftime("%H:%M")
                
                await bot.send_message(
                    user_id,
                    text=MESSAGES["task_notification"].format(
                        name=name,
                        time=user_time,
                        id=task['id'],
                        description=description if description else '(без описания)'
                    ),
                    parse_mode="HTML",
                )

                await db.mark_task_as_notified(task["id"])

            await asyncio.sleep(60)

        except Exception as e:
            logger.error(f"Ошибка в работе уведомлений: {e}")
            await asyncio.sleep(60)
