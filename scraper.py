# from turtle import ht
from datetime import datetime
from bs4 import BeautifulSoup
from app import app
from urllib.request import Request, urlopen
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, Game, Player, PlayerGame
from unidecode import unidecode
import time
import requests
import ipdb



with app.app_context():
    
    

    # for year in years:
       

            
    # headers = {'user-agent': 'my-app/0.0.1'}
    html = requests.get(f"https://www.hockey-reference.com/leagues/NHL_2025_games.html", headers={'User-Agent':"Mozilla/5.0"})
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
        
        db.session.add(match)
        db.session.commit()


        away_players = box_score_data.select('tbody')[0].select('tr')
        away_goalie = box_score_data.select('tbody')[1].select('tr')
        home_players = box_score_data.select('tbody')[2].select('tr')
        home_goalie = box_score_data.select('tbody')[3].select('tr')

        away_advanced_even =  box_score_data.select('tbody')[6].select('tr')
        away_advanced_pp =  box_score_data.select('tbody')[7].select('tr')

        home_advanced_even =  box_score_data.select('tbody')[13].select('tr')
        home_advanced_pp =  box_score_data.select('tbody')[14].select('tr')


        for index, player in enumerate(away_players):
            name = unidecode(player.select('td')[0].text)
            goals = player.select('td')[1].text
            assists = player.select('td')[2].text
            points = player.select('td')[3].text
            team = visitor
            pp_goals = player.select('td')[7].text
            pp_assists = player.select('td')[11].text
            shots = player.select('td')[13].text
            penalty_minutes = player.select('td')[5].text
            home = False
            
            minutes_string = player.select('td')[16].text
            minutes = (int(minutes_string[-2:])/60)+int(minutes_string[-5:2].replace(':',''))


            skater_advanced_even = away_advanced_even[index]

            even_corsi = skater_advanced_even.select('td')[0].text
            even_on_ice_corsi = skater_advanced_even.select('td')[1].text
            even_on_ice_against_corsi = skater_advanced_even.select('td')[2].text
            even_hits = skater_advanced_even.select('td')[8].text
            even_blocks = skater_advanced_even.select('td')[9].text

            skater_advanced_pp = away_advanced_pp[index]

            pp_corsi = skater_advanced_pp.select('td')[0].text
            pp_on_ice_corsi = skater_advanced_pp.select('td')[1].text
            pp_on_ice_against_corsi = skater_advanced_pp.select('td')[2].text
            pp_hits = skater_advanced_pp.select('td')[8].text
            pp_blocks = skater_advanced_pp.select('td')[9].text


            if (name in [person.name for person in Player.query.all()]):
                assoc_player = Player.query.filter(Player.name == name).first()
            else:
                assoc_player = Player(name=name)
                db.session.add(assoc_player)
                db.session.commit()

            player_game.player = assoc_player
            player_game.game = match
            db.session.add(player_game)
            db.session.commit()


        for index, player in enumerate(home_players):
            name = unidecode(player.select('td')[0].text)
            goals = player.select('td')[1].text
            assists = player.select('td')[2].text
            points = player.select('td')[3].text
            team = visitor
            pp_goals = player.select('td')[7].text
            pp_assists = player.select('td')[11].text
            shots = player.select('td')[13].text
            penalty_minutes = player.select('td')[5].text
            home = False
            
            minutes_string = player.select('td')[16].text
            minutes = (int(minutes_string[-2:])/60)+int(minutes_string[-5:2].replace(':',''))


            skater_advanced_even = home_advanced_even[index]

            even_corsi = skater_advanced_even.select('td')[0].text
            even_on_ice_corsi = skater_advanced_even.select('td')[1].text
            even_on_ice_against_corsi = skater_advanced_even.select('td')[2].text
            even_hits = skater_advanced_even.select('td')[8].text
            even_blocks = skater_advanced_even.select('td')[9].text

            skater_advanced_pp = home_advanced_pp[index]

            pp_corsi = skater_advanced_pp.select('td')[0].text
            pp_on_ice_corsi = skater_advanced_pp.select('td')[1].text
            pp_on_ice_against_corsi = skater_advanced_pp.select('td')[2].text
            pp_hits = skater_advanced_pp.select('td')[8].text
            pp_blocks = skater_advanced_pp.select('td')[9].text

            ipdb.set_trace()


# id = db.Column(db.Integer, primary_key=True)
#     team = db.Column(db.String)
#     minutes = db.Column(db.Float)
#     shots = db.Column(db.Integer)
#     points = db.Column(db.Integer)
#     assists = db.Column(db.Integer)
#     goals = db.Column(db.Integer)
#     pp_goals = db.Column(db.Integer)
#     pp_assists = db.Column(db.Integer)
#     penalty_minutes = db.Column(db.Integer)
#     home = db.Column(db.Boolean)

#     pp_corsi = db.Column(db.Integer)
#     even_corsi = db.Column(db.Integer)
#     even_on_ice_corsi = db.Column(db.Integer)
#     pp_on_ice_corsi = db.Column(db.Integer)
#     even_on_ice_against_corsi = db.Column(db.Integer)
#     pp_on_ice_against_corsi = db.Column(db.Integer)
#     pp_hits = db.column(db.Integer)
#     even_hits = db.Column(db.Integer)
#     pp_blocks = db.Column(db.Integer)
#     even_blocks = db.Column(db.Integer)

#     player_id = db.Column('player_id',db.Integer, db.ForeignKey('player.id'))
#     game_id = db.Column('game_id',db.Integer, db.ForeignKey('game.id'))






       
    #     date = game.select('th')[0].text
    #     new_date = date.replace(',','')
    #     my_time = (game.select('td')[0].text)
    #     empty_time = my_time.replace('p','').replace('a','').replace(":","")
    #     if my_time[-1]=='p':
    #         empty_time = str(int(empty_time)+1200)
    #         if int(empty_time) >= 2400:
    #             empty_time = "0"+empty_time[2:4]
    #     if int(empty_time)<1000:
    #         empty_time = '0'+empty_time
    #     if len(date)==16:
    #         date=date[0:9]+'0'+date[9:16]
    #         new_date=new_date[0:8]+'0'+new_date[8:14]
    #     full_date = new_date[0:10]+" "+empty_time[0:2]+":"+empty_time[2:4]+":"+"00 "+new_date[11:15]
    #     time_obj = datetime.strptime(full_date,"%a %b %d %H:%M:%S %Y")
        
    #     home = game.select('td.left')[1].text
    #     away = game.select('td.left')[0].text
    #     month_in_letters = date[5:8]
    #     if  month_in_letters=="Jan":
    #         month = "01"
    #     elif month_in_letters=="Feb":
    #         month = "02"
    #     elif month_in_letters=="Mar":
    #         month = "03"
    #     elif month_in_letters=="Apr":
    #         month = "04"
    #     elif month_in_letters=="May":
    #         month = "05"
    #     elif month_in_letters=="Jun":
    #         month = "06"
    #     elif month_in_letters=="Jul":
    #         month = "07"
    #     elif month_in_letters=="Aug":
    #         month = "08"
    #     elif month_in_letters=="Sep":
    #         month = "09"
    #     elif month_in_letters=="Oct":
    #         month = "10"
    #     elif month_in_letters=="Nov":
    #         month = "11"
    #     else:
    #         month = "12"

    #     if home==("Atlanta Hawks"):
    #         abb="ATL"
    #     elif home==("Boston Celtics"):
    #         abb="BOS"
    #     elif home==("Charlotte Hornets"):
    #         abb="CHO"
    #     elif home==("Chicago Bulls"):
    #         abb="CHI"
    #     elif home==("Cleveland Cavaliers"):
    #         abb="CLE"
    #     elif home==("Dallas Mavericks"):
    #         abb="DAL"
    #     elif home==("Denver Nuggets"):
    #         abb="DEN"
    #     elif home==("Detroit Pistons"):
    #         abb="DET"
    #     elif home==("Golden State Warriors"):
    #         abb="GSW"
    #     elif home==("Houston Rockets"):
    #         abb="HOU"
    #     elif home==("Indiana Pacers"):
    #         abb="IND"
    #     elif home==("Los Angeles Clippers"):
    #         abb="LAC"
    #     elif home==("Los Angeles Lakers"):
    #         abb="LAL"
    #     elif home==("Memphis Grizzlies"):
    #         abb="MEM"
    #     elif home==("Miami Heat"):
    #         abb="MIA"
    #     elif home==("Milwaukee Bucks"):
    #         abb="MIL"
    #     elif home==("Minnesota Timberwolves"):
    #         abb="MIN"
    #     elif home==("New Orleans Pelicans"):
    #         abb="NOP"
    #     elif home==("New York Knicks"):
    #         abb="NYK"
    #     elif home==("Brooklyn Nets"):
    #         abb="BRK"
    #     elif home==("Oklahoma City Thunder"):
    #         abb="OKC"
    #     elif home==("Orlando Magic"):
    #         abb="ORL"
    #     elif home==("Philadelphia 76ers"):
    #         abb="PHI"
    #     elif home==("Phoenix Suns"):
    #         abb="PHO"
    #     elif home==("Portland Trail Blazers"):
    #         abb="POR"
    #     elif home==("Sacramento Kings"):
    #         abb="SAC"
    #     elif home==("Toronto Raptors"):
    #         abb="TOR"
    #     elif home==("Utah Jazz"):
    #         abb="UTA"
    #     elif home==("Washington Wizards"):
    #         abb="WAS"
    #     elif home==("San Antonio Spurs"):
    #         abb="SAS"
        

    #     if away==("Atlanta Hawks"):
    #         abb_away="ATL"
    #     elif away==("Boston Celtics"):
    #         abb_away="BOS"
    #     elif away==("Charlotte Hornets"):
    #         abb_away="CHO"
    #     elif away==("Chicago Bulls"):
    #         abb_away="CHI"
    #     elif away==("Cleveland Cavaliers"):
    #         abb_away="CLE"
    #     elif away==("Dallas Mavericks"):
    #         abb_away="DAL"
    #     elif away==("Denver Nuggets"):
    #         abb_away="DEN"
    #     elif away==("Detroit Pistons"):
    #         abb_away="DET"
    #     elif away==("Golden State Warriors"):
    #         abb_away="GSW"
    #     elif away==("Houston Rockets"):
    #         abb_away="HOU"
    #     elif away==("Indiana Pacers"):
    #         abb_away="IND"
    #     elif away==("Los Angeles Clippers"):
    #         abb_away="LAC"
    #     elif away==("Los Angeles Lakers"):
    #         abb_away="LAL"
    #     elif away==("Memphis Grizzlies"):
    #         abb_away="MEM"
    #     elif away==("Miami Heat"):
    #         abb_away="MIA"
    #     elif away==("Milwaukee Bucks"):
    #         abb_away="MIL"
    #     elif away==("Minnesota Timberwolves"):
    #         abb_away="MIN"
    #     elif away==("New Orleans Pelicans"):
    #         abb_away="NOP"
    #     elif away==("New York Knicks"):
    #         abb_away="NYK"
    #     elif away==("Brooklyn Nets"):
    #         abb_away="BRK"
    #     elif away==("Oklahoma City Thunder"):
    #         abb_away="OKC"
    #     elif away==("Orlando Magic"):
    #         abb_away="ORL"
    #     elif away==("Philadelphia 76ers"):
    #         abb_away="PHI"
    #     elif away==("Phoenix Suns"):
    #         abb_away="PHO"
    #     elif away==("Portland Trail Blazers"):
    #         abb_away="POR"
    #     elif away==("Sacramento Kings"):
    #         abb_away="SAC"
    #     elif away==("Toronto Raptors"):
    #         abb_away="TOR"
    #     elif away==("Utah Jazz"):
    #         abb_away="UTA"
    #     elif away==("Washington Wizards"):
    #         abb_away="WAS"
    #     elif away==("San Antonio Spurs"):
    #         abb_away="SAS"
        

        
    #     url_date = date[13:17]+month+date[9:11]+'0'+abb

    #     box_score_url = f"https://www.basketball-reference.com/boxscores/{url_date}.html"

    #     box_score = requests.get(box_score_url)
        
    #     box_score_data = BeautifulSoup(box_score.text, 'html.parser')

    #     line_score = box_score_data.select('#line_score')

    #     away_players_data = box_score_data.select(f'#box-{abb_away}-game-basic')[0].select('tbody')[0].select('tr')
    #     away_players_data.pop(5)
    #     away_players_advanced_data = box_score_data.select(f'#box-{abb_away}-game-advanced')[0].select('tbody')[0].select('tr')
    #     away_players_advanced_data.pop(5)

    #     home_players_data = box_score_data.select(f'#box-{abb}-game-basic')[0].select('tbody')[0].select('tr')
    #     home_players_data.pop(5)
    #     home_players_advanced_data = box_score_data.select(f'#box-{abb}-game-advanced')[0].select('tbody')[0].select('tr')
    #     home_players_advanced_data.pop(5)
        
    #     match = Game(
    #         visitor= away,
    #         home= home,
    #         location= game.select('td.left')[2].text,
    #         home_score= int(game.select('td.right')[2].text),
    #         away_score= int(game.select('td.right')[1].text),
    #         date= time_obj
    #     )

    #     db.session.add(match)
    #     db.session.commit()

    #     away_players = []
    #     home_players = []

    #     for index, player in enumerate(away_players_data):
            
    #         if len(player.select('.right'))>1:
    #             played = True
    #         else:
    #             played = False
    #         if played:  

    #             name = unidecode(player.select('th a')[0].text)
    #             if (name in [person.name for person in Player.query.all()]):
    #                 assoc_player = Player.query.filter(Player.name == name).first()
    #             else:
    #                 assoc_player = Player(name=name)
    #                 db.session.add(assoc_player)
    #                 db.session.commit()


    #             player_game = PlayerGame(
    #                 minutes= int(player.select('.right')[0].text.replace(":","")),
    #                 # 'fg': player.select('.right')[1].text,
    #                 # 'fga': player.select('.right')[2].text,
    #                 # 'fg_pct': player.select('.right')[3].text,
    #                 three_pt= int(player.select('.right')[4].text),
    #                 # 'three_pt_att':player.select('.right')[5].text,
    #                 # 'three_pt_perc':player.select('.right')[6].text,
    #                 # 'ft': player.select('.right')[7].text,
    #                 # 'fta': player.select('.right')[8].text,
    #                 # 'ft_perc': player.select('.right')[9].text,
    #                 # 'orb': player.select('.right')[10].text,
    #                 # 'drb': player.select('.right')[11].text,
    #                 trb= int(player.select('.right')[12].text),
    #                 assists= int(player.select('.right')[13].text),
    #                 steals= int(player.select('.right')[14].text),
    #                 blocks= int(player.select('.right')[15].text),
    #                 # 'turnovers': player.select('.right')[16].text,
    #                 # 'fouls': player.select('.right')[17].text,
    #                 points= int(player.select('.right')[18].text),
    #                 # 'plus_minus': player.select('.right')[19].text
    #                 home= False,
    #                 tsp= 0.00 if (away_players_advanced_data[index].select('.right')[1].text=="") else float(away_players_advanced_data[index].select('.right')[1].text),
    #                 eft= 0.00 if (away_players_advanced_data[index].select('.right')[2].text=="") else float(away_players_advanced_data[index].select('.right')[2].text),
    #                 # player["3PAr"]=away_players_advanced_data[index].select('.right')[3].text
    #                 # player["FTr"]=away_players_advanced_data[index].select('.right')[4].text
    #                 # player["ORBP"]=away_players_advanced_data[index].select('.right')[5].text
    #                 # player["DRBP"]=away_players_advanced_data[index].select('.right')[6].text
    #                 # player["TRBP"]=away_players_advanced_data[index].select('.right')[7].text
    #                 # player["ASTP"]=away_players_advanced_data[index].select('.right')[8].text
    #                 # player["STLP"]=away_players_advanced_data[index].select('.right')[9].text
    #                 # player["BLKP"]=away_players_advanced_data[index].select('.right')[10].text
    #                 # player["TOVP"]=away_players_advanced_data[index].select('.right')[11].text
    #                 # player["USGP"]=away_players_advanced_data[index].select('.right')[12].text
    #                 ORtg=0 if (away_players_advanced_data[index].select('.right')[13].text=="") else int(away_players_advanced_data[index].select('.right')[13].text),
    #                 DRTg=0 if (away_players_advanced_data[index].select('.right')[14].text=="") else int(away_players_advanced_data[index].select('.right')[14].text),
    #                 # BPM=0.00 if (away_players_advanced_data[index].select('.right')[15].text=="") else float(away_players_advanced_data[index].select('.right')[15].text)
    #             )

    #             player_game.player = assoc_player
    #             player_game.game = match
    #             db.session.add(player_game)
    #             db.session.commit()
                

    #     for index, home_player in enumerate(home_players_data):
    #         if len(home_player.select('.right'))>1:
    #             played = True
    #         else:
    #             played = False
    #         if played:

    #             name = unidecode(home_player.select('th a')[0].text)
    #             if (name in [person.name for person in Player.query.all()]):
    #                 assoc_player = Player.query.filter(Player.name == name).first()
    #             else:
    #                 assoc_player = Player(name=name)
    #                 db.session.add(assoc_player)
    #                 db.session.commit()


    #             player_game = PlayerGame(
    #                 minutes= int(home_player.select('.right')[0].text.replace(":","")),
    #                 # 'fg': home_player.select('.right')[1].text,
    #                 # 'fga': home_player.select('.right')[2].text,
    #                 # 'fg_pct': home_player.select('.right')[3].text,
    #                 three_pt= int(home_player.select('.right')[4].text),
    #                 # 'three_pt_att': home_player.select('.right')[5].text,
    #                 # 'three_pt_perc': home_player.select('.right')[6].text,
    #                 # 'ft': home_player.select('.right')[7].text,
    #                 # 'fta': home_player.select('.right')[8].text,
    #                 # 'ft_perc': home_player.select('.right')[9].text,
    #                 # 'orb': home_player.select('.right')[10].text,
    #                 # 'drb': home_player.select('.right')[11].text,
    #                 trb= int(home_player.select('.right')[12].text),
    #                 assists= int(home_player.select('.right')[13].text),
    #                 steals= int(home_player.select('.right')[14].text),
    #                 blocks= int(home_player.select('.right')[15].text),
    #                 # 'to': home_player.select('.right')[16].text,
    #                 # 'fouls': home_player.select('.right')[17].text,
    #                 points= int(home_player.select('.right')[18].text),
    #                 # 'plus_minus': home_player.select('.right')[19].text
    #                 home= True,
    #                 tsp= 0.00 if (home_players_advanced_data[index].select('.right')[1].text=="") else float(home_players_advanced_data[index].select('.right')[1].text),
    #                 eft= 0.00 if (home_players_advanced_data[index].select('.right')[2].text=="") else float(home_players_advanced_data[index].select('.right')[2].text),
    #                 # player["tPAr"]=home_players_advanced_data[index].select('.right')[3].text
    #                 # player["FTr"]=home_players_advanced_data[index].select('.right')[4].text
    #                 # player["ORBP"]=home_players_advanced_data[index].select('.right')[5].text
    #                 # player["DRBP"]=home_players_advanced_data[index].select('.right')[6].text
    #                 # player["TRBP"]=home_players_advanced_data[index].select('.right')[7].text
    #                 # player["ASTP"]=home_players_advanced_data[index].select('.right')[8].text
    #                 # player["STLP"]=home_players_advanced_data[index].select('.right')[9].text
    #                 # player["BLKP"]=home_players_advanced_data[index].select('.right')[10].text
    #                 # player["TOVP"]=home_players_advanced_data[index].select('.right')[11].text
    #                 # player["USGP"]=home_players_advanced_data[index].select('.right')[12].text
    #                 ORtg=0 if (home_players_advanced_data[index].select('.right')[13].text=="") else int(home_players_advanced_data[index].select('.right')[13].text),
    #                 DRTg=0 if (home_players_advanced_data[index].select('.right')[14].text=="") else int(home_players_advanced_data[index].select('.right')[14].text),
    #                 # BPM=0.00 if (home_players_advanced_data[index].select('.right')[15].text=="") else float(home_players_advanced_data[index].select('.right')[15].text)
    #             )

    #             player_game.player = assoc_player
    #             player_game.game = match
    #             db.session.add(player_game)
    #             db.session.commit()

    #     print(date)
    #     time.sleep(3.2)

    # time.sleep(3.2)
