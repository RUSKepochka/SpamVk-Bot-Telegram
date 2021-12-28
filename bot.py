import telebot
import vk_api
import random
import time
from telebot import types

bot = telebot.TeleBot('TOKEN')
print('[~] Бот успешно запущен | Версия: 1.0.0')

profiles = []
groupIDs = []


def SPAM(COUNT):
    for profile in profiles:
        login = profile.split(" ")[0]
        password = profile.split(" ")[1]
        with open("messages.txt", encoding="UTF-8") as g:
            messages = [str(x) for x in g.readlines()]
        vk_session = vk_api.VkApi(
            login, password,
        )
        try:
            vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return

        tools = vk_session.get_api()
        for j in groupIDs:
            flag = False
            wall = tools.wall.get(owner_id=j, count=COUNT+1)
            if wall['items']:
                it = wall['items']
                for i in range(len(it)):
                    try:
                        if it[i]['is_pinned']:
                            flag = True
                    except Exception as ex:
                        if flag:
                            postID = it[i]['id']
                            ownerID = it[i]['owner_id']
                            try:
                                time.sleep(1)
                                tools.wall.createComment(owner_id=ownerID, post_id=postID, message=messages[random.randint(0, len(messages)-1)])
                            except Exception as ex1:
                                print(ex1)
                        else:
                            if i != len(it)-1:
                                postID = it[i]['id']
                                ownerID = it[i]['owner_id']
                                try:
                                    time.sleep(1)
                                    tools.wall.createComment(owner_id=ownerID, post_id=postID, message=messages[random.randint(0, len(messages) - 1)])
                                except Exception as ex1:
                                    print(ex1)


@bot.message_handler(commands=['start'])
def start_menu(message):
    bot.send_message(message.chat.id, "Здравствуйте, я СпамБот для начала работы напишите /spam")


@bot.message_handler(commands=['spam'])
def spam(message):
    msg = bot.send_message(message.chat.id, "Введите ссылки на группы для спама через запятую\n(Пример: 202436583,12353330,163452344)")
    bot.register_next_step_handler(msg, get_groups)


def get_groups(message):
    if message.content_type == 'text':
        groups_id = str(message.text)
        global groupIDs
        groupIDs = [str("-"+x) for x in groups_id.split(",")]
        msg = bot.send_message(message.chat.id, "Введите логин/логины и пароль/пароли от аккаунтов\n(Пример: +79999999999 qwerty123412, +79988888999 qwerty1212312)")
        bot.register_next_step_handler(msg, get_profiles)
    else:
        bot.reply_to(message, '❌Данные введены неверно')


def get_profiles(message):
    try:
        if message.content_type == 'text':
            input = str(message.text)
            global profiles
            profiles = input.split(",")
            msg = bot.send_message(message.chat.id, "Введите количество постов для спама")
            bot.register_next_step_handler(msg, get_count)
        else:
            bot.reply_to(message, '❌Данные введены неверно')
    except Exception as ex:
        bot.reply_to(message, '❌Ошибка❌')
        print("[x] Ошибка | {0}".format(ex))


def get_count(message):
    try:
        if message.content_type == 'text':
            count = str(message.text)
            bot.send_message(message.chat.id, "Начинаю спам")
            SPAM(COUNT=int(count))
            bot.send_message(message.chat.id, "Успех!")
    except Exception as ex:
        bot.reply_to(message, '❌Ошибка❌')
        print("[x] Ошибка | {0}".format(ex))


if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True, interval=2)
