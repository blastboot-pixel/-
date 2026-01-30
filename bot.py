import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# التوكن في الكود (كما طلبت)
TOKEN = "8427120813:AAEG9BnLBpoZH9s-oXyNes8yMLmEI4K50LA"
SERETEL_NUMBERS = ["99880820", "17875230"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"🚀 مرحباً {user.first_name}!\n/command1-7")

async def command1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ command1 - تفعيل البوت")

async def command2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 command2 - شحن الرصيد")

async def command3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎁 command3 - كود جائزة")

async def command4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎰 command4 - جاكبوت اليوم")

async def command5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👤 command5 - أيدي: {update.effective_user.id}")

async def command6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎪 command6 - العروض الحالية")

async def command7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👥 command7 - نظام الإحالات")

def main():
    logging.basicConfig(level=logging.INFO)
    
    # الكود القديم الذي كان يعمل
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("command1", command1))
    app.add_handler(CommandHandler("command2", command2))
    app.add_handler(CommandHandler("command3", command3))
    app.add_handler(CommandHandler("command4", command4))
    app.add_handler(CommandHandler("command5", command5))
    app.add_handler(CommandHandler("command6", command6))
    app.add_handler(CommandHandler("command7", command7))
    
    print("🚀 البوت يعمل...")
    app.run_polling()

if __name__ == '__main__':
    main()
