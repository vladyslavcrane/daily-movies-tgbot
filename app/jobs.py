import logging
import pdb
from typing import Dict, Optional
from aiogram import Bot

from aiogram.types import Message, URLInputFile, User
from aiogram.utils.media_group import MediaGroupBuilder
from app.templates import get_rendered_template
from app.api import fetch_post_movie_data
from app.parser import parse_imdb_urls
from app.keyboards import admin_inline

log = logging.getLogger(__name__)


async def post_movie(bot: Bot, chat_id: int, user: Optional[User] = None) -> Dict:
    # image = URLInputFile(openai_response["poster_image_url"])
    moovie = await fetch_post_movie_data()

    album_builder = MediaGroupBuilder()
    media_urls = parse_imdb_urls(moovie.imdb_link)

    for media_url in media_urls:
        try:
            media_file = URLInputFile(media_url)
            album_builder.add_photo(media=media_file)
        except:
            log.info(f'failed to add photo `{media_url}`')
            pass

    try:
        moovie.genres = ", ".join(g.lower() for g in moovie.genres)
        moovie.director = (
            moovie.director
            if isinstance(moovie.director, str)
            else ", ".join(moovie.director)
        )
        moovie.actors = ", ".join(moovie.actors)

        caption = get_rendered_template("post_random_movie.html", {'obj': moovie})
        album_builder.caption = caption

        log.info(f'Posting with data:\n{moovie}')

        messages = await bot.send_media_group(chat_id=chat_id, media=album_builder.build())
        
        if user:
            await bot.forward_messages(chat_id=user.id, from_chat_id=chat_id, message_ids=[message.message_id for message in messages])
            await bot.send_message(text="Post success!", chat_id=user.id, reply_markup=admin_inline)
            await moovie.update({'$set': {'posted': True}})

    except Exception as e:
        await bot.send_message(text='Post failed', chat_id=user.id)
        log.exception(f"Error posting movie: {e}")
