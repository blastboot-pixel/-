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
    
    def add_transaction(self, user_id, amount, receipt_code):
        tx_id = f"{user_id}_{int(datetime.now().timestamp())}"
        self.transactions[tx_id] = {
            'user_id': user_id,
            'amount': amount,
            'receipt_code': receipt_code,
            'status': 'pending',
            'timestamp': datetime.now()
        }
        return tx_id

db = Database()

SUBSCRIPTION_PLANS = {
    "15min": {"duration": 15, "price": 750, "name": "15 دقيقة", "points": 150},
    "30min": {"duration": 30, "price": 1000, "name": "30 دقيقة", "points": 300},
    "60min": {"duration": 60, "price": 1500, "name": "60 دقيقة", "points": 600}
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    if context.args:
        referral_code = context.args[0]
        if referral_code != user_data['referral_code']:
            user_data['referred_by'] = referral_code
    
    welcome_text = f"""
🚀 **مرحباً {user.first_name}!**
🤖 **بوت تنبؤ نتائج لعبة مدفع إيشانسي**

💰 **رصيدك:** {user_data['balance']:,} ل.س
⭐ **نقاطك:** {user_data['points']}
🎫 **تذاكر جاكبوت:** {user_data['jackpot_tickets']}

📋 **الأوامر:**
/charge - شحن الرصيد
/activate - تفعيل الاشتراك
/gift - أكواد الهدايا
/jackpot - الجاكبوت
/referral - الإحالات
/offers - العروض
/help - المساعدة
    """
    
    keyboard = [
        [InlineKeyboardButton("💳 شحن الرصيد", callback_data="charge")],
        [InlineKeyboardButton("🎯 تفعيل اشتراك", callback_data="activate")],
        [InlineKeyboardButton("🎁 أكواد هدايا", callback_data="gift")],
        [InlineKeyboardButton("💰 الجاكبوت", callback_data="jackpot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def charge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
💳 **شحن الرصيد عبر سيريتل كاش**

📱 **أرقام التحويل:**
`{SYRIA_TEL_CASH_NUMBERS[0]}`
`{SYRIA_TEL_CASH_NUMBERS[1]}`

📋 **كيفية الشحن:**
1. حول المبلغ لأي رقم أعلاه
2. احفظ رمز العملية (مثال: ABC123)
3. أرسل لي: `رمز_التحويل المبلغ`

📝 **مثال:** `ABC123 1000`
💵 **مثال:** `XYZ789 1500`

💰 **الحد الأدنى:** 100 ليرة
    """
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

# ✅ الكود المصحح لمعالجة التحويلات
async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    # تقسيم النص إلى رمز التحويل والمبلغ
    if ' ' in text:
        parts = text.split(' ')
        if len(parts) == 2:
            receipt_code = parts[0].strip()
            try:
                amount = int(parts[1].strip())
                
                # التحقق من المبلغ
                if amount < 100:
                    await update.message.reply_text("❌ الحد الأدنى للشحن هو 100 ليرة")
                    return
                
                # تسجيل العملية
                user_data = db.get_user(user_id)
                tx_id = f"TX{random.randint(10000, 99999)}"
                
                # إضافة الرصيد
                user_data['balance'] += amount
                
                await update.message.reply_text(
                    f"✅ **تم استلام طلب الشحن**\n\n"
                    f"📋 **رمز التحويل:** {receipt_code}\n"
                    f"💵 **المبلغ:** {amount:,} ليرة\n"
                    f"💰 **رصيدك الجديد:** {user_data['balance']:,} ليرة\n\n"
                    f"⏳ **جاري التحقق...**",
                    parse_mode=ParseMode.MARKDOWN
                )
                
                # محاكاة التحقق
                await asyncio.sleep(3)
                await update.message.reply_text("✅ **تم التحقق من الدفع بنجاح!**")
                
            except ValueError:
                await update.message.reply_text("❌ المبلغ يجب أن يكون رقماً")
        else:
            await update.message.reply_text("❌ استخدم التنسيق: `رمز_التحويل المبلغ`")
    else:
        await update.message.reply_text("❌ استخدم التنسيق: `رمز_التحويل المبلغ`")

async def activate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🎯 **باقات الاشتراك:**

1️⃣ **15 دقيقة** - 750 ليرة
2️⃣ **30 دقيقة** - 1,000 ليرة  
3️⃣ **60 دقيقة** - 1,500 ليرة

📌 **للتفعيل:** أرسل رقم الباقة (1، 2، أو 3)
    """
    await update.message.reply_text(text)

async def handle_activation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    plans = {"1": "15min", "2": "30min", "3": "60min"}
    
    if text in plans:
        plan_id = plans[text]
        plan = SUBSCRIPTION_PLANS[plan_id]
        user_data = db.get_user(user_id)
        
        if user_data['balance'] >= plan['price']:
            user_data['balance'] -= plan['price']
            user_data['points'] += plan['points']
            
            if user_data['subscription_end'] and user_data['subscription_end'] > datetime.now():
                user_data['subscription_end'] += timedelta(minutes=plan['duration'])
            else:
                user_data['subscription_end'] = datetime.now() + timedelta(minutes=plan['duration'])
            
            await update.message.reply_text(
                f"✅ **تم التفعيل!**\n"
                f"⏰ المدة: {plan['name']}\n"
                f"💰 المبلغ: {plan['price']:,} ليرة\n"
                f"⭐ النقاط: +{plan['points']}\n"
                f"⏳ ينتهي: {user_data['subscription_end'].strftime('%H:%M')}"
            )
        else:
            await update.message.reply_text(
                f"❌ **رصيد غير كافي**\n"
                f"💵 المطلوب: {plan['price']:,} ليرة\n"
                f"💰 لديك: {user_data['balance']:,} ليرة"
            )
    else:
        await update.message.reply_text("❌ أرسل 1، 2، أو 3 فقط")

async def gift_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🎁 **أكواد الهدايا:**

الكود: `BOT100`
الجائزة: 100 نقطة

استخدم: `/gift BOT100`
    """
    await update.message.reply_text(text)

async def jackpot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
💰 **جاكبوت البلاست**

الجائزة: 100,000 ليرة

🎫 **اشترك الآن للمشاركة**
    """
    await update.message.reply_text(text)

async def referral_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = db.get_user(user_id)
    
    text = f"""
👥 **نظام الإحالات**

💰 **مكافأة:** {REFERRAL_BONUS:,} ليرة لكل صديق

🔗 **رابطك:** 
https://t.me/بوتك?start={user_data['referral_code']}
    """
    await update.message.reply_text(text)

async def offers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📢 **العروض:**

🔥 **خصم 20% على أول شحن**
🎯 **كود:** FIRST20
    """
    await update.message.reply_text(text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🆘 **المساعدة:**

📞 الدعم: @support
📢 القناة: @channel
    """
    await update.message.reply_text(text)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "charge":
        await charge_command(update, context)
    elif query.data == "activate":
        await activate_command(update, context)
    elif query.data == "gift":
        await gift_command(update, context)
    elif query.data == "jackpot":
        await jackpot_command(update, context)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("charge", charge_command))
    application.add_handler(CommandHandler("activate", activate_command))
    application.add_handler(CommandHandler("gift", gift_command))
    application.add_handler(CommandHandler("jackpot", jackpot_command))
    application.add_handler(CommandHandler("referral", referral_command))
    application.add_handler(CommandHandler("offers", offers_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # ✅ معالجة التحويلات - الكود المصحح
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_payment
    ))
    
    # معالجة اختيار الباقات
    application.add_handler(MessageHandler(
        filters.Regex(r'^[123]$'),
        handle_activation
    ))
    
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
