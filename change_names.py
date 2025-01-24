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



with app.app_context():



    bets = FinalBet.query.all()

    current_date = bets[0].date.date()


    i=0
    while i <1:
        todays = [bet for bet in bets if bet.date.date()==current_date][0:5]




        print(f'\n{current_date}')
        for thing in todays:

            player_who_played = Player.query.filter(Player.name==thing.name).first()


            try:
                yesterdays_game = player_who_played.games[-1]
            except AttributeError:

                last_name = name.split(' ')[-1]
                first_two_letters = name.split(' ')[0][0:2]
                new_player_object_list = [guy for guy in Player.query.all() if guy.name.split(' ')[-1]==last_name]
                # if player["name"]=="Matthew Boldy":
                #     ipdb.set_trace()
                
                
                if len(new_player_object_list)==1:
                    player_who_played = new_player_object_list[0]
                elif len(new_player_object_list)>1:
                    newer_player_object_list = [guy for guy in new_player_object_list if guy.name.split(' ')[0][0:2]==first_two_letters]
                    if len(newer_player_object_list)==1:
                        player_who_played = newer_player_object_list[0]
                    else:
                        print(f'{player["name"]} not in database')
                        continue

                else:
                    print(f'{player["name"]} not in database')
                    continue

            try: 
                shots = [game for game in player_who_played.games if game.game.date.date()==current_date][0].shots
            except IndexError:
                shots = 0

            name = thing.name
            regular = thing.line
            prop = thing.prop
            arrays = thing.arrays
            low_stdev = thing.low_stdev
            if thing.result==0:
                result = "❌"
            elif thing.result==1:
                result = "✅"
            else:
                result = "✅✅✅"
            string_output = f"{name} {regular} {prop}"
            string_output = string_output.ljust(40,'.')

            print(f"{string_output} {result}, Actual: {shots}, (Arrays: {arrays}, Stdev: {low_stdev})")
        current_date = current_date+timedelta(1)
        if datetime.now().date()==current_date:
            i=1


    # for goalie in goalies:
    #     new_name = unidecode(goalie.name.replace('AP','o').replace('S1/2','y').replace('A!A!','as').replace('A%?','a').replace('dA','dre').replace('ASS','c').replace('A"',"e").replace('i!','a').replace('tA','te').replace('A$?','a').replace('i(c)','e').replace('i!','a').replace('lA','li').replace('A(c)','e').replace('rAA!','rna').replace('AA','ci').replace('mA','mi').replace('A 1/4','u').replace('A,','o').replace('A!A','ac').replace('A 3/4','z').replace('A ','S').replace('A!','a').replace('AY=','a').replace('A 1/2','y').replace('eAA!','era').replace('A<<','u').replace('i 1/4','u').replace('aA','ar'))
    #     goalie.name=new_name
    #     print(new_name)


    # db.session.commit()