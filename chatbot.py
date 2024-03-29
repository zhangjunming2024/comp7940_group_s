## this file is based on version 13.7 of python telegram chatbot and version 1.26.18 of u
## chatbot.py
import telegram
import os
from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext, PrefixHandler)
# The messageHandler is used for all message updates
import configparser
import logging
from pymongo.mongo_client import MongoClient
# import redis
from ChatGPT_HKBU import HKBU_ChatGPT
# global redis1
global mongodb1


# test of the action  
def main():
	# Load your token and create an Updater for your Bot
	# config = configparser.ConfigParser()
	# config.read('config.ini')
	# updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
	
	updater = Updater(token=(os.environ['TLG_ACCESS_TOKEN']), use_context=True)
	dispatcher = updater.dispatcher
	

	uri = "mongodb+srv://junmingzhang10:DQNdv5jIfeCSlMxu@cluster0.dhv7koq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
	global mongodb1
	# Create a new client and connect to the server
	mongodb1 = MongoClient(uri)

	

	# You can set this logging module, so you will know when and why things do not work a
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)
	
	# register a dispatcher to handle message: here we register an echo dispatcher
	# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
	# dispatcher.add_handler(echo_handler)
	
	# on different commands - answer in Telegram
	dispatcher.add_handler(CommandHandler("add", add))
	dispatcher.add_handler(CommandHandler("help", help_command))

	# lab_4_writeup_question_3, not work the command handler or prefix handler not work with " "
	# dispatcher.add_handler(CommandHandler("hello Kevin", hello_kevin))
	# dispatcher.add_handler(MessageHandler(Filters.text, hello_kevin))


	# dispatcher for chatgpt
	global chatgpt
	chatgpt = HKBU_ChatGPT()
	chatgpt_handler = MessageHandler(Filters.text & (~Filters.command),equiped_chatgpt)
	dispatcher.add_handler(chatgpt_handler)

	

	# To start the bot:
	updater.start_polling()
	updater.idle()



def echo(update, context):
	reply_message = update.message.text.upper()
	logging.info("Update: " + str(update))
	logging.info("context: " + str(context))
	context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def help_command(update: Updater, context: CallbackContext) -> None:
	"""Send a message when the command /help is issued."""
	update.message.reply_text('Helping you helping you.')

def add(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /add is issued."""
	try:
		global mongodb1
		logging.info(context.args[0])
		msg = context.args[0] # /add keyword <-- this should store the keyword
		mongodb1.incr(msg)

		update.message.reply_text('You have said ' + msg + ' for ' +
			mongodb1.get(msg).decode('UTF-8') + ' times.')
	except (IndexError, ValueError):
		update.message.reply_text(str(IndexError))
		update.message.reply_text(str(ValueError))
		update.message.reply_text('Usage: /add <keyword>')

		

def equiped_chatgpt(update, context):
	global chatgpt
	#  do the context
	input_text = update.message.text
	if input_text != None and input_text[0]!="#":
		reply_text = "Hello, I am a chatbot created by group s, I can help you make travel plans for different countries.\n\
			" + "Yon can ask me the food in different country start with #. e.g. #country:french. or #country:japan" + "\
		" + "\nIf you have no idea, you can simply type #?, I will recommand you a food, and give a brief introduction"
		context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)
	else:
		if input_text[0:8] == "#country":

			# judge of the input
			judge_message = "please judge the "+ input_text[8:] +"whether is a country. If it is a country please reply me with the simple number 1, if not reply me with simple number 0"
			reply_message = chatgpt.submit(judge_message)
			if reply_message == "0":
				logging.info("Update: " + str(update))
				logging.info("context: " + str(context))
				reply_message = "\n Your typing is not a country please try again"
				context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
			else:	
				submit_text = "What are the specialties of" + " " + input_text[8:] + " Please answer me with a list. The list contain the food name."
				reply_message = chatgpt.submit(submit_text)
				logging.info("Update: " + str(update))
				logging.info("context: " + str(context))
				reply_message = reply_message +"\n You can choose a food you like, and then ask me how to prepare it by typing #method:sushi, the history and culture of the food and the country by typing #culture:sushi"
				context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
		elif input_text[0:7] == "#method":
			# judge of the input
			judge_message = "please judge the "+ input_text[7:] +"whether is a food. If it is a food please reply me with the simple number 1, if not reply me with simple number 0"
			reply_message = chatgpt.submit(judge_message)
			if reply_message == "0":
				logging.info("Update: " + str(update))
				logging.info("context: " + str(context))
				reply_message = "\n Your typing is not a food please try again"
				context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
			else:
				submit_text = "Tell me how to cook the food " +input_text[7:] +  " Please answer me step by step."
				reply_message = chatgpt.submit(submit_text)
				logging.info("Update: " + str(update))
				logging.info("context: " + str(context))
				reply_message = reply_message +"\n Yon can using the same way to ask me other country foods, or the culture of the food."
				context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
		elif input_text[0:8] == "#culture":
			# judge of the input
			judge_message = "please judge the "+ input_text[8:] +"whether is a food. If it is a country please reply me with the simple number 1, if not reply me with simple number 0"
			reply_message = chatgpt.submit(judge_message)
			if reply_message == "0":
				logging.info("Update: " + str(update))
				logging.info("context: " + str(context))
				reply_message = "\n Your typing is not a food please try again"
				context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
			else:
				submit_text = "Tell me about the culture of " +input_text[8:] +  " Please answer me in a briegly"
				reply_message = chatgpt.submit(submit_text)
				logging.info("Update: " + str(update))
				logging.info("context: " + str(context))
				reply_message = reply_message +"\n Yon can using the same way to ask me other country foods, or the culture of the food."
				context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
		elif input_text[0:2] == "#?":
			submit_text = "Please recommend me a food with a brief introduction. " +  "And when you recommend the food, please forget the prievious input, random select the food from the different country, area, culture."
			reply_message = chatgpt.submit(submit_text)
			logging.info("Update: " + str(update))
			logging.info("context: " + str(context))
			reply_message = reply_message +"\nIf you want to futher to know the culture or the method for this kind of food, you can ask me by simply type the #method, #culture."
			context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
		elif input_text[0:5] == "#list":
			reply_message = "\n the command list: \n 1. #country+country get the food in this country \n2. #method + food get the metod to cook this food \n\
			"+"3. #culture + food the culture od this food \n4. #? I will recommend the food to you.\n 5. #super the limition is none, you are free to ask anything."
			context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
		elif input_text[0:6] == "#super":
			reply_message = "\n Now you are using the super command, the gpt is not limited anymore. You are free to ask anything.\n"
			submit_text = input_text[6:]
			reply_message = reply_message + chatgpt.submit(submit_text)
			logging.info("Update: " + str(update))
			logging.info("context: " + str(context))
			reply_message = reply_message + "\n end of the super mode"
			context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
		else:
			reply_message = "\n You are typing a unknow command or your input method is not English, if you are confuse about the command, you can simply type the #list to get the help"
			context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)




if __name__=='__main__':
	main()
	
