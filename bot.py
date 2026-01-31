import os
from flask import Flask, request, abort
import telebot

TOKEN = os.environ.get('BOT_TOKEN') or "8427120813:AAF7k0k0i3Ucb8zcaHBeB13IehKbqQmWecU"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ البوت شغال!")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "قائمة الأوامر:\n/start - بدء التشغيل\n/help - المساعدة")

@app.route('/')
def index():
    return "🚀 خادم ويب هوك جاهز لاستقبال طلبات Telegram."

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '', 200
    else:
        abort(403)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
