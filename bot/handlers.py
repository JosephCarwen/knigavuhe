import aiohttp
import aiofiles
import os

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from get_tracks_by_link import track_links


router = Router()



@router.message(F.text)
async def send_audio(message: Message):
    for index, title, url in track_links(message.text):
        file_path = f"{title}.mp3"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(file_path, mode='wb')
                    await f.write(await resp.read())
                    await f.close()
                else:
                    await message.answer(f"Не удалось скачать файл по ссылке {url}")
                    continue

        audio = FSInputFile(file_path)
        await message.answer_audio(audio)

        os.remove(file_path)

    await message.answer("Отправка завершена")