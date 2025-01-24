from datetime import datetime
from bs4 import BeautifulSoup
from app import app
from urllib.request import Request, urlopen
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, Game, Player, Goalie, GoalieGame, PlayerGame
from statistics import mean,mode,median,stdev
from unidecode import unidecode
import time
import requests
import ipdb



with app.app_context():



    for player in Player.query.all():

        games = player.games

        average = mean([game.pp_corsi + game.even_corsi for game in games])

        for game in games:

            if (game.even_corsi + game.pp_corsi) > average+2.1:
                game.shot_stdev = average*1.6
            else:
                game.shot_stdev = game.even_corsi + game.pp_corsi

        print(f'{player}: {round(average,2)}')

    db.session.commit()