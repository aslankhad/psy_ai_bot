from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.db_api import get_text
from db.models import DepositVariant, TherapyEnum


async def get_start_menu() -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.row(
		types.InlineKeyboardButton(
			text=await get_text('CHAT_BUTTON'),
			callback_data='cb_chat'
		)
	)
	builder.row(
		types.InlineKeyboardButton(
			text=await get_text('SUBS_BUTTON'),
			callback_data='cb_subs'
		)
	)
	builder.row(
		types.InlineKeyboardButton(
			text=await get_text('PSY_BUTTON'),
			callback_data='cb_psy'
		)
	)
	builder.row(
		types.InlineKeyboardButton(
			text=await get_text('SETTINGS_BUTTON'),
			callback_data='cb_settings'
		)
	)
	return builder.as_markup()


async def get_start_reg_menu() -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.button(
		text=await get_text('START_REG_BUTTON'),
		callback_data='cb_start_reg'
	)
	return builder.as_markup()


async def get_reg_gender_menu() -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.button(
		text=await get_text('MALE_BUTTON'),
		callback_data='cb_reg_gender_male'
	)
	builder.button(
		text=await get_text('FEMALE_BUTTON'),
		callback_data='cb_reg_gender_female'
	)
	builder.adjust(1, 1)
	return builder.as_markup()


async def get_edit_gender_menu() -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.button(
		text=await get_text('MALE_BUTTON'),
		callback_data='cb_edit_gender_male'
	)
	builder.button(
		text=await get_text('FEMALE_BUTTON'),
		callback_data='cb_edit_gender_female'
	)
	builder.adjust(1, 1)
	return builder.as_markup()


async def get_reg_therapy_menu() -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	for therapy in TherapyEnum:
		builder.row(
			types.InlineKeyboardButton(
				text=await get_text(f'THERAPY_{therapy.value.upper()}_BUTTON'),
				callback_data=f'cb_reg_therapy_{therapy.value}'
			)
		)
	return builder.as_markup()


async def get_edit_therapy_menu() -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	for therapy in TherapyEnum:
		builder.row(
			types.InlineKeyboardButton(
				text=await get_text(f'THERAPY_{therapy.value.upper()}_BUTTON'),
				callback_data=f'cb_edit_therapy_{therapy.value}'
			)
		)
	return builder.as_markup()


async def get_balance_menu() -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.button(
		text=await get_text('BACK_BUTTON'),
		callback_data='cb_back'
	)
	builder.button(
		text=await get_text('DEPOSIT_BUTTON'),
		callback_data='cb_deposit'
	)
	return builder.as_markup()


async def get_deposit_menu(variants: list[DepositVariant]) -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	for variant in sorted(variants, key=lambda x: x.count):
		builder.row(
			types.InlineKeyboardButton(
				text=variant.name,
				callback_data=f'cb_buy_{variant.id}'
			)
		)
	builder.row(
		types.InlineKeyboardButton(
			text=await get_text('BACK_BUTTON'),
			callback_data='cb_subs'
		)
	)
	return builder.as_markup()


async def get_buy_menu(payment_id: str, payment_url: str) -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.button(
		text=await get_text('PAY_BUTTON'),
		url=payment_url
	)
	builder.button(
		text=await get_text('CHECK_BUTTON'),
		callback_data=f'cb_check_{payment_id}'
	)
	builder.button(
		text=await get_text('BACK_BUTTON'),
		callback_data='cb_deposit'
	)
	builder.adjust(2, 1)
	return builder.as_markup()


async def get_limit_menu() -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.button(
		text=await get_text('GET_SUB_BUTTON'),
		callback_data='cb_deposit'
	)
	return builder.as_markup()


async def get_psy_menu() -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.button(
		text=await get_text('OPEN_PSY_BUTTON'),
		url='https://t.me/durov'
	)
	return builder.as_markup()


async def get_back_menu() -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.button(
		text=await get_text('BACK_BUTTON'),
		callback_data='cb_back'
	)
	return builder.as_markup()


async def get_settings_menu() -> types.InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.button(
		text=await get_text('EDIT_NAME_BUTTON'),
		callback_data='cb_edit_name'
	)
	builder.button(
		text=await get_text('EDIT_GENDER_BUTTON'),
		callback_data='cb_edit_gender'
	)
	builder.button(
		text=await get_text('EDIT_THERAPY_BUTTON'),
		callback_data='cb_edit_therapy'
	)
	builder.button(
		text=await get_text('BACK_BUTTON'),
		callback_data='cb_back'
	)
	builder.adjust(1, 1, 1, 1)
	return builder.as_markup()
