import asyncio
from datetime import datetime
from dateutil import parser as date_parser

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from config import settings

bot = Bot(token=settings.API_TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()

pending_posts = {}


@dp.message(CommandStart())
async def on_start(message: Message):
    await message.answer("Бот запущен. Отправь текст для публикации.")


@dp.message(F.text)
async def route_text_messages(message: Message):
    for post_id, post in pending_posts.items():
        if post.get("awaiting_date_from") == message.from_user.id:
            await handle_schedule_date(message, post_id, post)
            return
    await handle_user_submission_logic(message)


async def handle_user_submission_logic(message: Message):
    post_id = message.message_id
    pending_posts[post_id] = {
        'user_id': message.from_user.id,
        'content': message.text
    }

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Accept", callback_data=f"approve:{post_id}"),
         InlineKeyboardButton(text="❌ Decline", callback_data=f"reject:{post_id}")]
    ])

    await bot.send_message(settings.MODERATOR_CHAT_ID,
                           f"Запрос от @{message.from_user.username or 'Unknown'}:\n\n{message.text}",
                           reply_markup=kb)


@dp.callback_query(F.data.startswith('approve:') | F.data.startswith('reject:'))
async def handle_moderation(callback: CallbackQuery):
    action, post_id_str = callback.data.split(':')
    post_id = int(post_id_str)
    post = pending_posts.get(post_id)

    if not post:
        await callback.answer("Пост не найден или уже обработан.", show_alert=True)
        return

    if action == 'reject':
        await callback.message.edit_text("Пост отклонён.")
        pending_posts.pop(post_id, None)
    else:
        await callback.message.edit_text("Пост одобрен. Запрашиваем время публикации...")
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📤 Опубликовать сейчас", callback_data=f"publish_now:{post_id}")],
            [InlineKeyboardButton(text="🗓 Указать дату", callback_data=f"ask_date:{post_id}")]
        ])
        await bot.send_message(callback.from_user.id,
                               f"Пост:\n\n{post['content']}\n\nКак опубликовать?",
                               reply_markup=markup)


@dp.callback_query(F.data.startswith("publish_now:"))
async def publish_now(callback: CallbackQuery):
    post_id = int(callback.data.split(":")[1])
    post = pending_posts.get(post_id)

    if post:
        await bot.send_message(settings.CHANNEL_ID, f"#fromSubs\n\n{post['content']}")
        await callback.message.edit_text("Пост опубликован.")
        pending_posts.pop(post_id, None)


@dp.callback_query(F.data.startswith("ask_date:"))
async def ask_date(callback: CallbackQuery):
    post_id = int(callback.data.split(":")[1])
    post = pending_posts.get(post_id)

    if not post:
        await callback.answer("Пост не найден.", show_alert=True)
        return

    post['awaiting_date_from'] = callback.from_user.id
    await callback.message.edit_text(
        "Введите дату публикации в любом формате.\n\nНапример:\n`09.06 15:30` или `09.06.2025 1530`",
        parse_mode=ParseMode.MARKDOWN
    )


async def handle_schedule_date(message: Message, post_id: int, post: dict):
    try:
        dt = date_parser.parse(message.text, dayfirst=True)
        now = datetime.now()
        delay = (dt - now).total_seconds()

        if delay < 0:
            await message.reply("Дата уже прошла. Пожалуйста, введите новую.")
            return

        await message.reply(f"Пост запланирован на {dt.strftime('%d-%m-%Y %H:%M:%S')}")
        asyncio.create_task(schedule_publish(post_id, post['content'], delay))
    except Exception as e:
        await message.reply(f"Ошибка разбора даты: {e}")


async def schedule_publish(post_id: int, content: str, delay: float):
    await asyncio.sleep(delay)
    await bot.send_message(settings.CHANNEL_ID, f"#fromSubs\n\n{content}")
    pending_posts.pop(post_id, None)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
