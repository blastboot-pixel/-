import logging
from telegram.ext import Updater, CommandHandler

# التوكن هنا (سأضيفه لاحقاً)
TOKEN = "8427120813:AAEG9BnLBpoZH9s-oXyNes8yMLmEI4K50LA"

def start(update, context):
    update.message.reply_text("🚀 البوت يعمل!\n\n/command1-7")

def command1(update, context):
    update.message.reply_text("⚡ تفعيل البوت\n📱 سيريتل: 99880820\n💵 750 ليرة = 15 دقيقة")

def command2(update, context):
    update.message.reply_text("💰 شحن الرصيد\nأرسل رقم العملية بعد الدفع")

def command3(update, context):
    update.message.reply_text("🎁 كود الجائزة: GIFT123")

def command4(update, context):
    update.message.reply_text("🎰 جاكبوت اليوم\n🎊 100 نقطة!")

def command5(update, context):
    update.message.reply_text(f"👤 أيدي: {update.message.from_user.id}")

def command6(update, context):
    update.message.reply_text("🎪 العروض\nخصم 20%")

def command7(update, context):
    update.message.reply_text("👥 نظام الإحالات\nعمولة 20%")

def main():
    logging.basicConfig(level=logging.INFO)
    
    updater = Updater(TOKEN, use_context=True)
    
    # إضافة جميع الأوامر
    commands = [
        ("start", start), ("command1", command1), ("command2", command2),
        ("command3", command3), ("command4", command4), ("command5", command5),
        ("command6", command6), ("command7", command7)
    ]
    
    for cmd, func in commands:
        updater.dispatcher.add_handler(CommandHandler(cmd, func))
    
    print("✅ البوت يعمل...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
