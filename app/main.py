import requests
import json
import re
from flask import Flask, request
from flask import jsonify

# webhook activation - "https://api.telegram.org/TOKEN/setWebhook?url=https://evgeny88.pythonanywhere.com/"
# webhook deactivation - "https://api.telegram.org/TOKEN/deleteWebhook?url=https://f270934581ac.ngrok.io/"
#telegram bot token:
tok = "TOKEN"
URL = 'https://api.telegram.org/bot'
data = requests.get(URL)
info = {
		"usd":"usd_rur",
	}

def write_json(data, filename = 'data.json'):
	with open(filename, 'w') as file:
		json.dump(data,file, indent = 2, ensure_ascii = False)
		file.write(data)
	file.close()

def get_updates(URL = URL):
	url = URL + 'getUpdates'
	r = requests.get(url)
	if r.status_code == 200:
		write_json(r.json())
	else:
		None

def parce_text(text):
	pattern = r'/\w+'
	try:
		return re.search(pattern,text).group()[1:]
	except AttributeError:
		return None


def get_price(parce_text):
	url = f'https://yobit.net/api/2/{parce_text}/ticker'
	r = requests.get(url)
	print(r.status_code)
	if r.status_code == 200:
		return r.json()['ticker']['last']
	else:
		None

def send_message(url,chat_id,message='please wait a second...'):
	url+= f'sendmessage?chat_id={chat_id}&text={message}'
	requests.post(url)

def main():
	r = requests.get(URL + 'getMe')
	if r.status_code == 200:
		write_json(r.text)
	else:
		None


app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index(tok=tok):
	url = URL + tok + '/'
	if request.method == 'POST':
		r = request.get_json()
		chat_id = r['message']['chat']['id']
		message = r['message']['text']
		check = parce_text(message)
		if check in info:
			send_message(url,chat_id,f'info:{get_price(info.get(check))}')
			return jsonify(r)
	return '<h1>Home page</h1>'

if __name__ == '__main__':
	app.run(debug = True)

