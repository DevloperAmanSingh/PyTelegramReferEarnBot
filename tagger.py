#under developemnt

import telebot
from telebot import types

# Initialize your bot with the bot token obtained from BotFather
bot = telebot.TeleBot("5911757666:AAE_BIr3Qvi7MsR3yPNVl8op5dNtvSlxfJM")

# Handle the "/start" command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome to the User Tagger Bot! Type /tag to tag users.")

# Handle the "/tag" command
@bot.message_handler(commands=['tag'])
def tag_users(message):
    # Get a list of all users in the chat
    chat_id = message.chat.id
    users = bot.get_mem
    
    # Tag users in groups of 5
    tagged_users = []
    for user in users:
        user_id = user.user.id
        tagged_user = f"@{user.user.username}" if user.user.username else user.user.first_name
        tagged_users.append(tagged_user)
        if len(tagged_users) == 5:
            tag_message = " ".join(tagged_users)
            bot.reply_to(message, tag_message)
            tagged_users = []
    
    # If there are remaining tagged users
    if len(tagged_users) > 0:
        tag_message = " ".join(tagged_users)
        bot.reply_to(message, tag_message)

# Start the bot
bot.polling()
