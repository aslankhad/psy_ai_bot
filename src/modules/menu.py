import logging
from asyncio import sleep

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from db.db_api import get_user, get_text

from modules.common.loader import bot
from modules.common.filters import ChatTypeFilter
from modules.common.keyboard import get_start_menu, \
	get_start_reg_menu, get_psy_menu
from modules.common.utils import gender_to_str, therapy_to_str


router = Router(name=__name__)


@router.message(Command('start'), ChatTypeFilter('private'))
async def start(message: types.Message, state: FSMContext):
	try:
		await state.clear()

		user = await get_user(message.from_user.id)

		if not user:
			await bot.send_chat_action(message.from_user.id, action="typing")
			await sleep(2)

			return await message.answer(
				await get_text('REG_START_TEXT'),
				reply_markup=await get_start_reg_menu()
			)

		await message.answer(
			(await get_text('START_TEXT')).format(
				name=user.name,
				gender=gender_to_str(user.gender),
				therapy=therapy_to_str(user.therapy)
			),
			reply_markup=await get_start_menu()
		)

	except Exception as exc:
		logging.error(exc)


@router.callback_query(F.data == 'cb_psy')
async def psy(callback: types.CallbackQuery):
	try:
		await callback.message.answer(
			await get_text('PSY_TEXT'),
			reply_markup=await get_psy_menu()
		)
	except Exception as exc:
		logging.error(exc)
		return await callback.answer(
			await get_text('ERROR_TEXT')
		)


@router.callback_query(F.data == 'cb_back')
async def back(callback: types.CallbackQuery, state: FSMContext):
	try:
		await state.clear()

		user = await get_user(callback.from_user.id)

		await callback.message.edit_text(
			(await get_text('START_TEXT')).format(
				name=user.name,
				gender=gender_to_str(user.gender),
				therapy=therapy_to_str(user.therapy)
			),
			reply_markup=await get_start_menu()
		)
	except Exception as exc:
		logging.error(exc)
		return await callback.answer(
			await get_text('ERROR_TEXT')
		)
