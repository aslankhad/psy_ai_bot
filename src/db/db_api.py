import logging

from typing import Optional
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from data.config import DATABASE_URL

from db.models import User, Message, DepositVariant, \
	Payment, Setting, History, DayHint, GenderEnum, TherapyEnum


engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False
)


async def get_user(id: int) -> Optional[User]:
	async with async_session() as session:
		query = select(User).where(User.id == id)

		try:
			res = await session.execute(query)
			return res.scalar_one_or_none()
		except Exception as exc:
			logging.error(exc)


async def get_users() -> list[User]:
	async with async_session() as session:
		query = select(User)

		try:
			res = await session.execute(query)
			return res.scalars().all()
		except Exception as exc:
			logging.error(exc)


async def user_exists(id: int) -> bool:
	return not not await get_user(id)


async def add_user(
	tg_id: int,
	username: Optional[str],
	name: str,
	gender: GenderEnum,
	age: int,
	therapy: TherapyEnum
) -> None:
	async with async_session() as session:
		new_user = User(
			id=tg_id,
			username=username,
			name=name,
			gender=gender,
			age=age,
			therapy=therapy,
		)

		session.add(new_user)

		try:
			await session.commit()
		except Exception as exc:
			await session.rollback()
			logging.error(exc)


async def update_user(
	id: int,
	name: str = None,
	gender: GenderEnum = None,
	therapy: TherapyEnum = None
) -> None:
	async with async_session() as session:
		query = select(User).where(User.id == id)

		try:
			res = await session.execute(query)
			user: Optional[User] = res.scalar_one_or_none()

			if name:
				user.name = name
			if gender:
				user.gender = gender
			if therapy:
				user.therapy = therapy

			await session.commit()
		except Exception as exc:
			await session.rollback()
			logging.error(exc)


async def update_user_messages(id: int, count: int, increase: bool = False) -> None:
	async with async_session() as session:
		query = select(User).where(User.id == id)

		try:
			res = await session.execute(query)
			user: Optional[User] = res.scalar_one_or_none()

			if increase:
				user.available_messages += count
			else:
				user.available_messages -= count

			await session.commit()
		except Exception as exc:
			await session.rollback()
			logging.error(exc)


async def update_user_subscription(id: int, count: int) -> None:
	async with async_session() as session:
		query = select(User).where(User.id == id)

		try:
			res = await session.execute(query)
			user: Optional[User] = res.scalar_one_or_none()

			if user is None:
				logging.warning(f"User with id {id} not found")
				return

			current_date = datetime.now(timezone.utc).replace(tzinfo=None)

			if not user.subscribe_expired:
				user.subscribe_expired = current_date + timedelta(days=count)
			else:
				if user.subscribe_expired > current_date:
					user.subscribe_expired += timedelta(days=count)
				else:
					user.subscribe_expired = current_date + timedelta(days=count)

			await session.commit()
		except Exception as exc:
			await session.rollback()
			logging.error(exc)


async def get_text(key: str) -> str:
	async with async_session() as session:
		query = select(Message).where(Message.key == key)

		try:
			res = await session.execute(query)
			return res.scalar_one_or_none().value
		except Exception:
			return f'{key} not found!'


async def get_deposit_variant(id: int) -> Optional[DepositVariant]:
	async with async_session() as session:
		query = select(DepositVariant).where(DepositVariant.id == id)

		try:
			res = await session.execute(query)
			return res.scalar_one_or_none()
		except Exception as exc:
			logging.error(exc)


async def get_deposit_variants() -> list[DepositVariant]:
	async with async_session() as session:
		query = select(DepositVariant)

		try:
			res = await session.execute(query)
			return res.scalars().all()
		except Exception as exc:
			logging.error(exc)


async def get_payment(payment_id: int) -> Optional[Payment]:
	async with async_session() as session:
		query = select(Payment).where(Payment.payment_id == payment_id)

		try:
			res = await session.execute(query)
			return res.scalar_one_or_none()
		except Exception as exc:
			logging.error(exc)


async def add_payment(
	tg_id: int,
	payment_id: str,
	amount: int,
	count: int,
) -> None:
	async with async_session() as session:
		new_payment = Payment(
			tg_id=tg_id,
			payment_id=payment_id,
			amount=amount,
			count=count,
		)

		session.add(new_payment)

		try:
			await session.commit()
		except Exception as exc:
			await session.rollback()
			logging.error(exc)


async def get_setting(key: str) -> str:
	async with async_session() as session:
		query = select(Setting).where(Setting.key == key)

		try:
			res = await session.execute(query)
			return res.scalar_one_or_none().value
		except Exception as exc:
			logging.error(exc)


async def get_user_chat_history(tg_id: int, for_gpt: bool) -> list[History]:
	async with async_session() as session:
		query = select(History).where(History.tg_id == tg_id)

		try:
			res = await session.execute(query)
			history: list[History] = res.scalars().all()

			if for_gpt:
				gpt_format = []

				for story in history:
					gpt_format.append(
						{'role': story.role, 'content': story.content}
					)
				return gpt_format

			return history
		except Exception as exc:
			logging.error(exc)


async def update_history(
	tg_id: int,
	history: list[dict],
) -> None:
	async with async_session() as session:
		for story in history:
			new_history = History(
				tg_id=tg_id,
				role=story['role'],
				content=story['content']
			)

			session.add(new_history)

		try:
			await session.commit()
		except Exception as exc:
			await session.rollback()
			logging.error(exc)


async def get_hints() -> list[DayHint]:
	async with async_session() as session:
		query = select(DayHint)

		try:
			res = await session.execute(query)
			return res.scalars().all()
		except Exception as exc:
			logging.error(exc)


async def update_users_daily_limit():
	async with async_session() as session:
		stmt = update(User).values(available_messages=5)
		await session.execute(stmt)

		try:
			await session.commit()
		except Exception as exc:
			await session.rollback()
			logging.error(exc)
