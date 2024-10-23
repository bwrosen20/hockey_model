from datetime import datetime
from bs4 import BeautifulSoup
from app import app
from operator import itemgetter
from urllib.request import Request, urlopen
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, Game, Player, Goalie, GoalieGame, PlayerGame
from unidecode import unidecode
import time
import requests
import ipdb



with app.app_context():



    players = [player for player in Player.query.all()]
    goalies = [goalie for goalie in Goalie.query.all()]


    for player in players:
        for other_player in players:
            if player.id!=other_player.id:
                if player.name==other_player.name:
                    first_games = player.games
                    second_games = other_player.games
                    new_games = first_games + second_games
                    # sorted_new_games = sorted(new_games,key=itemgetter('game.date'))
                    db.session.delete(other_player)
                    players = Player.query.all()
                    player.games = new_games
                    print(f'{player} updated')

    # for goalie in goalies:

    #     for other_goalie in goalies:
    #         if goalie.id!=other_goalie.id:
    #             if goalie.name==other_goalie.name:
    #                 first_games = goalie.games
    #                 second_games = other_goalie.games
    #                 new_games = first_games + second_games
    #                 # sorted_new_games = sorted(new_games,key=itemgetter('game.date'))
    #                 db.session.delete(other_goalie)
    #                 goalie.games = new_games
    #                 print(f'{player} updated')
       

    # db.session.commit()
    ipdb.set_trace()