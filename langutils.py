from aiogram.types import User

# Словарь с переводами
translations = {
    "en": {
        "welcome": "Welcome! Send text, images, or videos for moderation.",
        "await_moderation": "Your post has been sent for moderation. Please wait.",
        "moderation_approved": "Post approved. Choose publication time:",
        "moderation_rejected": "Post rejected.",
        "select_language": "Choose your language:",
        "post_published": "The post has been published.",
        "enter_date": "Enter the publication date in the format `DD.MM HH:MM`.",
        "rejection_reason": "Enter the rejection reason or select a default option:",
        "rejected_reason": "Your post was rejected. Reason: {reason}",
    },
    "ru": {
        "welcome": "Добро пожаловать! Отправьте текст, изображение или видео для модерации.",
        "await_moderation": "Ваш пост отправлен на модерацию. Пожалуйста, ожидайте.",
        "moderation_approved": "Пост одобрен. Выберите время публикации:",
        "moderation_rejected": "Пост отклонен.",
        "select_language": "Выберите язык:",
        "post_published": "Пост опубликован.",
        "enter_date": "Введите дату и время публикации в формате `ДД.ММ ЧЧ:ММ`.",
        "rejection_reason": "Введите причину отказа или выберите стандартный вариант:",
        "rejected_reason": "Ваш пост был отклонен. Причина: {reason}",
    }
}

# Хранилище языковых настроек (вместо базы данных)
user_languages = {}

def get_user_language(user_id: int) -> str:
    """Получить язык пользователя. По умолчанию английский."""
    return user_languages.get(user_id, "en")

def set_user_language(user_id: int, language: str):
    """Сохранить язык пользователя."""
    user_languages[user_id] = language

def translate(user_id: int, key: str, **kwargs) -> str:
    """Перевести сообщение для пользователя."""
    lang = get_user_language(user_id)
    text = translations.get(lang, {}).get(key, key)
    return text.format(**kwargs)