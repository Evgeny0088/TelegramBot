import requests
import json
import bot_token
from time import sleep
import sys

t = bot_token.tok
URL = 'https://api.telegram.org/bot' + t + '/'
url_currency = 'https://yobit.net/api/2/usd_rur/ticker'
global last_update
last_update = 0
#new commit
def get_updates(URL=URL):
	url = URL + 'getUpdates'
	r = requests.get(url)
	if r.status_code == 200:
		return r.json()
	else:
		return False

def get_message():
	g = get_updates()
	current_update = g['result'][-1]['update_id']
	global last_update
	if last_update!=current_update:
		last_update = current_update
		chat_id = g['result'][-1]['message']['chat']['id']
		chat_message = g['result'][-1]['message']['text']
		return {'chat_id':chat_id,
			    'text':chat_message}
	else:
		return None

def send_message(chat_id, message = 'Wait a secong please...'):
	url = URL + f'sendmessage?chat_id={chat_id}&text={message}'
	requests.post(url)


def check_data():
	d = get_updates()
	with open('output.txt', 'w') as file:
		json.dump(d,file, indent = 2)
	file.close()

def main():
	while True:
		message = get_message()
		if message is not None:
			if message['text'] == 'usd/rub':
				currency = requests.get(url_currency).json()
				send_message(message['chat_id'],currency['ticker']['last'])
			elif message['text'] == 'stop':
				sys.exit()
			else:
				continue
		sleep(3)

if __name__ == '__main__':
	main()
