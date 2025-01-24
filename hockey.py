from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from app import app
from urllib.request import Request, urlopen
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, Game, Player, Goalie, GoalieGame, PlayerGame, FinalBet
from unidecode import unidecode
import requests
import time
import ipdb

html = requests.get(f"https://www.hockey-reference.com/leagues/NHL_2021_games.html", headers={'User-Agent':"Mozilla/5.0"})
doc = BeautifulSoup(html.text, 'html.parser')
rows = doc.select('tbody')[0].select('tr')

total_games= 0
even_games = 0
odd_games = 0


for game in rows:
    total_games+=1
    game_value = 0  
    odd_or_even = "odd"

    try:
        home=int(game.select('.right')[1].text)
    except:
        continue
    away=int(game.select('.right')[0].text)

    game_value = home+away

    if game_value%2==0:
        even_games+=1
        odd_or_even = "even"
    else:
        odd_games+=1
        odd_or_even = "odd"

    print(f'{home}, {away}, {odd_or_even}')


print(f'Total Games: {total_games}')
print(f'Odd Games: {odd_games}')
print(f'Even Games: {even_games}')
ipdb.set_trace()

