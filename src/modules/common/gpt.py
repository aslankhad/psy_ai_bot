import logging
import aiohttp
from aiohttp_socks import ProxyConnector

from data.config import GPT_TOKEN, SOCKS_URL


async def gpt_request(prompt, history=None):
	if not history:
		history = []

	history.append({'role': 'user', 'content': prompt})

	connector = ProxyConnector.from_url(SOCKS_URL)
	headers = {
		'Authorization': f'Bearer {GPT_TOKEN}',
		'Content-Type': 'application/json'
	}

	url = 'https://api.openai.com/v1/chat/completions'

	data = {
		'model': 'gpt-4',
		'messages': history,
		'temperature': 1,
		'top_p': 1,
		'frequency_penalty': 0,
		'presence_penalty': 0
	}

	try:
		async with aiohttp.ClientSession(connector=connector) as session:
			async with session.post(url, json=data, headers=headers) as response:
				return (await response.json())['choices'][0]['message']['content']
	except Exception as err:
		logging.warning(err)
