from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class HodimState(StatesGroup):
    idora = State()
    texnologiya = State()
    telefon = State()
    hudud = State()
    ism_familiya = State()
    murojaat_vaqti = State()
    ish_vaqti = State()
    maosh = State()
    qoshimcha = State()
    ha_yoq = State()


class IshJoyiState(StatesGroup):
    Ism_Fam = State()
    Yosh = State()
    texnologiya = State()
    telefon = State()
    hudud = State()
    narx = State()
    kasbi = State()
    maqsad = State()    
    ha_yoq = State()
