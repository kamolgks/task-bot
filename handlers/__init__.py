from aiogram import Dispatcher
from database.database import Database

from handlers.common import router as common_router
from handlers.view_task import router as view_task_router
from handlers.create_task import router as create_task_router
from handlers.delete_task import router as delete_task_router
from handlers.settings import router as settings_router

def register_routers(dp: Dispatcher, db: Database):
    dp.message.middleware.register(DatabaseMiddleware(db))
    dp.callback_query.middleware.register(DatabaseMiddleware(db))
    
    dp.include_router(common_router)
    dp.include_router(view_task_router)
    dp.include_router(create_task_router)
    dp.include_router(delete_task_router)
    dp.include_router(settings_router)
    
class DatabaseMiddleware:
    
    def __init__(self, db: Database):
        self.db = db
        
    async def __call__(self, handlers, event, data):
        data["db"] = self.db
        return await handlers(event, data)