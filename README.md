# Image-to-PDF-Converter-Telegram-Bot [@MakeImageToPDF_Bot](https://t.me/MakeImageToPDF_Bot) 🤖🎉

## Overview
**File Conversion Bot** is a Telegram bot designed to simplify file conversions. It enables users to convert images into PDFs and PDFs into individual images effortlessly. With intuitive commands like /image2pdf and /pdf2image, the bot provides a seamless and user-friendly experience for managing file transformations directly within Telegram.

## Features
### Image to PDF Conversion

  - Collect multiple images from the user.
  - Combine the images into a single PDF file.
  - Supports cancellation of ongoing operations.
### PDF to Image Conversion

  - Convert a PDF document into individual images (one image per page).
  - Send each page as an image to the user.
### User-Friendly Commands

  - Clear instructions and guided steps for all operations.
  - Option to cancel operations at any point.
### Error Handling

  - Provides user feedback for unsupported file types or unexpected errors.
  - Logs user activities for debugging purposes.

## Commands
### General Commands
| Command               | Description                                                        |
|-----------------------|--------------------------------------------------------------------|
| `/start`             | Welcomes the user and provides a list of available commands.       |
| `/help`              | Shows instructions and details about the bot's functionality.                                           |
| `/stop`             | Stops the bot's operations. You can resume using                   |
| `/cancel`             | Sends a motivational quote.                                        |


### Image to PDF Commands
| Command               | Description                                                        |
|-----------------------|--------------------------------------------------------------------|
| `/image2pdf`             | Starts the process of collecting images to convert into a PDF commands.       |
| `/convert2pdf`              | Finalizes the collected images and creates a single PDF file.functionality.                                           |


### PDF to Image Commands
| Command               | Description                                                        |
|-----------------------|--------------------------------------------------------------------|
| `/pdf2image`             | Starts the process of collecting a PDF to convert into images.       |
| `/convert2image`              | Converts the uploaded PDF into images and sends them back.                                           |


## Python Script
View bot source code on [**ImageToPDF_Bot**](https://github.com/abhijit-003/Image-to-PDF-Converter-Telegram-Bot/blob/main/Image%20to%20PDF%20Bot/ImageToPdf.py)

## Installation
### 1. Clone this repository:
```
git clone https://github.com/abhijit-003/Image-to-PDF-Converter-Telegram-Bot.git
```
### 2. Install dependencies: Ensure you have Python 3.8+ installed. Then install the required Python packages:

```
pip install -r requirements.txt
```
- dependencies file [**requirements.txt**](https://github.com/abhijit-003/Image-to-PDF-Converter-Telegram-Bot/blob/main/Image%20to%20PDF%20Bot/requirements.txt)
or
```
pip install aiohttp pillow img2pdf pdf2image python-telegram-bot
```

### 3. Set up the environment:

- Obtain a Telegram bot token by creating a bot on BotFather.
- Replace **TELEGRAM_BOT_TOKEN** in the code with your bot token.
### 4. Run the bot:
```python
python bot.py
```
## Example Usage
### Starting the Bot
- Open Telegram and search for your bot (created via BotFather).
- Start the bot by typing `/start`.
### Image to PDF Conversion
- Use `/image2pdf` to begin.
- Send one or more images.
- When finished, use `/convert2pdf` to receive a combined PDF.
### PDF to Image Conversion
- Use `/pdf2image` to begin.
- Upload a valid PDF file.
- Use `/convert2image` to receive the PDF pages as images.
### Cancel Operations
- At any point, type `/cancel` to stop the ongoing process.

## Dependencies
- **aiohttp:** For downloading files from Telegram.
- **Pillow (PIL):** For image processing.
- **img2pdf:** For converting images into PDF format.
- **pdf2image:** For converting PDFs into images.
- **Python Telegram Bot:** For interfacing with Telegram's API.
- 
## Learn Creating Telegram Bot
- To Get detailded infomation about starting creating [**Telegram**](https://telegram.org/) Bot visit [**Create Telegram Bot**](https://github.com/abhijit-003/How-to-Create-Telegram-Bot)


## Contributing
Feel free to contribute to the project by opening issues or submitting pull requests.

## License
This project is licensed under the MIT License.

## Acknowledgements
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/en/stable/)

---

## More Visisting Reposotories
- [**Telegram Bot Creation Begineer**](https://github.com/abhijit-003/How-to-Create-Telegram-Bot)<br>
- [**TelifyFactBot Telegram Bot**](https://github.com/abhijit-003/TelifyFactBot-Telegram-bot)


Happy chatting with your new Telegram bot! 🎉
