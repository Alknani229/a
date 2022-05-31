# SubmitBand_bot

import telebot
import requests
from urllib.parse import quote
from time import sleep

BOT_TOKEN = '5588822464:AAHk4CiXpgutk2i18lkCATXmaCgURCiM3To'
bot = telebot.TeleBot(BOT_TOKEN)
# مستخدمين البوت
bot_users = ['834403140', '466111814']
admin_id = '466111814'

def submit(data):
    url = "https://help.instagram.com/ajax/help/contact/submit/page"

    payload = f'jazoest=2928&lsd=AVow-_x2AkA&name={quote(data[0])}&email={data[2]}&instagram_username={data[1]}&mobile_number={data[3]}&appeal_reason={data[4]}&support_form_id=606967319425038&support_form_hidden_fields=%7B%7D&support_form_fact_false_fields=%5B%5D&__user=0&__a=1&__dyn=7xe6Fo4OQ1PyUbFuC1swgE98nwgU6C7UW8xi642-7E2vwXx60kO4o3Bw5VCwjE3awbG782Cwooa81Vrzo5-0jx0Fwww6DwtU6e0D83mwaS0zE5W0PU1AEG0hi0Lo6-&__csr=&__req=1o&__hs=19111.BP%3ADEFAULT.2.0.0.0.&dpr=1&__ccg=GOOD&__rev=1005434099&__s=vwzw0x%3Athko2k%3A5zd74l&__hsi=7092103901735683554-0&__comet_req=0&__spin_r=1005434099&__spin_b=trunk&__spin_t=1651259115'

    headers = {
        'authority': 'help.instagram.com',
        'accept': '*/*',
        'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'ig_did=F8AEBA80-F0D4-470D-8E4C-E46D8E6F9527; datr=6zZsYhxEcM_93oWfmD5ewLU8; ig_nrcb=1; mid=Ymw8pwALAAGzqrUzJXbioJc1Ky_p; csrftoken=3Bl75kKNr2qj0MzangmPiXHJVxXpM8HI; dpr=1.25',
        'origin': 'https://help.instagram.com',
        'referer': 'https://help.instagram.com/contact/606967319425038?helpref=page_content',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'x-fb-lsd': 'AVow-_x2AkA'
        }

    response = requests.request("POST", url, headers=headers, data=payload)

    if ("errorSummary") in str(response.text):
        return False
    else:
	    return True

welcome_message = '''مرحبا بك في بوت تقديم الطعن للحسابات المعطلة\n
للتقديم يرجى تحضير المتطلبات التالية (بللغة الانكيزية):\n
الاسم الكامل\n
اسم المستخدم\n
الاميل\n
رقم الهاتف\n
الرسالة\n
الوقت الفاصل بين كل طلب (ساعة)'''

contact = 'www.facebook.com/admail123'

@bot.message_handler(commands=['start'])
def welcome(message):
	sent = bot.send_message(message.chat.id, welcome_message)

@bot.message_handler(commands=['submit'])
def go(message):
	to_check_id = str(message.chat.id)
	if to_check_id in bot_users:
		sent = bot.send_message(message.chat.id, 'ادخل العلومات بلترتيب')
		bot.register_next_step_handler(sent, requirements_handler)
	else:
		bot.send_message(message.chat.id, f'لا يمكن للمستخدم {message.chat.id} استخدام البوت يرجى التواصل مع {contact}')

data = []
def requirements_handler(message):
	if '/' in message.text:
		bot.send_message(message.chat.id, 'ادخل الامر مره اخرى')
	else:
		try:
			for d in message.text.split('\n'):
				data.append(d)

			done_message = f'تم التقديم و سوف يتم تكرار العملية بعد {data[5]} ساعة'
			fail_message = 'المستخدم محضور سوف يتم تكرار العملية بعد 1 ساعة'
			while True:
				response = submit(data)
				if response == True:
					bot.send_message(message.chat.id, done_message)
					sleep(int(data[5]) * 60 * 60)
				else:
					bot.send_message(message.chat.id, fail_message)
					sleep(int(data[5]) * 60 * 60)
		except:
			bot.send_message(message.chat.id, 'يرجى اعادة التقديم و التحقق من المعلومات')

@bot.message_handler(commands=['add'])
def add(message):
	sent = bot.send_message(message.chat.id, 'ادخل رقم المستخدم الجديد')
	bot.register_next_step_handler(sent, add_user)

def add_user(message):
	if '/' in message.text:
		bot.send_message(message.chat.id, 'ادخل الامر مره اخرى')
	else:
		try:
			if str(message.chat.id) == admin_id and isinstance(int(message.text), int):
				bot_users.append(str(message.text))
				bot.send_message(message.chat.id, 'تم اضافة المستخدم')
			else:
				bot.send_message(message.chat.id, 'لا يمكنك اضافة مستخدم جديد. تحقق من رقم المستخدم او من صلاحياتك')
		except:
			bot.send_message(message.chat.id, 'لا يمكنك اضافة مستخدم جديد. تحقق من رقم المستخدم او من صلاحياتك')

@bot.message_handler(commands=['delete'])
def delete(message):
	sent = bot.send_message(message.chat.id, 'ادخل رقم المستخدم للحذف')
	bot.register_next_step_handler(sent, delete_user)

def delete_user(message):
	if '/' in message.text:
		bot.send_message(message.chat.id, 'ادخل الامر مره اخرى')
	else:
		try:
			if str(message.chat.id) == admin_id and isinstance(int(message.text), int):
				bot_users.remove(str(message.text))
				bot.send_message(message.chat.id, 'تم حذف المستخدم')
			else:
				bot.send_message(message.chat.id, 'لا يمكنك حذف المستخدم. تحقق من رقم المستخدم او من صلاحياتك')
		except:
			bot.send_message(message.chat.id, 'لا يمكنك حذف المستخدم. تحقق من رقم المستخدم او من صلاحياتك')

bot.polling()