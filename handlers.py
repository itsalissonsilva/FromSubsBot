from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from lang_utils import translate, set_user_language
from keyboards import moderation_keyboard, publish_keyboard, rejection_reason_keyboard
from scheduler import schedule_publish
from config import settings
from utils import format_post
import asyncio

pending_posts = {}

def register_handlers(dp: Dispatcher):
    dp.message.register(on_start, CommandStart())
    dp.message.register(on_language, Command(commands=["language"]))
    dp.message.register(handle_user_submission, F.text | F.photo | F.video)
    dp.callback_query.register(handle_language_selection, F.data.startswith("lang:"))
    dp.callback_query.register(handle_moderation, F.data.startswith("approve:") | F.data.startswith("reject:"))
    dp.callback_query.register(publish_now, F.data.startswith("publish_now:"))
    dp.callback_query.register(ask_date, F.data.startswith("ask_date:"))
    dp.callback_query.register(handle_rejection_reason, F.data.startswith("reject_reason:"))

async def on_start(message: Message):
    await message.answer(translate(message.from_user.id, "welcome"))

async def on_language(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="English", callback_data="lang:en"),
         InlineKeyboardButton(text="Русский", callback_data="lang:ru")]
    ])
    await message.answer(translate(message.from_user.id, "select_language"), reply_markup=kb)

async def handle_language_selection(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    set_user_language(callback.from_user.id, lang)
    await callback.message.edit_text(translate(callback.from_user.id, "welcome"))

async def handle_user_submission(message: Message):
    post_id = message.message_id
    content = {
        "user_id": message.from_user.id,
        "username": message.from_user.username or "Unknown",
        "text": message.text,
        "photo": message.photo[-1].file_id if message.photo else None,
        "video": message.video.file_id if message.video else None
    }
    pending_posts[post_id] = content

    await message.answer(translate(message.from_user.id, "await_moderation"))
    caption = f"Запрос от @{content['username']}:\n\n{content['text'] or ''}"
    media = content["photo"] or content["video"]

    if media:
        if content["photo"]:
            await bot.send_photo(settings.MODERATOR_CHAT_ID, media, caption=caption, reply_markup=moderation_keyboard(post_id))
        elif content["video"]:
            await bot.send_video(settings.MODERATOR_CHAT_ID, media, caption=caption, reply_markup=moderation_keyboard(post_id))
    else:
        await bot.send_message(settings.MODERATOR_CHAT_ID, caption, reply_markup=moderation_keyboard(post_id))

async def handle_moderation(callback: CallbackQuery):
    action, post_id = callback.data.split(":")
    post_id = int(post_id)
    post = pending_posts.get(post_id)

    if not post:
        await callback.answer(translate(callback.from_user.id, "moderation_rejected"), show_alert=True)
        return

    if action == "reject":
        await bot.send_message(callback.message.chat.id,
            translate(callback.from_user.id, "rejection_reason"),
            reply_markup=rejection_reason_keyboard(post_id))
    elif action == "approve":
        await callback.message.edit_text(translate(callback.from_user.id, "moderation_approved"))
        await bot.send_message(callback.message.chat.id,
            format_post(post, hashtag="#fromSubs"),
            reply_markup=publish_keyboard(post_id),
            parse_mode="Markdown"
        )