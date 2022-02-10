__version__ = (1, 0, 0)
"""
    █ █ ▀ █▄▀ ▄▀█ █▀█ ▀    ▄▀█ ▀█▀ ▄▀█ █▀▄▀█ ▄▀█
    █▀█ █ █ █ █▀█ █▀▄ █ ▄  █▀█  █  █▀█ █ ▀ █ █▀█

    Copyright 2022 t.me/hikariatama
    Licensed under the Creative Commons CC BY-NC-ND 4.0

    Full license text can be found at:
    https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

    Human-friendly one:
    https://creativecommons.org/licenses/by-nc-nd/4.0
"""

# <3 title: SpotifyDownloader
# <3 pic: https://img.icons8.com/fluency/48/000000/spotify.png
# <3 desc: Downloads track from spotify

from .. import loader, utils
from telethon.tl.types import *


@loader.tds
class SpotifyDownloaderMod(loader.Module):
    """Скачивание музыки из Spotify"""
    strings = {
        'name': 'Музыка Spotify'
    }

    async def client_ready(self, client, db):
        self.db = db
        self.client = client

    @loader.unrestricted
    async def sdcmd(self, message: Message) -> None:
        """<track> - найти и сказать музыку из Spotify"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "<b>❌ Возможно, вы не указали название музыки</b>")

        message = await utils.answer(message, "<b>⚡️ Скачиваю...</b>")
        try:
            message = message[0]
        except:
            pass
        music = await self.client.inline_query('spotifysavebot', args)
        for mus in music:
            if mus.result.type == 'audio':
                await self.client.send_file(message.peer_id, mus.result.document, reply_to=message.reply_to_msg_id)
                return await message.delete()

        return await utils.answer(message, f"<b>🥺 Название музыки: <code> {args} </code> не найдено. </b>")
