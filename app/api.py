import logging
import os
import json
from typing import Union

import aiofiles
import openai

from app.config import config
from app.db.mongo.documents import Moovie

log = logging.getLogger(__name__)

client = openai.Client()

def get_prompt_from_file(fp: Union[str, "os.PathLike[str]"]):
    try:
        with open(fp) as file:
            return file.read()
    except FileNotFoundError:
        log.error(
            f"Trying to get a prompt from file `{fp}` failed. Returning empty string."
        )
        return ""

async def get_mocked_completion():
    file_path = config.BASE_DIR / 'gpt_response.json'
    log.info(f'Using mock data `{file_path}` for posting.')
    async with aiofiles.open(file_path) as f:
        file_content = await f.read()
        return json.loads(file_content)
    
async def _get_completion(prompt: str = ""):
    if config.mock_data:
        return await get_mocked_completion()

    if not prompt:
        prompt = get_prompt_from_file(config.BASE_DIR / "prompt.txt")

    if prompt and isinstance(prompt, str):
        log.info('Asking ChatGPT....')

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "developer",
                    "content": 'Answer must be a JSON object',
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        answer = completion.choices[0].message.content

        log.info(f'ChatGPT answered:\n{answer}')

        current_response = json.loads(answer)

        # TODO: store in DB
        with open(config.BASE_DIR / 'openai_movies_response.json', 'r+') as file:
            responses = json.load(file)
            responses['all'].append(current_response)

            file.seek(0)
            file.write(json.dumps(responses, indent=2))

        return current_response

    log.warning("Couldn't parse a prompt. OpenAI API hasn't called")

    return {}

async def fetch_post_movie_data():
    moovie_data = await _get_completion()

    moovie = Moovie(**moovie_data)
    await moovie.insert()

    return moovie