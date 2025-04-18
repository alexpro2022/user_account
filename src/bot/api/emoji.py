from src.config import bot_config as c


class Emoji:
    @staticmethod
    def get_emoji(emoji: str, flag: bool = c.bot_conf.emoji):
        return emoji if flag else ""

    BABY_ANGEL = get_emoji(" \U0001f47c ")
    OK = get_emoji(" \U0001f44d ")
    PREV_PAGE = get_emoji(" \U0001f446 ")
    NEXT_PAGE = get_emoji(" \U0001f447 ")
    PRESS_BUTTON = get_emoji(" \U0001f447 ")
    GO_BACK = get_emoji(" \U0001f448 ")
    GO_AHEAD = get_emoji(" \U0001f449 ")
    WRITING_HAND = get_emoji(" \U0000270d ")
    HANDSHAKE = get_emoji(" \U0001f91d ")
    CLAPPING_HANDS = get_emoji(" \U0001f44f ")
    SHRUGGING = get_emoji(" \U0001f937 ")
    ROCKET = get_emoji(" \U0001f680 ")
    TROPHY = get_emoji(" \U0001f3c6 ")
    COMPASS = get_emoji(" \U0001f9ed ")
    MICROPHONE = get_emoji(" \U0001f3a4 ")
    MAIL = get_emoji(" \U0001f4e8 ")
    STAR = get_emoji(" \U0001f31f ")
    EYE = get_emoji(" 👁️ ")
    MEDAL = get_emoji(" 🏅 ")
    SAVE = get_emoji(" 💽 ")
    LIST = get_emoji(" 🧾 ")
    DEL = get_emoji(" ❌ ")
    STOP = get_emoji(" ⛔ ")
    DOOR = get_emoji(" 🚪 ")
