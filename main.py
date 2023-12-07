from fastapi import FastAPI
from pydantic import BaseModel
from HdRezkaApi import *
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Ссылка на поиск
search_url = 'https://hdrezka.ag/search/?do=search&subaction=search&q='

# Заголовок что-бы понимал что-мы заходим с  реального устройства
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

# Модель запроса
class Request(BaseModel):
    name: str
    year: str
    genre: str
    engname: str
    season: str
    episode: str


# Роутер с API-методом
@app.post("/api/link/")
async def create_link(req: Request):
    
    #Получаем данные из тела запроса
    reqName = req.name 
    reqYear = req.year
    reqGenre = req.genre
    reqEngName = req.engname


    # Составляем ссылку для поиска с query параметрами
    url = f'{search_url} + {reqName} + {reqYear} + {reqGenre} + {reqEngName}'

    # Делаем запрос на посик фильма на сайте
    search_res = requests.get(url, headers=headers)
    # Парсит данные
    soup = BeautifulSoup(search_res.content, "lxml")
    # print(soup) Проверка полученных данных
    search_results = soup.find("div", class_="b-content__inline_item")
    # print(search_results) Проверка полученных данных
    # Получаем ссылку из массива
    link = search_results.get('data-url')
    # print(link) Проверка правильности ссылки

    

    # Проверка на то что ссылка присутствует
    if not link:
        print("По вашему запросу ничего не найдено.")
    else:
        rezka = HdRezkaApi(link)
        filmSeason = req.season
        filmEpisode = req.episode
        if filmSeason == '': stream = rezka.getStream()
        else: stream = rezka.getStream(filmSeason, filmEpisode)
        return {
        "Name": rezka.name,
        "Link": stream,
        }
