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
        new_name = unidecode(player.name.replace('AP','o').replace('S1/2','y').replace('A!A!','as').replace('A%?','a').replace('dA','dre').replace('ASS','c').replace('A"',"e").replace('i!','a').replace('tA','te').replace('A$?','a').replace('i(c)','e').replace('i!','a').replace('lA','li').replace('A(c)','e').replace('rAA!','rna').replace('AA','ci').replace('mA','mi').replace('A 1/4','u').replace('A,','o').replace('A!A','ac').replace('A 3/4','z').replace('A ','S').replace('A!','a').replace('AY=','a').replace('A 1/2','y').replace('eAA!','era').replace('A<<','u').replace('i 1/4','u').replace('aA','ar'))
        player.name=new_name
        print(new_name)

    for goalie in goalies:
        new_name = unidecode(goalie.name.replace('AP','o').replace('S1/2','y').replace('A!A!','as').replace('A%?','a').replace('dA','dre').replace('ASS','c').replace('A"',"e").replace('i!','a').replace('tA','te').replace('A$?','a').replace('i(c)','e').replace('i!','a').replace('lA','li').replace('A(c)','e').replace('rAA!','rna').replace('AA','ci').replace('mA','mi').replace('A 1/4','u').replace('A,','o').replace('A!A','ac').replace('A 3/4','z').replace('A ','S').replace('A!','a').replace('AY=','a').replace('A 1/2','y').replace('eAA!','era').replace('A<<','u').replace('i 1/4','u').replace('aA','ar'))
        goalie.name=new_name
        print(new_name)


    db.session.commit()