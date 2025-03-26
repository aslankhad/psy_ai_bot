import jwt
from passlib.context import CryptContext

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from data.config import ROOT_LOGIN, ROOT_PASSWORD


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminAuth(AuthenticationBackend):
	def __init__(self, secret_key):
		super().__init__(secret_key)
		self.secret_key = secret_key

	async def login(self, request: Request) -> bool:
		form = await request.form()
		username, password = form['username'], form['password']

		if username == ROOT_LOGIN and password == ROOT_PASSWORD:
			encoded_jwt = jwt.encode(
				{'user': ROOT_LOGIN, 'hash_pass': pwd_context.hash(ROOT_PASSWORD)},
				self.secret_key,
				algorithm='HS256'
			)
			request.session.update({'token': encoded_jwt})
			return True

		return False

	async def logout(self, request: Request) -> bool:
		request.session.clear()
		return True

	async def authenticate(self, request: Request) -> bool:
		token = request.session.get('token')

		if not token:
			return False

		decoded_jwt = jwt.decode(token, self.secret_key, algorithms=["HS256"])

		if decoded_jwt['user'] == ROOT_LOGIN and \
			pwd_context.verify(ROOT_PASSWORD, decoded_jwt['hash_pass']):
			return True

		return False
