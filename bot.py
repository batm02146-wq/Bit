import os
import time
import threading
import telebot
from telebot import types

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8646648924:AAGJsNgW_LdaFUU8K0AJha2GfPON2dmXiEw")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "8520444725"))

bot = telebot.TeleBot(BOT_TOKEN)

# ذخیره اطلاعات کاربران
user_data = {}          # {chat_id: {"plan": ..., "state": ...}}
subscribed_users = set()  # کاربرانی که اشتراکشون تایید شده
waiting_support = set()   # کاربرانی که منتظر نوشتن پیام پشتیبانی هستن
waiting_card = set()      # کاربرانی که منتظر ارسال شماره کارت هستن


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


# ---------- متن ها (بولد با HTML) ----------

WELCOME_TEXT = """<b>~ Wᴇʟᴄᴏᴍᴇ ᴛᴏ 𝐕ᴇxᴏʀ</b>
<b>ᴠᴇxᴏʀ ɪꜱ ᴛʜᴇ ʟᴇᴀᴅɪɴɢ ᴘʟᴀᴛꜰᴏʀᴍ ꜰᴏʀ ʀᴀᴛ ꜱɪɢɴᴀᴛᴜʀᴇꜱ, ᴄᴀʀᴅ ꜱᴄᴀɴɴɪɴɢ, ᴀɴᴅ...</b>

<b>- ꜱᴇʟᴇᴄᴛ ʏᴏᴜʀ ᴅᴇꜱɪʀᴇᴅ ꜱᴇᴄᴛɪᴏɴ ꜰʀᴏᴍ ᴛʜᴇ ᴍᴇɴᴜ ʙᴇʟᴏᴡ.</b>"""

NO_SUB_TEXT = """<b>ʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ !!</b>
<b>ᴘʟᴇᴀꜱᴇ ꜱᴜʙꜱᴄʀɪʙᴇ ꜰɪʀꜱᴛ.</b>"""

SIGNATURE_REPAIR_TEXT = "<b>این بخش درحال تعمیرات میباشد</b>"

PRICES_TEXT = """<b>3 ᴅᴀʏ - 10 ᴛʀᴏɴ</b>

<b>7 ᴅᴀʏ - 15 ᴛʀᴏɴ</b>

<b>14 ᴅᴀʏ - 30 ᴛʀᴏɴ</b>

<b>21 ᴅᴀʏ - 45 ᴛʀᴏɴ</b>

<b>60 ᴅᴀʏ - 60 ᴛʀᴏɴ</b>

<b>ᴘʀɪᴄᴇꜱ ᴀʀᴇ ᴀᴅᴊᴜꜱᴛᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ꜱɪᴛᴜᴀᴛɪᴏɴ ᴀɴᴅ ᴀʀᴇ ɴᴏᴛ ꜱᴏ ꜱᴘᴀᴄᴇ-ꜱᴀᴠɪɴɢ,
ʜɪɢʜ Qᴜᴀʟɪᴛʏ, ʜɪɢʜ ꜱᴇᴄᴜʀɪᴛʏ, ꜰɪʀꜱᴛ ᴘᴏᴡᴇʀ</b>"""

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


def admin_support_menu(user_id):
    kb = types.InlineKeyboardMarkup()
    kb.row(
        make_button("پاسخ", f"admin_reply_{user_id}", "primary"),
    )
    return kb


# ---------- دستورات ----------

@bot.message_handler(commands=['start'])
def cmd_start(message):
    waiting_support.discard(message.chat.id)
    waiting_card.discard(message.chat.id)
    bot.send_message(
        message.chat.id,
        WELCOME_TEXT,
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


# ---------- هندل پیام های متنی (کارت و پشتیبانی) ----------

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.strip()

    # --- حالت انتظار برای شماره کارت ---
    if chat_id in waiting_card:
        waiting_card.discard(chat_id)

        # پیام "درحال اسکن"
        bot.send_message(
            chat_id,
            "<b>درحال اسکن منتظر بمانید</b>",
            parse_mode="HTML"
        )

        # تایمر ۵ دقیقه و ۳۰ ثانیه بعد پیام پیدا نشد
        def scan_timeout():
            time.sleep(330)  # 5.5 دقیقه
            try:
                bot.send_message(
                    chat_id,
                    "<b>اطلاعات کارت مورد نظر یافت نشد</b>",
                    parse_mode="HTML",
                    reply_markup=back_menu("back_main")
                )
            except Exception as e:
                print("Scan timeout error:", e)

        threading.Thread(target=scan_timeout, daemon=True).start()
        return

    # --- حالت انتظار برای پیام پشتیبانی ---
    if chat_id in waiting_support:
        waiting_support.discard(chat_id)

        username = message.from_user.username or "بدون یوزرنیم"
        full_name = message.from_user.full_name or "-"

        admin_text = (
            f"<b>پیام پشتیبانی جدید</b>\n\n"
            f"<b>نام : {full_name}</b>\n"
            f"<b>یوزرنیم : @{username}</b>\n"
            f"<b>ایدی عددی : {chat_id}</b>\n\n"
            f"<b>متن پیام :</b>\n"
            f"<b>{text}</b>"
        )

        try:
            bot.send_message(
                ADMIN_ID,
                admin_text,
                parse_mode="HTML",
                reply_markup=admin_support_menu(chat_id)
            )
        except Exception as e:
            print("Admin support send error:", e)

        bot.send_message(
            chat_id,
            "<b>پیام شما برای پشتیبانی ارسال شد</b>",
            parse_mode="HTML",
            reply_markup=back_menu("back_main")
        )
        return


# ---------- Callback ها ----------

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    data = call.data
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    # --- اسکن ---
    if data == "scan":
        if chat_id not in subscribed_users:
            try:
                bot.edit_message_text(
                    NO_SUB_TEXT, chat_id, msg_id,
                    reply_markup=back_menu("back_main"),
                    parse_mode="HTML"
                )
            except Exception:
                pass
            bot.answer_callback_query(call.id)
            return

        waiting_card.add(chat_id)
        try:
            bot.edit_message_text(
                "<b>لطفا شماره کارت خود را ارسال کنید</b>",
                chat_id, msg_id,
                reply_markup=back_menu("back_main"),
                parse_mode="HTML"
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id)

    # --- امضا ---
    elif data == "signature":
        if chat_id not in subscribed_users:
            try:
                bot.edit_message_text(
                    NO_SUB_TEXT, chat_id, msg_id,
                    reply_markup=back_menu("back_main"),
                    parse_mode="HTML"
                )
            except Exception:
                pass
            bot.answer_callback_query(call.id)
            return

        try:
            bot.edit_message_text(
                SIGNATURE_REPAIR_TEXT, chat_id, msg_id,
                reply_markup=back_menu("back_main"),
                parse_mode="HTML"
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id)

    # --- پشتیبانی ---
    elif data == "support":
        waiting_support.add(chat_id)
        try:
            bot.edit_message_text(
                "<b>پیام خود را بنویسید</b>",
                chat_id, msg_id,
                reply_markup=back_menu("back_main"),
                parse_mode="HTML"
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id)

    # --- خرید اشتراک ---
    elif data == "buy":
        try:
            bot.edit_message_text(
                PRICES_TEXT, chat_id, msg_id,
                reply_markup=plans_menu(),
                parse_mode="HTML"
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
            f"<b>~ ʏᴏᴜʀ ᴘʟᴀɴ : {plan['days']}</b>\n"
            f"<b>ᴘʀɪᴄᴇ : {plan['price']}</b>\n\n"
            f"<b>ᴡᴀʟʟᴇᴛ : <code>{WALLET}</code></b>\n\n"
            f"<b>اول واریزی رو انجام بدید و بعد بزنید روی پرداخت ، "
            f"تراکنش شما در لحظه چک و خرید شما تایید میشه.</b>"
        )

        try:
            bot.edit_message_text(
                text, chat_id, msg_id,
                reply_markup=payment_menu(),
                parse_mode="HTML"
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
            f"<b>سفارش جدید</b>\n\n"
            f"<b>نام : {full_name}</b>\n"
            f"<b>یوزرنیم : @{username}</b>\n"
            f"<b>ایدی عددی : {chat_id}</b>\n\n"
            f"<b>پلن : {plan['days']}</b>\n"
            f"<b>قیمت : {plan['price']}</b>\n"
        )

        try:
            bot.send_message(
                ADMIN_ID, admin_text,
                parse_mode="HTML",
                reply_markup=admin_order_menu(chat_id, plan_key)
            )
        except Exception as e:
            print("Admin send error:", e)

        try:
            bot.edit_message_text(
                "<b>سفارش شما برای بررسی به ادمین ارسال شد.</b>\n"
                "<b>پس از تایید پرداخت، اشتراک شما فعال خواهد شد.</b>",
                chat_id, msg_id,
                reply_markup=back_menu("back_main"),
                parse_mode="HTML"
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id, "ارسال شد")

    # --- کنسل ---
    elif data == "cancel":
        try:
            bot.edit_message_text(
                WELCOME_TEXT, chat_id, msg_id,
                reply_markup=main_menu(),
                parse_mode="HTML"
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id, "لغو شد")

    # --- بازگشت به منوی اصلی ---
    elif data == "back_main":
        waiting_support.discard(chat_id)
        waiting_card.discard(chat_id)
        try:
            bot.edit_message_text(
                WELCOME_TEXT, chat_id, msg_id,
                reply_markup=main_menu(),
                parse_mode="HTML"
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id)

    # --- بازگشت به لیست پلن ها ---
    elif data == "back_plans":
        try:
            bot.edit_message_text(
                PRICES_TEXT, chat_id, msg_id,
                reply_markup=plans_menu(),
                parse_mode="HTML"
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

        # اضافه کردن به لیست کاربران اشتراک دار
        subscribed_users.add(target_id)

        try:
            bot.send_message(
                target_id,
                f"<b>سفارش شما تایید شد.</b>\n"
                f"<b>پلن : {plan['days']}</b>\n"
                f"<b>اشتراک شما فعال شد.</b>",
                parse_mode="HTML"
            )
        except Exception as e:
            print("User notify error:", e)

        try:
            bot.edit_message_text(
                call.message.text + "\n\n<b>تایید شد</b>",
                call.message.chat.id,
                call.message.message_id,
                parse_mode="HTML"
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

        # حذف از لیست کاربران اشتراک دار
        subscribed_users.discard(target_id)

        try:
            bot.send_message(
                target_id,
                "<b>سفارش شما به علت عدم‌ پرداخت موجودی لغو شد</b>",
                parse_mode="HTML"
            )
        except Exception as e:
            print("User notify error:", e)

        try:
            bot.edit_message_text(
                call.message.text + "\n\n<b>رد شد</b>",
                call.message.chat.id,
                call.message.message_id,
                parse_mode="HTML"
            )
        except Exception:
            pass
        bot.answer_callback_query(call.id, "رد شد")

    # --- پاسخ به پشتیبانی (ادمین) ---
    elif data.startswith("admin_reply_"):
        try:
            target_id = int(data[len("admin_reply_"):])
        except Exception:
            bot.answer_callback_query(call.id, "داده نامعتبر")
            return

        bot.answer_callback_query(call.id, "برای پاسخ، روی پیام کاربر ریپلای کنید")
        try:
            bot.send_message(
                ADMIN_ID,
                f"<b>برای پاسخ به کاربر {target_id}، روی پیام او ریپلای کنید.</b>",
                parse_mode="HTML"
            )
        except Exception:
            pass


if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
