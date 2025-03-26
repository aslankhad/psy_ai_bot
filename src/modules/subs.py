import logging
from datetime import datetime, timezone

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from db.db_api import get_user, get_text, \
	get_deposit_variant, get_deposit_variants, \
	update_user_subscription, add_payment

from modules.common.loader import bot
from modules.common.filters import ChatTypeFilter, ContentTypeFilter
from modules.common.keyboard import get_balance_menu, \
	get_deposit_menu, get_buy_menu, get_back_menu
from modules.common.payment import create_payment, get_payment
from modules.common.utils import check_email


router = Router(name=__name__)


class SubState(StatesGroup):
	enter_email = State()


@router.callback_query(F.data == 'cb_subs')
async def subs(callback: types.CallbackQuery):
	try:
		user = await get_user(callback.from_user.id)

		if not user.subscribe_expired or \
			user.subscribe_expired.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
			await callback.message.edit_text(
				await get_text('SUBS_INACTIVE_TEXT'),
				reply_markup=await get_balance_menu()
			)
		else:
			await callback.message.edit_text(
				(await get_text('SUBS_ACTIVE_TEXT')).format(
					expired=user.subscribe_expired.strftime('%d.%m.%Y'),
				),
				reply_markup=await get_balance_menu()
			)
	except Exception as exc:
		logging.error(exc)

		await callback.answer(
			await get_text('ERROR_TEXT')
		)


@router.callback_query(F.data == 'cb_deposit')
async def deposit(callback: types.CallbackQuery):
	try:
		deposit_variants = await get_deposit_variants()

		await callback.message.edit_text(
			await get_text('DEPOSIT_TEXT'),
			reply_markup=await get_deposit_menu(deposit_variants)
		)
	except Exception as exc:
		logging.error(exc)

		await callback.answer(
			await get_text('ERROR_TEXT')
		)


@router.callback_query(F.data.contains('cb_buy_'))
async def buy(callback: types.CallbackQuery, state: FSMContext):
	try:
		variant_id = int(callback.data.split('_')[-1])

		await callback.message.edit_text(
			await get_text('ENTER_EMAIL_TEXT'),
			reply_markup=await get_back_menu()
		)
		await state.update_data(
			{'variant_id': variant_id, 'message_id': callback.message.message_id}
		)
		await state.set_state(SubState.enter_email)
	except Exception as exc:
		logging.error(exc)

		await callback.answer(
			await get_text('ERROR_TEXT')
		)


@router.message(
	SubState.enter_email,
	ChatTypeFilter('private'),
	ContentTypeFilter('text')
)
async def email(message: types.Message, state: FSMContext):
	try:
		await message.delete()

		if not check_email(message.text):
			return

		message_id = await state.get_value('message_id')
		variant_id = await state.get_value('variant_id')
		variant = await get_deposit_variant(variant_id)

		payment = await create_payment(
			variant.price,
			variant.name,
			{'count': variant.count, 'price': variant.price},
			message.text
		)

		await bot.edit_message_text(
			(await get_text('BUY_TEXT')).format(
				count=variant.count,
				price=variant.price
			),
			reply_markup=await get_buy_menu(
				payment.id,
				payment.confirmation.confirmation_url,
			),
			chat_id=message.from_user.id,
			message_id=message_id
		)
	except Exception as exc:
		logging.error(exc)

		await message.answer(
			await get_text('ERROR_TEXT')
		)


@router.callback_query(F.data.contains('cb_check_'))
async def check(callback: types.CallbackQuery):
	try:
		payment_id = callback.data.split('_')[-1]
		payment = await get_payment(payment_id)

		if not payment or not payment.status == 'succeeded':
			return await callback.answer(
				await get_text('PAYMENT_CHECK_FAILED_TEXT'),
				show_alert=True
			)

		count = int(payment.metadata['count'])
		price = int(payment.metadata['price'])

		await add_payment(callback.from_user.id, payment_id, price, count)
		await update_user_subscription(callback.from_user.id, count)
		await subs(callback)
	except Exception as exc:
		logging.error(exc)

		await callback.answer(
			await get_text('ERROR_TEXT')
		)
