import gettext
from fastapi import Query

_translations = {}

def load_translations():
    for lang in ["en", "fa"]:
        _translations[lang] = gettext.translation(
            domain="messages",
            localedir="locales",
            languages=[lang],
            fallback=True
        )

def translate(key: str, lang: str = "en") -> str:
    trans = _translations.get(lang, _translations.get("en"))
    return trans.gettext(key)
