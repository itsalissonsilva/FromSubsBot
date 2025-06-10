import asyncio
from aiogram import Bot
from config import settings

async def schedule_publish(delay: float, content: dict):
    await asyncio.sleep(delay)
    bot = Bot(token=settings.API_TOKEN)
    await bot.send_message(
        settings.CHANNEL_ID,
        f"#fromSubs\n\n{content.get('text', '')}"
    )