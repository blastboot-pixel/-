import os
import logging
import random
import hashlib
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# التوكن في الكود (عالي الخطورة)
TOKEN = "8427120813:AAEG9BnLBpoZH9s-oXyNes8yMLmEI4K50LA"
SERETEL_NUMBERS = ["99880820", "17875230"]

# تخزين البيانات
users = {}
payments = {}

# الباقات
PLANS = {
    "15": {"price": 750, "minutes": 15, "old": 75000},
    "30": {"price": 1000, "minutes": 30, "old": 100000},
    "60": {"price": 1500, "minutes": 60, "old": 150000}
}

# ----- الأوامر الرئيسية -----
def start(update, context):
    user = update.message.from_user
    user_id = user.id
    
    # تسجيل المستخدم
    if user_id not in users:
        users[user_id] = {
            "name": user.first_name,
            "balance": 0,
            "points": 100,
            "active": False,
            "active_until": None,
            "referral": f"REF{user_id:06d}",
            "referrals": []
        }
    
    keyboard = [
        [InlineKeyboardButton("⚡ تفعيل البوت", callback_data='activate')],
        [InlineKeyboardButton("💰 شحن الرصيد", callback_data='charge')],
        [InlineKeyboardButton("🎮 تنبؤ اللعبة", callback_data='predict')],
        [InlineKeyboardButton("🎰 جاكبوت اليوم", callback_data='jackpot')],
        [InlineKeyboardButton("🎁 كود جائزة", callback_data='gift')],
        [InlineKeyboardButton("👥 نظام الإحالات", callback_data='referral')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"""
🚀 **مرحباً {user.first_name} في Blast Boot!**

💰 **باقات الشحن:**
• 15 دقيقة - 750 ليرة جديدة (75,000 قديمة)
• 30 دقيقة - 1000 ليرة جديدة (100,000 قديمة)
• 60 دقيقة - 1500 ليرة جديدة (150,000 قديمة)

📱 **أرقام الدفع:**
`{SERETEL_NUMBERS[0]}` أو `{SERETEL_NUMBERS[1]}`

📊 **حسابك:**
⭐ نقاط: {users[user_id]['points']}
💰 رصيد: {users[user_id]['balance']} ل.س
⚡ مفعل: {'✅ نعم' if users[user_id]['active'] else '❌ لا'}
    """
    
    update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)

# command1 - تفعيل البوت
def command1(update, context):
    user_id = update.message.from_user.id
    
    keyboard = [
        [InlineKeyboardButton("🕒 15 دقيقة - 750 ليرة", callback_data='plan_15')],
        [InlineKeyboardButton("🕓 30 دقيقة - 1000 ليرة", callback_data='plan_30')],
        [InlineKeyboardButton("🕔 60 دقيقة - 1500 ليرة", callback_data='plan_60')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"""
⚡ **تفعيل Blast Boot**

📱 **أرقام الدفع:**
• `{SERETEL_NUMBERS[0]}`
• `{SERETEL_NUMBERS[1]}`

⏰ **اختر المدة:**
    """
    
    update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)

# command2 - شحن البوت
def command2(update, context):
    text = f"""
💰 **شحن Blast Boot**

💳 **طريقة الشحن:**
1. اختر الباقة من /command1
2. ادفع عبر سيريتل كاش
3. أرسل رقم العملية هنا
4. يتم التفعيل تلقائياً

📱 **الأرقام:**
`{SERETEL_NUMBERS[0]}` أو `{SERETEL_NUMBERS[1]}`
    """
    
    update.message.reply_text(text, parse_mode='Markdown')

# command3 - كود جائزة
def command3(update, context):
    user_id = update.message.from_user.id
    gift_code = hashlib.md5(f"{user_id}{datetime.now()}".encode()).hexdigest()[:8].upper()
    
    text = f"""
🎁 **كود الجائزة**

🎫 الكود: `{gift_code}`
⭐ القيمة: 50 نقطة
📅 الصلاحية: 7 أيام

🔗 رابط المشاركة:
https://t.me/BlastBootBot?start={gift_code}
    """
    
    update.message.reply_text(text, parse_mode='Markdown')

# command4 - جاكبوت اليوم
def command4(update, context):
    user_id = update.message.from_user.id
    
    # جائزة عشوائية
    prize = random.choice([50, 100, 200, 500])
    users[user_id]['points'] += prize
    
    text = f"""
🎰 **جاكبوت اليوم**

🎊 مبروك! فزت بـ **{prize} نقطة**

⭐ نقاطك الإجمالية: {users[user_id]['points']}

⏰ الجائزة القادمة بعد: {random.randint(1, 60)} دقيقة
    """
    
    update.message.reply_text(text, parse_mode='Markdown')

# command5 - أيدي المستخدم
def command5(update, context):
    user = update.message.from_user
    user_id = user.id
    
    text = f"""
👤 **معلومات حسابك**

🆔 User ID: `{user.id}`
👤 Username: @{user.username if user.username else 'غير محدد'}
📅 الانضمام: {datetime.now().strftime('%Y-%m-%d')}

⭐ النقاط: {users.get(user_id, {}).get('points', 0)}
💰 الرصيد: {users.get(user_id, {}).get('balance', 0)} ل.س
🔗 كود الإحالة: {users.get(user_id, {}).get('referral', 'REF000000')}
    """
    
    update.message.reply_text(text, parse_mode='Markdown')

# command6 - العروض الحالية
def command6(update, context):
    text = """
🎪 **العروض الحالية**

🔥 **عرض المبتدئين:**
• أول شحن: +30 دقيقة مجانية
• هدية: 100 نقطة ترحيب

👥 **نظام الإحالات:**
• لكل صديق: 100 نقطة
• عمولة: 20% من شحنات الأصدقاء
• بونص: 500 نقطة عند 5 إحالات

💰 **عرض الجمعة:**
• خصم 20% على جميع الباقات
• جائزة مزدوجة للإحالات

📅 **ينتهي: 30 فبراير 2025**
    """
    
    update.message.reply_text(text, parse_mode='Markdown')

# command7 - نظام الإحالات
def command7(update, context):
    user_id = update.message.from_user.id
    user_data = users.get(user_id, {})
    ref_code = user_data.get('referral', f"REF{user_id:06d}")
    ref_link = f"https://t.me/BlastBootBot?start=ref{ref_code}"
    
    text = f"""
👥 **نظام الإحالات**

🔗 **رابط دعوتك:**
`{ref_link}`

💰 **معدلات العمولات:**
• الإحالة المباشرة: 20%
• الإحالة غير المباشرة: 10%
• بونص 5 إحالات: 500 نقطة

📊 **إحصائياتك:**
• الإحالات: {len(user_data.get('referrals', []))}
• الأرباح: {len(user_data.get('referrals', [])) * 100} نقطة
    """
    
    update.message.reply_text(text, parse_mode='Markdown')

# معالجة أزرار Inline
def button_handler(update, context):
    query = update.callback_query
    query.answer()
    
    data = query.data
    
    if data == 'activate':
        command1(update, context)
    elif data == 'charge':
        command2(update, context)
    elif data == 'gift':
        command3(update, context)
    elif data == 'jackpot':
        command4(update, context)
    elif data == 'referral':
        command7(update, context)
    elif data.startswith('plan_'):
        plan = data.split('_')[1]
        price = PLANS[plan]['price']
        minutes = PLANS[plan]['minutes']
        old_price = PLANS[plan]['old']
        seretel_num = random.choice(SERETEL_NUMBERS)
        
        text = f"""
💰 **تفاصيل الدفع**

🔢 الرقم: `{seretel_num}`
💵 المبلغ: {price} ليرة جديدة ({old_price} قديمة)
⏰ المدة: {minutes} دقيقة

📌 **خطوات التنفيذ:**
1. اذهب لتطبيق سيريتل كاش
2. أرسل {price} ليرة للرقم أعلاه
3. احفظ رقم العملية
4. أرسل رقم العملية هنا
5. سنفعل حسابك خلال 1-5 دقائق
        """
        
        query.edit_message_text(text, parse_mode='Markdown')
    elif data == 'predict':
        user_id = query.from_user.id
        if users.get(user_id, {}).get('active'):
            # إنشاء تنبؤات
            predictions = []
            for i in range(10):
                num = round(random.uniform(1, 150), 2)
                win = random.choice(['✅', '❌'])
                predictions.append(f"{num} {win}")
            
            text = f"""
🎮 **تنبؤات اللعبة**

{' | '.join(predictions[:5])}
{' | '.join(predictions[5:])}

🎯 **نصيحة:** {'العب الآن! ✅' if '✅' in predictions[-1] else 'انتظر قليلاً ❌'}
            """
            query.edit_message_text(text, parse_mode='Markdown')
        else:
            query.edit_message_text("⚠️ يجب تفعيل البوت أولاً! استخدم /command1")

# معالجة المدفوعات
def handle_payment(update, context):
    user_id = update.message.from_user.id
    transaction_id = update.message.text.strip()
    
    if transaction_id.isdigit() and len(transaction_id) >= 6:
        # تفعيل المستخدم
        users[user_id]['active'] = True
        users[user_id]['active_until'] = datetime.now() + timedelta(hours=1)
        users[user_id]['balance'] += 1000
        users[user_id]['points'] += 100
        
        text = f"""
✅ **تم التفعيل بنجاح!**

🔢 رقم العملية: `{transaction_id}`
💰 الرصيد المضاف: 1000 ليرة
⭐ النقاط المضافة: 100 نقطة
⏰ المدة: 60 دقيقة

🎮 **يمكنك الآن استخدام /predict**
        """
        
        update.message.reply_text(text, parse_mode='Markdown')
    else:
        update.message.reply_text("⚠️ أرسل رقم عملية التحويل فقط (6 أرقام على الأقل)")

# الرئيسي
def main():
    logging.basicConfig(level=logging.INFO)
    
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # إضافة الأوامر
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("command1", command1))
    dp.add_handler(CommandHandler("command2", command2))
    dp.add_handler(CommandHandler("command3", command3))
    dp.add_handler(CommandHandler("command4", command4))
    dp.add_handler(CommandHandler("command5", command5))
    dp.add_handler(CommandHandler("command6", command6))
    dp.add_handler(CommandHandler("command7", command7))
    
    # معالجة الأزرار والرسائل
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_payment))
    
    print("🚀 Blast Boot يعمل الآن...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
