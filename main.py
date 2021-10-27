import config
import todo
import exceptions

import telebot

bot = telebot.TeleBot(config.TOKEN)

todos = dict()


@bot.message_handler(commands=['help'])
def _help(message):
    bot.send_message(message.chat.id, config.HELP)


@bot.message_handler(commands=['todo'])
def add(message):
    message_text = message.text[5:]
    try:
        todo.add_todo(message_text, message.from_user.id)
    except exceptions.NotCorrectMessage as e:
        bot.send_message(message.chat.id, str(e))

    answer = "Задача добавлена!"
    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['show'])
def _print(message):
    tasks = todo.get_tasks_by_date(message.text[6:])
    for task in tasks:
        bot.send_message(message.chat.id, f"Категория: {task.category_codename}\n"
                                          f"Текст: {task.text}")

    if len(tasks) == 0:
        bot.send_message(message.chat.id, "Заданий на этот день нет.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
