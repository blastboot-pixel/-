import os
import logging
import random
import hashlib
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# إعدادات
TOKEN = os.getenv("BOT_TOKEN", "8427120813:AAEG9BnLBpoZH9s-oXyNes8yMLmEI4K50LA")
SERETEL_NUMBERS = ["99880820", "17875230"]

# تخزين
users_db = {}

def get_user_data(user_id):
    if user_id not in users_db:
        users_db[user_id] = {"points": 100, "is_active": False, "balance": 0}
    return users_db[user_id]

# الأوامر
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = get_user_data(user.id)
    
    keyboard = [
        [InlineKeyboardButton("⚡ تفعيل /command1", callback_data='cmd1')],
        [InlineKeyboardButton("💰 شحن /command2", callback_data='cmd2')],
        [InlineKeyboardButton("🎁 كود /command3", callback_data='cmd3')],
        [InlineKeyboardButton("🎰 جاكبوت /command4", callback_data='cmd4')],
        [InlineKeyboardButton("👤 أيدي /command5", callback_data='cmd5')],
        [InlineKeyboardButton("🎪 عروض /command6", callback_data='cmd6')],
        [InlineKeyboardButton("👥 إحالات /command7", callback_data='cmd7')],
    ]
    
    text = f"🚀 مرحباً {user.first_name}\n\n💰 رصيدك: {user_data['balance']} ل.س\n⭐ نقاط: {user_data['points']}\n⚡ مفعل: {'✅' if user_data['is_active'] else '❌'}"
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def command1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"🔧 تفعيل البوت\n\n📱 أرقام الدفع:\n• `{SERETEL_NUMBERS[0]}`\n• `{SERETEL_NUMBERS[1]}`\n\n💵 الأسعار:\n• 15 دقيقة: 750 ليرة\n• 30 دقيقة: 1000 ليرة\n• 60 دقيقة: 1500 ليرة"
    await update.message.reply_text(text, parse_mode='Markdown')

async def command2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "💰 شحن الرصيد\n\n1. اختر المدة من /command1\n2. ادفع لسيريتل كاش\n3. أرسل رقم العملية\n4. يتم التفعيل تلقائياً"
    await update.message.reply_text(text)

async def command3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = hashlib.md5(str(update.effective_user.id).encode()).hexdigest()[:8].upper()
    text = f"🎁 كود الجائزة: `{code}`\n⭐ القيمة: 50 نقطة\n📅 صلاحية: 7 أيام"
    await update.message.reply_text(text, parse_mode='Markdown')

async def command4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prize = random.choice([50, 100, 200, 500])
    user_data = get_user_data(update.effective_user.id)
    user_data["points"] += prize
    text = f"🎰 جاكبوت اليوم\n\n🎊 فزت بـ {prize} نقطة!\n⭐ نقاطك: {user_data['points']}"
    await update.message.reply_text(text)

async def command5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = get_user_data(user.id)
    text = f"👤 حسابك\n\n🆔 ID: `{user.id}`\n⭐ نقاط: {user_data['points']}\n💰 رصيد: {user_data['balance']}\n🔗 كود إحالة: REF{user.id:06d}"
    await update.message.reply_text(text, parse_mode='Markdown')

async def command6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🎪 العروض الحالية\n\n• أول شحن: +30 دقيقة\n• لكل إحالة: 100 نقطة\n• 5 إحالات: 500 نقطة\n• عرض الجمعة: خصم 20%"
    await update.message.reply_text(text)

async def command7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ref_link = f"https://t.me/BlastBootBot?start=ref{user.id}"
    text = f"👥 نظام الإحالات\n\n🔗 رابطك:\n`{ref_link}`\n\n💰 عمولة 20% من شحنات الأصدقاء"
    await update.message.reply_text(text, parse_mode='Markdown')

async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = get_user_data(update.effective_user.id)
    user_data["is_active"] = True
    user_data["balance"] += 1000
    user_data["points"] += 100
    text = f"✅ تم التفعيل!\n\n💰 +1000 ليرة\n⭐ +100 نقطة\n🎮 يمكنك استخدام /predict الآن"
    await update.message.reply_text(text)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    commands = {
        'cmd1': command1, 'cmd2': command2, 'cmd3': command3,
        'cmd4': command4, 'cmd5': command5, 'cmd6': command6,
        'cmd7': command7
    }
    
    if data in commands:
        await commands[data](update, context)

def main():
    logging.basicConfig(level=logging.INFO)
    
    application = Application.builder().token(TOKEN).build()
    
    # الأوامر
    commands = [
        ("start", start), ("command1", command1), ("command2", command2),
        ("command3", command3), ("command4", command4), ("command5", command5),
        ("command6", command6), ("command7", command7)
    ]
    
    for cmd, func in commands:
        application.add_handler(CommandHandler(cmd, func))
    
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_payment))
    
    logging.info("🚀 البوت يعمل...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
