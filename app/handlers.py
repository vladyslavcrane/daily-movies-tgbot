from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, BotCommand

from app.config import config
from app.jobs import post_movie

router = Router()


async def set_default_commands(bot):
    await bot.set_my_commands(
        [
            BotCommand(
                command="postrandommovie", description="Запостить рандомный фильм"
            ),
            BotCommand(
                command="postcontentfromfile",
                description="Запостить контент из файла (.json)",
            ),
            BotCommand(
                command="postcontentfromjson",
                description="Запостить контент из JSON-объекта",
            ),
        ]
    )


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    user = message.from_user
    await message.reply(f"Hello, {user}. Click on a menu to see available commands.")


@router.message(Command("postrandommovie"))
async def post_movie_handler(message: Message, bot) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    user = message.from_user

    if not user.username == config.OWNER_USERNAME:
        await message.answer(f"You can't perform this action.")
        return

    await message.answer(f"Posting...")
    await post_movie(bot, config.MOOVIES_CHAT_USERNAME, user)

@router.callback_query(F.data == "edit_post")
async def edit_post_handler(callback: CallbackQuery):
    await callback.answer("...")
    await callback.message.answer("ok")
