#!/usr/bin/python3

from telegram.ext import Updater, CommandHandler
import os
import requests
import json
import urllib
from forex_python.converter import CurrencyRates
from optparse import OptionParser
from deribit_api import RestClient

def start(bot, update):
	update.message.reply_text('Hello World!')

def hello(bot, update):
	update.message.reply_text(
	'Hello {}'.format(update.message.from_user.first_name))

def k0(bot,update):
	os.system("k0")
	update.message.reply_text('k kapandı')

def k1(bot,update):
	os.system("k1")
	update.message.reply_text('k acıldı')

def s0(bot,update):
	os.system("s0")
	update.message.reply_text('s kapandı')

def s1(bot,update):
	os.system("s1")
	update.message.reply_text('s acıldı')

def reboot(bot,update):
	update.message.reply_text('restart atılıyor')
	os.system("reboot")

def mail(bot,update):
	os.system("python3 /home/uad/prog/mail/ip_crypto_mail.py")
	update.message.reply_text("ip_crypt mail gönderildi")

def dervis(bot,update):
	update.message.reply_text('...')
	path = "/home/uad/prog/bot/telegram/dervis.txt"
	os.chdir("/home/uad/Desktop/dervis-yilmaz/asur/")
	os.system("python3 /home/uad/Desktop/dervis-yilmaz/asur/asur.py 1 " + path)
	file_siir = open(path, "r")
	siir = file_siir.read()
	update.message.reply_text(siir)
	file_siir.close()
	os.remove(path)

def curr(bot, update):
	def options():
		client = RestClient()
		call = "BTC-29DEC17-11000-C"
		put = "BTC-29DEC17-3000-P"
		myc = client.getsummary(call)
		myp = client.getsummary(put)
		result = str(myc['instrumentName']) + ": " + str(myc['bidPrice']) + "\n" + str(myp['instrumentName']) + ": " + str(myp['bidPrice'])
		return result
	def currencies():
		coins = ["bitcoin", "ethereum", "bitcoin-cash"]
		n = 0
		coin_usd = []
		coin_try = []
		for coin in coins[:]:
			url = "https://api.coinmarketcap.com/v1/ticker/"+coin+"/"
			#print("Fetching prices for " + coin + "...")
			resp = requests.get(url, verify=True) #verify is checking SSL certificate
			#if(resp.status_code != 200):
				#print("Status: ", resp.status_code,)
			data = json.loads(resp.text)[0]
			cr = CurrencyRates()
			usd = float(data['price_usd'])
			tl = cr.convert("USD","TRY",usd)
			coin_usd.append(usd)
			coin_try.append(tl)
			n += 1
		usdtry = cr.get_rate('USD','TRY')
		chftry = cr.get_rate('CHF','TRY')
		eurtry = cr.get_rate('EUR','TRY')
		result = "BTC: " + str(coin_usd[0]) + " USD" + "\n" + "ETH: " + str(coin_usd[1]) + " USD" + "\n" + "BCH: " + str(coin_usd[2]) + " USD" + "\n" + "USD/TRY: " + str(usdtry) + "\n" + "CHF/TRY: " + str(chftry) + "\n" + "EUR/TRY: " + str(eurtry) + "\n"
		return result
	update.message.reply_text('...')
	update.message.reply_text(currencies())
	update.message.reply_text(options())

def ip(bot, update):
	ip_req = requests.get('http://ipinfo.io/ip')
	ip_text = ip_req.text
	update.message.reply_text(ip_text)

def arbstat(bot,update,args):
	update.message.reply_text('...')
	cmd = "python3 /home/uad/prog/bot/stat-arb/stats.py %s %s %s %s upload" % (args[0], args[1], args[2], args[3]) 
	os.system(cmd)
	update.message.reply_text('done\n stat results uploaded to drive')

def ls(bot,update):
	update.message.reply_text("/start\n/hello\n/k0\n/k1\n/mail\n/reboot\n/dervis\n/curr\n/ip\n/arbstat (coin1) (coin2) (start_date) (end_date) update\n/options\n/arb\nls\n")


def arb(bot,update):
	def b_btc():
		btcturk = "https://www.btcturk.com/api/ticker"
		return requests.get(btcturk).json()
	def p_btc():
		paribu = "https://www.paribu.com/ticker"
		return requests.get(paribu).json()
	b = b_btc()
	p = p_btc()
	#dif_bid = b[0]["bid"] - p["BTC_TL"]["highestBid"]
	#dif_ask = b[0]["ask"] - p["BTC_TL"]["lowestAsk"]
	dif = p["BTC_TL"]["highestBid"] - b[0]["ask"]
	#arb_data = "bid, ask, " + str(round(dif_bid,4)) + ", " + str(round(dif_ask,4))
	arb_data = "pbid - bask = " + str(round(dif,4))
	update.message.reply_text(arb_data)





updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('k0', k0))
updater.dispatcher.add_handler(CommandHandler('k1', k1))
updater.dispatcher.add_handler(CommandHandler('s0', s0))
updater.dispatcher.add_handler(CommandHandler('s1', s1))
updater.dispatcher.add_handler(CommandHandler('mail', mail))
updater.dispatcher.add_handler(CommandHandler('reboot', reboot))
updater.dispatcher.add_handler(CommandHandler('dervis', dervis))
updater.dispatcher.add_handler(CommandHandler('curr', curr))
updater.dispatcher.add_handler(CommandHandler('ls', ls))
updater.dispatcher.add_handler(CommandHandler('ip',ip))
updater.dispatcher.add_handler(CommandHandler('arbstat', arbstat, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('arb', arb))


updater.start_polling()
updater.idle()


