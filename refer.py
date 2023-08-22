import telebot 
import pymongo
from telebot import types
import os
import datetime 
import timedelta
import requests
import psutil
import json
import smtplib
import random
import string
import pandas as pd
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton , ReplyKeyboardMarkup , KeyboardButton
import logging
bot = telebot.TeleBot("5349720426:AAHcuwBWX9zUZzW2ZBNZjCiIZWMz3AZNHVM", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
myclient = pymongo.MongoClient("mongodb+srv://aman:S3MqZLiEy2ee5SPl@cluster0.bqqkj.mongodb.net/")
mydb = myclient["pydb"]
mycol = mydb["userinfo"]

def verifyMembership(msg):
    status = bot.get_chat_member('@pytelegramtestgroup',msg.from_user.id)
    if status.status in ['creator','administrator','member']:
        return True
    else:
        return False

def mustjoin(msg):
    bot.send_message(msg.chat.id, "You must join the group to use the bot")

def sendKeyboard(msg):
   keyboard = ReplyKeyboardMarkup(row_width=3 , resize_keyboard=True)
   row1 = KeyboardButton("💵 Balance")
   row2 = ["👨‍👩‍👧‍👦 Reffer","🎁 Bonus","💰 Withdraw"]
   row3 = ["🗳 Wallet","📊 Stat"]
   keyboard.add(row1)
   keyboard.add(*row2)
   keyboard.add(*row3)
   bot.send_message(msg.chat.id, "Choose an option to get started" , reply_markup=keyboard)

def generateOtp():
    otp = random.randint(100000,999999)
    return otp

def sendOtp(email,msg):
    otp = generateOtp()
    print(otp)
    sender_email= ""
    sender_pass = ""
    subject = "OTP for your verification"
    body = f"Your OTP is {otp} for your acc with username {msg.from_user.username}"
    message = f'Subject: {subject}\n\n{body}'
    with smtplib.SMTP('smtp.gmail.com',587) as server:
     server.starttls()
     server.login(sender_email,sender_pass)
     server.sendmail(sender_email,email,message)
    print("OTP sent")



@bot.message_handler(commands=['email'])
def send_email(message):
    user = mycol.find_one({"userid":message.from_user.id})
    if user:
        email = message.text.split()[1]
        sendOtp(email,message)
    

@bot.message_handler(commands=['start'])
def start_process(message):
    data = message.text.split()
    # print(user)
    if len(data) < 2:
        user = mycol.find_one({"userid":message.from_user.id})
        if user is None:
            myUserData = { "username" : message.from_user.username , 
                            "name" : message.from_user.first_name ,
                            "userid" : message.from_user.id , 
                            "balance" : 0 , 
                            "isInvited" : "false" , 
                            "totalInvited" : 0 , 
                            "invitedBy" : "None" , 
                            "isVerified" : "false" , 
                            "bonus" : 0 
                        }
            mycol.insert_one(myUserData)
            bot.send_message(message.chat.id, "Welcome to the bot")
        res = verifyMembership(message)
        if res:
            userData = mycol.find_one({"userid":message.from_user.id})
            mycol.update_one({"userid":message.from_user.id},{ "$set": { "isVerified": "true" }})
            if userData.get("isVerified") == "false" and userData.get("isInvited") == "true":
                mycol.update_one({"userid":message.from_user.id},{ "$set": { "isVerified": "true" }})
                inviter = userData.get("invitedBy")
                infos = mycol.update_one({"userid":int(inviter)},{ "$set": { "balance": 222 }}) 
                text = f"Welcome to the bot\nYou have been invited by {inviter} . //"
                inviterText = f"Your friend from user id {inviter} has joined the bot"
                bot.send_message(message.chat.id, text)
                bot.send_message(inviter, inviterText)
                sendKeyboard(message)
            else :
                sendKeyboard(message)
        else:
            mustjoin(message)
    elif len(data) == 2 and data[0] == '/start' and data[1].isdigit():
        inviter = data[1]
        inviter_data = mycol.find_one({},{"userid":inviter})
        user = mycol.find_one({"userid":message.from_user.id})
        if inviter_data:
            if user is None and inviter is not message.from_user.id:
             myUserData = { "username" : message.from_user.username , "name" : message.from_user.first_name , "userid" : message.from_user.id , "balance" : 0 , "isInvited" : "true" , "totalInvited" : 0 , "invitedBy" : inviter , "isVerified" : "false" , "bonus" : 0 }
             mycol.insert_one(myUserData)
            res = verifyMembership(message)
            if res:
             bot.send_message(message.chat.id, "Welcome to the bot after joining the group")
             infos = mycol.update_one({"userid":int(inviter)},{ "$set": { "balance": 222 }}) 
             text = f"Welcome to the bot\nYou have been invited by {inviter}"
             inviterText = f"Your friend from user id {inviter} has joined the bot"
             bot.send_message(message.chat.id, text)
             bot.send_message(inviter, inviterText)
             sendKeyboard(message)
            else:
             mustjoin(message)
             
        else:
            bot.send_message(message.chat.id, "No such inviter found")
    else:
        bot.send_message(message.chat.id, "Invalid command")

@bot.message_handler(func=lambda message: message.text == "💵 Balance")
def balance(message):
   user = mycol.find_one({"userid":message.from_user.id})
   if user:
      balance = user.get("balance")
      bot.send_message(message.chat.id, f"Your balance is {balance}")
   else:
        bot.send_message(message.chat.id, "You are not registered in the bot. Please use /start to register")

@bot.message_handler(func=lambda message: message.text == "👨‍👩‍👧‍👦 Reffer")
def reffer(message):
    user = mycol.find_one({"userid":message.from_user.id})
    if user:
        invitedBy = user.get("invitedBy")
        print(datetime.timedelta(days=1))
        curenttime = datetime.datetime.now()
        print(curenttime)
        bot.send_message(message.chat.id, f"You are invited by {invitedBy} \n"+"Share your refferal link to get more refferals\n"+ "Your refferal link is https://t.me/PyTelegramTestBot?start="+str(message.from_user.id))
    else:
          bot.send_message(message.chat.id, "You are not registered in the bot. Please use /start to register")
        
@bot.message_handler(func=lambda message: message.text == "🎁 Bonus")
def bonus(message):
    user = mycol.find_one({"userid":message.from_user.id})
    if user:
        bonusvalue = 100
        bonusStatus = user.get("bonus")
        if bonusStatus == 0:
            currentTime = datetime.datetime.now()
            infos = mycol.update_one({"userid":message.from_user.id},{ "$set": { "balance": user.get("balance")+bonusvalue , "bonus": currentTime }})
            bot.send_message(message.chat.id, f"Bonus of {bonusvalue} added to your account")

        elif bonusStatus != 0:
            currentTimes = datetime.datetime.now()
            timeDifference = currentTimes - bonusStatus
            if timeDifference > datetime.timedelta(days=1):
                infos = mycol.update_one({"userid":message.from_user.id},{ "$set": { "balance": user.get("balance")+bonusvalue , "bonus": currentTimes }})
                bot.send_message(message.chat.id, f"Bonus of {bonusvalue} added to your account")
            else:
                remainingTime = datetime.timedelta(days=1) - timeDifference
                remainingHours  = remainingTime.seconds//3600
                remainingMinutes = (remainingTime.seconds//60)%60
                remainingSeconds = remainingTime.seconds - remainingHours*3600 - remainingMinutes*60
                bot.send_message(message.chat.id, f"Bonus already claimed. You can claim again after {remainingHours} hours {remainingMinutes} minutes {remainingSeconds} seconds")
        else:
            remaining_time = timedelta(days=1) - timeDifference
            remaining_hours  = remaining_time.seconds//3600
            remaining_minutes = (remaining_time.seconds//60)%60
            remaining_seconds = remaining_time.seconds - remaining_hours*3600 - remaining_minutes*60
            bot.send_message(message.chat.id, f"Bonus already claimed. You can claim again after {remaining_hours} hours {remaining_minutes} minutes {remaining_seconds} seconds")

    else:
        bot.send_message(message.chat.id, "You are not registered in the bot. Please use /start to register")

@bot.message_handler(commands=['export'])
def handle_export(message):
    # Fetch the data from MongoDB collection
    cursor = mycol.find()

    # Create a DataFrame from the cursor
    selected_columns = ['username', 'name', 'userid', 'balance', 'totalInvited', 'invitedBy']
    df = pd.DataFrame(list(cursor), columns=selected_columns)

    # Specify the output file path and name
    output_file = 'output.xlsx'

    # Export the DataFrame to Excel
    df.to_excel(output_file, index=False)

    # Send the exported file to the user
    with open(output_file, 'rb') as file:
        bot.send_document(message.chat.id, file)

    # Delete the temporary file
    os.remove(output_file)

@bot.inline_handler(lambda query: query.query == 'sgt')
def query_text(inline_query):
    print(inline_query)
    try:
        r = types.InlineQueryResultArticle('1', 'Send Suggestion', types.InputTextMessageContent('hi' , parse_mode="Markdown" , disable_web_page_preview=True , entities=None ))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('hi'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: query.query == 'photo1')
def query_photo(inline_query):
    try:
        r = types.InlineQueryResultPhoto('1',
                                         'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/kitten.jpg',
                                         'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/kitten.jpg',
                                         input_message_content=types.InputTextMessageContent('hi'))
        r2 = types.InlineQueryResultPhoto('2',
                                          'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/rooster.jpg',
                                          'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/rooster.jpg')
        bot.answer_inline_query(inline_query.id, [r, r2], cache_time=1)
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: query.query == 'video')
def query_video(inline_query):
    try:
        r = types.InlineQueryResultVideo('1',
                                         'https://github.com/eternnoir/pyTelegramBotAPI/blob/master/tests/test_data/test_video.mp4?raw=true',
                                         'video/mp4', 
                                         'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/rooster.jpg',
                                         'Title'
                                         )
        bot.answer_inline_query(inline_query.id, [r])
        print(inline_query)
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: len(query.query) == 0)
def default_query(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'default', types.InputTextMessageContent('default'))
        bot.answer_inline_query(inline_query.id, [r])
        
    except Exception as e:
        print(e)

# if no result found then this will be shown 
@bot.inline_handler(lambda query: True)
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'No results', types.InputTextMessageContent('hi'))
        bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)

bot.polling()