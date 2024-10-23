# from turtle import ht
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
    
    

    # for year in years:

    years = ["2018","2019","2020","2021","2022","2023"]

    for year in years:   

            
        # headers = {'user-agent': 'my-app/0.0.1'}
        html = requests.get(f"https://www.hockey-reference.com/leagues/NHL_{year}_games.html", headers={'User-Agent':"Mozilla/5.0"})
        # date = html.select('div.ScheduleDay_sd_GFE_w')[0]
        doc = BeautifulSoup(html.text, 'html.parser')
        rows = doc.select('tbody')[0].select('tr')

        # rows.pop(0)

        # ipdb.set_trace()
        games = []

        for game in rows:


            url_ending = game.select('a')[0].get("href")

            # ipdb.set_trace()

            box_score_url = f"https://www.hockey-reference.com{url_ending}"

            box_score = requests.get(box_score_url, headers={'User-Agent':"Mozilla/5.0"})

            box_score_data = BeautifulSoup(box_score.text, 'lxml')

            visitor =  box_score_data.select('.scorebox')[0].select('strong')[0].select('a')[0].text
            home =  box_score_data.select('.scorebox')[0].select('strong')[1].select('a')[0].text


            away_score =  box_score_data.select('.scorebox')[0].select('.score')[0].text
            home_score = box_score_data.select('.scorebox')[0].select('.score')[1].text


            site_time = box_score_data.select('.scorebox')[0].select(".scorebox_meta")[0].select('div')[0].text

            real_time = datetime.strptime(site_time,"%B %d, %Y, %I:%M %p")
            location = box_score_data.select('.scorebox')[0].select(".scorebox_meta")[0].select('div')[2].text.replace('Arena: ','')



            match = Game(
                visitor = visitor,
                home = home,
                away_score = away_score,
                home_score = home_score,
                location = location,
                date = real_time
            )
            
            # db.session.add(match)


            away_players = box_score_data.select('tbody')[0].select('tr')
            away_goalie = box_score_data.select('tbody')[1].select('tr')
            home_players = box_score_data.select('tbody')[2].select('tr')
            home_goalie = box_score_data.select('tbody')[3].select('tr')

            away_advanced_even =  box_score_data.select('tbody')[6].select('tr')
            away_advanced_pp =  box_score_data.select('tbody')[7].select('tr')

            home_advanced_even =  box_score_data.select('tbody')[13].select('tr')
            home_advanced_pp =  box_score_data.select('tbody')[14].select('tr')


            home_even_corsi = 0
            away_even_corsi = 0
            home_even_hits = 0
            away_even_hits = 0 
            home_even_blocks = 0
            away_even_blocks = 0
            home_pp_corsi = 0
            away_pp_corsi = 0
            home_pp_hits = 0
            away_pp_hits = 0
            home_pp_blocks = 0
            away_pp_blocks = 0
            away_penalty_mins = 0
            home_penalty_mins = 0

            for goalie in away_goalie:
                name = unidecode(goalie.select('td')[0].text.replace('AP','o').replace('S1/2','y').replace('A!A!','as').replace('A%?','a').replace('dA','dre').replace('ASS','c').replace('A"',"e").replace('i!','a').replace('tA','te').replace('A$?','a').replace('i(c)','e').replace('i!','a').replace('lA','li').replace('A(c)','e').replace('rAA!','rna').replace('AA','ci').replace('mA','mi').replace('A 1/4','u').replace('A,','o').replace('A!A','ac').replace('A 3/4','z').replace('A ','S').replace('A!','a').replace('AY=','a').replace('A 1/2','y').replace('eAA!','era').replace('A<<','u').replace('i 1/4','u').replace('aA','ar'))
                if name=="Empty Net":
                    break

                goals = int(goalie.select('td')[2].text)
                saves = int(goalie.select('td')[3].text)
                penalty_minutes = int(goalie.select('td')[7].text)
                minutes_string = goalie.select('td')[8].text
                minutes = (float(minutes_string[-2:])/60)+int(minutes_string[-5:2].replace(':',''))

                away_penalty_mins+=penalty_minutes

                goalie_game = GoalieGame(
                    goals = goals,
                    saves = saves,
                    penalty_minutes = penalty_minutes,
                    minutes = minutes
                )

                if (name in [person.name for person in Goalie.query.all()]):
                    assoc_player = Goalie.query.filter(Goalie.name == name).first()
                else:
                    assoc_player = Goalie(name=name)
                    db.session.add(assoc_player)
                    # db.session.commit()


                goalie_game.goalie = assoc_player
                goalie_game.game = match
                db.session.add(goalie_game)
                # db.session.commit()

            for goalie in home_goalie:
                name = unidecode(goalie.select('td')[0].text.replace('AP','o').replace('S1/2','y').replace('A!A!','as').replace('A%?','a').replace('dA','dre').replace('ASS','c').replace('A"',"e").replace('i!','a').replace('tA','te').replace('A$?','a').replace('i(c)','e').replace('i!','a').replace('lA','li').replace('A(c)','e').replace('rAA!','rna').replace('AA','ci').replace('mA','mi').replace('A 1/4','u').replace('A,','o').replace('A!A','ac').replace('A 3/4','z').replace('A ','S').replace('A!','a').replace('AY=','a').replace('A 1/2','y').replace('eAA!','era').replace('A<<','u').replace('i 1/4','u').replace('aA','ar'))
                if name=="Empty Net":
                    break
                goals = int(goalie.select('td')[2].text)
                saves = int(goalie.select('td')[3].text)
                penalty_minutes = int(goalie.select('td')[7].text)
                minutes_string = goalie.select('td')[8].text
                minutes = (float(minutes_string[-2:])/60)+int(minutes_string[-5:2].replace(':',''))

                away_penalty_mins+=penalty_minutes

                goalie_game = GoalieGame(
                    goals = goals,
                    saves = saves,
                    penalty_minutes = penalty_minutes,
                    minutes = minutes
                )

                if (name in [person.name for person in Goalie.query.all()]):
                    assoc_player = Goalie.query.filter(Goalie.name == name).first()
                else:
                    assoc_player = Goalie(name=name)
                    db.session.add(assoc_player)
                    # db.session.commit()


                goalie_game.goalie = assoc_player
                goalie_game.game = match
                db.session.add(goalie_game)
                # db.session.commit()
    


            for index, player in enumerate(away_players[0:-1]):
                name = unidecode(player.select('td')[0].text.replace('AP','o').replace('S1/2','y').replace('A!A!','as').replace('A%?','a').replace('dA','dre').replace('ASS','c').replace('A"',"e").replace('i!','a').replace('tA','te').replace('A$?','a').replace('i(c)','e').replace('i!','a').replace('lA','li').replace('A(c)','e').replace('rAA!','rna').replace('AA','ci').replace('mA','mi').replace('A 1/4','u').replace('A,','o').replace('A!A','ac').replace('A 3/4','z').replace('A ','S').replace('A!','a').replace('AY=','a').replace('A 1/2','y').replace('eAA!','era').replace('A<<','u').replace('i 1/4','u').replace('aA','ar'))
                goals = int(player.select('td')[1].text)
                assists = int(player.select('td')[2].text)
                points = int(player.select('td')[3].text)
                team = visitor
                pp_goals = int(player.select('td')[7].text)
                pp_assists = int(player.select('td')[11].text)
                shots = int(player.select('td')[13].text)
                penalty_minutes = int(player.select('td')[5].text)
                
                minutes_string = player.select('td')[16].text
                minutes = (int(minutes_string[-2:])/60)+int(minutes_string[-5:2].replace(':',''))


                try:
                    skater_advanced_even = away_advanced_even[index]
                except IndexError:
                    break

                even_corsi = int(skater_advanced_even.select('td')[0].text)
                even_on_ice_corsi = int(skater_advanced_even.select('td')[1].text)
                even_on_ice_against_corsi = int(skater_advanced_even.select('td')[2].text)
                even_hits = int(skater_advanced_even.select('td')[8].text)
                try:
                    even_blocks = int(skater_advanced_even.select('td')[9].text)
                except ValueError:
                    even_blocks=0

                skater_advanced_pp = away_advanced_pp[index]

                pp_corsi = int(skater_advanced_pp.select('td')[0].text)
                pp_on_ice_corsi = int(skater_advanced_pp.select('td')[1].text)
                pp_on_ice_against_corsi = int(skater_advanced_pp.select('td')[2].text)
                pp_hits = int(skater_advanced_pp.select('td')[8].text)
                try:
                    pp_blocks = int(skater_advanced_pp.select('td')[9].text)
                except ValueError:
                    pp_blocks = 0

                
                away_even_corsi += even_corsi
                away_even_hits += even_hits 
                away_even_blocks += even_blocks
                away_pp_corsi += pp_corsi
                away_pp_hits += pp_hits 
                away_pp_blocks += pp_blocks
                away_penalty_mins += penalty_minutes
            


                player_game = PlayerGame(
                    goals=goals,
                    assists=assists,
                    points=points,
                    team=team,
                    pp_goals=pp_goals,
                    pp_assists=pp_assists,
                    shots=shots,
                    penalty_minutes=penalty_minutes,
                    home=False,
                    minutes=minutes,
                    even_corsi=even_corsi,
                    even_on_ice_corsi=even_on_ice_corsi,
                    even_on_ice_against_corsi=even_on_ice_against_corsi,
                    even_hits=even_hits,
                    even_blocks=even_blocks,
                    pp_corsi=pp_corsi,
                    pp_on_ice_corsi=pp_on_ice_corsi,
                    pp_on_ice_against_corsi=pp_on_ice_against_corsi,
                    pp_hits=pp_hits,
                    pp_blocks=pp_blocks
                )


                if (name in [person.name for person in Player.query.all()]):
                    assoc_player = Player.query.filter(Player.name == name).first()
                else:
                    assoc_player = Player(name=name)
                    db.session.add(assoc_player)
                    # db.session.commit()

                player_game.player = assoc_player
                player_game.game = match
                db.session.add(player_game)
                # db.session.commit()


            for index, player in enumerate(home_players[0:-1]):
                name = unidecode(player.select('td')[0].text.replace('AP','o').replace('S1/2','y').replace('A!A!','as').replace('A%?','a').replace('dA','dre').replace('ASS','c').replace('A"',"e").replace('i!','a').replace('tA','te').replace('A$?','a').replace('i(c)','e').replace('i!','a').replace('lA','li').replace('A(c)','e').replace('rAA!','rna').replace('AA','ci').replace('mA','mi').replace('A 1/4','u').replace('A,','o').replace('A!A','ac').replace('A 3/4','z').replace('A ','S').replace('A!','a').replace('AY=','a').replace('A 1/2','y').replace('eAA!','era').replace('A<<','u').replace('i 1/4','u').replace('aA','ar'))
                goals = int(player.select('td')[1].text)
                assists = int(player.select('td')[2].text)
                points = int(player.select('td')[3].text)
                team = visitor
                pp_goals = int(player.select('td')[7].text)
                pp_assists = int(player.select('td')[11].text)
                shots = int(player.select('td')[13].text)
                penalty_minutes = int(player.select('td')[5].text)
                
                minutes_string = player.select('td')[16].text
                minutes = (int(minutes_string[-2:])/60)+int(minutes_string[-5:2].replace(':',''))


                try:
                    skater_advanced_even = home_advanced_even[index]
                except IndexError:
                    break

                even_corsi = int(skater_advanced_even.select('td')[0].text)
                even_on_ice_corsi = int(skater_advanced_even.select('td')[1].text)
                even_on_ice_against_corsi = int(skater_advanced_even.select('td')[2].text)
                even_hits = int(skater_advanced_even.select('td')[8].text)
                try:
                    even_blocks = int(skater_advanced_even.select('td')[9].text)
                except ValueError:
                    even_blocks=0

                skater_advanced_pp = home_advanced_pp[index]

                pp_corsi = int(skater_advanced_pp.select('td')[0].text)
                pp_on_ice_corsi = int(skater_advanced_pp.select('td')[1].text)
                pp_on_ice_against_corsi = int(skater_advanced_pp.select('td')[2].text)
                pp_hits = int(skater_advanced_pp.select('td')[8].text)
                try:
                    pp_blocks = int(skater_advanced_pp.select('td')[9].text)
                except ValueError:
                    pp_blocks = 0


                home_even_corsi += even_corsi
                home_even_hits += even_hits 
                home_even_blocks += even_blocks
                home_pp_corsi += pp_corsi
                home_pp_hits += pp_hits 
                home_pp_blocks += pp_blocks
                home_penalty_mins += penalty_minutes

                
                player_game = PlayerGame(
                    goals=goals,
                    assists=assists,
                    points=points,
                    team=team,
                    pp_goals=pp_goals,
                    pp_assists=pp_assists,
                    shots=shots,
                    penalty_minutes=penalty_minutes,
                    home=True,
                    minutes=minutes,
                    even_corsi=even_corsi,
                    even_on_ice_corsi=even_on_ice_corsi,
                    even_on_ice_against_corsi=even_on_ice_against_corsi,
                    even_hits=even_hits,
                    even_blocks=even_blocks,
                    pp_corsi=pp_corsi,
                    pp_on_ice_corsi=pp_on_ice_corsi,
                    pp_on_ice_against_corsi=pp_on_ice_against_corsi,
                    pp_hits=pp_hits,
                    pp_blocks=pp_blocks
                )



                if (name in [person.name for person in Player.query.all()]):
                    assoc_player = Player.query.filter(Player.name == name).first()
                else:
                    assoc_player = Player(name=name)
                    db.session.add(assoc_player)
                    # db.session.commit()

                player_game.player = assoc_player
                player_game.game = match
                db.session.add(player_game)
                # db.session.commit()


            match.home_even_corsi = home_even_corsi
            match.home_even_hits = home_even_hits
            match.home_even_blocks = home_even_blocks
            match.home_pp_corsi = home_pp_corsi
            match.home_pp_hits = home_pp_hits 
            match.home_pp_blocks = home_pp_blocks
            match.home_penalty_mins = home_penalty_mins   
            match.away_even_corsi = away_even_corsi
            match.away_even_hits = away_even_hits
            match.away_even_blocks = away_even_blocks
            match.away_pp_corsi = away_pp_corsi
            match.away_pp_hits = away_pp_hits 
            match.away_pp_blocks = away_pp_blocks
            match.away_penalty_mins = away_penalty_mins


            db.session.commit()
            print(match)
            time.sleep(3.2)
        time.sleep(3.2)


            



