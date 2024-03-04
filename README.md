# Scheduled Message Telegram bot 

"Scheduled Message Telegram bot" - it is developed to send scheduled messages to users.

## Features

- Collecting mail from new users
- Send scheduled messages 
- The administrator can send a newsletter to all users

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/IlyaGrynyshyn/LectionBot

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Create the configuration file `.env` and add next parameters:
   ```bash
    BOT_TOKEN = 'your_telegram_bot_token'
    ADMINS = "your_telegram_id"

4. Run the bot:
    ```bash
     python -m bot

## Bot Commands
    
   `/start` - Start using the bot.

   `/post` - Send a newsletter to all users

   `/dump` - Make a database dump
