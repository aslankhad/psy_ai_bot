from os import getenv
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

DATABASE_HOST = getenv('POSTGRES_HOST')
DATABASE_NAME = getenv('POSTGRES_DB')
DATABASE_USER = getenv('POSTGRES_USER')
DATABASE_PASS = getenv('POSTGRES_PASSWORD')

DATABASE_URL = 'postgresql+asyncpg://{user}:{passw}@{host}/{name}'.format(
	user=DATABASE_USER,
	passw=DATABASE_PASS,
	host=DATABASE_HOST,
	name=DATABASE_NAME
)

BOT_TOKEN = getenv('BOT_TOKEN')

ROOT_LOGIN = getenv('ROOT_LOGIN')
ROOT_PASSWORD = getenv('ROOT_PASSWORD')

SECRET_KEY = getenv('SECRET_KEY')

APP_URL = getenv('APP_URL')
APP_TITLE = getenv('APP_TITLE')

YOOKASSA_SHOP_ID = getenv('YOOKASSA_SHOP_ID')
YOOKASSA_SECRET_KEY = getenv('YOOKASSA_SECRET_KEY')

GPT_TOKEN = getenv('GPT_TOKEN')
SOCKS_URL = getenv('SOCKS_URL')
