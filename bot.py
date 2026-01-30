import os
import logging
from telegram.ext import Application, CommandHandler

TOKEN = os.getenv("BOT_TOKEN", "8427120813:AAEG9BnLBpoZH9s-oXyNes8yMLmEI4K50LA")

async def start(update, context):
    await update.message.reply_text("🚀 البوت يعمل!")

async def command1(update, context):
    await update.message.reply_text("⚡ تفعيل البوت")

async def command2(update, context):
    await update.message.reply_text("💰 شحن الرصيد")

async def command3(update, context):
    await update.message.reply_text("🎁 كود جائزة")

async def command4(update, context):
    await update.message.reply_text("🎰 جاكبوت اليوم")

async def command5(update, context):
    await update.message.reply_text("👤 أيدي المستخدم")

async def command6(update, context):
    await update.message.reply_text("🎪 العروض الحالية")

async def command7(update, context):
    await update.message.reply_text("👥 نظام الإحالات")

def main():
    logging.basicConfig(level=logging.INFO)
    
    app = Application.builder().token(TOKEN).updater(None).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("command1", command1))
    app.add_handler(CommandHandler("command2", command2))
    app.add_handler(CommandHandler("command3", command3))
    app.add_handler(CommandHandler("command4", command4))
    app.add_handler(CommandHandler("command5", command5))
    app.add_handler(CommandHandler("command6", command6))
    app.add_handler(CommandHandler("command7", command7))
    
    logging.info("🚀 البوت يعمل...")
    app.run_polling()

if __name__ == '__main__':
    main()
