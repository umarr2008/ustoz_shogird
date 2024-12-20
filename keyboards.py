
from aiogram import types

start_keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        types.KeyboardButton("Hodim kerak"), types.KeyboardButton("Ish joyi kerak")
    ],
    [
        types.KeyboardButton("Shogird kerak"), types.KeyboardButton("Ustoz kerak")
    ]
])

tasdiqlash_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        types.KeyboardButton("✅ HA"), types.KeyboardButton("❌ YO'Q")
    ]
])


admin_tasdiqlash_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        types.KeyboardButton("✅👑 HA"), types.KeyboardButton("❌👑 YO'Q")
    ]
])

contact_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        types.KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)
    ]
])