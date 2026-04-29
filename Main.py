import random
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import os
TOKEN = os.getenv("TOKEN")
word_bank = {}

async def collect_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    if not text:
        return

    if chat_id not in word_bank:
        word_bank[chat_id] = set()

    for w in text.split():
        word_bank[chat_id].add(w)


async def play_mnp5lyrics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        return

    if random.random() < 0.95:
        await update.message.reply_text("no")
        return

    lines = [
        "Oh my god I need you to be honest I need you to be honest I need you to be honest I need you to be honest I need you to be honest with me",
        "and I love you Then I love you and I need you to be honest and you",
        "I need you to avoid me and my royal baby, you can To put me in my place and then come home and do it just after and the right",
        "name is just and then the right name is just hours and then I can be Jesus and then you can become Jesus in the right place and then you come back to avoid"
    ]

    for line in lines:
        await update.message.reply_text(line)
        await asyncio.sleep(1)


async def send_loop(app):
    while True:
        await asyncio.sleep(1800)

        for chat_id, words in word_bank.items():
            if len(words) < 5:
                continue

            chance = random.random()

            if chance < 0.05:
                sentence = "supercalifragilisticexpialidocious"
            elif chance < 0.10:
                sentence = "hyperbolic elephants"
            else:
                count = random.randint(5, 15)
                chosen = random.sample(list(words), min(len(words), count))
                sentence = " ".join(chosen)

            await app.bot.send_message(chat_id=chat_id, text=sentence)


async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, collect_words))
    app.add_handler(CommandHandler("playmnp5lyrics", play_mnp5lyrics))

    print("Bot is running...")

    asyncio.create_task(send_loop(app))

    await app.run_polling()


import nest_asyncio
nest_asyncio.apply()

asyncio.get_event_loop().run_until_complete(main())
