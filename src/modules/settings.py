import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from db.db_api import update_user, get_text

from modules.common.loader import bot
from modules.common.filters import ChatTypeFilter, ContentTypeFilter
from modules.common.keyboard import get_settings_menu, get_edit_gender_menu, \
	get_edit_therapy_menu, get_back_menu


router = Router(name=__name__)


class EditState(StatesGroup):
	enter_name = State()


@router.callback_query(F.data == 'cb_settings')
async def settings(callback: types.CallbackQuery):
	try:
		await callback.message.edit_text(
			await get_text('SETTINGS_TEXT'),
			reply_markup=await get_settings_menu()
		)

	except Exception as exc:
		logging.error(exc)


@router.callback_query(F.data == 'cb_edit_name')
async def edit_name(callback: types.CallbackQuery, state: FSMContext):
	try:
		await callback.message.edit_text(
			await get_text('EDIT_ENTER_NAME_TEXT'),
			reply_markup=await get_back_menu()
		)
		await state.update_data({'message_id': callback.message.message_id})
		await state.set_state(EditState.enter_name)
	except Exception as exc:
		logging.error(exc)

		return await callback.answer(
			await get_text('ERROR_TEXT')
		)


@router.message(
	EditState.enter_name,
	ChatTypeFilter('private'),
	ContentTypeFilter('text')
)
async def name(message: types.Message, state: FSMContext):
	try:
		await message.delete()
		await state.set_state(None)

		message_id = await state.get_value('message_id')

		await update_user(message.from_user.id, name=message.text)

		await bot.edit_message_text(
			await get_text('SETTINGS_TEXT'),
			reply_markup=await get_settings_menu(),
			chat_id=message.from_user.id,
			message_id=message_id
		)
	except Exception as exc:
		logging.error(exc)

		return await message.answer(
			await get_text('ERROR_TEXT')
		)


@router.callback_query(F.data == 'cb_edit_gender')
async def edit_gender(callback: types.CallbackQuery):
	try:
		await callback.message.edit_text(
			await get_text('EDIT_ENTER_GENDER_TEXT'),
			reply_markup=await get_edit_gender_menu()
		)
	except Exception as exc:
		logging.error(exc)

		return await callback.answer(
			await get_text('ERROR_TEXT')
		)


@router.callback_query(F.data.contains('cb_edit_gender_'))
async def gender(callback: types.CallbackQuery):
	try:
		gender = callback.data.split('_')[-1]

		await update_user(callback.from_user.id, gender=gender)
		await settings(callback)
	except Exception as exc:
		logging.error(exc)

		return await callback.answer(
			await get_text('ERROR_TEXT')
		)


@router.callback_query(F.data == 'cb_edit_therapy')
async def edit_therapy(callback: types.CallbackQuery):
	try:
		await callback.message.edit_text(
			await get_text('EDIT_ENTER_THERAPY_TEXT'),
			reply_markup=await get_edit_therapy_menu()
		)
	except Exception as exc:
		logging.error(exc)

		return await callback.answer(
			await get_text('ERROR_TEXT')
		)


@router.callback_query(F.data.contains('cb_edit_therapy_'))
async def therapy(callback: types.CallbackQuery):
	try:
		therapy = callback.data.split('_')[-1]

		await update_user(callback.from_user.id, therapy=therapy)
		await settings(callback)
	except Exception as exc:
		logging.error(exc)

		return await callback.answer(
			await get_text('ERROR_TEXT')
		)
