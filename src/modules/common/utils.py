import re

from db.models import GenderEnum, TherapyEnum


def gender_to_str(gender: GenderEnum):
	data = {
		GenderEnum.MALE: 'Мужской',
		GenderEnum.FEMALE: 'Женский'
	}

	return data[gender]


def therapy_to_str(therapy: TherapyEnum):
	data = {
		TherapyEnum.CBT: 'КПТ',
		TherapyEnum.PSY_ANALISYS: 'Психоанализ',
		TherapyEnum.COUCHING: 'Коучинг',
		TherapyEnum.GESTALT: 'Гештальт-терапия',
		TherapyEnum.IDK: 'Не знаю'

	}

	return data[therapy]


def check_email(email: str):
	pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
	return bool(re.fullmatch(pattern, email))
