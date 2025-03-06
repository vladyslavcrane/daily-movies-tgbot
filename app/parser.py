import re
import logging
import requests
from bs4 import BeautifulSoup


log = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


def find_poster_image_src(soup):
    div_ipc_media = soup.find(class_="ipc-media")
    img_poster = div_ipc_media.img
    return strip_media_amazon_url(
        img_poster["src"], delimeter="@@" if "@@" in img_poster["src"] else "@"
    )


def find_movie_photos_src(soup, limit=4):
    section_photos = soup.find("section", attrs={"data-testid": "Photos"})
    img_photos = section_photos.find_all("img", limit=limit)
    return [
        strip_media_amazon_url(
            img["src"], delimeter="@@" if "@@" in img["src"] else "@"
        )
        for img in img_photos
    ]


def strip_media_amazon_url(url, delimeter="@"):
    images_sub_pattern = re.compile(rf"(?<={delimeter}).*(?=\.)")
    stripped_url = re.sub(images_sub_pattern, "._V1_QL75", url)
    return stripped_url


def parse_imdb_urls(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, features="html.parser")

    try:
        poster_url = find_poster_image_src(soup)

    except (KeyError, AttributeError, TypeError) as exc:
        log.exception("Parsing `{url}` movie poster failed with `{exc}`")
        poster_url = ""
    try:
        photos_url = find_movie_photos_src(soup)
    except (KeyError, AttributeError, TypeError) as exc:
        log.exception("Parsing `{url}` movie's photos failed with exception: {exc}")
        photos_url = []

    return [poster_url, *photos_url]
