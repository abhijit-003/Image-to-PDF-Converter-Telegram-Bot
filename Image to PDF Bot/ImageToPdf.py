import logging
import os
import aiohttp
import sqlite3
import asyncio
from collections import defaultdict
#from PIL import Image
import img2pdf
from pdf2image import convert_from_path
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your token
TELEGRAM_BOT_TOKEN = 'TELEGRAM_BOT_TOKEN'

# Database setup
conn = sqlite3.connect('subscriptions.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS converterBotUsers (user_id INTEGER PRIMARY KEY)''')
conn.commit()

text =f"""
I'm here to assist you:💡

/help - get help.
    
Convert images to PDF:
/image2pdf - sending images.
/convert2pdf - convert to pdf.

Convert PDF to images:
/pdf2image - Send a pdf.
/convert2image - convert into images.

/cancel - cancel any operation.
"""
    
# Other update class methods for bot
#     chat_id = update.message.chat_id
#     message_id = update.message.message_id
#     user_id = update.message.from_user.id
#     username = update.message.from_user.username
#     message_text = update.message.text

# Helper Methods
# To tell user details on console
def log_user_data(update):
    """Log and track user data."""
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    logger.info(f"User ID: {user_id}, Username: {username}")

    # Insert user data into database if not already exists
    cursor.execute(
        "INSERT OR IGNORE INTO converterBotUsers (user_id) VALUES (?)",
        (user_id,)
    )
    conn.commit()

# Giver user message details in console
def log_user_chat(update):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    message = update.message.text
    
    logger.info(f"{user_id} {username} Text: {message}")

# Bot Handler Methods
# /start command Handler 
async def start(update: Update, context: CallbackContext):
    """Handle the /start command."""
    logger.info("File Conversion Bot Strted...")
    log_user_data(update)
    
    await update.message.reply_text(f"🌟 Welcome to the File Conversion Bot, {update.message.from_user.username}!\n 🌟 {text} ")


# /help Command handler
async def help_handler(update: Update, context: CallbackContext):
    """Handle the /help command."""
    await update.message.reply_text(text)

# /stop command handler
async def stop(update: Update, context: CallbackContext):
    """Handle the /stop command."""
    logger.info("Image to PDF Conversion Bot Stoped...!!")
    await update.message.reply_text("Bot stopped. Type /start to resume.")


# message update feature code
async def send_loading_message(update: Update, context: CallbackContext, stage: str):
    """Send a status message to the user during processing."""
    await update.message.reply_text(f"Processing your {stage}... Please wait.")

# User-specific storage for images and states
user_sessions = defaultdict(lambda: {"images": [], "collecting": False})

# Command to start image collection
async def start_image_collection(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_sessions[user_id]["images"] = []
    user_sessions[user_id]["collecting"] = True

    await update.message.reply_text(
        "Send me images, and I will combine them into a single PDF. \n Use \n/convert2pdf to finish, or \n/cancel to stop."
    )

# Command to stop collecting images
async def cancel_image_collection(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_sessions[user_id]["collecting"]:
        user_sessions[user_id] = {"images": [], "collecting": False}
        await update.message.reply_text("Operation canceled. You can start again with /image2pdf.")
    else:
        await update.message.reply_text("No active image collection to cancel.")

# Collect images from user
async def collect_images(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if not user_sessions[user_id]["collecting"]:
        await update.message.reply_text("Please use /image2pdf to start collecting images.")
        return

    # Save the received image
    try:
        file = update.message.photo[-1]
        file_info = await file.get_file()
        file_path = f"image_{update.message.message_id}.jpg"

        # Download the image
        async with aiohttp.ClientSession() as session:
            async with session.get(file_info.file_path) as resp:
                with open(file_path, "wb") as f:
                    f.write(await resp.read())

        # Append the file path to the user's session
        user_sessions[user_id]["images"].append(file_path)
        await update.message.reply_text(f"{len(user_sessions[user_id]['images'])} Image(s) added!")
    except Exception as e:
        logger.error(f"Error in collect_images: {e}")
        await update.message.reply_text("Failed to process the image. Please try again.")

# Command to finalize and convert images to a single PDF
async def convert_to_pdf(update: Update, context: CallbackContext):
    log_user_data(update)
    logger.info("Image to PDF Conversion Strted...")
    user_id = update.message.from_user.id
    
    if not user_sessions[user_id]["collecting"]:
        await update.message.reply_text("No images have been collected.\n Start with /image2pdf.")
        return

    if not user_sessions[user_id]["images"]:
        await update.message.reply_text("No images were sent. Please send some images first.")
        return

    user_sessions[user_id]["collecting"] = False  # Stop collecting images

    # Combine all images into a single PDF
    try:
        # Notify the user about the start of the process
        await send_loading_message(update, context, "image")
        
        output_pdf_path = f"Img2PDF_{user_id}.pdf"
        with open(output_pdf_path, "wb") as f:
            f.write(img2pdf.convert(user_sessions[user_id]["images"]))
            

        # Notify the user that the PDF is ready
        await update.message.reply_text("Conversion complete. Sending your PDF...")

        # Send the PDF back to the user
        with open(output_pdf_path, "rb") as pdf:
            await update.message.reply_document(pdf)

        await update.message.reply_text("Your PDF is ready! 😊")
    except Exception as e:
        logger.error(f"Error in convert_to_pdf: {e}")
        await update.message.reply_text("An error occurred while creating the PDF. Please try again.")
    finally:
        # Clean up temporary files
        for img_path in user_sessions[user_id]["images"]:
            if os.path.exists(img_path):
                os.remove(img_path)

        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)

        # Clear the session data
        user_sessions[user_id] = {"images": [], "collecting": False}


# User-specific storage for PDFs and states
user_pdf_sessions = defaultdict(lambda: {"pdf": None, "collecting": False})

# Command to start PDF collection
async def start_pdf_collection(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_pdf_sessions[user_id]["pdf"] = None
    user_pdf_sessions[user_id]["collecting"] = True

    await update.message.reply_text(
        "Send me a PDF, and I will convert it to images. Use /convert2image to finish, or /cancel to stop."
    )

# Collect PDF from the user
async def collect_pdf(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if not user_pdf_sessions[user_id]["collecting"]:
        await update.message.reply_text("Please use /pdf2image to start sending a PDF.")
        return

    # Save the received PDF
    try:
        file = update.message.document
        if file.mime_type != "application/pdf":
            await update.message.reply_text("Please upload a valid PDF file.")
            return

        file_info = await file.get_file()
        file_path = f"pdf_{update.message.message_id}.pdf"

        # Set a higher timeout value (e.g., 60 seconds)
        timeout = aiohttp.ClientTimeout(total=60)

        # Download the PDF
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(file_info.file_path) as resp:
                    with open(file_path, "wb") as f:
                        f.write(await resp.read())
        except asyncio.TimeoutError:
            logger.error(f"Timeout while downloading {file_info.file_path}")
            await update.message.reply_text("The operation timed out. Please try again later.")
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            await update.message.reply_text("An error occurred while downloading the file. Please try again.")

        # Save the PDF path in the session
        user_pdf_sessions[user_id]["pdf"] = file_path
        await update.message.reply_text("PDF received! Use /convert2image to start conversion.")
    except Exception as e:
        logger.error(f"Error in collect_pdf: {e}")
        await update.message.reply_text("Failed to process the PDF. Please try again.")

# Convert PDF to images
async def convert_to_images(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if not user_pdf_sessions[user_id]["collecting"]:
        await update.message.reply_text("No PDF has been sent. Start with /pdf2image.")
        return

    pdf_path = user_pdf_sessions[user_id]["pdf"]
    if not pdf_path:
        await update.message.reply_text("No PDF was sent. Please send a PDF first.")
        return

    user_pdf_sessions[user_id]["collecting"] = False  # Stop collecting PDFs

    try:
        # Notify the user about the conversion process
        await send_loading_message(update, context, "PDF")

        # Convert the PDF to images
        images = convert_from_path(pdf_path)

        # Notify the user about the images being sent
        await update.message.reply_text(f"Conversion complete. Sending {len(images)} images...")

        # Send each page as an image
        for idx, img in enumerate(images):
            image_path = f"{pdf_path.replace('.pdf', '')}_page_{idx + 1}.jpg"
            img.save(image_path, "JPEG")

            with open(image_path, "rb") as f:
                await update.message.reply_photo(f)

            os.remove(image_path)  # Clean up each image after sending it

        await update.message.reply_text("All images have been sent! 😊")
    except Exception as e:
        logger.error(f"Error in convert_to_images: {e}")
        await update.message.reply_text("An error occurred while processing your PDF. Please try again.")
    finally:
        # Clean up the original PDF file
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        # Clear the session data
        user_pdf_sessions[user_id] = {"pdf": None, "collecting": False}

# /cancel command handler
async def cancel_operation(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    # Check if the user is in the middle of an image collection
    if user_id in user_sessions and user_sessions[user_id]["collecting"]:
        user_sessions[user_id] = {"images": [], "collecting": False}
        await update.message.reply_text("Image collection operation canceled. You can start again with /image2pdf.")
        return

    # Check if the user is in the middle of a PDF collection
    if user_id in user_pdf_sessions and user_pdf_sessions[user_id]["collecting"]:
        user_pdf_sessions[user_id] = {"pdf": None, "collecting": False}
        await update.message.reply_text("PDF collection operation canceled. You can start again with /pdf2image.")
        return

    # If no active session
    await update.message.reply_text("No active operation to cancel.")

# Chat text handler
async def chat(update: Update, context: CallbackContext):
    """Handle unrecognized text messages."""
    log_user_chat(update)
    reply = f"Sorry, I can't process your text! 😢\n{text}"
    await update.message.reply_text(reply)

# error handler
async def error_handler(update: Update, context: CallbackContext):
    """Handle unexpected errors."""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text("An unexpected error occurred. Please try again later.")


# Main function to run the bot
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("cancel", cancel_operation))
    
    # command handler image to pdf 
    application.add_handler(CommandHandler("image2pdf", start_image_collection))
    application.add_handler(CommandHandler("convert2pdf", convert_to_pdf))
    
    # Command handlers pdf to image 
    application.add_handler(CommandHandler("pdf2image", start_pdf_collection))
    application.add_handler(CommandHandler("convert2image", convert_to_images))
    
    # Message handlers
    application.add_handler(MessageHandler(filters.PHOTO, collect_images))
    application.add_handler(MessageHandler(filters.Document.MimeType("application/pdf"), collect_pdf))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Error handler
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()
