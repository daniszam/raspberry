import os
from datetime import datetime, timedelta
from multiprocessing import Process
from time import sleep

import paho.mqtt.client as mqtt
import telebot

raspberry_subscriber = {}
# This is the Subscriber
# hostname
broker = "localhost"
# port
port = 1883
# time to live
timelive = 60

unresolved_not = {}


def init():
    global raspberry_subscriber
    for i in range(1, 10):
        raspberry_subscriber[str(i)] = list()
        try:
            f = (open('notifications_' + str(i) + '.txt'))
            for line in f:
                raspberry_subscriber.get(str(i)).append(line.replace('\n', ''))
            f.close()
        except Exception as e:
            pass
    print("Initialization subscribers")
    print(raspberry_subscriber)


def get_latest_update_id(bot):
    last_upd = bot.get_updates()['result']
    if len(last_upd) == 0:
        return 0
    else:
        return last_upd[-1]['update_id']


def save_notification(pi_number):
    print("Save subscribers list")
    try:
        f = open('notifications_' + str(pi_number) + '.txt', 'w').close()
    except Exception as e:
        pass
    f = open('notifications_' + str(pi_number) + '.txt', 'tw')
    for chat in raspberry_subscriber[pi_number]:
        f.write(str(chat) + '\n')
    f.close()


def need_to_notificate(msg):
    f = open('need_to_notificate.txt', 'tw')
    f.write(msg)
    f.close()


def check_to_notice():
    try:
        f = open('need_to_notificate.txt')
        if not os.stat('need_to_notificate.txt').st_size == 0:
            print("Send notifications")
            for line in f:
                pi_number = line.split(' ')[1]
                val = line.split(' ')[0]
                send_notifications(pi_number, val)
        os.remove('need_to_notificate.txt')
        f.close()
    except FileNotFoundError:
        print("Nothing to notificate")


def send_notifications(pi_number, msg):
    f = open('notifications_' + str(pi_number) + '.txt')
    for chat_id in f:
        unresolved_not[pi_number] = msg
        bot.send_message(chat_id,
                         "🔥Alert for pi: " + str(pi_number) + " 🔥\nYour thing was moved. And new value is " + msg +
                         ". Please text me OK if everything is okey 😎")
    f.close()


def resolve_not(pi_number):
    print("resolve pi" + str(pi_num))
    f = open('notifications_' + str(pi_number) + '.txt')
    if str(pi_number) in unresolved_not:
        print("resolve")
        for chat_id in f:
            print(str(chat_id))
            bot.send_message(chat_id, "👌Alert resolved for pi:" + str(
                pi_number) + " 👌\nGood day, mate! I'm keeping an eye on your stuf.")
        del unresolved_not[pi_number]


def start_server():
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("/data")

    def on_message(client, userdata, msg):
        print(msg.payload.decode())
        need_to_notificate(msg.payload.decode())

    client = mqtt.Client()
    client.connect(broker, port, timelive)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


if __name__ == '__main__':

    p = Process(target=start_server)
    p.start()
    bot = telebot.TeleBot(import_name='distance_bot')
    bot.config['api_key'] = '1735365027:AAGYLp4qYUj0y45zIG14ik0CaS6zrAfTa80'
    # Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
    print(bot.config)
    print(bot.get_me())
    # MessageLoop(bot, handle).run_as_thread()
    print('Listening...')

    init()

    update_id = get_latest_update_id(bot)
    while True:
        try:
            upd = bot.get_updates(timeout=1, offset=update_id + 1)
            print(upd)
            check_to_notice()
            result = upd.get('result')
            res_len = len(result)
            if res_len == 0:
                continue
            last_update = result[0]
            last_message = last_update['message']
            chat_id = last_message['chat']['id']
            message_text = last_message['text']
            raspberry_number = '1'

            if '/subscribe' in message_text or '/unsubscribe' in message_text:
                try:
                    raspberry_number = message_text.split(" ")[1]
                except Exception as e:
                    pass
            if message_text == '/hello':
                bot.send_message(chat_id=chat_id, text='Hello, @' + last_message['from']['username'])
            elif '/subscribe' in message_text:
                if chat_id not in raspberry_subscriber[raspberry_number]:
                    raspberry_subscriber.get(raspberry_number).append(chat_id)
                    planned_time = datetime.strptime('10:10', "%H:%M")
                    planned_date = datetime.now().replace(hour=planned_time.hour, minute=planned_time.minute,
                                                          second=0) + timedelta(seconds=1)
                    diff = planned_date - datetime.now()
                    diff_sec = diff.total_seconds()
                    bot.send_message(chat_id=chat_id,
                                     text='You got subscription on this bot, if you want to unsubscribe, '
                                          'please, then just type /unsubscribe command')
                    save_notification(raspberry_number)
                else:
                    bot.send_message(chat_id=chat_id,
                                     text='You already have a subscription')
            elif '/unsubscribe' in message_text:
                if chat_id not in raspberry_subscriber[raspberry_number]:
                    bot.send_message(chat_id=chat_id,
                                     text='You dont have a subscription')
                else:
                    raspberry_subscriber[raspberry_number].remove(chat_id)
                    bot.send_message(chat_id=chat_id, text='Okay :(')
                    save_notification(raspberry_number)
            elif '/ok' in message_text and ' ' in message_text:
                pi_num = message_text.split(' ')[1]
                resolve_not(int(pi_num))
            update_id = last_update['update_id']
            sleep(1)
        except Exception as e:
            print('GOT ERROR')
            print(e)
            update_id = update_id + 1
            pass
