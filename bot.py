import os
import logging
from datetime import datetime, timedelta
import asyncio
import random

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode

# ⚙️ إعدادات البوت
BOT_TOKEN = "8427120813:AAF7k0k0i3Ucb8zcaHBeB13IehKbqQmWecU"
ADMIN_ID = 5552288292
SYRIA_TEL_CASH_NUMBERS = ["/99880820/", "/17875230/"]
REFERRAL_BONUS = 5000

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.users = {}
        self.transactions = {}
    
    def get_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = {
                'id': user_id,
                'balance': 0,
                'points': 100,
                'subscription_end': None,
                'referral_code': str(user_id)[-6:],
                'referred_by': None,
                'jackpot_tickets': 0
            }
        return self.users[user_id]

db = Database()

SUBSCRIPTION_PLANS = {
    "15min": {"duration": 15, "price": 750, "name": "15 دقيقة", "points": 150},
    "30min": {"duration": 30, "price": 1000, "name": "30 دقيقة", "points": 300},
    "60min": {"duration": 60, "price": 1500, "name": "60 دقيقة", "points": 600}
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    welcome_text = f"""
🚀 **مرحباً {user.first_name}!**
🤖 **بوت تنبؤ نتائج لعبة مدفع إيشانسي**

💰 **رصيدك:** {user_data['balance']:,} ل.س
⭐ **نقاطك:** {user_data['points']}

📋 **الأوامر:**
/charge - شحن الرصيد
/activate - تفعيل الاشتراك
/gift - أكواد الهدايا
/jackpot - الجاكبوت
/referral - الإحالات
/offers - العروض
/help - المساعدة
    """
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)

async def charge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
💳 **شحن الرصيد عبر سيريتل كاش**

📱 **أرقام التحويل:**
`{SYRIA_TEL_CASH_NUMBERS[0]}`
`{SYRIA_TEL_CASH_NUMBERS[1]}`

📋 **كيفية الشحن:**
1. حول المبلغ لأي رقم أعلاه
2. احفظ رمز العملية
3. أرسل لي: `رمز_التحويل المبلغ`

📝 **مثال:** `ABC123 1000`
💰 **الحد الأدنى:** 100 ليرة
    """
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    if ' ' in text:
        parts = text.split(' ')
        if len(parts) == 2:
            receipt_code = parts[0]
            try:
                amount = int(parts[1])
                if amount >= 100:
                    user_data = db.get_user(user_id)
                    user_data['balance'] += amount
                    
                    await update.message.reply_text(
                        f"✅ **تم استلام {amount:,} ليرة**\n"
                        f"💰 رصيدك الجديد: {user_data['balance']:,} ليرة",
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    await update.message.reply_text("❌ الحد الأدنى 100 ليرة")
            except:
                await update.message.reply_text("❌ المبلغ يجب أن يكون رقماً")
        else:
            await update.message.reply_text("❌ استخدم: `رمز_التحويل المبلغ`")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("charge", charge_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_payment))
    
    print("🤖 بوت بلاست يعمل على Render.com المجاني")
    application.run_polling()

# ⚠️ هذا السطر مهم لـ Render.com فقط
if __name__ == '__main__':
    main()
