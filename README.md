# MatchMagic

This project is a python-based telegram bot that interacts with users to provide data from the [Predicd API](https://www.predicd.com/en/predicdAPI.html). 
The bot is built on top of the base telegram bot [BotFather](https://telegram.me/BotFather).

### Features

- Fetch and display data from the Predicd API.
- Interactive commands for user engagement.
- Basic error handling and logging.

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)
- A Telegram bot token from BotFather
- Access to the Predicd API

## `.env`
```env
# Predicd API
PREDICD_API_URL = "https://www.predicd.com/api/v1/matches/today/"
PREDICD_AUTH_TOKEN = "Token xxxxx"

# Predicd Settings
DOUBLE_CHANCE_MIN = 82
ONLY_WIN_MIN = 68

# Telegram Bot Settings
BOT_ACCESS_TOKEN = "xxxxx"
BOT_USERNAME = "@xxxxx"

# Telegram Bot Triggers
TIP_TRIGGER = "tips"

# Betting API
BETTING_API_URL = "https://api.betting-api.com/1xbet/football/line/all"
BETTING_AUTH_TOKEN = "xxxxx"

```