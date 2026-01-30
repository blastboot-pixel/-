import os
import sys
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

# إعدادات السجلة
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# قراءة التوكن من متغيرات Railway
TOKEN = os.getenv('BOT_TOKEN')
ADMIN = int(os.getenv('ADMIN_ID', 0))

if not TOKEN:
    print("❌ خطأ: لم يتم العثور على BOT_TOKEN في متغيرات Railway")
    print("💡 الحل: أضف متغير BOT_TOKEN في Railway Dashboard → Variables")
    sys.exit(1)

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
    user_id = message.from_user.id
    
    if user_id not in users_db:
        users_db[user_id] = {"نقاط": 0, "إحالات": 0, "مفعل": False}
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🔓 تفعيل البوت", "💰 شحن البوت")
    keyboard.add("🎁 كود جائزة", "🎰 الجاكبوت")
    keyboard.add("📊 الإحالات", "🎯 العروض")
    
    await message.reply("🔮 بوت تنبؤات مدفع ايشانسي\nاختر من الأزرار:", reply_markup=keyboard)

@dp.message_handler(lambda m: m.text == "💰 شحن البوت")
async def charge_btn(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    for time, details in PLANS.items():
        btn = types.InlineKeyboardButton(
            f"⏰ {details['دقائق']} دقيقة - {details['سعر']}",
            callback_data=f"buy_{time}"
        )
        keyboard.add(btn)
    
    await message.reply(
        f"💰 اختر خطة:\n\n"
        f"📱 ارسل لأحد الرقمين:\n• {WALLETS[0]}\n• {WALLETS[1]}\n\n"
        f"ثم أرسل رمز العملية",
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data.startswith('buy_'))
async def process_buy(callback: types.CallbackQuery):
    plan = callback.data.split('_')[1]
    details = PLANS[plan]
    
    await callback.message.edit_text(
        f"✅ اخترت {details['دقائق']} دقيقة\n"
        f"💵 {details['سعر']}\n\n"
        f"📤 ارسل المبلغ ثم أرسل رمز العملية"
    )

@dp.message_handler(lambda m: m.text == "🔓 تفعيل البوت")
async def activate_btn(message: types.Message):
    user_id = message.from_user.id
    
    if user_id in active_subs and active_subs[user_id] > datetime.now():
        expiry = active_subs[user_id]
        remaining = expiry - datetime.now()
        mins = int(remaining.total_seconds() / 60)
        await message.reply(f"✅ مفعل\n⏰ متبقي: {mins} دقيقة")
    else:
        await message.reply("❌ اشحن أولاً من زر '💰 شحن البوت'")

@dp.message_handler(lambda m: m.text == "📊 الإحالات")
async def ref_btn(message: types.Message):
    user_id = message.from_user.id
    ref_link = f"https://t.me/{(await bot.me).username}?start=ref_{user_id}"
    await message.reply(f"🔗 رابط الإحالة:\n{ref_link}\n🎯 50 نقطة لكل إحالة")

@dp.message_handler(lambda m: m.text == "🎁 كود جائزة")
async def gift_btn(message: types.Message):
    await message.reply("🎁 أدخل كود الهدية للحصول على 100 نقطة")

@dp.message_handler(lambda m: m.text == "🎰 الجاكبوت")
async def jackpot_btn(message: types.Message):
    await message.reply("🎰 الجاكبوت: 5000 نقطة\n🎫 التذكرة: 50 نقطة\n🏆 السحب يومياً")

@dp.message_handler(lambda m: m.text == "🎯 العروض")
async def offers_btn(message: types.Message):
    await message.reply("🎯 العروض:\n🔥 60+30 دقيقة - 1500 ل.س\n💎 3 أحالات = 30 دقيقة مجانية")

# ============ Startup ============

async def on_startup(_):
    print("=" * 50)
    print("✅ بوت التنبؤات يعمل بنجاح على Railway!")
    print(f"👤 أيدي المشرف: {ADMIN}")
    print(f"🔗 @{(await bot.me).username}")
    print("=" * 50)

# ============ التشغيل ============

if __name__ == '__main__':
    print("🚀 بدء تشغيل البوت...")
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
