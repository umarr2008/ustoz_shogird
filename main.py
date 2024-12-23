import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, ADMIN_ID, CHANNEL_ID
from keyboards import start_keyboards, tasdiqlash_kb, admin_tasdiqlash_kb, contact_kb
from database import create_table, insert_data, select_data, select_data_by_id
from states import HodimState, IshJoyiState

from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
result_text = ""
result_dict = {}

@dp.message_handler(commands=['start'], state='*')
async def salom_ber(message: types.Message):
    await message.answer(text="Assalomu aleykum, USTOZ SHOGIRD botga xush kelibsiz!\
                         \nKerakli menuni tanlang", reply_markup=start_keyboards)
    
@dp.message_handler(lambda message: message.text == "Hodim kerak")
async def hodim_kerak(message: types.Message):
    text = """Xodim topish uchun ariza berishingiz mumkin

Hozir sizga birnecha savollar beriladi, har biriga javob bering. 
Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi."""
    await message.answer(text=text)
    await message.answer(text="🎓 Idora nomini kiriting:")
    await HodimState.idora.set()
    

@dp.message_handler(state=HodimState.idora)
async def idora_state(message: types.Message, state: FSMContext):
    await state.update_data(idora=message.text)
    text = '''📚 Texnologiya kiriting:
Texnologiya nomlarini vergul bilan ajrating. Masalan, 
Java, C++, C#'''
    await message.answer(text=text)
    await HodimState.next()

@dp.message_handler(state=HodimState.texnologiya)
async def texnologiya_state(message: types.Message, state: FSMContext):
    await state.update_data(texnologiya=message.text)
    text = '''📞 Telefon raqamingizni yuboring'''
    await message.answer(text=text, reply_markup=contact_kb)
    await HodimState.next()


@dp.message_handler(state=HodimState.telefon, content_types=types.ContentType.CONTACT)
async def telefon_state(message: types.Message, state: FSMContext):
    await state.update_data(telefon=message.contact.phone_number)
    text = '''📍 Hududingizni kiriting'''
    await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())
    await HodimState.next()

@dp.message_handler(state=HodimState.hudud)
async def hudud_state(message: types.Message, state: FSMContext):
    await state.update_data(hudud=message.text)
    text = '''👤 Ismingiz va Familiyangizni kiriting'''
    await message.answer(text=text)
    await HodimState.next()


@dp.message_handler(state=HodimState.ism_familiya)
async def ism_familiya_state(message: types.Message, state: FSMContext):
    await state.update_data(ism_familiya=message.text)
    text = '''⏰ Murojaat vaqtingizni kiriting'''
    await message.answer(text=text)
    await HodimState.next()


@dp.message_handler(state=HodimState.murojaat_vaqti)
async def murojaat_vaqti_state(message: types.Message, state: FSMContext):
    await state.update_data(murojaat_vaqti=message.text)
    text = '''🕒 Ish vaqtingizni kiriting'''
    await message.answer(text=text)
    await HodimState.next()


@dp.message_handler(state=HodimState.ish_vaqti)
async def ish_vaqti_state(message: types.Message, state: FSMContext):
    await state.update_data(ish_vaqti=message.text)
    text = '''💰 Maoshingizni kiriting'''
    await message.answer(text=text)
    await HodimState.next()


@dp.message_handler(state=HodimState.maosh)
async def maosh_state(message: types.Message, state: FSMContext):
    await state.update_data(maosh=message.text)
    text = '''📝 Qo'shimcha ma'lumotlar'''
    await message.answer(text=text)
    await HodimState.next()


@dp.message_handler(state=HodimState.qoshimcha)
async def qoshimcha_state(message: types.Message, state: FSMContext):
    await state.update_data(qoshimcha=message.text)
    data = await state.get_data() # {}
    global result_text, result_dict
    result_dict = data
    result_text = f"""Xodim kerak:

🏢 Idora: {data.get('idora')}
📚 Texnologiya: {data.get('texnologiya')} 
🇺🇿 Telegram: @{message.from_user.username if message.from_user.username else ''}
📞 Aloqa: {data.get('telefon')}
🌐 Hudud: {data.get('hudud')}
✍️ Mas'ul: {data.get('ism_familiya')}
🕰 Murojaat vaqti: {data.get('murojaat_vaqti')}
🕰 Ish vaqti: {data.get('ish_vaqti')}
💰 Maosh: {data.get('maosh')}
‼️ Qo`shimcha: {data.get('qoshimcha')}

#ishJoyi #{data.get('hudud')} #{data.get('idora')}"""
    await message.answer(text=result_text, reply_markup=tasdiqlash_kb)
    await HodimState.ha_yoq.set()


@dp.message_handler(state=HodimState.ha_yoq)
async def ha_yoq_state(message: types.Message, state: FSMContext):
    global result_text
    if message.text == "✅ HA":
        await message.answer("Ariza ko'rib chiqish uchun adminga yuborildi! 💬", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(chat_id=ADMIN_ID, text=result_text, reply_markup=admin_tasdiqlash_kb)
        await state.finish()
    elif message.text == "❌ YO'Q":
        await message.answer("Ariza bekor qilindi! ❌", reply_markup=types.ReplyKeyboardRemove())
        result_text = ""
        await state.finish()
    else:
        await message.answer("Iltimos, faqat quyidagi tugmalardan birini bosing!", reply_markup=tasdiqlash_kb)
        return








@dp.message_handler(lambda message: message.text == "Ish joyi kerak")
async def ishjoyi_kerak(message: types.Message):
    text = """Ish joyi topish uchun ariza berishingiz mumkin

Hozir sizga birnecha savollar beriladi, har biriga javob bering. 
Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi."""
    await message.answer(text=text)
    await message.answer(text="🎓 Ism va Familiya kiriting:")
    await IshJoyiState.Ism_Fam.set()
    

@dp.message_handler(state=IshJoyiState.Ism_Fam)
async def idora_state(message: types.Message, state: FSMContext):
    await state.update_data(Ism_Fam=message.text)
    text = '''🕑 Yosh: 

Yoshingizni kiriting?
Masalan, 19'''
    await message.answer(text=text)
    await IshJoyiState.next()

@dp.message_handler(state=IshJoyiState.texnologiya)
async def texnologiya_state(message: types.Message, state: FSMContext):
    await state.update_data(texnologiya=message.text)
    text = '''📞 Telefon raqamingizni yuboring'''
    await message.answer(text=text, reply_markup=contact_kb)
    await IshJoyiState.next()


@dp.message_handler(state=IshJoyiState.telefon, content_types=types.ContentType.CONTACT)
async def telefon_state(message: types.Message, state: FSMContext):
    await state.update_data(telefon=message.contact.phone_number)
    text = '''📍 Hududingizni kiriting'''
    await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())
    await IshJoyiState.next()

@dp.message_handler(state=IshJoyiState.hudud)
async def hudud_state(message: types.Message, state: FSMContext):
    await state.update_data(hudud=message.text)
    text = '''👤 Ismingiz va Familiyangizni kiriting'''
    await message.answer(text=text)
    await IshJoyiState.next()



@dp.message_handler(state=IshJoyiState.narx)
async def maosh_state(message: types.Message, state: FSMContext):
    await state.update_data(narx=message.text)
    text = '''📝 Kasbingizni kiriting'''
    await message.answer(text=text)
    await IshJoyiState.next()
    
@dp.message_handler(state=IshJoyiState.kasbi)
async def kasb_state(message: types.Message, state: FSMContext):
    await state.update_data(kasbi=message.text)
    text = '''✍️ Maqsadingizni kiriting'''
    await message.answer(text=text)
    await IshJoyiState.next()
    

@dp.message_handler(state=IshJoyiState.maqsad)
async def qoshimcha_state(message: types.Message, state: FSMContext):
    await state.update_data(maqsad0=message.text)
    data = await state.get_data() # {}
    global result_text, result_dict
    result_dict = data
    result_text = f"""IIsh joyi kerak:

👨‍💼 Xodim: {data.get("Ism_Fam")}
🕑 Yosh: {data.get("Yosh")}
📚 Texnologiya: {data.get("texnologiya")}  
📞 Aloqa: {data.get("telefon")}
🌐 Hudud: {data.get("hudud")} 
💰 Narxi:  {data.get("narx")} 
👨🏻‍💻 Kasbi: {data.get("kasbi")} 
🔎 Maqsad: {data.get("maqsad")}  

#xodim #{data.get('hudud')} #{data.get('idora')}"""
    await message.answer(text=result_text, reply_markup=tasdiqlash_kb)
    await IshJoyiState.ha_yoq.set()


@dp.message_handler(state=IshJoyiState.ha_yoq)
async def ha_yoq_state(message: types.Message, state: FSMContext):
    global result_text
    if message.text == "✅ HA":
        await message.answer("Ariza ko'rib chiqish uchun adminga yuborildi! 💬", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(chat_id=ADMIN_ID, text=result_text, reply_markup=admin_tasdiqlash_kb)
        await state.finish()
    elif message.text == "❌ YO'Q":
        await message.answer("Ariza bekor qilindi! ❌", reply_markup=types.ReplyKeyboardRemove())
        result_text = ""
        await state.finish()
    else:
        await message.answer("Iltimos, faqat quyidagi tugmalardan birini bosing!", reply_markup=tasdiqlash_kb)
        return


@dp.message_handler()
async def admin_confirm(message: types.Message, state: FSMContext):
    global result_text, result_dict
    if message.text == "✅👑 HA":
        if message.from_user.id != ADMIN_ID:
            await message.answer("Siz admin emassiz! ❌")
            return
        await message.answer("Post tasdiqlandi! ✅\n\nXabar kanalga yuborildi!", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(chat_id=CHANNEL_ID, text=result_text)
        
        data = result_dict
        user_id = message.from_user.id
        username = message.from_user.username if message.from_user.username else ""
        data = (user_id, username, data.get('Ism_Fam'), data.get('Yosh'), data.get('texnologiya'), data.get('telefon'), data.get('hudud'), data.get('narx'), data.get('kasbi'), data.get('maqsad'))
        insert_data(data)

    elif message.text == "❌👑 YO'Q":
        if message.from_user.id != ADMIN_ID:
            await message.answer("Siz admin emassiz! ❌")
            return
        await message.answer("Post bekor qilindi! ❌")
        result_text = ""
    else:
        if message.from_user.id != ADMIN_ID:
            await message.answer("Boshidan boshlash uchun /start ni bosing", reply_markup=types.ReplyKeyboardRemove())
            return
        else:
            await message.answer("Iltimos, faqat quyidagi tugmalardan birini bosing!", reply_markup=admin_tasdiqlash_kb)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=create_table(dp))
