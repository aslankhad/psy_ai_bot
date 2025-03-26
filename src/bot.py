import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from uvicorn import Config, Server

from modules.common.loader import dp, bot, web

from modules.menu import router as menu_router
from modules.subs import router as subs_router
from modules.reg import router as reg_router
from modules.settings import router as settings_router
from modules.chat import router as chat_router

from modules.tasks import send_daily_hint, update_daily_limit


async def on_startup(bot: Bot):
	commands = [
		BotCommand(command="/start", description="Главное меню"),
	]
	await bot.set_my_commands(commands)


if __name__ == "__main__":
	try:
		logging.basicConfig(
			format=u'%(filename)s [LINE:%(lineno)d] \
				#%(levelname)-8s [%(asctime)s]  %(message)s',
			level=logging.INFO,
		)

		loop = asyncio.new_event_loop()

		# Запуск веба
		config = Config(
			app=web,
			host='0.0.0.0',
			port=5000,
			root_path='',
			proxy_headers=True,
			forwarded_allow_ips='*'
		)
		server = Server(config)
		loop.create_task(server.serve())

		print('Веб начал работу...')
		logging.info('The web is running...')

		dp.startup.register(on_startup)
		dp.include_router(menu_router)
		dp.include_router(subs_router)
		dp.include_router(reg_router)
		dp.include_router(settings_router)
		dp.include_router(chat_router)

		loop.create_task(dp.start_polling(bot))
		logging.info('The bot is running...')

		scheduler = AsyncIOScheduler(event_loop=loop)
		scheduler.add_job(send_daily_hint, "cron", hour=10)
		scheduler.add_job(update_daily_limit, "cron", hour=17, minute=6)
		scheduler.start()
		logging.info('The scheduler is running...')

		loop.run_forever()

	except (KeyboardInterrupt, SystemExit):
		logging.error('Bot stopped!')
	except Exception as exc:
		logging.error(exc)
