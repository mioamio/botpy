import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from database import create_db, add_birthday, remove_birthday
from datetime import datetime

# логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот для поздравлений с днём рождения.')

# /add для добавления дня рождения
def add(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 2:
        update.message.reply_text('Используй: /add Фамилия Имя дд.мм')
        return
    name = ' '.join(context.args[:-1])
    date = context.args[-1]
    add_birthday(name, date)
    update.message.reply_text(f'Добавлен: {name} - {date}')

# /remove для удаления дня рождения
def remove(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text('Используй: /remove Фамилия Имя')
        return
    name = ' '.join(context.args)
    remove_birthday(name)
    update.message.reply_text(f'Удалён: {name}')

# Проверка дней рождения
def check_birthdays(context: CallbackContext) -> None:
    today = datetime.now().strftime('%d.%m')
    # Здесь нужно добавить логику для проверки базы данных и отправки сообщений
    # ...

def main():
    create_db()
    updater = Updater("7738581806:AAFWv74dqG48tEYcpgZRjnMGytNC9_VDF4I")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("remove", remove))

    # Запуск проверки дней рождения каждый день
    job_queue = updater.job_queue
    job_queue.run_daily(check_birthdays, time=datetime.time(hour=9, minute=0, second=0))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()