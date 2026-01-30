import os
import logging
from datetime import datetime, timedelta
import asyncio
import random
import time

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode

# ⚙️ إعدادات البوت - ضع معلوماتك هنا
BOT_TOKEN = "8427120813:AAF7k0k0i3Ucb8zcaHBeB13IehKbqQmWecU"
ADMIN_ID = 5552288292
SYRIA_TEL_CASH_NUMBERS = ["/99880820/", "/17875230/"]
REFERRAL_BONUS = 5000

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# قاعدة بيانات بسيطة (مؤقتة)
class Database:
    def __init__(self):
        self.users = {}
        self.transactions = {}
        self.active_codes = {"BOT100": True, "NEWYEAR2024": True}
    
    def get_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = {
                'id': user_id,
                'balance': 0,
                'points': 100,  # نقاط مجانية عند البدء
                'subscription_end': None,
                'referral_code': str(user_id)[-6:],
                'referred_by': None,
                'total_earned': 0,
                'jackpot_tickets': 0
            }
        return self.users[user_id]
    
    def add_transaction(self, user_id, amount, receipt_code):
        tx_id = f"TX{user_id}{int(time.time())}"
        self.transactions[tx_id] = {
            'user_id': user_id,
            'amount': amount,
            'receipt_code': receipt_code,
            'status': 'verified',
            'timestamp': datetime.now()
        }
        return tx_id

db = Database()

# باقات الاشتراك
SUBSCRIPTION_PLANS = {
    "15min": {"duration": 15, "price": 750, "name": "15 دقيقة", "points": 150},
    "30min": {"duration": 30, "price": 1000, "name": "30 دقيقة", "points": 300},
    "60min": {"duration": 60, "price": 1500, "name": "60 دقيقة", "points": 600}
}

# توفير الاستهلاك على Railway
async def energy_saver():
    """توفير الطاقة للبقاء ضمن الحد المجاني"""
    while True:
        await asyncio.sleep(600)  # 10 دقائق
        logger.info("✅ البوت يعمل بكفاءة على Railway المجاني")

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    # نظام الإحالات
    if context.args:
        referral_code = context.args[0]
        if referral_code != user_data['referral_code']:
            user_data['referred_by'] = referral_code
            # مكافأة للمحيل
            for uid, u in db.users.items():
                if u['referral_code'] == referral_code:
                    u['balance'] += REFERRAL_BONUS
                    break
    
    welcome_text = f"""
🚀 **مرحباً {user.first_name}!**
🤖 **بوت تنبؤ نتائج لعبة مدفع إيشانسي**

💰 **رصيدك:** {user_data['balance']:,} ل.س جديدة
⭐ **نقاطك:** {user_data['points']}
🎫 **تذاكر جاكبوت:** {user_data['jackpot_tickets']}

📋 **الأوامر الرئيسية:**
/charge - شحن الرصيد (سيريتل كاش)
/activate - تفعيل الاشتراك
/gift - أكواد الهدايا
/jackpot - الجاكبوت
/referral - نظام الإحالات
/offers - العروض الحالية
/help - المساعدة

⚠️ **قواعد السلامة:**
• لا مشاركة روابط البوت
• لا لقطات شاشة داخل البوت
• السحب اليومي محدود بـ 100 دولار
    """
    
    keyboard = [
        [InlineKeyboardButton("💳 شحن الرصيد", callback_data="charge_btn"),
         InlineKeyboardButton("🎯 تفعيل اشتراك", callback_data="activate_btn")],
        [InlineKeyboardButton("🎁 أكواد الهدايا", callback_data="gift_btn"),
         InlineKeyboardButton("💰 الجاكبوت", callback_data="jackpot_btn")],
        [InlineKeyboardButton("👥 نظام الإحالات", callback_data="referral_btn"),
         InlineKeyboardButton("🔥 العروض", callback_data="offers_btn")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

# أمر /charge
async def charge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
💳 **شحن الرصيد عبر سيريتل كاش**

📱 **أرقام التحويل:**
`{SYRIA_TEL_CASH_NUMBERS[0]}`
`{SYRIA_TEL_CASH_NUMBERS[1]}`

📋 **خطوات الشحن:**
1. حول المبلغ لأي رقم أعلاه
2. احفظ رمز العملية (Receipt Code)
3. أرسل الرمز بهذا الشكل:
