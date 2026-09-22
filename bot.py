import os
import telebot
from telebot import types

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8646648924:AAGJsNgW_LdaFUU8K0AJha2GfPON2dmXiEw")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "8520444725"))

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# ---------- بررسی پشتیبانی از style ----------
def make_button(text, callback_data, style=None):
    try:
        if style:
            return types.InlineKeyboardButton(
                text=text,
                callback_data=callback_data,
                style=style
            )
    except TypeError:
        pass
    return types.InlineKeyboardButton(text=text, callback_data=callback_data)


# ---------- متن ها ----------

WELCOME_TEXT = """~ Wᴇʟᴄᴏᴍᴇ ᴛᴏ 𝐕ᴇxᴏʀ
ᴠᴇxᴏʀ ɪꜱ ᴛʜᴇ ʟᴇᴀᴅɪɴɢ ᴘʟᴀᴛꜰᴏʀᴍ ꜰᴏʀ ʀᴀᴛ ꜱɪɢɴᴀᴛᴜʀᴇꜱ, ᴄᴀʀᴅ ꜱᴄᴀɴɴɪɴɢ, ᴀɴᴅ...

- ꜱᴇʟᴇᴄᴛ ʏᴏᴜʀ ᴅᴇꜱɪʀᴇᴅ ꜱᴇᴄᴛɪᴏɴ ꜰʀᴏᴍ ᴛʜᴇ ᴍᴇɴᴜ ʙᴇʟᴏᴡ."""

NO_SUB_TEXT = """ʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ !!
ᴘʟᴇᴀꜱᴇ ꜱᴜʙꜱᴄʀɪʙᴇ ꜰɪʀꜱᴛ."""

PRICES_TEXT = """3 ᴅᴀʏ - 10 ᴛʀᴏɴ

7 ᴅᴀʏ - 15 ᴛʀᴏɴ

14 ᴅᴀʏ - 30 ᴛʀᴏɴ

21 ᴅᴀʏ - 45 ᴛʀᴏɴ

60 ᴅᴀʏ - 60 ᴛʀᴏɴ

ᴘʀɪᴄᴇꜱ ᴀʀᴇ ᴀᴅᴊᴜꜱᴛᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ꜱɪᴛᴜᴀᴛɪᴏɴ ᴀɴᴅ ᴀʀᴇ ɴᴏᴛ ꜱᴏ ꜱᴘᴀᴄᴇ-ꜱᴀᴠɪɴɢ,
ʜɪɢʜ Qᴜᴀʟɪᴛʏ, ʜɪɢʜ ꜱᴇᴄᴜʀɪᴛʏ, ꜰɪʀꜱᴛ ᴘᴏᴡᴇʀ"""

WALLET = "TCSM67WSMgEGM44fV7eb4m7LqV6f23q84Z"

PLANS = {
    "3":  {"days": "3 ᴅᴀʏ",  "price": "10 ᴛʀᴏɴ"},
    "7":  {"days": "7 ᴅᴀʏ",  "price": "15 ᴛʀᴏɴ"},
    "14": {"days": "14 ᴅᴀʏ", "price": "30 ᴛʀᴏɴ"},
    "21": {"days": "21 ᴅᴀʏ", "price": "45 ᴛʀᴏɴ"},
    "60": {"days": "60 ᴅᴀʏ", "price": "60 ᴛʀᴏɴ"},
}


# ---------- کیبورد ها ----------

def main_menu():
    kb = types.InlineKeyboardMarkup()
    kb.row(
        make_button("𝐒𝐜𝐚𝐧", "scan", "primary"),
        make_button("𝐒𝐢𝐠𝐧𝐚𝐭𝐮𝐫𝐞", "signature", "primary"),
    )
    kb.row(make_button("𝐁𝐮𝐲 𝐚 𝐬𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧", "buy", "success"))
    kb.row(make_button("𝐒𝐮𝐩𝐩𝐨𝐫𝐭", "support", "primary"))
    return kb


def plans_menu():
    kb = types.InlineKeyboardMarkup()
    kb.row(
        make_button("3 ᴅᴀʏ", "plan_3", "success"),
        make_button("7 ᴅᴀʏ", "plan_7", "success"),
        make_button("14 ᴅᴀʏ", "plan_14", "success"),
    )
    kb.row(
        make_button("21 ᴅᴀʏ", "plan_21", "success"),
        make_button("60 ᴅᴀʏ", "plan_60", "success"),
    )
    kb.row(make_button("𝐁𝐚𝐜𝐤", "back_main", "primary"))
    return kb


def payment_menu():
    kb = types.InlineKeyboardMarkup()
    kb.row(
        make_button("Pᴀɪᴅ", "paid", "success"),
        make_button("Cᴀɴᴄᴇʟ", "cancel", "danger"),
    )
    return kb


def back_menu(cb="back_main"):
    kb = types.InlineKeyboardMarkup()
    kb.row(make_button("𝐁𝐚𝐜𝐤", cb, "primary"))
    return kb


def admin_order_menu(user_id, plan_key):
    kb = types.InlineKeyboardMarkup()
    kb.row(
        make_button("تایید", f"admin_ok_{user_id}_{plan_key}", "success"),
        make_button("رد", f"admin_no_{user_id}_{plan_key}", "danger"),
    )
    return kb


# ---------- دستورات ----------

@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=main_menu())


# ---------- Callback ها ----------

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    data = call.data
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    # --- اسکن و ساینچر ---
    if data in ("scan", "signature"):
        try:
            bot.edit_message_text(
                NO_SUB_TEXT, chat_id, msg_id,
                reply_markup=back_menu("back_main")
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id)

    # --- ساپورت ---
    elif data == "support":
        try:
            bot.edit_message_text(
                "𝐒𝐮𝐩𝐩𝐨𝐫𝐭 : @VexorSupport",
                chat_id, msg_id,
                reply_markup=back_menu("back_main")
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id)

    # --- خرید اشتراک ---
    elif data == "buy":
        try:
            bot.edit_message_text(
                PRICES_TEXT, chat_id, msg_id,
                reply_markup=plans_menu()
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id)

    # --- انتخاب پلن ---
    elif data.startswith("plan_"):
        plan_key = data.split("_")[1]
        plan = PLANS.get(plan_key)
        if not plan:
            bot.answer_callback_query(call.id, "پلن نامعتبر")
            return

        user_data[chat_id] = {"plan": plan_key}

        text = (
            f"~ ʏᴏᴜʀ ᴘʟᴀɴ : {plan['days']}\n"
            f"ᴘʀɪᴄᴇ : {plan['price']}\n\n"
            f"ᴡᴀʟʟᴇᴛ : `{WALLET}`\n\n"
            f"اول واریزی رو انجام بدید و بعد بزنید روی پرداخت ، "
            f"تراکنش شما در لحظه چک و خرید شما تایید میشه."
        )

        try:
            bot.edit_message_text(
                text, chat_id, msg_id,
                reply_markup=payment_menu(),
                parse_mode="Markdown"
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id)

    # --- پرداخت (Paid) ---
    elif data == "paid":
        info = user_data.get(chat_id)
        if not info:
            bot.answer_callback_query(call.id, "اطلاعات یافت نشد.")
            return

        plan_key = info.get("plan")
        plan = PLANS.get(plan_key)

        username = call.from_user.username or "بدون یوزرنیم"
        full_name = call.from_user.full_name or "-"

        admin_text = (
            f"سفارش جدید\n\n"
            f"نام : {full_name}\n"
            f"یوزرنیم : @{username}\n"
            f"ایدی عددی : {chat_id}\n\n"
            f"پلن : {plan['days']}\n"
            f"قیمت : {plan['price']}\n"
        )

        try:
            bot.send_message(
                ADMIN_ID, admin_text,
                reply_markup=admin_order_menu(chat_id, plan_key)
            )
        except Exception as e:
            print("Admin send error:", e)

        try:
            bot.edit_message_text(
                "سفارش شما برای بررسی به ادمین ارسال شد.\n"
                "پس از تایید پرداخت، اشتراک شما فعال خواهد شد.",
                chat_id, msg_id,
                reply_markup=back_menu("back_main")
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id, "ارسال شد")

    # --- کنسل ---
    elif data == "cancel":
        try:
            bot.edit_message_text(
                WELCOME_TEXT, chat_id, msg_id,
                reply_markup=main_menu()
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id, "لغو شد")

    # --- بازگشت به منوی اصلی ---
    elif data == "back_main":
        try:
            bot.edit_message_text(
                WELCOME_TEXT, chat_id, msg_id,
                reply_markup=main_menu()
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id)

    # --- بازگشت به لیست پلن ها ---
    elif data == "back_plans":
        try:
            bot.edit_message_text(
                PRICES_TEXT, chat_id, msg_id,
                reply_markup=plans_menu()
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id)

    # --- تایید ادمین ---
    elif data.startswith("admin_ok_"):
        rest = data[len("admin_ok_"):]
        try:
            target_id_str, plan_key = rest.rsplit("_", 1)
            target_id = int(target_id_str)
        except Exception:
            bot.answer_callback_query(call.id, "داده نامعتبر")
            return

        plan = PLANS.get(plan_key)
        if not plan:
            bot.answer_callback_query(call.id, "پلن نامعتبر")
            return

        try:
            bot.send_message(
                target_id,
                f"سفارش شما تایید شد.\n"
                f"پلن : {plan['days']}\n"
                f"اشتراک شما فعال شد."
            )
        except Exception as e:
            print("User notify error:", e)

        try:
            bot.edit_message_text(
                call.message.text + "\n\nتایید شد",
                call.message.chat.id,
                call.message.message_id
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id, "تایید شد")

    # --- رد ادمین ---
    elif data.startswith("admin_no_"):
        rest = data[len("admin_no_"):]
        try:
            target_id_str, plan_key = rest.rsplit("_", 1)
            target_id = int(target_id_str)
        except Exception:
            bot.answer_callback_query(call.id, "داده نامعتبر")
            return

        try:
            bot.send_message(
                target_id,
                "سفارش شما به علت عدم‌ پرداخت موجودی لغو شد"
            )
        except Exception as e:
            print("User notify error:", e)

        try:
            bot.edit_message_text(
                call.message.text + "\n\nرد شد",
                call.message.chat.id,
                call.message.message_id
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id, "رد شد")


if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()