class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    API_ID = 27386028
    API_HASH = "213f0f9fa79670df4db888afa7bad14f"

    CASH_API_KEY = "QA9PEESE00DCDEIH"  # Get this value for currency converter from https://www.alphavantage.co/support/#api-key

    DATABASE_URL = "postgres://dkpooiwa:m5zv9E9zxlWmqSmV4JpvTAq8AwGgfXA3@manny.db.elephantsql.com/dkpooiwa"  # A sql database url from elephantsql.com

    EVENT_LOGS = (-1002664907086)  # Event logs channel to note down important bot level events

    MONGO_DB_URI = "mongodb+srv://new69502:Gaurav@gaurav.3hyfz.mongodb.net/?retryWrites=true&w=majority&appName=Gaurav"  # Get ths value from cloud.mongodb.com

    # Telegraph link of the image which will be shown at start command.
    START_IMG = "https://te.legra.ph/file/40eb1ed850cdea274693e.jpg"

    SUPPORT_CHAT = "Fake_Scout"  # Your Telegram support group chat username where your users will go and bother you

    TOKEN = "7906475321:AAExx0rr0gNfwYaiZa8YfTQNiEG-qe9AUwY"  # Get bot token from @BotFather on Telegram

    TIME_API_KEY = "5EREIPTJM5JV"  # Get this value from https://timezonedb.com/api

    OWNER_ID = 6878311635  # User id of your telegram account (Must be integer)

    # Optional fields
    BL_CHATS = []  # List of groups that you want blacklisted.
    DRAGONS = []  # User id of sudo users
    DEV_USERS = []  # User id of dev users
    DEMONS = []  # User id of support users
    TIGERS = []  # User id of tiger users
    WOLVES = []  # User id of whitelist users

    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = 8


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
