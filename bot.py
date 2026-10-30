import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
# Get your token from @BotFather on Telegram
TOKEN = os.environ.get("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Image filenames (Make sure these images are in the same folder as bot.py)
IMAGES = [
    "image1.jpg", # Cockfight
    "image2.jpg", # Joker/Shark
    "image3.jpg", # Cat Jackpot
    "image4.jpg", # Casino Live
    "image5.jpg", # P99
    "image6.jpg"  # Lotto88
]

# Message Text
WELCOME_TEXT = """
Wecome To 855GOAL

សូមស្វាគមន៍មកកាន់គេហទំព័រ 855GOAL ដែលជាគោលដៅដ៏ល្អបំផុតសម្រាប់អ្វីៗគ្រប់យ៉ាងដែលទាក់ទងនឹងការបង្កើនសមត្ថភាព និងការសម្រេចគោលដៅរបស់អ្នក។ សូមស្វែងយល់ពីធនធាន គន្លឹះ និងឧបករណ៍នានាដែលត្រូវបានរៀបចំឡើងដើម្បីផ្តល់ថាមពល និងការគាំទ្រដល់អ្នកនៅលើដំណើរឆ្ពោះទៅរកភាពជោគជ័យ។
"""

# Button Links
DM_LINK = "https://t.me/Game855GOAL"
WEBSITE_LINK = "https://heylink.me/855goal/"
CHANNEL_LINK = "https://t.me/GOALWIN855"

# Create the keyboard layout
def get_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("DM NOW", url=DM_LINK),
            InlineKeyboardButton("WEBSITE", url=WEBSITE_LINK),
        ],
        [
            InlineKeyboardButton("CHANNEL", url=CHANNEL_LINK)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- BOT FUNCTIONS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Send the Welcome Message with the FIRST image
    try:
        with open(IMAGES[0], 'rb') as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=WELCOME_TEXT,
                reply_markup=get_keyboard()
            )
    except FileNotFoundError:
        logger.error(f"Image {IMAGES[0]} not found. Sending text only.")
        await context.bot.send_message(
            chat_id=chat_id,
            text=WELCOME_TEXT,
            reply_markup=get_keyboard()
        )

    # Schedule the 3-hour recurring reminder
    # First, check if a job already exists for this user to prevent duplicates
    current_jobs = context.job_queue.get_jobs_by_name(str(user_id))
    for job in current_jobs:
        job.schedule_removal()

    # Run the reminder job every 3 hours (10800 seconds)
    context.job_queue.run_repeating(
        send_reminder,
        interval=10800, # 3 hours
        first=10800,    # Wait 3 hours before the first reminder (since welcome was just sent)
        chat_id=chat_id,
        name=str(user_id)
    )

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Sends the recurring reminder message."""
    job = context.job
    chat_id = job.chat_id

    # Pick a random image from the list, excluding the first one (welcome image)
    import random
    image_to_send = random.choice(IMAGES[1:])

    try:
        with open(image_to_send, 'rb') as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=WELCOME_TEXT,
                reply_markup=get_keyboard()
            )
    except FileNotFoundError:
        logger.error(f"Image {image_to_send} not found.")
        await context.bot.send_message(
            chat_id=chat_id,
            text=WELCOME_TEXT,
            reply_markup=get_keyboard()
        )

# --- MAIN EXECUTION ---

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # Run the bot until the user presses Ctrl-C
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
