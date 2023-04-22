import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor, markdown
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Инициализация бота и диспетчера
bot = Bot(token='5948835614:AAHkb6OLH52yklEmy2DT5oNttfcOfRK5r0Y')
dp = Dispatcher(bot)

# Логирование
logging.basicConfig(level=logging.INFO)

# Кнопки меню
menu_markup = ReplyKeyboardMarkup(resize_keyboard=True)
media_button = KeyboardButton('Медиа')
menu_markup.add(media_button)

# Функция для обработки команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Это функция для работы с медиафайлами. Нажми на кнопку 'Медиа', чтобы начать.", reply_markup=menu_markup)

gauth = GoogleAuth()
gauth.DEFAULT_SETTINGS['client_config_file'] = os.path.join(os.path.dirname(__file__), 'client_secret.json')
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)


# Функция для обработки нажатия кнопки "Медиа"
@dp.message_handler(text=['Медиа'])
async def media_menu(message: types.Message):
    output_list = check_google_drive()
    # output_str = '\n'.join([str(folder['title'])+":"+str(folder['alternateLink']) for folder in output_list])
    output_str = 'Если ты хочешь добавить или посмотреть фото/видео с различных мероприятий ОИ "Адаптеры", то переходи по нужной тебе ссылке:\n '+'\n'.join(str("["+folder['title'])+"]"+"("+str(folder['alternateLink']+")") for folder in output_list)
    await message.answer(output_str, parse_mode='Markdown')
# Ищем какие папки существуют
def check_google_drive():
    folder_id = "1_mV319eKOf3aK-zL8YbUQTCWH50YNwCt" #Указываем id папки которую шарим
    file_lists = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
    return file_lists



if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

