import os
import pytest
from bs4 import BeautifulSoup

from app.parser import find_poster_image_src, find_movie_photos_src, strip_media_amazon_url

success_results = {
    "poster_url": "https://m.media-amazon.com/images/M/MV5BY2IzNzMxZjctZjUxZi00YzAxLTk3ZjMtODFjODdhMDU5NDM1XkEyXkFqcGc@._V1_QL75.jpg",
    "photos_url": [
        "https://m.media-amazon.com/images/M/MV5BMjI3MTU0ODQ2MF5BMl5BanBnXkFtZTcwNTQzNTIwNA@@._V1_QL75.jpg",
        "https://m.media-amazon.com/images/M/MV5BMTYzNDc3NzYzOF5BMl5BanBnXkFtZTcwNjQzNTIwNA@@._V1_QL75.jpg",
        "https://m.media-amazon.com/images/M/MV5BMTMwNjcyOTIzOV5BMl5BanBnXkFtZTcwNzQzNTIwNA@@._V1_QL75.jpg",
        "https://m.media-amazon.com/images/M/MV5BMTI5MTUxNDI2NV5BMl5BanBnXkFtZTcwOTQzNTIwNA@@._V1_QL75.jpg",
    ],
}
DIR_NAME = os.path.dirname(__file__)


class TestParser:

    @pytest.fixture
    def soup(self):
        with open(os.path.join(DIR_NAME, "test_soup.html")) as f:
            html = f.read()
        return BeautifulSoup(html, features="html.parser")

    def test_find_poster_image_src(self, soup):
        assert find_poster_image_src(soup) == success_results["poster_url"]

    def test_find_movie_photos_src(self, soup):
        assert find_movie_photos_src(soup) == success_results["photos_url"]
    
    @pytest.mark.parametrize('test_input, expected', [
        ["https://m.media-amazon.com/images/M/MV5BY2IzNzMxZjctZjUxZi00YzAxLTk3ZjMtODFjODdhMDU5NDM1XkEyXkFqcGc@._V1_QL75_UX190_CR0,8,190,281_.jpg", "https://m.media-amazon.com/images/M/MV5BY2IzNzMxZjctZjUxZi00YzAxLTk3ZjMtODFjODdhMDU5NDM1XkEyXkFqcGc@._V1_QL75.jpg"],
        ["1234", "1234"],
        ["http://localhost:8000/image/test@QWERTY.jpg", "http://localhost:8000/image/test@._V1_QL75.jpg"],

    ])
    def test_strip_media_amazon_url(self, test_input, expected):
        assert strip_media_amazon_url(test_input) == expected
        
    @pytest.mark.parametrize('test_input, expected', [
        ["1234", "1234"], 
        ["1@@3.png", "1@@._V1_QL75.png"], 
        ["https://m.media-amazon.com/images/M/MV5BMjI3MTU0ODQ2MF5BMl5BanBnXkFtZTcwNTQzNTIwNA@@._V1_QL75_UX321_.jpg", "https://m.media-amazon.com/images/M/MV5BMjI3MTU0ODQ2MF5BMl5BanBnXkFtZTcwNTQzNTIwNA@@._V1_QL75.jpg"], 
         
    ])
    def test_strip_media_amazon_url_with_delimeter(self, test_input, expected):
        assert strip_media_amazon_url(test_input, delimeter='@@') == expected
