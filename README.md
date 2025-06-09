# ✉️ FromSubsBot

**FromSubsBot** is a Telegram bot for moderation and delayed publication of user content in a Telegram channel. Suitable for publics where subscribers can send their thoughts or suggestions, and moderators can approve and publish them manually or on a schedule.

---

## 🚀 Features

- Receiving texts from subscribers.
- Transferring for moderation with the "Accept" / "Reject" buttons.
- Request for publication immediately or by date.
- Flexible parsing of the publication date.
- Secure storage of tokens and configuration via `.env`.

---

## 📦 Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/fromsubsbot.git
    cd fromsubsbot

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Create a .env file:
    ```ini
    API_TOKEN=your_bot_token
    MODERATOR_CHAT_ID=your_moderator_chat_id
    CHANNEL_ID=@your_channel_name
4. Run the bot:
    ```bash
    python main.py
---
🛠 Configuration
All configuration is stored centrally in the config.py file, which uses pydantic and dotenv.
    ```python
    
    from config import settings
    print(settings.API_TOKEN)
---
🔐 Security
All keys and tokens are moved to .env.

The .env file is added to .gitignore and should not be included in the public repository.
