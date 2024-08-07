# Import necessary modules
import os, re

from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
from predicd_data import GetPredicdData

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables from a .env file
load_dotenv(find_dotenv())

# Bot Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! I'm ready to give some tips");

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Custom Tips: {os.environ.get('TIP_TRIGGER')} (doubleChance) (win)");

async def tips_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(GetPredicdData(os.environ.get("PREDICD_AUTH_TOKEN"), os.environ.get("PREDICD_API_URL"), int(os.environ.get("DOUBLE_CHANCE_MIN")), int(os.environ.get("ONLY_WIN_MIN"))));

# Bot Responses
def handle_response(text: str) -> str:
    
    # Convert the text to lowercase
    processed: str = text.lower()

    if processed.startswith(os.environ.get("TIP_TRIGGER")):
        # Define the pattern to find all numbers
        pattern: Final = r'\d+'

        # Use findall() to get a list of all numbers found in the string
        numMatches = re.findall(pattern, processed)

        # Check if there are two numbers
        if len(numMatches) == 2:
            # Convert the list of number to a list of integers
            foundNumbers = [int(num) for num in numMatches]
            
            # Retrieve and return the predicted data
            return GetPredicdData(os.environ.get("PREDICD_AUTH_TOKEN"), os.environ.get("PREDICD_API_URL"), int(foundNumbers[0]), int(foundNumbers[1]))
        else:
            return f"Invalid Input!\n\nTry: {os.environ.get('TIP_TRIGGER')} (doubleChance) (win)"
            
    return "Invalid Command!"

# Asynchronously handle incoming messages based on the chat type and content
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
     # Get the type of chat ('private', 'group')
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # If the message is from a group chat
    if message_type == 'group':
        # Check if the bots username is mentioned in the message
        if os.environ.get("BOT_USERNAME") in text:
            new_text: str = text.replace(os.environ.get("BOT_USERNAME"), '').strip()
            
            # Handle the response based on the remaining text
            response: str = handle_response(new_text)
        else:
            # If the bots is not mentioned do nothing
            return
    else:
        # If the message is from a private chat handle the response directly
        response: str = handle_response(text)
    
    # Reply to the message with the generated response
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Print the update and the error that occurred to the console for debugging
    print(f"Update {update} caused error {context.error}")

# Entry point of the script when run as a standalone program
if __name__ == '__main__':

    # Create an instance of the Application with the bot access token from environment variables
    app = Application.builder().token(os.environ.get("BOT_ACCESS_TOKEN")).build()

    # Register command handlers for specific commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('tips', tips_command))

    # Register a message handler to process all text messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Register an error handler to handle any errors that occur
    app.add_error_handler(error)

    # Start polling for updates from the bot
    app.run_polling(poll_interval=2)