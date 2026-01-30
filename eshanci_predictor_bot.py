import os
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor

# إعدادات السجلة
logging.basicConfig(level=logging.INFO)

# قراءة التوكن من متغيرات البيئة
TOKEN = os.getenv('BOT_TOKEN')
ADMIN = int(os.getenv('ADMIN_ID', 0))

if not TOKEN:
    print("❌ خطأ: ضع متغير BOT_TOKEN في البيئة")
    exit(1)

# تهيئة البوت
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# بيانات التخزين (مؤقت)
users_db = {}
active_subs = {}

# محافظ سيريتل
WALLETS = ["99880820", "17875230"]

# خطط الأسعار
PLANS = {
    "15": {"دقائق": 15, "سعر": "750 ل.س جديدة"},
    "30": {"دقائق": 30, "سعر": "1000 ل.س جديدة"},
    "60": {"دقائق": 60, "سعر": "1500 ل.س جديدة"}
}

# ============ أوامر البوت ============

@dp.message_handler(Command("start"))
async def start_cmd(message: types.Message):
    """بدء البوت"""
    user_id = message.from_user.id
    
    if user_id not in users_db:
        users_db[user_id] = {
            "نقاط": 0,
            "إحالات": 0,
            "كود": f"REF{user_id}",
            "مفعل": False
        }
    
    await message.reply(
        "🔮 بوت تنبؤات مدفع ايشانسي\n\n"
        "📌 الأوامر:\n"
        "• /activate - تفعيل البوت\n"
        "• /charge - شحن رصيد\n"
        "• /gift - أكواد الهدايا\n"
        "• /jackpot - الجاكبوت\n"
        "• /ref - نظام الإحالات\n"
        "• /offers - العروض"
    )

@dp.message_handler(Command("charge"))
async def charge_cmd(message: types.Message):
    """شحن الرصيد"""
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    for time, details in PLANS.items():
        btn = types.InlineKeyboardButton(
            f"⏰ {details['دقائق']} دقيقة - {details['سعر']}",
            callback_data=f"buy_{time}"
        )
        keyboard.add(btn)
    
    await message.reply(
        "💰 اختر خطة الشحن:\n\n"
        "1️⃣ 15 دقيقة - 750 ل.س جديدة\n"
        "2️⃣ 30 دقيقة - 1000 ل.س جديدة\n"
        "3️⃣ 60 دقيقة - 1500 ل.س جديدة\n\n"
        "📱 ارسل المبلغ لأحد الرقمين:\n"
        f"• {WALLETS[0]}\n"
        f"• {WALLETS[1]}",
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data.startswith('buy_'))
async def process_buy(callback: types.CallbackQuery):
    """معالجة الشراء"""
    plan = callback.data.split('_')[1]
    details = PLANS[plan]
    
    await callback.message.edit_text(
        f"✅ اخترت {details['دقائق']} دقيقة\n"
        f"💵 السعر: {details['سعر']}\n\n"
        f"📤 ارسل المبلغ إلى:\n"
        f"• {WALLETS[0]}\n"
        f"أو\n"
        f"• {WALLETS[1]}\n\n"
        "📩 ثم أرسل رمز العملية هنا"
    )
    
    # هنا ننتظر رمز العملية
    # (يمكن إضافة FSMState لمعالجة الخطوة التالية)

@dp.message_handler(Command("activate"))
async def activate_cmd(message: types.Message):
    """تفعيل البوت"""
    user_id = message.from_user.id
    
    if user_id in active_subs and active_subs[user_id] > datetime.now():
        expiry = active_subs[user_id]
        remaining = expiry - datetime.now()
        mins = int(remaining.total_seconds() / 60)
        
        await message.reply(f"✅ البوت مفعل\n⏰ متبقي: {mins} دقيقة")
    else:
        await message.reply("❌ اشحن أولاً باستخدام /charge")

@dp.message_handler(Command("ref"))
async def ref_cmd(message: types.Message):
    """نظام الإحالات"""
    user_id = message.from_user.id
    user = users_db.get(user_id, {})
    
    ref_link = f"https://t.me/{(await bot.me).username}?start=ref_{user_id}"
    
    await message.reply(
        f"👥 نظام الإحالات\n\n"
        f"📊 إحالاتك: {user.get('إحالات', 0)}\n"
        f"⭐ نقاطك: {user.get('نقاط', 0)}\n"
        f"🔗 رابطك: {ref_link}\n\n"
        f"🎯 مكافأة: 50 نقطة لكل إحالة"
    )

@dp.message_handler(Command("gift"))
async def gift_cmd(message: types.Message):
    """أكواد الهدايا"""
    await message.reply(
        "🎁 نظام الأكواد:\n\n"
        "• أدخل كود الهدية للحصول على نقاط\n"
        "• الأكواد تتجدد يومياً\n"
        "• لكل كود 100 نقطة"
    )

@dp.message_handler(Command("jackpot"))
async def jackpot_cmd(message: types.Message):
    """الجاكبوت"""
    await message.reply(
        "🎰 جاكبوت النقاط\n\n"
        "💰 القيمة: 5000 نقطة\n"
        "🎫 التذكرة: 50 نقطة\n"
        "⏰ السحب: يومياً\n\n"
        "🎯 اشتر تذكرة للفوز!"
    )

@dp.message_handler(Command("offers"))
async def offers_cmd(message: types.Message):
    """العروض"""
    await message.reply(
        "🎯 العروض الحالية:\n\n"
        "🔥 عرض خاص:\n"
        "• 60 دقيقة + 30 مجانية\n"
        "• السعر: 1500 ل.س فقط\n\n"
        "💎 عرض الإحالات:\n"
        "• 3 أحالات = 30 دقيقة مجانية"
    )

@dp.message_handler(Command("admin"))
async def admin_cmd(message: types.Message):
    """لوحة التحكم"""
    if message.from_user.id != ADMIN:
        return
    
    await message.reply(
        "🛠 لوحة التحكم:\n\n"
        f"👥 المستخدمين: {len(users_db)}\n"
        f"🔋 المفعلين: {len(active_subs)}\n\n"
        "📊 الإحصائيات جاهزة"
    )

# ============ التشغيل ============

if __name__ == '__main__':
    print("✅ البوت يبدأ التشغيل...")
    executor.start_polling(dp, skip_updates=True)
