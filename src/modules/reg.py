import logging
from asyncio import sleep

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from db.db_api import user_exists, add_user, get_text

from modules.chat import chat
from modules.common.loader import bot
from modules.common.filters import ChatTypeFilter, ContentTypeFilter
from modules.common.keyboard import get_reg_gender_menu, get_reg_therapy_menu


router = Router(name=__name__)


class RegState(StatesGroup):
	enter_name = State()
	enter_age = State()


@router.callback_query(F.data == 'cb_start_reg')
async def start_reg(callback: types.CallbackQuery, state: FSMContext):
	try:
		if await user_exists(callback.from_user.id):
			return await callback.answer()

		await bot.send_chat_action(callback.from_user.id, action="typing")
		await sleep(3)

		await callback.message.answer(
			await get_text('REG_ENTER_NAME_TEXT')
		)

		await state.set_state(RegState.enter_name)
	except Exception as exc:
		logging.error(exc)

		return await callback.answer(
			await get_text('ERROR_TEXT')
		)


@router.message(
	RegState.enter_name,
	ChatTypeFilter('private'),
	ContentTypeFilter('text')
)
async def name(message: types.Message, state: FSMContext):
	try:
		if await user_exists(message.from_user.id):
			return

		await state.set_state(None)
		await state.update_data({'name': message.text})

		await bot.send_chat_action(message.from_user.id, action="typing")
		await sleep(4)

		await message.answer(
			await get_text('REG_SELECT_GENDER_TEXT'),
			reply_markup=await get_reg_gender_menu()
		)
	except Exception as exc:
		logging.error(exc)

		return await message.answer(
			await get_text('ERROR_TEXT')
		)


@router.callback_query(F.data.contains('cb_reg_gender_'))
async def gender(callback: types.CallbackQuery, state: FSMContext):
	try:
		if await user_exists(callback.from_user.id):
			return await callback.answer()

		gender = callback.data.split('_')[-1]

		await state.set_state(None)
		await state.update_data({'gender': gender})

		await bot.send_chat_action(callback.from_user.id, action="typing")
		await sleep(4)

		await callback.message.answer(
			await get_text('REG_ENTER_AGE_TEXT')
		)

		await state.set_state(RegState.enter_age)
	except Exception as exc:
		logging.error(exc)

		return await callback.answer(
			await get_text('ERROR_TEXT')
		)


@router.message(
	RegState.enter_age,
	ChatTypeFilter('private'),
	ContentTypeFilter('text')
)
async def age(message: types.Message, state: FSMContext):
	try:
		if await user_exists(message.from_user.id):
			return

		await bot.send_chat_action(message.from_user.id, action="typing")
		await sleep(2)

		if not message.text.isdigit():
			return await message.answer(
				await get_text('ERROR_AGE_INT_TEXT')
			)

		age = int(message.text)

		if age < 18:
			return await message.answer(
				await get_text('ERROR_AGE_TEXT')
			)

		await state.set_state(None)
		await state.update_data({'age': age})

		await sleep(2)

		await message.answer(
			await get_text('REG_SELECT_THERAPY_TEXT'),
			reply_markup=await get_reg_therapy_menu()
		)
	except Exception as exc:
		logging.error(exc)

		return await message.answer(
			await get_text('ERROR_TEXT')
		)


@router.callback_query(F.data.contains('cb_reg_therapy_'))
async def therapy(callback: types.CallbackQuery, state: FSMContext):
	try:
		if await user_exists(callback.from_user.id):
			return await callback.answer()

		data = await state.get_data()
		name = data['name']
		gender = data['gender']
		age = data['age']
		therapy = callback.data.split('_')[-1]

		if not await user_exists(callback.from_user.id):
			await add_user(
				callback.from_user.id,
				callback.from_user.username,
				name,
				gender,
				age,
				therapy
			)

		await state.clear()

		await chat(callback)
	except Exception as exc:
		logging.error(exc)

		return await callback.answer(
			await get_text('ERROR_TEXT')
		)
