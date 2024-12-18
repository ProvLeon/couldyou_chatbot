# couldyou_chatbot/telegram_bot/bot.py
import os
import logging
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ChatAction, ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from utils import create_formatted_response, format_api_response
from config import Config
from session_manager import SessionManager
from typing import List

# Initialize session manager
session_manager = SessionManager()

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()

def get_welcome_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="How to Use", callback_data="how_to_use"),
            InlineKeyboardButton(text="Safety Info", callback_data="safety")
        ],
        [
            InlineKeyboardButton(text="FAQs", callback_data="faqs"),
            InlineKeyboardButton(text="Contact Us", callback_data="contact")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_website_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="Visit Website", url="https://couldyou.org")
        ]]
    )

async def send_safety_info(message: types.Message):
    safety_text = (
        "🛡️ *Safety Information*\n\n"
        "*General Safety Guidelines:*\n"
        "• _Made from medical\\-grade silicone_\n"
        "• *Safe to wear up to 12 hours*\n"
        "• Can be used overnight\n"
        "• Does not affect virginity\n"
        "• Cannot get lost inside body\n\n"
        "*Important Precautions:*\n"
        "• `Always wash hands before handling`\n"
        "• Clean cup thoroughly between uses\n"
        "• Do not use soap on the cup\n"
        "• Store in breathable cotton bag\n"
        "• Replace if damaged\n\n"
        "*When to Consult Healthcare Provider:*\n"
        "• _Abnormal bleeding or pain_\n"
        "• Existing gynecological conditions\n"
        "• During pregnancy\n"
        "• If using IUD\n\n"
        "[Click here for more safety information](https://couldyou.org/safety)\n\n"
        "⚠️ *TSS Information:*\n"
        "_Toxic Shock Syndrome risk is very low with menstrual cups compared to tampons\\. "
        "However, if you experience fever, rash, or flu\\-like symptoms, "
        "remove the cup and seek medical attention\\._"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Safety Guidelines",
            url="https://couldyou.org/safety"
        )
    ]])

    await message.answer(
        safety_text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=keyboard
    )

async def send_faqs(message: types.Message):
    faq_text = (
        "❓ *Frequently Asked Questions*\n\n"
        "*How long can I wear the cup?*\n"
        "Up to 12 hours, depending on flow\\.\n\n"
        "*Will I still be a virgin if I use the cup?*\n"
        "Yes\\! Using a menstrual cup does not affect virginity\\.\n\n"
        "*Can the cup get lost inside me?*\n"
        "No, it's physically impossible for the cup to get lost\\.\n\n"
        "*Is it safe to sleep with the cup?*\n"
        "Yes, you can safely wear it overnight\\.\n\n"
        "*What if I have heavy periods?*\n"
        "The cup can hold 3\\-5 times more than tampons\\.\n\n"
        "*How long does the cup last?*\n"
        "With proper care, up to 10\\+ years\\.\n\n"
        "*Can I use it with an IUD?*\n"
        "Yes, but consult your healthcare provider first\\.\n\n"
        "*How do I clean it?*\n"
        "Boil for 5 minutes between cycles, rinse with water during use\\.\n\n"
        "_Have more questions? Feel free to ask\\!_"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="More FAQs",
            url="https://couldyou.org/faq"
        )
    ]])

    await message.answer(
        faq_text,
        parse_mode="MarkdownV2",
        reply_markup=keyboard
    )

async def send_contact_info(message: types.Message):
    contact_text = (
        "📞 *Contact Information*\n\n"
        "*Need Support?*\n"
        "We're here to help\\!\n\n"
        "*Email:*\n"
        "mycup@couldyou\\.org\n\n"
        "*Phone:*\n"
        "\\(888\\) 994\\-1961\n\n"
        "*Social Media:*\n"
        "• Facebook: @couldyoucup\n"
        "• Instagram: @couldyoucup\n"
        "• Twitter: @couldyoucup\n\n"
        "*Website:*\n"
        "www\\.couldyou\\.org\n\n"
        "*Office Hours:*\n"
        "Monday\\-Friday: 9AM\\-5PM EST\n\n"
        "*Emergency Support:*\n"
        "For medical emergencies, please contact your healthcare provider "
        "or visit the nearest medical facility\\.\n\n"
        "_We typically respond to inquiries within 24 hours_"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Visit Website",
                    url="https://couldyou.org"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Email Us",
                    url="mailto:mycup@couldyou.org"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Facebook",
                    url="https://facebook.com/couldyoucup"
                ),
                InlineKeyboardButton(
                    text="Instagram",
                    url="https://instagram.com/couldyoucup"
                )
            ]
        ]
    )

    await message.answer(
        contact_text,
        parse_mode="MarkdownV2",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

# Add these helper functions for reusability
def get_back_to_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="↩️ Back to Main Menu",
                callback_data="start"
            )
        ]]
    )

# Add this case to your callback handler
@dp.callback_query(lambda c: c.data == "start")
async def back_to_start(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await cmd_start(callback_query.message)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        "🌸 *Welcome to CouldYou? Cup Assistant\\!*\n\n"
        "I'm here to help you with:\n"
        "✨ *Information about menstrual health*\n"
        "📱 *CouldYou? Cup usage guidance*\n"
        "❓ *Answering your questions*\n"
        "🔍 *Finding resources*\n\n"
        "_How can I assist you today\\?_"
    )
    await message.answer(
        welcome_text,
        parse_mode="MarkdownV2",
        reply_markup=get_welcome_keyboard()
    )

@dp.callback_query()
async def handle_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    if callback_query.data == "how_to_use":
        await send_usage_guide(callback_query.message)
    elif callback_query.data == "safety":
        await send_safety_info(callback_query.message)
    elif callback_query.data == "faqs":
        await send_faqs(callback_query.message)
    elif callback_query.data == "contact":
        await send_contact_info(callback_query.message)

async def send_usage_guide(message: types.Message):
    guide_text = (
        "📝 *CouldYou? Cup Usage Guide*\n\n"
        "*Before First Use:*\n"
        "1\\. Wash the cotton storage bag\n"
        "2\\. Boil the cup for 5 minutes\n"
        "3\\. Let it air dry\n\n"
        "*To Insert:*\n"
        "1\\. Wash hands thoroughly\n"
        "2\\. Fold the cup\n"
        "3\\. Insert gently\n"
        "4\\. Ensure it opens fully\n\n"
        "_Need more detailed instructions? Just ask\\!_"
    )
    await message.answer(
        guide_text,
        parse_mode="MarkdownV2",
        reply_markup=get_website_keyboard()
    )

def get_interactive_keyboard():
    """Create an interactive keyboard with common actions"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📖 Usage Guide", callback_data="how_to_use"),
            InlineKeyboardButton(text="❓ FAQs", callback_data="faqs")
        ],
        [
            InlineKeyboardButton(text="🛡️ Safety Info", callback_data="safety"),
            InlineKeyboardButton(text="📞 Contact Us", callback_data="contact")
        ],
        [
            InlineKeyboardButton(text="🌐 Visit Website", url="https://couldyou.org"),
            InlineKeyboardButton(text="📱 Share Feedback", callback_data="feedback")
        ]
    ])

async def send_long_message(message: types.Message, chunks: List[str]):
    """Send long messages with progress indicators"""
    total_chunks = len(chunks)
    for i, chunk in enumerate(chunks, 1):
        if total_chunks > 1:
            chunk += f"\n\n_Part {i} of {total_chunks}_"

        await message.answer(
            chunk,
            parse_mode="MarkdownV2",
            reply_markup=get_interactive_keyboard() if i == total_chunks else None,
            # disable_web_page_preview=True
        )

        if i < total_chunks:
            await asyncio.sleep(0.5)  # Prevent flooding



@dp.message()
async def handle_message(message: types.Message):
    user_id = str(message.from_user.id)

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{Config.BACKEND_URL}/api/chat",
                json={
                    "message": message.text,
                    "session_id": user_id,
                    "language": message.from_user.language_code or "en"
                }
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    response_text = result["response"]["text"]

                    # Format the response with proper Markdown
                    formatted_text = format_api_response(response_text)
                    formatted_chunks = create_formatted_response(formatted_text)

                    # Send using the long message handler
                    await send_long_message(message, formatted_chunks)
                else:
                    await message.answer(
                        "❌ *Sorry\\!* I'm having trouble processing your request\\. "
                        "Please try again later\\.",
                        parse_mode=ParseMode.MARKDOWN_V2
                    )
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        await message.answer(
            "⚠️ *Oops\\!* Something went wrong\\. "
            "Please try again or contact support if the issue persists\\.",
            parse_mode=ParseMode.MARKDOWN_V2
        )
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
