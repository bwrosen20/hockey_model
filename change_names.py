from datetime import datetime
from bs4 import BeautifulSoup
from app import app
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
        games = player.games
        for index,game in enumerate(games):
            game_team = game.team
            if index==0 or index == 1:
                try:
                    next_game = games[index+1]
                except IndexError:
                    continue
                try:
                    game_after = games[index+2]
                except IndexError:
                    continue
                if ((next_game.game.home==game_team or next_game.game.visitor==game_team) and (game_after.game.home==game_team or game_after.game.visitor==game_team)):
                    continue
                else:
                    game.team=game.game.home
            elif index==len(games)-1 or index==len(games)-2:
                try:
                    two_games_ago = games[index-2]
                except IndexError:
                    continue
                try:
                    last_game = games[index-1]
                except IndexError:
                    continue
                if ((two_games_ago.game.home==game_team or two_games_ago.game.visitor==game_team) and (last_game.game.home==game_team or last_game.game.visitor==game_team)):
                    continue
                else:
                    game.team=game.game.home
            else:
                try:
                    two_games_ago = games[index-2]
                except IndexError:
                    continue
                try:
                    previous_game = games[index-1]
                except IndexError:
                    continue
                try:
                    next_game = games[index+1]
                except IndexError:
                    continue
                try:
                    game_after = games[index+2]
                except IndexError:
                    continue
                if ((next_game.game.home==game_team or next_game.game.visitor==game_team) and (game_after.game.home==game_team or game_after.game.visitor==game_team)) or ((two_games_ago.game.home==game_team or two_games_ago.game.home==game_team) and (previous_game.game.home==game_team or previous_game.game.visitor==game_team)):
                    continue
                else:
                    game.team=game.game.home

    ipdb.set_trace()


    # for goalie in goalies:
    #     new_name = unidecode(goalie.name.replace('AP','o').replace('S1/2','y').replace('A!A!','as').replace('A%?','a').replace('dA','dre').replace('ASS','c').replace('A"',"e").replace('i!','a').replace('tA','te').replace('A$?','a').replace('i(c)','e').replace('i!','a').replace('lA','li').replace('A(c)','e').replace('rAA!','rna').replace('AA','ci').replace('mA','mi').replace('A 1/4','u').replace('A,','o').replace('A!A','ac').replace('A 3/4','z').replace('A ','S').replace('A!','a').replace('AY=','a').replace('A 1/2','y').replace('eAA!','era').replace('A<<','u').replace('i 1/4','u').replace('aA','ar'))
    #     goalie.name=new_name
    #     print(new_name)


    # db.session.commit()