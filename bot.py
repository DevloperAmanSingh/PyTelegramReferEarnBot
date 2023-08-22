import telebot
import os
import watchdog
import requests
import psutil
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton , ReplyKeyboardMarkup , KeyboardButton
import logging
bot = telebot.TeleBot("your-bot-token", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")
#     logging.info(message)

def inline_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
                                 InlineKeyboardButton("No", callback_data="cb_no"))
    return markup

@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id,"That's great")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id,"sorry to hear that")
    

@bot.message_handler(commands=['group'])
def generatelink(msg):
    invite = bot.create_chat_invite_link(msg.chat.id,member_limit=1,expire_date=0)
    print(invite)
    inlinekeyboard = InlineKeyboardMarkup()
    inlinekeyboard.row = 1
    inlinekeyboard.add(InlineKeyboardButton("Join Group",url=invite.invite_link))
    bot.send_message(msg.chat.id, "Joim Group" , reply_markup=inlinekeyboard )
    invitelinklist = bot.get_chat_administrators(msg.chat.id)
    bot.send_message(msg.chat.id, invitelinklist.username)

# @bot.message_handler(content_types=['photo'])
# def handle_photo(message):
#     # Retrieve the photo ID and file path
#     photo_id = message.photo[-1].file_id
#     file_info = bot.get_file(photo_id)
#     file_path = file_info.file_path

#     # Download the image file
#     file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_path}'
#     image_name = f'{message.message_id}.jpg'  # Change the name as needed
#     image_path = os.path.join('downloads', image_name)  # Specify your desired download path

#     # Create the 'downloads' directory if it doesn't exist
#     os.makedirs('downloads', exist_ok=True)

#     # Download the image
#     response = requests.get(file_url)
#     with open(image_path, 'wb') as file:
#         file.write(response.content)




 # generate payload link
@bot.message_handler(commands=['payload'])
def generatelink(msg):
    bot_username = bot.get_me().username;
    inviteLink = f"https://t.me/{bot_username}?start={msg.chat.id}"
    bot.send_message(msg.chat.id, inviteLink)

@bot.message_handler(commands=['start'])
def start(msg):
    message = msg.text.split()
    if len(message) < 2:
        bot.send_message(msg.chat.id,"simple start")
        isinchannel = bot.get_chat_member('@pytelegramtestgroup', msg.from_user.id)
        try:
            if isinchannel.status in ['creator', 'administrator', 'member']:
                bot.send_message(msg.chat.id,"you are in channel")
                keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                button1 =  ['Option 1']
                row2_buttons = ['oo' , 'pp']
                row3_buttons = ['oo' , 'pp']
                keyboard.add(*button1)
                keyboard.add(*row2_buttons)
                keyboard.add(*row3_buttons)

    # Send the keyboard to the user
                bot.reply_to(msg, "Please select an option:", reply_markup=keyboard)

            else:
             bot.send_message(msg.chat.id,"you are not in channel")
        except telebot.apihelper.ApiException as e:
        # Handle any errors that may occur
            bot.reply_to(message, "An error occurred while checking membership.")

        return
    elif len(message) >= 2:
        bot.reply_to(msg,"start with parameter")
        bot.reply_to(msg,msg.text.split()[1])
        
        return
    



    # Send a confirmation message
bot.polling()


@bot.message_handler(commands=['inline'])
def send_inline(message):
    bot.send_message(message.chat.id, "Do you love Telebot?", reply_markup=inline_keyboard())

bot.infinity_polling()
logging.info("Bot started")
