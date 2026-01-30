import logging
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== إعدادات البوت ==========
BOT_TOKEN = "8427120813:AAHhejkBSGwQO25ldAnqdQogLVFCnHOAx0w"
SERETEL_NUMBERS = ["99880820", "17875230"]

# ========== الباقات والأسعار ==========
PLANS = {
    "15": {"price": 750, "minutes": 15},
    "30": {"price": 1000, "minutes": 30},
    "60": {"price": 1500, "minutes": 60}
}

# ========== أمر /start ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("💰 شحن الرصيد", callback_data='charge')],
        [InlineKeyboardButton("⚡ تفعيل البوت", callback_data='activate')],
        [InlineKeyboardButton("🎮 تنبؤ اللعبة", callback_data='predict')],
        [InlineKeyboardButton("🎰 جاكبوت اليوم", callback_data='jackpot')],
    ]
    
    welcome_text = f"""
    🚀 **مرحباً {user.first_name} في Blast Boot!**
    
    ✨ *المميزات المتاحة:*
    ✅ تنبؤ لعبة مدفع إيشانسي
    ✅ شحن عبر سيريتل كاش
    ✅ نظام إحالات ربحي
    ✅ جوائز يومية
    
    💰 *باقات الشحن:*
    • 15 دقيقة - 750 ليرة جديدة
    • 30 دقيقة - 1000 ليرة جديدة
    • 60 دقيقة - 1500 ليرة جديدة
    
    📞 *أرقام الدفع:*
    `{SERETEL_NUMBERS[0]}` أو `{SERETEL_NUMBERS[1]}`
    
    اختر من القائمة 👇
    """
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

# ========== قائمة الشحن ==========
async def charge_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🕒 15 دقيقة - 750 ليرة", callback_data='buy_15')],
        [InlineKeyboardButton("🕓 30 دقيقة - 1000 ليرة", callback_data='buy_30')],
        [InlineKeyboardButton("🕔 60 دقيقة - 1500 ليرة", callback_data='buy_60')],
    ]
    
    await update.message.reply_text(
        "💰 **اختر باقة الشحن:**\n\nكل الباقات بالليرة السورية الجديدة",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ========== معالجة الأزرار ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == 'charge':
        keyboard = [
            [InlineKeyboardButton("15 دقيقة - 750 ليرة", callback_data='buy_15')],
            [InlineKeyboardButton("30 دقيقة - 1000 ليرة", callback_data='buy_30')],
            [InlineKeyboardButton("60 دقيقة - 1500 ليرة", callback_data='buy_60')],
        ]
        await query.edit_message_text("💰 اختر الباقة:", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data.startswith('buy_'):
        plan_id = data.split('_')[1]
        plan = PLANS.get(plan_id)
        
        if plan:
            seretel_num = random.choice(SERETEL_NUMBERS)
            text = f"""
            💰 **تفاصيل الدفع**
            
            🔢 الرقم: `{seretel_num}`
            💵 المبلغ: {plan['price']} ليرة جديدة
            ⏰ المدة: {plan['minutes']} دقيقة
            
            📌 *خطوات التنفيذ:*
            1. اذهب لتطبيق سيريتل كاش
            2. أرسل {plan['price']} ليرة للرقم أعلاه
            3. احفظ إيصال الدفع
            4. أرسل الإيصال هنا
            5. سنفعل حسابك خلال 1-5 دقائق
            """
            await query.edit_message_text(text, parse_mode='Markdown')
    
    elif data == 'predict':
        predictions = ["🔴 أحمر", "🟢 أخضر", "🔵 أزرق", "⭐ جائزة خاصة"]
        prediction = random.choices(predictions, weights=[40, 35, 20, 5])[0]
        await query.edit_message_text(f"🎯 **تنبؤ Blast Boot**\n\nالنتيجة المقترحة: {prediction}")
    
    elif data == 'jackpot':
        prizes = ["🎉 50 نقطة", "🎁 100 نقطة", "💰 200 نقطة", "⭐ جائزة خاصة"]
        prize = random.choice(prizes)
        await query.edit_message_text(f"🎰 **جاكبوت اليوم**\n\nمبروك! فزت بـ {prize}")

# ========== أمر العروض ==========
async def offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
    🎪 **العروض الحالية**
    
    🔥 *عرض المبتدئين:*
    • أول شحن: 30 دقيقة مجانية إضافية
    
    👥 *عرض الإحالات:*
    • لكل صديق: 100 نقطة
    • عند شحن صديق: 10% عمولة
    
    🎁 *عرض الجوائز:*
    • 1000 نقطة = 30 دقيقة مجانية
    
    📅 *العرض ينتهي: 30 فبراير 2025*
    """
    await update.message.reply_text(text, parse_mode='Markdown')

# ========== تشغيل البوت ==========
def main():
    # إعداد التسجيل
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    # إنشاء التطبيق
    app = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("charge", charge_menu))
    app.add_handler(CommandHandler("offers", offers))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # تشغيل البوت
    print("🚀 Blast Bot يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
