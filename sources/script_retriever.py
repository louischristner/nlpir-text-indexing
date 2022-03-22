import os
import re
import sys
import requests

from bs4 import BeautifulSoup
from functools import reduce


def get_movie_scripts(url, folder_name):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    a_attrs = { 'href': re.compile(r'\/Movie Scripts.+\.html$') }
    para_m = [ para.find_all('a', attrs=a_attrs) for para in soup.find_all('p') ]

    movies_script_name = [ movie.text.strip().replace(':', '').replace(' ', '-') for movie in reduce(lambda a, b: a + b, para_m) ]

    if len(movies_script_name) > 0 and not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for movie_script_name in movies_script_name:
        print(movie_script_name)
        movie_script_url = "https://imsdb.com/scripts/" + movie_script_name + ".html"

        movie_html_text = requests.get(movie_script_url).text
        movie_soup = BeautifulSoup(movie_html_text, 'html.parser')

        movie_pre_balise = movie_soup.find('pre')
        if movie_pre_balise != None:
            movie_script_text = movie_pre_balise.text.strip()
            if len(movie_script_text) != 0:
                file = open(folder_name + "/" + movie_script_name + ".txt", "w")
                file.write(movie_script_text)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        get_movie_scripts("https://imsdb.com/all-scripts.html", "movies")
    else: get_movie_scripts(sys.argv[1], sys.argv[2])
