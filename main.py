import asyncio
import logging
from utils import utils
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from os import getenv
from dotenv import load_dotenv; load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=getenv("API-KEY"), default=DefaultBotProperties(parse_mode = ParseMode.HTML))
dp = Dispatcher()

from json import load

with open('utils/strings.json') as file:
    strings = load(file)
    file.close()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.from_user.language_code not in strings.keys(): code = 'en'
    else: code = message.from_user.language_code
    await message.reply(strings[code]['greet'], disable_web_page_preview = True)

@dp.inline_query()
async def inline(query: types.InlineQuery):
    if query.from_user.language_code not in strings.keys(): code = 'en'
    else: code = query.from_user.language_code
    query_text = query.query
    if utils.ishex(query_text) == True:
        if len(query_text) == 7:
            color = query_text[1:]
        else:
            color = query_text

        title = strings[code]['title'].replace("<input>", query_text)
        response = utils.makeresponse(utils.generate(color), query_text, strings[code]['output'])
    elif (len(query_text.split(' ')) == 3) and all(utils.isnum(c) for c in query_text.split(' ')) and all(int(c) <= 255 for c in query_text.split(' ')) and all(int(c) >= 0 for c in query_text.split(' ')):
        rgb = query_text.split(' ')
        color = '%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))
        if utils.ishex(color) == True:
            title = strings[code]['title'].replace("<input>", query_text)
            response = utils.makeresponse(utils.generate(color), query_text, strings[code]['output'])
            strings[code]['title'].replace("<input>", query_text)
        else:
            response = strings[code]['badcolor']
            title = strings[code]['badcolor']
    elif query_text in utils.db.keys():
        color = utils.hexbycolorname(query_text)
        title = strings[code]['title'].replace("<input>", query_text)
        response = utils.makeresponse(utils.generate(color), query_text, strings[code]['output'])
    else:
        response = strings[code]['badcolor']
        title = strings[code]['badcolor']

    result = types.InlineQueryResultArticle(
        id = query.id,
        title = title,
        input_message_content = types.InputTextMessageContent(message_text=response)
    )

    await bot.answer_inline_query(query.id, results=[result])

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
