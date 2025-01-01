import telebot
from datetime import datetime
import psycopg2
from psycopg2 import sql

# Токен вашего бота
API_TOKEN = '8036311859:AAE7m4dxXLV5E4mjuOZD4s24HcRluylrvLc'
bot = telebot.TeleBot(API_TOKEN)

# Подключение к базе данных PostgreSQL
DB_URL = "postgresql://postgres:YfGwvFlshmeByqXNizSyKqDDCnSBSCHN@autorack.proxy.rlwy.net:20268/railway"
connection = psycopg2.connect(DB_URL)
cursor = connection.cursor()

# Создание таблицы, если она еще не создана
cursor.execute("""
CREATE TABLE IF NOT EXISTS birthdays (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    birthday DATE NOT NULL,
    chat_id BIGINT NOT NULL
);
""")
connection.commit()

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для напоминания о днях рождения. Используй команды /add_birthday и /list_birthdays.")

# Команда добавления дня рождения
@bot.message_handler(commands=['add_birthday'])
def add_birthday(message):
    bot.reply_to(message, "Введите день рождения в формате: Имя DD.MM")

    @bot.message_handler(func=lambda m: True)
    def save_birthday(msg):
        try:
            name, date = msg.text.split()
            birthday_date = datetime.strptime(date, '%d.%m').date()
            chat_id = msg.chat.id

            # Сохранение в базу данных
            cursor.execute(
                "INSERT INTO birthdays (name, birthday, chat_id) VALUES (%s, %s, %s)",
                (name, birthday_date, chat_id)
            )
            connection.commit()

            bot.reply_to(msg, f"День рождения {name} добавлен: {birthday_date.strftime('%d.%m')}")
        except ValueError:
            bot.reply_to(msg, "Некорректный формат. Попробуйте снова.")

# Команда просмотра списка дней рождения
@bot.message_handler(commands=['list_birthdays'])
def list_birthdays(message):
    chat_id = message.chat.id
    cursor.execute("SELECT name, birthday FROM birthdays WHERE chat_id = %s ORDER BY birthday", (chat_id,))
    rows = cursor.fetchall()

    if rows:
        response = "Список дней рождения:\n"
        for row in rows:
            name, birthday = row
            response += f"{name}: {birthday.strftime('%d.%m')}\n"
    else:
        response = "Список дней рождения пуст."

    bot.reply_to(message, response)

# Проверка на дни рождения
def check_birthdays():
    today = datetime.now().date()
    cursor.execute("SELECT name, chat_id FROM birthdays WHERE birthday = %s", (today,))
    rows = cursor.fetchall()

    for row in rows:
        name, chat_id = row
        bot.send_message(chat_id, text=f"Сегодня день рождения у {name}! Не забудьте поздравить!")

# Планировщик для ежедневной проверки
import schedule
import time

def run_scheduler():
    schedule.every().day.at("09:00").do(check_birthdays)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Запуск бота
if __name__ == '__main__':
    from threading import Thread
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.start()
    bot.polling()
