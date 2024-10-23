from app import *
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime, date, timedelta
import http.client
from statistics import mean,mode,median
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

    # ipdb.set_trace()




    #find the best algorithm to predict shots on goal
    #teams and goalies that give up more corsi than average
    #players that have more corsi than average players
    #players that excel on certain days/vs certain teams
    

   
        

   


    #find league averages

    #use last 1300 games (about 1 full season)

    seasons_games = [game for game in Game.query.all()][-1300:]

    avg_even_blocks = mean([(game.home_even_blocks + game.away_even_blocks)/2 for game in seasons_games])
    #~12.2

    avg_even_hits = mean([(game.home_even_hits + game.away_even_hits)/2 for game in seasons_games])
    #~21.1

    avg_even_corsi = mean([(game.home_even_corsi + game.away_even_corsi)/2 for game in seasons_games])
    #~48.6

    # avg_home_even_corsi = mean([game.home_even_corsi  for game in seasons_games])
    # avg_away_even_corsi = mean([game.away_even_corsi  for game in seasons_games])

    avg_pp_corsi = mean([(game.home_pp_corsi + game.away_pp_corsi)/2 for game in seasons_games])
    #~7.7

    avg_pp_blocks = mean([(game.home_pp_blocks + game.away_pp_blocks)/2 for game in seasons_games])
    #~0.14

    avg_pp_hits = mean([(game.home_pp_hits + game.away_pp_hits)/2 for game in seasons_games])
    #~0.36

    avg_goals = mean({(game.home_score + game.away_score)/2 for game in seasons_games})
    #~3.78

    avg_goals_per_corsi = mean({(game.home_score/game.home_even_corsi + game.away_score/game.away_even_corsi)/2 for game in seasons_games})
    #~0.067

    avg_pp_per_minute_corsi_list = []
    for game in seasons_games:
        if game.home_penalty_mins > 0:
            avg_pp_per_minute_corsi_list.append(game.home_pp_corsi/game.home_penalty_mins)
        if game.away_penalty_mins > 0:
            avg_pp_per_minute_corsi_list.append(game.away_pp_corsi/game.away_penalty_mins)
    avg_pp_per_minute_corsi = mean(avg_pp_per_minute_corsi_list)
    #~1.35


    avg_penalty_minutes = mean([(game.home_penalty_mins + game.away_penalty_mins)/2 for game in seasons_games])
    #~8.07


   


    #team multipliers (find differences between team performance and leauge average)
        #blocked shots
        #made shot percentage (goals/corsi)
        #hits
        #goals against
        #corsi against
        #corsi for
        #penalty minutes
            #pp corsi depending on how many penalty minutes

    team_mults = []
    for team in list_of_teams:
        team_games = [game for game in Game.query.all() if game.visitor==team or game.home==team][-50:]
        
        for game in team_games:
            #these are multipliers against the team so do the opposite home/away
            #they will tell how well teams do against the team
            if game.home==team:
                team_block_avg = mean([game.away_even_blocks for game in team_games])
                team_corsi_avg = mean([game.away_even_corsi for game in team_games])
                team_hits_avg = mean([game.away_even_hits for game in team_games])
                team_goals_avg = mean([game.away_score for game in team_games])
                team_penalty_mins_avg = mean([game.home_penalty_mins for game in team_games])
                team_goals_per_corsi_avg = mean([game.away_score/game.away_even_corsi for game in team_games])

            else:
                team_block_avg = mean([game.home_even_blocks for game in team_games])
                team_corsi_avg = mean([game.home_even_corsi for game in team_games])
                team_hits_avg = mean([game.home_even_hits for game in team_games])
                team_goals_avg = mean([game.home_score for game in team_games])
                team_penalty_mins_avg = mean([game.away_penalty_mins for game in team_games])
                team_goals_per_corsi_avg = mean([game.home_score/game.home_even_corsi for game in team_games])

        team_mults.append({"team":team,"team_block_mult":avg_even_blocks/team_block_avg,"team_corsi_mult":team_corsi_avg/avg_even_corsi,"team_hits_mult":avg_even_hits/team_hits_avg,"team_goals_mult":team_goals_avg/avg_goals,"team_penalty_mins_mult":team_penalty_mins_avg/avg_penalty_minutes,"team_goals_per_corsi_mult":team_goals_per_corsi_avg/avg_goals_per_corsi})


    # for item in team_mults:
    #     print(item)



     #individual things to look for
        #stats vs team
        #stats recently

    #check if teammates are injured and try to find times they didn't play with them

    for player in odds_list:
        
        print(player["name"])
        player_object_list = Player.query.filter(Player.name==player["name"]).all()

        if len(player_object_list)>0:
            player_object=player_object_list[0]
        else:
            continue


      

        player_team = player_object.games[-1].team

        for game in todays_games:
            if game["home"]==player_team:
                other_team = game["away"]
            elif game["away"]==player_team:
                other_team = game["home"]


        team_mult_object = [item for item in team_mults if item["team"]==other_team][0]


        #THINGS I'M LEARNING
            #PLAYERS TEND TO SHOOT MORE WILDLY/THERE ARE MORE BLOCKS DURING A POWER PLAY


        #maybe take a players average shot per corsi and that is the standard

        last_fifty_games = player_object.games[-50:]
        average_shot_per_corsi = mean([game.shots/(game.even_corsi+game.pp_corsi) if (game.even_corsi+game.pp_corsi)>0 else 0 for game in last_fifty_games])
        #averages ~0.5

        

        #only find corsi for recent games, then use opposing team multipliers to adjust it

        #multipy player average shot per corsi by final corsi value- that will be the shot estimation


        #check if players corsi per non penalty minute is larger than players corsi per penalty minute

        #if team hit and block multiplier are both higher than average, don't multiply 

        recent_even_corsi_list = []
        recent_pp_corsi_list = []

        for game in last_fifty_games:
            #find corsi per non penalty minute
            #find shots per non penalty minute
            if game.home==True:
                non_penalty_mins = 60-game.game.away_penalty_mins
                penalty_mins = game.game.away_penalty_mins
            else:
                non_penalty_mins = 60-game.game.home_penalty_mins
                penalty_mins = game.game.home_penalty_mins

            recent_even_corsi_list.append(game.even_corsi/non_penalty_mins if non_penalty_mins>0 else 0)
            recent_pp_corsi_list.append(game.pp_corsi/penalty_mins if penalty_mins>0 else 0)



        recent_even_corsi = mean(recent_even_corsi_list)
        recent_pp_corsi = mean(recent_pp_corsi_list)

        ipdb.set_trace()

        #last 10 games vs opponent

        opponent_even_corsi_list = []
        opponent_pp_corsi_list = []
        
        opponent_games = [game for game in player_object.games if home==other_team or visitor==other_team][-10:]

        for game in opponent_games:
            #find corsi per non penalty minute
            #find shots per non penalty minute
            if game.home==True:
                non_penalty_mins = 60-game.game.away_penalty_mins
                penalty_mins = game.game.away_penalty_mins
            else:
                non_penalty_mins = 60-game.game.home_penalty_mins
                penalty_mins = game.game.home_penalty_mins

        opponent_even_corsi_list.append(game.even_corsi/non_penalty_mins if non_penalty_mins>0 else 0)
        opponent_pp_corsi_list.append(game.pp_corsi/penalty_mins if penalty_mins>0 else 0)

        opponent_even_corsi = mean(opponent_even_corsi_list)
        opponent_pp_corsi = mean(opponent_pp_corsi_list)


        #possible high pp multiplier (only if avg_pp_corsi > avg_even_corsi)
            #multiply teams penalty_minute multipler by new_pp_multiplier = (((avg_pp_corsi-avg_even_corsi)/avg_pp_corsi)+1)*team_pp_multiplier
            #if low pp multiplier, possibly do the opposite without adding 1 new_pp_multiplier = (((avg_even_corsi-avg_pp_corsi)/avg_even_corsi))*team_pp_multiplier

            #more logic so future Brian can follow this
                #the only reason for the avg_pp_corsi is to adjust the penalty minute multiplier\
                #if the team penalty minute multiplier is high, the individual players pp corsi will weigh more
                #high team penalty minute multiplier and low player pp corsi: decrease the multiplier to take into account players individual pp ability
                #high team penalty minute multiplier and high player pp corsi: increase the multiplier to take into acount players individual pp ability
            #when calculating final shot- always take pp into account as 8 out of 60 minutes. Some players will have lower pp multipliers on the same team
        
        

        #add position and side later when add them to db

        #players pp shots per corsi


        #players even shots per corsi
        #players corsi in general

        #lower projection if other team averages more hits or blocks than other team
        #opposite in other case

        #players shots over last few games
        #players shots vs team
        #players shots home or away
        #players shots after certain amount of rest

        #if opposing team has more penalty minutes than average then account for pp corsi and shots



    # ipdb.set_trace()
