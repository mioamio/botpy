import os
import logging
import sqlite3
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Создание базы данных
def create_db():
    conn = sqlite3.connect('birthdays.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS birthdays (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот для поздравлений с днём рождения. Используйте /startbot для активации.')

# Команда /startbot для активации бота
def start_bot(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Бот активирован! Теперь вы можете использовать команды /add и /remove.')

# Команда /add для добавления дня рождения
def add(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 2:
        update.message.reply_text('Используйте: /add Фамилия Имя ДД.ММ')
        return
    name = ' '.join(context.args[:-1])
    date = context.args[-1]
    
    # Добавление в базу данных
    conn = sqlite3.connect('birthdays.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO birthdays (name, date) VALUES (?, ?)', (name, date))
    conn.commit()
    conn.close()
    
    update.message.reply_text(f'Добавлен: {name} - {date}')

# Команда /remove для удаления дня рождения
def remove(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text('Используйте: /remove Фамилия Имя')
        return
    name = ' '.join(context.args)
    
    # Удаление из базы данных
    conn = sqlite3.connect('birthdays.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM birthdays WHERE name = ?', (name,))
    conn.commit()
    conn.close()
    
    update.message.reply_text(f'Удалён: {name}')

def main():
    # Создание базы данных
    create_db()
    
    # Получите токен из переменной окружения
    TOKEN = os.getenv("7738581806:AAFWv74dqG48tEYcpgZRjnMGytNC9_VDF4I")
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("startbot", start_bot))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("remove", remove))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
