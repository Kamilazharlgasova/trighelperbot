import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart



API_TOKEN = '8113500779:AAEJz2y_GwH-Behxb12ie1F0Ka2ZoeIEZvg'

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
user_states = {}

# --- Главное меню ---
language_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇰🇿 Қазақша")],
    ],
    resize_keyboard=True
)


mode_menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👨‍🏫 Помощник по тригонометрии")],
        [KeyboardButton(text="📚 Учебный курс (пошаговое обучение)")],
        [KeyboardButton(text="🔙 Назад")],
    ],
    resize_keyboard=True
)

mode_menu_kz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👨‍🏫 Тригонометрия бойынша көмекші")],
        [KeyboardButton(text="📚 Оқу курсы (кезеңмен оқыту)")],
        [KeyboardButton(text="🔙 Қайту")],
    ],
    resize_keyboard=True
)

helper_menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Тригонометрическая таблица")],
        [KeyboardButton(text="📐 Тригонометрические формулы")],
        [KeyboardButton(text="📈 Тригонометрические функции")],
        [KeyboardButton(text="🧮 Формулы тригонометрических уравнений")],
        [KeyboardButton(text="⚖️ Тригонометрические неравенства")],
        [KeyboardButton(text="🔙 Назад")],
    ],
    resize_keyboard=True
)

helper_menu_kz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Тригонометриялық кесте")],
        [KeyboardButton(text="📐 Тригонометриялық формулалар")],
        [KeyboardButton(text="📈 Тригонометриялық функциялар")],
        [KeyboardButton(text="🧮 Тригонометриялық теңдеулердің формулалары")],
        [KeyboardButton(text="⚖️ Тригонометриялық теңсіздіктер")],
        [KeyboardButton(text="🔙 Қайту")],
    ],
    resize_keyboard=True
)
user_states = {}
user_progress = {}

pdf_lectures_ru = {
    "1": {"title": "📖 Тема 1: Тригонометрические функции острого угла (синус, косинус, тангенс и котангенс)", "file_id": "BQACAgIAAxkBAAIGZGgAAdgL6EKyZOKBd2FaRQ_fX4v3MQACTm4AAomQCEgJieGaIYEqNjYE"},
    "2": {"title": "📖 Тема 2: Градусные и радианные меры углов и дуг", "file_id": "BQACAgIAAxkBAAIGZmgAAdgO01mNVNqbH8hlqJozmG0ABE9uAAKJkAhIxKSPhrtWiwABNgQ"},
    "3": {"title": "📖 Тема 3: Синус, косинус, тангенс и котангенс любого угла. Значения синуса, косинуса, тангенса и котангенса угла", "file_id": "BQACAgIAAxkBAAIGaGgAAdgSvZtyAgptFThAEfefJCbpCQACUG4AAomQCEhALXyO8EIs4DYE"},
    "4": {"title": "📖 Тема 4: Свойства тригонометрических функций", "file_id": "BQACAgIAAxkBAAIGamgAAdgYHjapNqEIBxpMTHwYr6-hqgACUm4AAomQCEgNBV1MPoWLfDYE"},
    "5": {"title": "📖 Тема 5: Тригонометрические тождества", "file_id": "BQACAgIAAxkBAAIKI2gBbdnTzChJYcIvU2nXJ71r0xtkAAJHdwACiZAISIZft4oZeM1VNgQ"},
    "6": {"title": "📖 Тема 6: Формулы приведения", "file_id": "BQACAgIAAxkBAAIKKWgBbeLNgSB49OHH155fo0u7hzjJAAJIdwACiZAISLgVLxuh8E-8NgQ"},
    "7": {"title": "📖 Тема 7: Формулы для суммы и разности двух углов", "file_id": "BQACAgIAAxkBAAIKMGgBbe2Ou2UQbmWhOJ2tvTttEbriAAJJdwACiZAISAyRQQ5jymbkNgQ"},
    "8": {"title": "📖 Тема 8: Формулы для удвоенного угла", "file_id": "BQACAgIAAxkBAAIKOmgBbffgmCGxZRo6W9qepv1BxNEkAAJKdwACiZAISMhetsn5PvdINgQ"},
    "9": {"title": "📖 Тема 9: Формулы для половинного угла", "file_id": "BQACAgIAAxkBAAIKQGgBbf0jzFlLTdwfgoUj05cI6SgYAAJLdwACiZAISPOKQzvdS_khNgQ"},
    "10": {"title": "📖 Тема 10: Формулы преобразования суммы и разности тригонометрических функций в произведение", "file_id": "BQACAgIAAxkBAAIKSmgBbgPXnWxs-PcXnQ4M9Jw4tKzaAAJMdwACiZAISFvhrCovG-nkNgQ"},
    "11": {"title": "📖 Тема 11: Формулы преобразования произведения тригонометрических функций в сумму или разность", "file_id": "BQACAgIAAxkBAAIKUGgBbglS5UAzMFcliQS25aVQ_p12AAJNdwACiZAISJlOgLyRIIfDNgQ"},
    "12": {"title": "📖 Тема 12: Основные свойства и графики тригонометрических функций", "file_id": "BQACAgIAAxkBAAIKVmgBbg8bPfgCnfkLwBkVMZ2WYFpVAAJOdwACiZAISJMZV2NjkiKQNgQ"},
    "13": {"title": "📖 Тема 13: Построение графиков тригонометрических функций с помощью преобразований", "file_id": "BQACAgIAAxkBAAIKXGgBbhSTz2jKYFHjHf5GbQquQPgzAAJPdwACiZAISEaHCEtbgIlGNgQ"},
    "14": {"title": "📖 Тема 14: Обратные тригонометрические функции", "file_id": "BQACAgIAAxkBAAIKYmgBbhu4OrrNzw9h0JiEgpmE4OsSAAJRdwACiZAISHaaAAEXgLTLujYE"},
    "15": {"title": "📖 Тема 15: Тригонометрические уравнения", "file_id": "BQACAgIAAxkBAAIKaGgBbiFVUcGIAAFaFmmFOieVkODpHQACUncAAomQCEgkdw42uDnAvzYE"},
    "16": {"title": "📖 Тема 16: Методы решения тригонометрических уравнений", "file_id": "BQACAgIAAxkBAAIKcGgBbie0wuwB9HyGiw-ga7kdhaCAAAJTdwACiZAISEMpuoBcsaYYNgQ"},
    "17": {"title": "📖 Тема 17: Решение системы тригонометрических уравнений", "file_id": "BQACAgIAAxkBAAIKdWgBbiwC7ZOpN7kxNP4j4_nepKcSAAJUdwACiZAISN7C0preObQINgQ"},
    "18": {"title": "📖 Тема 18: Решение тригонометрических неравенств", "file_id": "BQACAgIAAxkBAAIKd2gBbjGJuPrtMtWqQuBlR-AAAaC6MAACVXcAAomQCEg6BJzmNHNdkTYE"},
}

pdf_lectures_kz = {
    "1": {"title": "📖 Тақырып 1: Сүйір бұрыштың тригонометриялық функциялары (синус, косинус, тангенс және котангенс)", "file_id": "BQACAgIAAxkBAAIDaGgAAQQq5U5Gtx1XvNfqQtUntFVLPwAC628AAomQAAFIqzZjY9tXxgM2BA"},
    "2": {"title": "📖 Тақырып 2: Бұрыш пен доғаның градустық және радиандық өлшемдері", "file_id": "BQACAgIAAxkBAAIDamgAAQQyhvONss1HmAifloAwS_ylPAAC7W8AAomQAAFIXXDTpxfLVdQ2BA"},
    "3": {"title": "📖 Тақырып 3: Кез келген бұрыштың синусы, косинусы, тангенсі котангенсі.", "file_id": "BQACAgIAAxkBAAIDbGgAAQQ3EDccC2dNVmzsESnEYPpfDgAC7m8AAomQAAFIQ8havR01msI2BA"},
    "4": {"title": "📖 Тақырып 4: Тригонометриялық функциялардың қасиеттері", "file_id": "BQACAgIAAxkBAAIDbmgAAQQ8m2iwBNpeGSOit66mCvHxegAC728AAomQAAFIxBpYuqm-2co2BA"},
    "5": {"title": "📖 Тақырып 5: Тригонометриялық тепе-теңдіктер", "file_id": "BQACAgIAAxkBAAIDcGgAAQRCitWUXvHWqforPrampc5UlQAC8G8AAomQAAFIVVisOyma1EU2BA"},
    "6": {"title": "📖 Тақырып 6: Келтіру формулалары", "file_id": "BQACAgIAAxkBAAIDcmgAAQRGHmYUcJobZDRCM7EO3c9eqwAC8m8AAomQAAFIODkpmZvTeOM2BA"},
    "7": {"title": "📖 Тақырып 7: Екі бұрыштың қосындысы мен айырымының формулалары", "file_id": "BQACAgIAAxkBAAIDdGgAAQRLid3X_9Yf2H9VK8moMVpQ4QAC828AAomQAAFIa5iII7YPr-A2BA"},
    "8": {"title": "📖 Тақырып 8: Қос бұрыштың формулалары", "file_id": "BQACAgIAAxkBAAIDdmgAAQRSzQ7Sfb8hIkBuwArB217JAQAC9W8AAomQAAFIwUVjHl0iV7U2BA"},
    "9": {"title": "📖 Тақырып 9: Жарты бұрыштың формулалары", "file_id": "BQACAgIAAxkBAAIDeGgAAQRYV24C9zRVc4FN5cQhoCWW4AAC928AAomQAAFIuQe7udbvLLI2BA"},
    "10": {"title": "📖 Тақырып 10: Тригонометриялық функциялардың қосындысы мен айырымын көбейтіндіге түрлендіру формулалары", "file_id": "BQACAgIAAxkBAAIDemgAAQRdTZOdNdPt6k2U18kcmM4olQAC-G8AAomQAAFIOvGzazc4Mc82BA"},
    "11": {"title": "📖 Тақырып 11: Тригонометриялық функциялардың көбейтіндісін қосынды немесе айырымға түлендіру формулалары", "file_id": "BQACAgIAAxkBAAIDfGgAAQRjn6tUtG-dqtzqDDlT9dS2eAAC-W8AAomQAAFI1lijUwOywws2BA"},
    "12": {"title": "📖 Тақырып 12: Тригонометриялық функциялардың негізгі қасиеттері мен графиктері", "file_id": "BQACAgIAAxkBAAIDfmgAAQRor-ZscShno3WRwSF6g_IYBQAC-28AAomQAAFI1qI91nDvIAk2BA"},
    "13": {"title": "📖 Тақырып 13: Тригонометриялық функциялардың графиктерін түрлендірулер көмегімен салу", "file_id": "BQACAgIAAxkBAAIDgGgAAQRye3rCu4GHe2uR3w7a8574fwAC_W8AAomQAAFIULN8A4bfT_02BA"},
    "14": {"title": "📖 Тақырып 14: Кері тригонометриялық функциялар", "file_id": "BQACAgIAAxkBAAIDgmgAAQR4s9-GYW7GQijytI_TWcx1BgAC_m8AAomQAAFI6faT9PuGX4w2BA"},
    "15": {"title": "📖 Тақырып 15: Тригонометриялық теңдеулер", "file_id": "BQACAgIAAxkBAAIDhGgAAQR8Ttl5FdY-Lro6T-h0yhVCRwADcAACiZAAAUhbvw19kYgyGTYE"},
    "16": {"title": "📖 Тақырып 16: Тригонометриялық теңдеулерді шешу тәсілдері", "file_id": "BQACAgIAAxkBAAIDhmgAAQSBc1T5U9MBJukoCSQCrhz-qgACAXAAAomQAAFIzL5aAwABXEU1NgQ"},
    "17": {"title": "📖 Тақырып 17: Тригонометриялық теңдеулер жүйесін шешу", "file_id": "BQACAgIAAxkBAAIDiGgAAQSF0jf1bU1h0W4NqFelolLEggACA3AAAomQAAFIGj-Dq3DhSvU2BA"},
    "18": {"title": "📖 Тақырып 18: Тригонометриялық теңсіздіктерді шешу", "file_id": "BQACAgIAAxkBAAIDimgAAQSJeLk-T6kzutN5D0W_lYHFSwACBXAAAomQAAFI3tAkbSD2DTg2BA"},
}
assignments_ru = {
    6: "BQACAgIAAxkBAAIKfGgBbjj9T7s8lMIg5jQBrzdughAvAAJWdwACiZAISNw4R_E4VxN_NgQ",
    7: "BQACAgIAAxkBAAIKgWgBbl9NmpL56Uq6b4yypfWfacO0AAJYdwACiZAISN4Vmz4vaMY4NgQ",
    13: "BQACAgIAAxkBAAIKg2gBbmbknkh92Ru8ux6g4CXYThANAAJZdwACiZAISB-Vlt0d0T7WNgQ",
    16: "BQACAgIAAxkBAAIKhWgBbm66ohkEXD8ItK7nGd2gLHx7AAJadwACiZAISKgYjGWLmaiCNgQ",
    18: "BQACAgIAAxkBAAIKh2gBbn0AAUzUgjRN6j2C-0_H5IZxMQACW3cAAomQCEi0SkFGDuki8DYE"
}

answers_ru = {
    6: "AgACAgIAAxkBAAIGdmgAAduzKWhLgLJbZCQfpOGN-o8xNgACNfAxG4mQCEj7rwABXH82owoBAAMCAAN4AAM2BA",
    7: "AgACAgIAAxkBAAIGeGgAAdu4ilAJkeT_piyiokLXzjvU7gACNvAxG4mQCEgLm0WF7A7EJQEAAwIAA3gAAzYE",
    13: "AgACAgIAAxkBAAIGemgAAdu9vnnQfA7A3kogYzpsKdp_qgACN_AxG4mQCEjUzUnvTUl4awEAAwIAA3gAAzYE",
    16: "AgACAgIAAxkBAAIGfGgAAdvB27nviCMiRZ1iWK1qsp3nkQACOPAxG4mQCEgQz5NB2Ul3wAEAAwIAA3gAAzYE",
    18: "AgACAgIAAxkBAAIGfmgAAdvHC-ZJgZj_KVKJOsRZsXkTyQACOfAxG4mQCEjppKt2oQbKQgEAAwIAA3gAAzYE"
}

assignments_kz = {
    6: "BQACAgIAAxkBAAIKiWgBcCA4iNKpCYDWLgcJTlhXfVNOAAJldwACiZAISBdm_qDUQGjdNgQ",
    7: "BQACAgIAAxkBAAIKjWgBcCtpRXpdfYJ1PNfZ2w5PGQ-CAAJodwACiZAISJ4xlNjDZIqkNgQ",
    13: "BQACAgIAAxkBAAIKi2gBcCQb4FpxnvW1DYBLfxqDOrpqAAJndwACiZAISFmN-T3vr4fVNgQ",
    16: "BQACAgIAAxkBAAIKj2gBcDG-JZ8kfD8ycL-JOexp1nDSAAJqdwACiZAISOvAbYGG6v9DNgQ",
    18: "BQACAgIAAxkBAAIKkWgBcDVR1W7IRQ-RVBSpw2KIMfttAAJrdwACiZAISDZda_bdRuFeNgQ"
}

answers_kz = {
    6: "AgACAgIAAxkBAAIGdmgAAduzKWhLgLJbZCQfpOGN-o8xNgACNfAxG4mQCEj7rwABXH82owoBAAMCAAN4AAM2BA",
    7: "AgACAgIAAxkBAAIGeGgAAdu4ilAJkeT_piyiokLXzjvU7gACNvAxG4mQCEgLm0WF7A7EJQEAAwIAA3gAAzYE",
    13: "AgACAgIAAxkBAAIGXmgAAdam5lBjMwVkbFJaC58ZroFJ-gAC-u8xG4mQCEjnreDtWa4O9gEAAwIAA3gAAzYE",
    16: "AgACAgIAAxkBAAIGYGgAAdarm_9lY59ySYH8x0QyHxKz_wAC--8xG4mQCEjrxjPSjGjYYwEAAwIAA3gAAzYE",
    18: "AgACAgIAAxkBAAIGYmgAAdavN7kJ6jnnPmCmF012i0whhQAC_e8xG4mQCEgOK35m0dOsiwEAAwIAA3gAAzYE"
}

test_links = {
    3: {
        "ru": "https://docs.google.com/forms/d/e/1FAIpQLSdUWd_nYCn3ICcZNYmp6g2hrdwBFSqnquCQ4Ymz4FWp2DFsIg/viewform?usp=dialog",
        "kz": "https://docs.google.com/forms/d/e/1FAIpQLSdUWd_nYCn3ICcZNYmp6g2hrdwBFSqnquCQ4Ymz4FWp2DFsIg/viewform?usp=dialog"
    },
    16: {
        "ru": "https://docs.google.com/forms/d/e/1FAIpQLSeNoJ3S6p-EU41ovxr2wcV3d6rdGxT3dlxHC1FgXRhstUboQw/viewform?usp=dialog",
        "kz": "https://docs.google.com/forms/d/e/1FAIpQLSeNoJ3S6p-EU41ovxr2wcV3d6rdGxT3dlxHC1FgXRhstUboQw/viewform?usp=dialog"
    },
    18: {
        "ru": "https://docs.google.com/forms/d/e/1FAIpQLScHt3mJYI3C8TN8prFcqZIZyYYPup3aNZhf2P6Cj1Iq6HCpZQ/viewform?usp=dialog",
        "kz": "https://docs.google.com/forms/d/e/1FAIpQLScHt3mJYI3C8TN8prFcqZIZyYYPup3aNZhf2P6Cj1Iq6HCpZQ/viewform?usp=dialog"
    }
}

# Темы с заданиями
topics_with_tasks = [6, 7, 13, 16, 18]
topics_with_tests = [3, 16, 18]



course_menu_ru = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=pdf_lectures_ru[key]["title"])] for key in pdf_lectures_ru] + [[KeyboardButton(text="🔙 Назад")]],
    resize_keyboard=True
)


course_menu_kz = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=pdf_lectures_kz[key]["title"])] for key in pdf_lectures_kz] + [[KeyboardButton(text="🔙 Қайту")]],
    resize_keyboard=True
)



course_menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📖 Тема 1: Тригонометрические функции острого угла (синус, косинус, тангенс и котангенс)")],
        [KeyboardButton(text="📖 Тема 2: Градусные и радианные меры углов и дуг")],
        [KeyboardButton(text="📖 Тема 3: Синус, косинус, тангенс и котангенс любого угла. Значения синуса, косинуса, тангенса и котангенса угла")],
        [KeyboardButton(text="📖 Тема 4: Свойства тригонометрических функций")],
        [KeyboardButton(text="📖 Тема 5: Тригонометрические тождества")],
        [KeyboardButton(text="📖 Тема 6: Формулы приведения")],
        [KeyboardButton(text="📖 Тема 7: Формулы для суммы и разности двух углов")],
        [KeyboardButton(text="📖 Тема 8: Формулы для удвоенного угла")],
        [KeyboardButton(text="📖 Тема 9: Формулы для половинного угла")],
        [KeyboardButton(text="📖 Тема 10: Формулы преобразования суммы и разности тригонометрических функций в произведение")],
        [KeyboardButton(text="📖 Тема 11: Формулы преобразования произведения тригонометрических функций в сумму или разность")],
        [KeyboardButton(text="📖 Тема 12: Основные свойства и графики тригонометрических функций")],
        [KeyboardButton(text="📖 Тема 13: Построение графиков тригонометрических функций с помощью преобразований")],
        [KeyboardButton(text="📖 Тема 14: Обратные тригонометрические функции")],
        [KeyboardButton(text="📖 Тема 15: Тригонометрические уравнения")],
        [KeyboardButton(text="📖 Тема 16: Методы решения тригонометрических уравнений")],
        [KeyboardButton(text="📖 Тема 17: Решение системы тригонометрических уравнений")],
        [KeyboardButton(text="📖 Тема 18: Решение тригонометрических неравенств")],
        [KeyboardButton(text="🔙 Назад")],
    ],
    resize_keyboard=True
)

course_menu_kz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📖 Тақырып 1: Сүйір бұрыштың тригонометриялық функциялары (синус, косинус, тангенс және котангенс)")],
        [KeyboardButton(text="📖 Тақырып 2: Бұрыш пен доғаның градустық және радиандық өлшемдері")],
        [KeyboardButton(text="📖 Тақырып 3: Кез келген бұрыштың синусы, косинусы, тангенсі котангенсі.")],
        [KeyboardButton(text="📖 Тақырып 4: Тригонометриялық функциялардың қасиеттері")],
        [KeyboardButton(text="📖 Тақырып 5: Тригонометриялық тепе-теңдіктер")],
        [KeyboardButton(text="📖 Тақырып 6: Келтіру формулалары")],
        [KeyboardButton(text="📖 Тақырып 7: Екі бұрыштың қосындысы мен айырымының формулалары")],
        [KeyboardButton(text="📖 Тақырып 8: Қос бұрыштың формулалары")],
        [KeyboardButton(text="📖 Тақырып 9: Жарты бұрыштың формулалары")],
        [KeyboardButton(text="📖 Тақырып 10: Тригонометриялық функциялардың қосындысы мен айырымын көбейтіндіге түрлендіру формулалары")],
        [KeyboardButton(text="📖 Тақырып 11: Тригонометриялық функциялардың көбейтіндісін қосынды немесе айырымға түлендіру формулалары")],
        [KeyboardButton(text="📖 Тақырып 12: Тригонометриялық функциялардың негізгі қасиеттері мен графиктері")],
        [KeyboardButton(text="📖 Тақырып 13: Тригонометриялық функциялардың графиктерін түрлендірулер көмегімен салу")],
        [KeyboardButton(text="📖 Тақырып 14: Кері тригонометриялық функциялар")],
        [KeyboardButton(text="📖 Тақырып 15: Тригонометриялық теңдеулер")],
        [KeyboardButton(text="📖 Тақырып 16: Тригонометриялық теңдеулерді шешу тәсілдері")],
        [KeyboardButton(text="📖 Тақырып 17: Тригонометриялық теңдеулер жүйесін шешу")],
        [KeyboardButton(text="📖 Тақырып 18: Тригонометриялық теңсіздіктерді шешу")],
        [KeyboardButton(text="🔙 Қайту")],
    ],
    resize_keyboard=True
)


# Тексты по языкам
texts = {
    "ru": {
        "start_course": "Выберите тему для начала курса:",
        "read_button": "✅ Прочитал",
        "done_button": "✅ Выполнил",
        "checked_button": "✅ Проверил",
        "passed_button": "✅ Сдал тест",
        "next_topic": "➡️ Следующая тема",
        "task_msg": "📚 Задание к теме",
        "answers_msg": "📄 Ответы к теме",
        "test_msg": "🧪 Тест по теме",
        "course_done": "🎉 Курс завершён! Молодец!",
    },
    "kz": {
        "start_course": "Курсты бастау үшін тақырыпты таңдаңыз:",
        "read_button": "✅ Оқыдым",
        "done_button": "✅ Орындадым",
        "checked_button": "✅ Тексердім",
        "passed_button": "✅ Тест тапсырдым",
        "next_topic": "➡️ Келесі тақырып",
        "task_msg": "📚 Тақырып бойынша тапсырма",
        "answers_msg": "📄 Жауаптар",
        "test_msg": "🧪 Тест",
        "course_done": "🎉 Курс аяқталды! Жарайсың!",
    },
}

# Создаём кнопку
def get_button(text, callback_data):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text, callback_data=callback_data)]])

trig_inequalities_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="фукнция sinx"), KeyboardButton(text="фукнция cosx")],
        [KeyboardButton(text="фукнция tgx"), KeyboardButton(text="фукнция ctgx")],
        [KeyboardButton(text="🔙 Назад")],
    ],
    resize_keyboard=True
)



# --- Подменю тригонометрических функций ---
trig_functions_menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📉 y = sin(x)"), KeyboardButton(text="📉 y = cos(x)")],
        [KeyboardButton(text="📉 y = tg(x)"), KeyboardButton(text="📉 y = ctg(x)")],
        [KeyboardButton(text="🔙 Назад")],
    ],
    resize_keyboard=True
)

trig_functions_menu_kz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📉 y = sin(x)"), KeyboardButton(text="📉 y = cos(x)")],
        [KeyboardButton(text="📉 y = tg(x)"), KeyboardButton(text="📉 y = ctg(x)")],
        [KeyboardButton(text="🔙 Қайту")],
    ],
    resize_keyboard=True
)

# --- Картинки функций ---
function_images_ru = {
    "📉 y = sin(x)": "AgACAgIAAxkBAAIJYGgBYS1ByuVbb3najapkfpqm1G1SAAKw8DEbn20JSEctvCloCp38AQADAgADeAADNgQ",
    "📉 y = cos(x)": "AgACAgIAAxkBAAIJYmgBYTC6_PxE82MG1iY1_MTjfslFAAKx8DEbn20JSL6f-igf1dJmAQADAgADeAADNgQ",
    "📉 y = tg(x)":  "AgACAgIAAxkBAAIJZGgBYTTDBhfw8FR82Cwq1AsvqmnjAAKy8DEbn20JSPge8xVMIr4WAQADAgADeAADNgQ",
    "📉 y = ctg(x)": "AgACAgIAAxkBAAIJZmgBYTnwXxP0s6PRFgOF49_hm7-_AAKz8DEbn20JSBSPZ_za8YTPAQADAgADeAADNgQ",
}

function_images_kz = {
    "📉 y = sin(x)": "AgACAgIAAxkBAAIH32gBSg7fH1NCgp3qOcR-R6QxldXFAALz8zEbiZAISG6STTpDXS1SAQADAgADeAADNgQ",
    "📉 y = cos(x)": "AgACAgIAAxkBAAIH42gBSi8OVcmMUVSZ1LNK060nDdhSAAL18zEbiZAISHeNmni7eAx8AQADAgADeAADNgQ",
    "📉 y = tg(x)":  "AgACAgIAAxkBAAIJXGgBYSTqdF_phyFDFIdt3kdXTWoQAAKs8DEbn20JSCWF3OKYq2p0AQADAgADeAADNgQ",
    "📉 y = ctg(x)": "AgACAgIAAxkBAAIJXmgBYSiveUuljBFcrGY3YGGeQM2yAAKt8DEbn20JSPF-s8NkhvqgAQADAgADeAADNgQ"
,
}



# --- Подменю формул ---
trig_formulas_menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Основные тождества")],
        [KeyboardButton(text="Формулы приведения")],
        [KeyboardButton(text="Формулы сложения")],
        [KeyboardButton(text="Формулы перехода от произведения к сумме")],
        [KeyboardButton(text="Формулы двойного угла")],
        [KeyboardButton(text="Формулы тройного угла")],
        [KeyboardButton(text="Некоторые суммы")],
        [KeyboardButton(text="Формулы перехода от суммы к произведению")],
        [KeyboardButton(text="Формулы понижения степени")],
        [KeyboardButton(text="Формулы половинного угла")],
        [KeyboardButton(text="🔙 Назад")],
    ],
    resize_keyboard=True
)
trig_formulas_menu_kz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Негізгі тепе-теңдіктер")],
        [KeyboardButton(text="Қосу формулалары")],
        [KeyboardButton(text="Көбейтіндіні қосындыға түрлендіру формулалары")],
        [KeyboardButton(text="Қос бұрыштың формулалары")],
        [KeyboardButton(text="Үш еселенген бұрыштың формулалары")],
        [KeyboardButton(text="Кейбір қосындылар")],
        [KeyboardButton(text="Қосындыны көбейтіндіге түрлендіру формулалары")],
        [KeyboardButton(text="Дәрежені төмендету формулалары")],
        [KeyboardButton(text="Жарты бұрыштың формулалары")],
        [KeyboardButton(text="🔙 Қайту")],
    ],
    resize_keyboard=True
)


# --- Формулы и таблицы ---
formula_images = {
    "📊 Тригонометрическая таблица": "AgACAgIAAyEFAASegP1XAAMDZ_pCDBiGAAGfjLYJbgSDFz0N9EoGAALY7zEbEtzQS4kmmcDa3O4nAQADAgADeQADNgQ" ,
    "Основные тождества": "AgACAgIAAxkBAAPGZ_pc15laEIA7Tu-HXsHqmMBMY7YAApzuMRsVr9FLyoRE5LAdT7sBAAMCAAN4AAM2BA",
    "Формулы приведения": "AgACAgIAAxkBAAPWZ_peUsk587A8aOCXRiCzGByQDjQAApvuMRsVr9FLID02cSbULDkBAAMCAAN5AAM2BA",
    "Формулы сложения": "AgACAgIAAxkBAAPeZ_pfsq_0-NpJwEYJvEW4FPVeGbsAAm_uMRsVr9FL5hLinf7FxL8BAAMCAAN4AAM2BA",
    "Формулы перехода от произведения к сумме": "AgACAgIAAxkBAAPgZ_pfvtHgMpS8uCjgXFu8JpsKdn4AAnXuMRsVr9FLvcDg9n93XjYBAAMCAAN4AAM2BA",
    "Формулы двойного угла": "AgACAgIAAxkBAAPiZ_pfzXK720kgOPdeaiC2hLeWgoEAAnbuMRsVr9FLYMDq2S5slL4BAAMCAAN4AAM2BA",
    "Формулы тройного угла": "AgACAgIAAxkBAAPmZ_pf4xUtHa5768QL0ihym6OtQQQAAnnuMRsVr9FLq-r2dAMNnrcBAAMCAAN4AAM2BA",
    "Некоторые суммы": "AgACAgIAAxkBAAPaZ_pfcJx9PXt1pIW9Or2Lqg5LugoAAl_1MRt2ctFL4QjzIsxn96QBAAMCAAN4AAM2BA",
    "Формулы перехода от суммы к произведению": "AgACAgIAAxkBAAPkZ_pf1tcTJbooue_N052VQEIU-8UAAnfuMRsVr9FLV6caYSFui0wBAAMCAAN5AAM2BA",
    "Формулы понижения степени": "AgACAgIAAxkBAAPoZ_pf8qBWBqsOVqT8vcBkcWT5QLsAAn_uMRsVr9FL_jkCPvu4MpgBAAMCAAN4AAM2BA",
    "Формулы половинного угла": "AgACAgIAAxkBAAIJt2gBYrlQmU7_Eo4D6bwqk-lNpx8rAALR9DEbiZAISCe6DQH7S7pIAQADAgADeAADNgQ",
    "🧮 Формулы тригонометрических уравнений": "AgACAgIAAxkBAAIDXmf_4FqTO3_7j6JNszdngCQ56pE5AAJb7TEb3Y74S0oRhf_rK2neAQADAgADeQADNgQ",
    "функция sinx": "AgACAgIAAxkBAAIDYGf_769n2Fatsg6of90wS3iwMK6JAAJS6TEb3Y4AAUj9lzCuLv_URgEAAwIAA3kAAzYE",
    "функция cosx": "AgACAgIAAxkBAAIDYmf_77aU4bZxnrXev8jxCdKUW5xLAAJU6TEb3Y4AAUhDsXQBhf95swEAAwIAA3kAAzYE",
    "функция tgx":  "AgACAgIAAxkBAAIDZGf_77iOimiKwnJowe3wh3J8KuGVAAJV6TEb3Y4AAUhp1AX_z6A3xgEAAwIAA3kAAzYE",
    "функция ctgx": "AgACAgIAAxkBAAIDZmf_77sGAAGZUJ686I-At0gAAQMeSicAAlbpMRvdjgABSJoLT3aakqCjAQADAgADeQADNgQ",
    "📊 Тригонометриялық кесте": "AgACAgIAAyEFAASegP1XAAMDZ_pCDBiGAAGfjLYJbgSDFz0N9EoGAALY7zEbEtzQS4kmmcDa3O4nAQADAgADeQADNgQ" ,
    "Негізгі тепе-теңдіктер": "AgACAgIAAxkBAAPGZ_pc15laEIA7Tu-HXsHqmMBMY7YAApzuMRsVr9FLyoRE5LAdT7sBAAMCAAN4AAM2BA",
    "Қосу формулалары": "AgACAgIAAxkBAAPeZ_pfsq_0-NpJwEYJvEW4FPVeGbsAAm_uMRsVr9FL5hLinf7FxL8BAAMCAAN4AAM2BA",
    "Көбейтіндіні қосындыға түрлендіру формулалары": "AgACAgIAAxkBAAPgZ_pfvtHgMpS8uCjgXFu8JpsKdn4AAnXuMRsVr9FLvcDg9n93XjYBAAMCAAN4AAM2BA",
    "Қос бұрыштың формулалары": "AgACAgIAAxkBAAPiZ_pfzXK720kgOPdeaiC2hLeWgoEAAnbuMRsVr9FLYMDq2S5slL4BAAMCAAN4AAM2BA",
    "Үш еселенген бұрыштың формулалары": "AgACAgIAAxkBAAPmZ_pf4xUtHa5768QL0ihym6OtQQQAAnnuMRsVr9FLq-r2dAMNnrcBAAMCAAN4AAM2BA",
    "Кейбір қосындылар": "AgACAgIAAxkBAAPaZ_pfcJx9PXt1pIW9Or2Lqg5LugoAAl_1MRt2ctFL4QjzIsxn96QBAAMCAAN4AAM2BA",
    "Қосындыны көбейтіндіге түрлендіру формулалары": "AgACAgIAAxkBAAPkZ_pf1tcTJbooue_N052VQEIU-8UAAnfuMRsVr9FLV6caYSFui0wBAAMCAAN5AAM2BA",
    "Дәрежені төмендету формулалары": "AgACAgIAAxkBAAPoZ_pf8qBWBqsOVqT8vcBkcWT5QLsAAn_uMRsVr9FL_jkCPvu4MpgBAAMCAAN4AAM2BA",
    "Жарты бұрыштың формулалары": "AgACAgIAAxkBAAIJt2gBYrlQmU7_Eo4D6bwqk-lNpx8rAALR9DEbiZAISCe6DQH7S7pIAQADAgADeAADNgQ",
    "🧮 Тригонометриялық теңдеулердің формулалары": "AgACAgIAAxkBAAIDXmf_4FqTO3_7j6JNszdngCQ56pE5AAJb7TEb3Y74S0oRhf_rK2neAQADAgADeQADNgQ",
}

# --- Команды и хендлеры ---
@dp.message(F.text == "/start")
async def start(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = {"lang": None, "mode": None, "history": []}
    await message.answer("Выберите язык / Тілді таңдаңыз:", reply_markup=language_menu)

@dp.message(F.text.in_(["🇷🇺 Русский", "🇰🇿 Қазақша"]))
async def select_language(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = {"lang": "ru" if message.text == "🇷🇺 Русский" else "kz", "mode": None, "history": ["lang_selected"]}
    lang = user_states[user_id]["lang"]

    await message.answer(
        "Выберите режим работы:" if lang == "ru" else "Жұмыс режимін таңдаңыз:",
        reply_markup=mode_menu_ru if lang == "ru" else mode_menu_kz
    )

@dp.message(F.text.in_([
    "👨‍🏫 Помощник по тригонометрии", "👨‍🏫 Тригонометрия бойынша көмекші",
    "📚 Учебный курс (пошаговое обучение)", "📚 Оқу курсы (кезеңмен оқыту)"
]))
async def select_mode(message: types.Message):
    user_id = message.from_user.id
    lang = user_states[user_id]["lang"]

    if "👨‍🏫" in message.text:
        user_states[user_id]["mode"] = "helper"
        user_states[user_id]["history"].append("helper_menu")
        await message.answer("Вы в режиме помощника 📋" if lang == "ru" else "Сіз көмекші режиміндесіз 📋",
                             reply_markup=helper_menu_ru if lang == "ru" else helper_menu_kz)

    elif "📚" in message.text:
        user_states[user_id]["mode"] = "course"
        user_states[user_id]["history"].append("mode_selected")

        # Сформировать меню курса из данных
        course_menu = generate_course_menu(lang)
        await message.answer(
            "Выберите тему курса:" if lang == "ru" else "Курс тақырыбын таңдаңыз:",
            reply_markup=course_menu
        )

def generate_course_menu(lang="ru"):
    lectures = pdf_lectures_ru if lang == "ru" else pdf_lectures_kz
    back_text = "🔙 Назад" if lang == "ru" else "🔙 Қайту"
    
    keyboard = [[KeyboardButton(text=lecture["title"])] for lecture in lectures.values()]
    keyboard.append([KeyboardButton(text=back_text)])  # добавляем кнопку "назад"
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


@dp.message(F.text.in_(["📐 Тригонометрические формулы", "📐 Тригонометриялық формулалар"]))
async def trig_formulas(message: types.Message):
    user_id = message.from_user.id
    if user_states.get(user_id, {}).get("mode") != "helper":
        return

    lang = user_states[user_id]["lang"]
    await message.answer("Выберите категорию формул:", reply_markup=trig_formulas_menu_ru if lang == "ru" else trig_formulas_menu_kz)

@dp.message(F.text.in_(["📈 Тригонометрические функции", "📈 Тригонометриялық функциялар"]))
async def trig_functions_menu(message: types.Message):
    user_id = message.from_user.id
    if user_states.get(user_id, {}).get("mode") != "helper":
        return

    lang = user_states[user_id]["lang"]
    await message.answer("Выберите функцию:" if lang == "ru" else "Функцияны таңдаңыз:",
                         reply_markup=trig_functions_menu_ru if lang == "ru" else trig_functions_menu_kz)

@dp.message(F.text.in_(["📉 y = sin(x)", "📉 y = cos(x)", "📉 y = tg(x)", "📉 y = ctg(x)"]))
async def send_function_graph(message: types.Message):
    user_id = message.from_user.id
    if user_states.get(user_id, {}).get("mode") != "helper":
        return

    lang = user_states.get(user_id, {}).get("lang", "ru")
    text = message.text

    file_id = (function_images_ru if lang == "ru" else function_images_kz).get(text)
    if file_id:
        await message.answer_photo(file_id, caption=text)
    else:
        await message.answer("⚠️ График не найден.")


@dp.message(F.text.in_(["⚖️ Тригонометрические неравенства", "⚖️ Тригонометриялық теңсіздіктер"]))
async def inequalities_menu(message: types.Message):
    user_id = message.from_user.id
    if user_states.get(user_id, {}).get("mode") != "helper":
        return

    lang = user_states[user_id]["lang"]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="функция sinx"), KeyboardButton(text="функция cosx")],
            [KeyboardButton(text="функция tgx"), KeyboardButton(text="функция ctgx")],
            [KeyboardButton(text="🔙 Назад")],
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите функцию:" if lang == "ru" else "Функцияны таңдаңыз:", reply_markup=keyboard)


@dp.message(F.text.in_(formula_images.keys()))
async def send_formula(message: types.Message):
    user_id = message.from_user.id
    if user_states.get(user_id, {}).get("mode") != "helper":
        return

    file_id = formula_images[message.text]
    await message.answer_photo(file_id, caption=f"<b>{message.text}</b>")


@dp.message(F.text.in_(["📊 Тригонометрическая таблица", "📊 Тригонометриялық кесте"]))
async def trig_table(message: types.Message):
    user_id = message.from_user.id
    if user_states.get(user_id, {}).get("mode") != "helper":
        return

    lang = user_states[user_id]["lang"]
    key = "📊 Тригонометрическая таблица" if lang == "ru" else "📊 Тригонометриялық кесте"
    file_id = formula_images.get(key)
    await message.answer_photo(file_id, caption=key)


@dp.message(F.text.in_(["🧮 Формулы тригонометрических уравнений", "🧮 Тригонометриялық теңдеулердің формулалары"]))
async def trig_equations(message: types.Message):
    user_id = message.from_user.id
    if user_states.get(user_id, {}).get("mode") != "helper":
        return

    lang = user_states[user_id]["lang"]
    key = "🧮 Формулы тригонометрических уравнений" if lang == "ru" else "🧮 Тригонометриялық теңдеулердің формулалары"
    file_id = formula_images.get(key)
    await message.answer_photo(file_id, caption=key)


@dp.message(F.text == "функция sinx")
async def func_sinx(message: types.Message):
    file_id = formula_images.get("функция sinx")
    await message.answer_photo(file_id, caption="Неравенства sinx")

@dp.message(F.text == "функция cosx")
async def func_cosx(message: types.Message):
    file_id = formula_images.get("функция cosx")
    await message.answer_photo(file_id, caption="Неравенства cosx")

@dp.message(F.text == "функция tgx")
async def func_tgx(message: types.Message):
    file_id = formula_images.get("функция tgx")
    await message.answer_photo(file_id, caption="Неравенства tgx")

@dp.message(F.text == "функция ctgx")
async def func_ctgx(message: types.Message):
    file_id = formula_images.get("функция ctgx")
    await message.answer_photo(file_id, caption="Неравенства ctgx")

@dp.message(F.text.in_(["🔙 Назад", "🔙 Қайту"]))
async def go_back(message: types.Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    if not state or not state["history"]:
        await message.answer("Вы уже в начале.", reply_markup=language_menu)
        return

    last = state["history"].pop()
    lang = state["lang"]

    if last == "mode_selected":
        await message.answer(
            "Выберите режим работы:" if lang == "ru" else "Жұмыс режимін таңдаңыз:",
            reply_markup=mode_menu_ru if lang == "ru" else mode_menu_kz
        )
    elif last == "lang_selected":
        await message.answer("Выберите язык / Тілді таңдаңыз:", reply_markup=language_menu)
    elif last == "helper_menu":
        await message.answer(
            "Вы в режиме помощника 📋" if lang == "ru" else "Сіз көмекші режиміндесіз 📋",
            reply_markup=helper_menu_ru if lang == "ru" else helper_menu_kz
        )



@dp.message(F.document)
async def handle_document_upload(message: types.Message):
    file_id = message.document.file_id
    file_name = message.document.file_name
    mime = message.document.mime_type

    await message.reply(
        f"📎 Файл получен!\n<b>Название:</b> {file_name}\n<b>MIME тип:</b> {mime}\n<b>file_id:</b>\n<code>{file_id}</code>",
        parse_mode="HTML"
    )

# === Вывод file_id при загрузке фото ===
@dp.message(F.photo)
async def handle_photo_upload(message: types.Message):
    file_id = message.photo[-1].file_id
    await message.reply(
        f"🖼 Фото получено!\n<b>file_id:</b>\n<code>{file_id}</code>",
        parse_mode="HTML"
    )



@dp.message(F.text == "🎓 Курс по тригонометрии")
async def start_course(message: types.Message):
    user_id = message.from_user.id
    lang = user_states.get(user_id, {}).get("lang", "ru")
    user_progress[user_id] = {"topic": 1, "step": "lecture", "lang": lang}
    await send_lecture(message.chat.id, 1, lang)


@dp.message()
async def handle_topic_selection(message: types.Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if not state or state.get("mode") != "course":
        return  # пользователь не в режиме курса — пропускаем

    lang = state.get("lang", "ru")
    lectures = pdf_lectures_ru if lang == "ru" else pdf_lectures_kz
    user_text = message.text.strip()

    for num, data in lectures.items():
        if data["title"].strip() == user_text:
            user_progress[user_id] = {"topic": int(num), "step": "lecture", "lang": lang}
            await send_lecture(message.chat.id, int(num), lang)
            return

    await message.answer("⚠️ Тема не найдена. Выберите из меню.")


    # Защита от отсутствия в user_states
    if user_id not in user_states:
        user_states[user_id] = {"lang": "ru", "mode": None, "history": []}

    lang = user_states[user_id]["lang"]
    lectures = pdf_lectures_ru if lang == "ru" else pdf_lectures_kz
    text = message.text

    for num, data in lectures.items():
        if data["title"] == text:
            user_progress[user_id] = {"topic": int(num), "step": "lecture", "lang": lang}
            await send_lecture(message.chat.id, int(num), lang)
            return

# Отправка лекции

async def send_lecture(chat_id, topic_num, lang):
    lecture = pdf_lectures_ru[str(topic_num)] if lang == "ru" else pdf_lectures_kz[str(topic_num)]
    await bot.send_document(chat_id, lecture["file_id"], caption=f"<b>{lecture['title']}</b>")
    await bot.send_message(chat_id, texts[lang]["read_button"], reply_markup=get_button(texts[lang]["read_button"], "read"))

# Отправка задания

async def send_task(chat_id, topic_num, lang):
    assignments = assignments_ru if lang == "ru" else assignments_kz
    if topic_num in assignments:
        await bot.send_document(chat_id, assignments[topic_num], caption=texts[lang]["task_msg"])
    else:
        await bot.send_message(chat_id, "📭 Для этой темы нет задания." if lang == "ru" else "📭 Бұл тақырыпта тапсырма жоқ.")
    await bot.send_message(chat_id, texts[lang]["done_button"], reply_markup=get_button(texts[lang]["done_button"], "done_task"))


# Отправка ответов
async def send_answers(chat_id, topic_num, lang):
    answers = answers_ru if lang == "ru" else answers_kz
    if topic_num in answers:
        await bot.send_photo(chat_id, answers[topic_num], caption=texts[lang]["answers_msg"])
    else:
        await bot.send_message(chat_id, "📭 Ответов к этому заданию пока нет." if lang == "ru" else "📭 Бұл тапсырмаға жауаптар жоқ.")
    await bot.send_message(chat_id, texts[lang]["checked_button"], reply_markup=get_button(texts[lang]["checked_button"], "checked"))


# Отправка теста
async def send_test(chat_id, topic_num, lang):
    if topic_num in test_links:
        link = test_links[topic_num][lang]
        await bot.send_message(chat_id, f"{texts[lang]['test_msg']}:\n{link}", 
                               reply_markup=get_button(texts[lang]["passed_button"], "passed"))
    else:
        # если теста нет, сразу переходим к кнопке "Следующая тема"
        await bot.send_message(chat_id, texts[lang]["next_topic"], 
                               reply_markup=get_button(texts[lang]["next_topic"], "next_topic"))


# Обработка кнопок
@dp.callback_query(F.data.in_(["read", "done_task", "checked", "passed", "next_topic"]))
async def handle_steps(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    progress = user_progress.get(user_id)

    if not progress:
        await callback.message.answer("Запусти курс сначала.")
        return

    topic = progress["topic"]
    step = progress["step"]
    lang = progress["lang"]

    if callback.data == "read":
        if topic in topics_with_tasks:
            user_progress[user_id]["step"] = "task"
            await send_task(chat_id, topic, lang)
        else:
            user_progress[user_id]["step"] = "test"
            await send_test(chat_id, topic, lang)

    elif callback.data == "done_task":
        user_progress[user_id]["step"] = "answers"
        await send_answers(chat_id, topic, lang)

    elif callback.data == "checked":
        user_progress[user_id]["step"] = "test"
        await send_test(chat_id, topic, lang)

    elif callback.data == "passed":
        if topic < len(pdf_lectures_ru):
            user_progress[user_id]["step"] = "lecture"
            await bot.send_message(chat_id, texts[lang]["next_topic"], reply_markup=get_button(texts[lang]["next_topic"], "next_topic"))
        else:
            await bot.send_message(chat_id, texts[lang]["course_done"])

    elif callback.data == "next_topic":
        user_progress[user_id]["topic"] += 1
        next_topic = user_progress[user_id]["topic"]
        await send_lecture(chat_id, next_topic, lang)

    await callback.answer()

# --- Запуск ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
