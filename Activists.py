__version__ = (1, 0, 1)
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

# <3 title: Активность
# <3 pic: https://img.icons8.com/fluency/48/000000/edit-message.png
# <3 desc: Поиск самых активных юзеров чата

from .. import loader, utils
from telethon.tl.types import *
import logging
import time

logger = logging.getLogger(__name__)


def get_link(user: User or Channel) -> str:
    return (
        f'tg://user?id={user.id}'
        if isinstance(user, User)
        else (
            f"tg://resolve?domain={user.username}"
            if getattr(user, 'username', None)
            else ""
        )
    )


def get_full_name(user: User or Channel) -> str:
    return (
        user.title
        if isinstance(user, Channel)
        else (
            str(user.first_name) + ' ' + str(
                user.last_name if getattr(user, 'last_name', False) else ''
            )
        )
    )


@loader.tds
class ActivistsMod(loader.Module):
    """Looks for the most active users in chat"""
    strings = {
        "name": "Активность",
        "searching": "🔎 <b>Начинаю сбор активных юзеров чата...\nЭто займет немного времени.</b>",
        "user": "👨🏻‍💻 {}. <a href=\"{}\">{}</a>: {} сообщений",
        "active": "⚡️ <b>Самые активные юзеры чата:</b>\n\n{}\n<i>Парсинг занял: {} секунд</i>"
    }

    async def client_ready(self, client, db) -> None:
        self.db = db
        self.client = client

    async def check_admin(self, chat: int or Chat, user_id: int or User) -> bool:
        try:
            return (await self.client.get_permissions(chat, user_id)).is_admin
        except Exception:
            return False

    async def activistscmd(self, message: Message) -> None:
        """[quantity] [-m <int>] - Поиск самых активных юзеров чата"""
        args = utils.get_args_raw(message)
        limit = None
        if '-m' in args:
            limit = int(''.join([_ for _ in args[args.find('-m') + 2:] if _.isdigit()]))
            args = args[:args.find('-m')].strip()

        quantity = int(args) if args.isdigit() else 15

        message = await utils.answer(message, self.strings('searching'))
        message = message[0] if isinstance(
            message, (list, tuple, set)) else message

        st = time.perf_counter()

        temp = {}
        async for msg in self.client.iter_messages(message.peer_id, limit=limit):
            user = getattr(msg, 'sender_id', False)
            if not user:
                continue

            if user not in temp:
                temp[user] = 0

            temp[user] += 1

        stats = [_[0] for _ in list(sorted([(user, q) for user, q in temp.items()], key=lambda x: x[1], reverse=True))]
        top_users = []
        for u in stats:
            if len(top_users) >= quantity:
                break

            if not await self.check_admin(message.peer_id, u):
                top_users += [(await self.client.get_entity(u), u)]

        top_users_formatted = [
            self.strings('user')\
                .format(
                    i + 1,
                    get_link(_[0]),
                    get_full_name(_[0]),
                    temp[_[1]]
                ) \
            for i, _ in enumerate(top_users)
        ]
        
        await utils.answer(message,
                            self.strings('active')\
                                .format(
                                    '\n'.join(top_users_formatted),
                                    round(time.perf_counter() - st, 2)
                                )
                        )
