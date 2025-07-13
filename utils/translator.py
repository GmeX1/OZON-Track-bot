from googletrans import Translator
import re

async def translate(text: str, split=True) -> str:
    if split:
        text = re.sub(r"(\w)([A-Z])", r"\1 \2", text)

    async with Translator(raise_exception=True, timeout=1) as translator:
        tries = 5
        ex = None
        while tries > 0:
            try:
                return (await translator.translate(text, dest='ru')).text
            except Exception as ex:
                tries -= 1
        raise ex