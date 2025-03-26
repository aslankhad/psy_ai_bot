import logging
from datetime import datetime, timezone

from aiogram import Router, types, F

from db.db_api import get_user, get_text, get_setting, \
	update_user_messages, get_user_chat_history, update_history
from db.models import RoleEnum

from modules.common.loader import bot
from modules.common.keyboard import get_limit_menu
from modules.common.gpt import gpt_request
from modules.common.utils import gender_to_str, therapy_to_str


router = Router(name=__name__)


@router.callback_query(F.data == 'cb_chat')
async def chat(callback: types.CallbackQuery):
	try:
		await callback.message.answer(
			await get_text('CHAT_TEXT')
		)
	except Exception as exc:
		logging.error(exc)

		return await callback.answer(
			await get_text('ERROR_TEXT')
		)


@router.message()
async def other(message: types.Message):
	try:
		user = await get_user(message.from_user.id)

		if not user:
			return

		if not user.subscribe_expired:
			if user.available_messages <= 0:
				return await message.answer(
					await get_text('MESSAGES_LIMIT_TEXT'),
					reply_markup=await get_limit_menu()
				)

			await update_user_messages(message.from_user.id, 1)
		else:
			current_date = datetime.now(timezone.utc).replace(tzinfo=None)

			if user.subscribe_expired < current_date:
				return await message.answer(
					await get_text('SUB_EXPIRED_TEXT'),
					reply_markup=await get_limit_menu()
				)

		await bot.send_chat_action(message.from_user.id, action="typing")

		prompt = (await get_setting('prompt')).format(
			name=user.name,
			therapy=therapy_to_str(user.therapy),
			gender=gender_to_str(user.gender),
			text=message.text
		)

		history = await get_user_chat_history(message.from_user.id, True)
		response = await gpt_request(prompt, history)

		await message.answer(response)

		await update_history(message.from_user.id, [
			{'role': RoleEnum.USER, 'content': message.text},
			{'role': RoleEnum.ASSISTANT, 'content': response}
		])
	except Exception as exc:
		logging.error(exc)
