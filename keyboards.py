from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def moderation_keyboard(post_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Approve", callback_data=f"approve:{post_id}"),
         InlineKeyboardButton(text="❌ Reject", callback_data=f"reject:{post_id}")]
    ])

def publish_keyboard(post_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 Publish now", callback_data=f"publish_now:{post_id}")],
        [InlineKeyboardButton(text="🗓 Schedule", callback_data=f"ask_date:{post_id}")]
    ])

def rejection_reason_keyboard(post_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Default reason", callback_data=f"reject_reason:Default reason")],
        [InlineKeyboardButton(text="Does not meet rules", callback_data=f"reject_reason:Does not meet rules")]
    ])