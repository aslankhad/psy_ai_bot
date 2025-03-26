import enum

from sqlalchemy import Column, Integer, BigInteger, \
	String, DateTime, Text, Index
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ENUM


Base = declarative_base()


class GenderEnum(str, enum.Enum):
	MALE = 'male'
	FEMALE = 'female'


class RoleEnum(str, enum.Enum):
	USER = 'user'
	ASSISTANT = 'assistant'


class TherapyEnum(str, enum.Enum):
	CBT = 'cbt'
	PSY_ANALISYS = 'analisys'
	COUCHING = 'couching'
	GESTALT = 'gestalt'
	IDK = 'idk'


class User(Base):
	__tablename__ = 'users'

	id = Column(BigInteger, primary_key=True, unique=True)

	username = Column(String, nullable=True)
	name = Column(String, nullable=False)
	gender = Column(ENUM(GenderEnum), nullable=False)
	age = Column(Integer, nullable=False)
	therapy = Column(ENUM(TherapyEnum), nullable=False)

	available_messages = Column(Integer, nullable=False, default=5)
	subscribe_expired = Column(DateTime, nullable=True)

	created_at = Column(DateTime, default=func.now())
	updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

	def __repr__(self):
		return f'#{self.id}'


class Message(Base):
	__tablename__ = 'messages'

	id = Column(Integer, primary_key=True, autoincrement=True)

	key = Column(String, nullable=False)
	value = Column(Text, nullable=False)
	description = Column(String, nullable=True)


class DepositVariant(Base):
	__tablename__ = 'deposit_variants'

	id = Column(Integer, primary_key=True, autoincrement=True)

	name = Column(String, nullable=False)
	count = Column(Integer, nullable=False)
	price = Column(Integer, nullable=False)


class Payment(Base):
	__tablename__ = 'payments'

	id = Column(Integer, primary_key=True, autoincrement=True)
	tg_id = Column(BigInteger, nullable=False)
	payment_id = Column(String, nullable=False)

	amount = Column(Integer, nullable=False)
	count = Column(Integer, nullable=False)

	created_at = Column(DateTime, default=func.now())
	updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Setting(Base):
	__tablename__ = 'settings'

	id = Column(Integer, primary_key=True, autoincrement=True)

	key = Column(String, nullable=False)
	value = Column(Text, nullable=False)
	description = Column(String, nullable=True)


class History(Base):
	__tablename__ = 'history'

	id = Column(Integer, primary_key=True, autoincrement=True)
	tg_id = Column(BigInteger, nullable=False)
	role = Column(ENUM(RoleEnum), nullable=False)
	content = Column(Text, nullable=False)

	created_at = Column(DateTime, default=func.now())
	updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class DayHint(Base):
	__tablename__ = 'day_hints'

	id = Column(Integer, primary_key=True, autoincrement=True)

	hint = Column(Text, nullable=False)


Index('idx_texts_key', Message.key)
Index('idx_history_tg_id', History.tg_id)
