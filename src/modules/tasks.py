import random
import logging

from db.db_api import get_users, get_hints, \
	update_users_daily_limit

from modules.common.loader import bot


async def send_daily_hint():
	try:
		users = await get_users()
		hints = await get_hints()

		for user in users:
			await bot.send_message(
				chat_id=user.id,
				text=random.choice(hints).hint
			)
	except Exception as exc:
		logging.error(exc)


async def update_daily_limit():
	try:
		await update_users_daily_limit()
	except Exception as exc:
		logging.error(exc)
