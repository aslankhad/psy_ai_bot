from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChatTypeFilter(BaseFilter):
	def __init__(self, chat_type: Union[str, list]):
		self.chat_type = chat_type

	async def __call__(self, message: Message) -> bool:
		if isinstance(self.chat_type, str):
			return message.chat.type == self.chat_type
		else:
			return message.chat.type in self.chat_type


class ContentTypeFilter(BaseFilter):
	def __init__(self, content_type: Union[str, list]):
		self.content_type = content_type

	async def __call__(self, message: Message) -> bool:
		if isinstance(self.content_type, str):
			return message.content_type == self.content_type
		else:
			return message.content_type in self.content_type
