from app import *
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime, date, timedelta
import http.client
import ipdb

with app.app_context():



   
    time_url = "https://time.is/"
    time_page = requests.get(time_url, headers = {'User-Agent':"Mozilla/5.0"})
    time_doc = BeautifulSoup(time_page.text, 'html.parser')
    date_string = time_doc.select("#dd")[0].text
    time_string = time_doc.select('#clock')[0].text 
    format_time = datetime.strptime(time_string,"%I:%M:%S%p").time()
    
   
    #set current date to todays date and run the algorithm to see projections
    full_date = datetime.strptime(date_string, "%A, %B %d, %Y")
    current_date = full_date.date()
    # current_date = datetime(2023,11,27).date()

    yesterday = current_date - timedelta(1)
    time_list = date_string.replace(",","").split()
    month = time_list[1].lower()
    year = int(time_list[3])
    end_months = ["september", "october", "november", "december"]
    if month in end_months:
        year = year+1
    year_string = str(year)





    #https://sportsbook-nash.draftkings.com/api/sportscontent/dkusny/v1/leagues/42133/categories/1189
    #https://sportsbook-nash.draftkings.com/api/sportscontent/dkusny/v1/leagues/42133/categories/1189/subcategories/12040


    # Open the JSON file
    with open('draftkings.json') as f:
    # Load the JSON data into a Python dictionary
        data = json.load(f)

        # Now you can work with the data

    odds_list = []
    odds_objects = data["selections"]

    for item in odds_objects:
        name = item["participants"][0]["name"]
        over_under = item["label"]
        odds = item["displayOdds"]["decimal"]
        line = item["points"]

       


        player = {"name":name,"line":line}

        if over_under=="Over":
            player["Over"]=odds
        else:
            player["Under"]=odds


        if len(odds_list)>0:
            names_list = [nombre["name"] for nombre in odds_list]
        else:
            names_list = ["Jeff"]

        if name not in names_list:
            odds_list.append(player) 
        else:
            [guy for guy in odds_list if guy["name"]==name][0][over_under]=odds
    
    for odd in odds_list:
        print(odd)

    # ipdb.set_trace()

    injury_url = "https://www.espn.com/nhl/injuries"
    injury_page = requests.get(injury_url, headers={'User-Agent':"Mozilla/5.0"})
    injuries = BeautifulSoup(injury_page.text, 'html.parser')
    injury_page = injuries.select('.ResponsiveTable')

    

    #collect injury dictionary
    injured_list = {}


    for injured in injury_page:
        team_name = injured.select('.Table__Title')[0].text
        
        players = injured.select('tbody')[0].select('tr')
        injured_players = []
        for player in players:
            player_info = player.select('td')[0].text
            player_comment = player.select('td')[3].text
            if (player_comment=='Injured Reserve' or player_comment=='Out') and "is expected to be cleared" not in player_info and "will play" not in player_info and "plans to play" not in player_info:
                injured_players.append(player.select('td')[0].text)
                
        injured_list[team_name] = injured_players

    # ipdb.set_trace()


    schedule_page_url = f"https://www.hockey-reference.com/leagues/NHL_2025_games.html"
    schedule_page = requests.get(schedule_page_url, headers = {'User-Agent':"Mozilla/5.0"})
    schedule = BeautifulSoup(schedule_page.text, 'html.parser')

    monthly_games = schedule.select('tbody')[0].select('tr')

    todays_games = []
    list_of_teams = []
    for game in monthly_games:
        date = datetime.strptime(game.select('th')[0].text,"%Y-%m-%d").date()
        if date == current_date:
            game_data = {}
            game_data["home"] = game.select('td')[3].text
            game_data["away"] = game.select('td')[1].text
            list_of_teams.append(game.select('td')[3].text)
            list_of_teams.append(game.select('td')[1].text)
            my_time = game.select('td')[0].text
            empty_time = my_time.replace('PM','').replace('AM','').replace(":","").replace(' ','')
        
            if my_time[-2]=='P':
                empty_time = str(int(empty_time)+1200)
                if int(empty_time) >= 2400:
                    empty_time = "0"+empty_time[2:4]
            if int(empty_time)<1000:
                empty_time = '0'+empty_time

            time = datetime.strptime(empty_time,"%H%M").time()
            game_data["time"]=time

            todays_games.append(game_data)


    for equipo in todays_games:
        print(equipo)

    ipdb.set_trace()