from settings import token
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           Message,  BotCommand, BotCommandScopeDefault)
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class TelegramBot:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.keyboard = self.create_keyboard()

    @staticmethod
    def create_keyboard():
        keyboard: list[KeyboardButton] = [
            KeyboardButton(text="Текущий спринт"),
            KeyboardButton(text="Выберите спринт")
        ]

        # Инициализируем билдер
        builder = ReplyKeyboardBuilder()

        builder.row(*keyboard)

        # Создаем объект клавиатуры, добавляя в него кнопки
        my_keyboard: ReplyKeyboardMarkup = builder.as_markup(
            resize_keyboard=True
        )

        return my_keyboard

    async def set_menu_commands(self):
        commands = [
            BotCommand(command="/start", description="Начать"),
        ]
        await self.bot.set_my_commands(commands, scope=BotCommandScopeDefault())

    def register_handlers(self):
        self.dp.message.register(self.process_start_command, CommandStart())

    async def process_start_command(self, message: Message):
        await message.answer(
            text='Выберите спринт',
            reply_markup=self.keyboard)

    async def run(self):
        self.register_handlers()
        await self.set_menu_commands()

        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(BOT)
        await self.bot.session.close()


if __name__ == '__main__':
    BOT = Bot(token)
    DP = Dispatcher()

    telegram_bot = TelegramBot(BOT, DP)
    asyncio.run(telegram_bot.run())