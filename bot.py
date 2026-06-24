import telebot
import requests
import io

# =========================
# CONFIG
# =========================

BOT_TOKEN = "8743115028:AAGWYA2yp_vtNRKA14A9t53_Z5uAoapN-8g"

TARGET_URL = "https://khorasantelecom.co/transactions/receipts?tab=all"

bot = telebot.TeleBot(BOT_TOKEN)


# =========================
# گرفتن اسکرین‌شات از API
# =========================

def get_screenshot(url: str):

    api = "https://image.thum.io/get/png/fullpage/" + url

    response = requests.get(api, timeout=60)

    if response.status_code == 200:
        return io.BytesIO(response.content)

    return None


# =========================
# Telegram Bot
# =========================

@bot.message_handler(commands=["start"])
def start(message):

    chat_id = message.chat.id

    bot.send_message(
        chat_id,
        "📸 در حال گرفتن اسکرین‌شات از سایت..."
    )

    try:

        image = get_screenshot(TARGET_URL)

        if image:

            bot.send_photo(
                chat_id,
                photo=image,
                caption="✅ اسکرین‌شات آماده شد"
            )

        else:

            bot.send_message(
                chat_id,
                "❌ خطا در گرفتن تصویر از سایت"
            )

    except Exception as e:

        bot.send_message(
            chat_id,
            f"❌ خطا:\n{e}"
        )


@bot.message_handler(func=lambda m: True)
def fallback(message):

    bot.reply_to(
        message,
        "برای گرفتن عکس سایت دستور /start را بفرست"
    )


# =========================
# RUN
# =========================

print("Bot is running...")

bot.infinity_polling()