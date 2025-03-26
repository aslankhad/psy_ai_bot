import logging
import uuid

from yookassa import Payment, Configuration

from modules.common.loader import bot
from data.config import YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY


Configuration.account_id = YOOKASSA_SHOP_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY


async def create_payment(
	amount: str,
	description: str,
	data: dict,
	email: str = None
) -> Payment:
	# Формат amount - '100.00'
	bot_username = await bot.get_me()

	body = {
		'amount': {
			'value': amount,
			'currency': 'RUB'
		},

		# Если нужна генерация чека - раскоментить эту часть
		'receipt': {
			'customer': {
				'email': email
			},
			'items': [{
				'description': description,
				'amount': {
					'value': amount,
					'currency': 'RUB'
				},
				'vat_code': 1,
				'quantity': 1,
				'payment_subject': 'service',
				'payment_mode': 'full_payment'
			}]
		},


		'confirmation': {
			'type': 'redirect',
			'return_url': f'https://t.me/{bot_username.username}'
		},
		'metadata': data,
		'capture': True,
		'description': f'{description}',
		'save_payment_method': False
	}

	return Payment.create(body, uuid.uuid4())


async def get_payment(payment_id: str) -> bool:
	try:
		return Payment.find_one(payment_id)
	except Exception as exc:
		logging.info(f'{exc}')
		return False


async def check_payment(payment_id: str) -> bool:
	try:
		payment = Payment.find_one(payment_id)

		if payment and payment.status == 'succeeded':
			return True

		return False

	except Exception as exc:
		logging.info(f'{exc}')
		return False
