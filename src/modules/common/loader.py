from fastapi import FastAPI

from sqladmin import Admin

from admin.auth import AdminAuth
from admin.views import UserAdmin, MessageAdmin, \
	DepositVariantAdmin, PaymentAdmin, SettingAdmin, \
	HistoryAdmin, DayHintAdmin

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from db.db_api import engine, async_session

from data.config import BOT_TOKEN, SECRET_KEY, APP_URL, APP_TITLE


# Admin-panel
web = FastAPI()

auth_backend = AdminAuth(secret_key=SECRET_KEY)
admin = Admin(
	app=web,
	engine=engine,
	session_maker=async_session,
	base_url=f'{APP_URL}',
	title=APP_TITLE,
	templates_dir='admin/templates/',
	authentication_backend=auth_backend,
	debug=True
)

admin.add_view(UserAdmin)
admin.add_view(MessageAdmin)
admin.add_view(PaymentAdmin)
admin.add_view(DepositVariantAdmin)
admin.add_view(SettingAdmin)
admin.add_view(HistoryAdmin)
admin.add_view(DayHintAdmin)

# Bot
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='Markdown'))

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
