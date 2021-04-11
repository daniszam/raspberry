import threading
from datetime import datetime, timedelta
from time import sleep

import telebot

running_events = dict()


def handle_plan(chat_id):
    print("Sending subscription to {}...".format(chat_id))
    # todo doesnt work
    bot.sendMessage(chat_id, 'sdfsdf', parse_mode='Markdown')
    event = threading.Timer(timedelta(seconds=10).total_seconds(), handle_plan, args=(chat_id,))
    running_events[chat_id] = event
    event.start()


def get_latest_update_id(bot):
    last_upd = bot.get_updates()['result']
    if len(last_upd) == 0:
        return 0
    else:
        return last_upd[-1]['update_id']


if __name__ == '__main__':
    bot = telebot.TeleBot(import_name='distance_bot')
    bot.config['api_key'] = '1735365027:AAGYLp4qYUj0y45zIG14ik0CaS6zrAfTa80'
    # Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
    print(bot.config)
    print(bot.get_me())
    # MessageLoop(bot, handle).run_as_thread()
    print('Listening...')

    update_id = get_latest_update_id(bot)
    while True:
        try:
            upd = bot.get_updates(timeout=1, offset=update_id + 1)
            print(upd)
            result = upd.get('result')
            res_len = len(result)
            if res_len == 0:
                continue
            last_update = result[0]
            last_message = last_update['message']
            chat_id = last_message['chat']['id']
            message_text = last_message['text']
            if message_text == '/hello':
                bot.send_message(chat_id=chat_id, text='Hello, @' + last_message['from']['username'])
            elif message_text == '/subscribe':
                if chat_id not in running_events:
                    planned_time = datetime.strptime('10:10', "%H:%M")
                    planned_date = datetime.now().replace(hour=planned_time.hour, minute=planned_time.minute,
                                                          second=0) + timedelta(seconds=1)
                    diff = planned_date - datetime.now()
                    diff_sec = diff.total_seconds()
                    event = threading.Timer(diff_sec, handle_plan, args=(chat_id,))
                    running_events[chat_id] = event
                    bot.send_message(chat_id=chat_id,
                                     text='You got subscription on this bot, if you want to unsubscribe, please, then just '
                                          'type /unsubscribe command')
                else:
                    bot.send_message(chat_id=chat_id,
                                     text='You already have a subscription')
            elif message_text == '/unsubscribe':
                if chat_id not in running_events:
                    bot.send_message(chat_id=chat_id,
                                     text='You dont have a subscription')
                else:
                    running_events[chat_id].cancel()
                    bot.send_message(chat_id=chat_id, text='Okay :(')
            update_id = last_update['update_id']
            sleep(1)
        except Exception:
            print('GOT ERROR')
            update_id = update_id + 1
            pass
