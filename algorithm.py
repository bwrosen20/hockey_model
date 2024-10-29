from app import *
from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
import json
from datetime import datetime, date, timedelta
import http.client
import time
from operator import itemgetter
from statistics import mean,mode,median,stdev
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
    
    # for odd in odds_list:
    #     print(odd)

    # ipdb.set_trace()

    injury_url = "https://www.espn.com/nhl/injuries"
    injury_page = requests.get(injury_url, headers={'User-Agent':"Mozilla/5.0"})
    injuries = BeautifulSoup(injury_page.text, 'html.parser')
    injury_page = injuries.select('.ResponsiveTgamele')

    

    #collect injury dictionary
    injured_list = {}


    for injured in injury_page:
        team_name = injured.select('.Tgamele__Title')[0].text
        
        players = injured.select('tbody')[0].select('tr')
        injured_players = []
        for player in players:
            player_info = player.select('td')[0].text
            player_comment = player.select('td')[3].text
            if (player_comment=='Injured Reserve' or player_comment=='Out') and "is expected to be cleared" not in player_info and "will play" not in player_info and "plans to play" not in player_info:
                injured_players.append(player.select('td')[0].text)
                
        injured_list[team_name] = injured_players

    # ipdb.set_trace()


    # schedule_page_url = f"https://www.hockey-reference.com/leagues/NHL_2025_games.html"
    # schedule_page = requests.get(schedule_page_url, headers = {'User-Agent':"Mozilla/5.0"})
    # schedule = BeautifulSoup(schedule_page.text, 'html.parser')

    # monthly_games = schedule.select('tbody')[0].select('tr')

    # todays_games = []
    # list_of_teams = []
    # for game in monthly_games:
    #     date = datetime.strptime(game.select('th')[0].text,"%Y-%m-%d").date()
    #     if date == current_date:
    #         game_data = {}
    #         game_data["home"] = game.select('td')[3].text
    #         game_data["away"] = game.select('td')[1].text
    #         list_of_teams.append(game.select('td')[3].text)
    #         list_of_teams.append(game.select('td')[1].text)
    #         my_time = game.select('td')[0].text
    #         empty_time = my_time.replace('PM','').replace('AM','').replace(":","").replace(' ','')
        
    #         if my_time[-2]=='P':
    #             empty_time = str(int(empty_time)+1200)
    #             if int(empty_time) >= 2400:
    #                 empty_time = "0"+empty_time[2:4]
    #         if int(empty_time)<1000:
    #             empty_time = '0'+empty_time

    #         time = datetime.strptime(empty_time,"%H%M").time()
    #         game_data["time"]=time

    #         todays_games.append(game_data)


    schedule_page_url = f"https://www.hockey-reference.com/leagues/NHL_2023_games.html"
    schedule_page = requests.get(schedule_page_url, headers = {'User-Agent':"Mozilla/5.0"})
    schedule = BeautifulSoup(schedule_page.text, 'html.parser')

    monthly_games = schedule.select('tbody')[0].select('tr')
    latest_game_date = Game.query.all()[-1].date.date()
    tomorrow = latest_game_date

    todays_games = []
    list_of_teams = []

    games = []

    while len(games)==0:
        tomorrow = tomorrow + timedelta(1)
        games = [game for game in monthly_games if datetime.strptime(game.select('th')[0].text,"%Y-%m-%d").date()==tomorrow]
        
    players = []
    for game in monthly_games:
        date = datetime.strptime(game.select('th')[0].text,"%Y-%m-%d").date()
        if date == tomorrow:
            game_data = {}
            game_data["home"] = game.select('td')[3].text
            game_data["away"] = game.select('td')[1].text
            list_of_teams.append(game.select('td')[3].text)
            list_of_teams.append(game.select('td')[1].text)
            my_time = game.select('td')[0].text
            empty_time = my_time.replace('PM','').replace('AM','').replace(":","").replace(' ','')
        
            if my_time[-2]=='P':
                if (my_time[0]=="1") and my_time[1]=="2":
                    empty_time = str(int(empty_time))
                else:
                    empty_time = str(int(empty_time)+1200)
                    
                if int(empty_time) >= 2400:
                    empty_time = "0"+empty_time[2:4]
            if int(empty_time)<1000:
                empty_time = '0'+empty_time

            the_time = datetime.strptime(empty_time,"%H%M").time()
            game_data["time"]=the_time

            todays_games.append(game_data)

            url_ending = game.select('a')[0].get("href")

            # ipdb.set_trace()

            box_score_url = f"https://www.hockey-reference.com{url_ending}"

            box_score = requests.get(box_score_url, headers={'User-Agent':"Mozilla/5.0"})

            box_score_data = BeautifulSoup(box_score.content.decode('utf-8'), "html.parser")
            with open("output.html", "w") as file:
                file.write(box_score_data.decode('utf-8'))


            away_players = box_score_data.select('tbody')[0].select('tr')
            home_players = box_score_data.select('tbody')[2].select('tr')

           

            for index, player in enumerate(away_players[0:-1]):
                name = unidecode(player.select('td')[0].text)
                # name = name.replace('AP','o').replace('S1/2','y').replace('A!A!','as').replace('A%?','a').replace('dA','dre').replace('ASS','c').replace('A"',"e").replace('i!','a').replace('tA','te').replace('A$?','a').replace('i(c)','e').replace('i!','a').replace('lA','li').replace('A(c)','e').replace('rAA!','rna').replace('AA','ci').replace('mA','mi').replace('A 1/4','u').replace('A,','o').replace('A!A','ac').replace('A 3/4','z').replace('A ','S').replace('A!','a').replace('AY=','a').replace('A 1/2','y').replace('eAA!','era').replace('A<<','u').replace('i 1/4','u').replace('aA','ar')
                shots = int(player.select('td')[13].text)
                player = {"name":name,"shots":shots}
                players.append(player)

            for index, player in enumerate(home_players[0:-1]):
                name = unidecode(player.select('td')[0].text)
                # name = name.replace('AP','o').replace('S1/2','y').replace('A!A!','as').replace('A%?','a').replace('dA','dre').replace('ASS','c').replace('A"',"e").replace('i!','a').replace('tA','te').replace('A$?','a').replace('i(c)','e').replace('i!','a').replace('lA','li').replace('A(c)','e').replace('rAA!','rna').replace('AA','ci').replace('mA','mi').replace('A 1/4','u').replace('A,','o').replace('A!A','ac').replace('A 3/4','z').replace('A ','S').replace('A!','a').replace('AY=','a').replace('A 1/2','y').replace('eAA!','era').replace('A<<','u').replace('i 1/4','u').replace('aA','ar')
                shots = int(player.select('td')[13].text)
                player = {"name":name,"shots":shots}
                players.append(player)

            print(url_ending)
            time.sleep(3.2)


    for equipo in todays_games:
        print(equipo)

    # ipdb.set_trace()




    #find the best algorithm to predict shots on goal
    #teams and goalies that give up more corsi than average
    #players that have more corsi than average players
    #players that excel on certain days/vs certain teams
    

   
        

   


    #find league averages

    #use last 1300 games (gameout 1 full season)

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

    league_shots_per_corsi = []

    for game in seasons_games:
        single_game_shots = 0
        for player in game.players:
            single_game_shots+=player.shots
        league_shots_per_corsi.append(single_game_shots/(game.home_even_corsi+game.away_even_corsi+game.home_pp_corsi+game.away_pp_corsi))
    avg_shots_per_corsi = mean(league_shots_per_corsi)
        
   
        

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
            shots = []
            blocks = []
            corsi = []
            hits = []
            goals = []
            team_penalty_mins = []
            opposing_penalty_mins = []
            shots_per_corsi = []

            if game.home==team:

                blocks.append(game.away_even_blocks+game.away_pp_blocks)
                corsi.append(game.away_even_corsi+game.away_pp_corsi)
                hits.append(game.away_even_corsi+game.away_pp_corsi)
                goals.append(game.away_score)
                team_penalty_mins.append(game.home_penalty_mins)
                opposing_penalty_mins.append(game.away_penalty_mins)


                shots_iterator = 0
                for skater in [player for player in game.players if player.team!=team]:
                    shots_iterator+=skater.shots
                shots.append(shots_iterator)
                shots_per_corsi.append(shots_iterator/(game.away_even_corsi+game.away_pp_corsi))


            else:

                blocks.append(game.home_even_blocks+game.home_pp_blocks)
                corsi.append(game.home_even_corsi+game.home_pp_corsi)
                hits.append(game.home_even_corsi+game.home_pp_corsi)
                goals.append(game.home_score)
                team_penalty_mins.append(game.away_penalty_mins)
                opposing_penalty_mins.append(game.home_penalty_mins)


                shots_iterator = 0
                for skater in [player for player in game.players if player.team!=team]:
                    shots_iterator+=skater.shots
                shots.append(shots_iterator)
                shots_per_corsi.append(shots_iterator/(game.home_even_corsi+game.home_pp_corsi))



        #edit these
        team_block_avg = mean(blocks)
        team_corsi_avg = mean(corsi)
        team_hits_avg = mean(hits)
        team_goals_avg = mean(goals)
        #penalties commited by team
        team_penalty_mins_avg = mean(team_penalty_mins)
        #penalties drawn by team
        opposing_penalty_mins_avg = mean(opposing_penalty_mins)
        team_shots_per_corsi_avg = mean(shots_per_corsi)

        

        team_mults.append({"team":team,"team_block_mult":avg_even_blocks/team_block_avg,"team_corsi_mult":team_corsi_avg/avg_even_corsi,"team_hits_mult":avg_even_hits/team_hits_avg,"team_goals_mult":team_goals_avg/avg_goals,"team_penalty_mins_mult":team_penalty_mins_avg/avg_penalty_minutes,"opposing_team_penalty_mins_mult":opposing_penalty_mins_avg/avg_penalty_minutes,"team_shots_per_corsi_mult":team_shots_per_corsi_avg/avg_shots_per_corsi})


    # for item in team_mults:
    #     print(item)



     #individual things to look for
        #stats vs team
        #stats recently

    #check if teammates are injured and try to find times they didn't play with them

    # for player in odds_list:
    player_estimate_list = []
    
    for player in players:

        #things to add
            #elevation games
            #games at time
            #games on day
            #multiplier for favorite or underdog (decrease if favorite, increase if underdog)

        
        print(player["name"])
        player_object_list = Player.query.filter(Player.name==player["name"]).all()

        if len(player_object_list)>0:
            player_object=player_object_list[0]
        else:
            print(f'{player["name"]} not in database')
            continue

        games_to_use = player_object.games
      

        player_team = player_object.games[-1].team

        if len(games_to_use)<10:
            continue
        if player["name"]=="Sebastian Aho":
            continue

        # if (games_to_use[-5].game.home!=player_team) and (games_to_use[-5].game.visitor!=player_team):
        #     continue

        for game in todays_games:
            if game["home"]==player_team:
                other_team = game["away"]
                player_game = game
            elif game["away"]==player_team:
                player_game = game
                other_team = game["home"]


        try:
            team_mult_object = [item for item in team_mults if item["team"]==other_team][0]
        except NameError:
            continue

        if game["home"]==player_team:
            home_or_away = True
        else:
            home_or_away = False

        


        #THINGS I'M LEARNING
            #PLAYERS TEND TO SHOOT MORE WILDLY/THERE ARE MORE BLOCKS DURING A POWER PLAY


        #maybe take a players average shot per corsi and that is the standard

        last_fifty_games = player_object.games[-10:]
        #averages ~0.5

        average_minutes = mean([game.minutes for game in last_fifty_games][-5:])
        # average_shot_per_corsi = mean([game.shots/(game.shots) if (game.shots)>0 else 0 for game in last_fifty_games])*team_mult_object["team_shots_per_corsi_mult"]
        # if average_shot_per_corsi > 0.9:
        #     average_shot_per_corsi = 0.9



        #only find corsi for recent games, then use opposing team multipliers to adjust it

        #multipy player average shot per corsi by final corsi value- that will be the shot estimation


        #check if players corsi per non penalty minute is larger than players corsi per penalty minute

        #if team hit and block multiplier are both higher than average, don't multiply 



        injury_games = []
        games_without_players = []
        if player_team in injured_list.keys():
            if len(injured_list[player_team])>0:
                injured_players = injured_list[player_team]
                for game in games_to_use:
                    players = [player.player.name for player in game.game.players]
                    x = 0
                    for person in injured_players:
                        if person in players:
                            x=1
                    if ((game.game.visitor==player_team or game.game.home==player_team) and (x==len(injured_players) or (len(injured_players)>2 and (x>=((len(injured_players))-1))))):
                        injury_games.append(game)
                    
                


        recent_even_corsi_list = []
        recent_pp_corsi_list = []
        recent_games = []

        for game in last_fifty_games:
            #find corsi per non penalty minute
            #find shots per non penalty minute
            if game.home==True:
                non_penalty_mins = 60-game.game.away_penalty_mins
                penalty_mins = game.game.away_penalty_mins
            else:
                non_penalty_mins = 60-game.game.home_penalty_mins
                penalty_mins = game.game.home_penalty_mins

            # recent_even_corsi_list.append(game.even_corsi/non_penalty_mins if non_penalty_mins>0 else 0)
            # recent_pp_corsi_list.append(game.pp_corsi/penalty_mins if penalty_mins>0 else 0)

            # recent_games.append(game)


        # recent_even_corsi = mean(recent_even_corsi_list)
        # recent_pp_corsi = mean(recent_pp_corsi_list)

        #recent games vs opponent

        opponent_even_corsi_list = []
        opponent_pp_corsi_list = []
        opponent_games_list = []
        
        opponent_games = [game for game in player_object.games if game.game.home==other_team or game.game.visitor==other_team]

        for game in opponent_games:
            #find corsi per non penalty minute
            #find shots per non penalty minute
            if game.home==True:
                non_penalty_mins = 60-game.game.away_penalty_mins
                penalty_mins = game.game.away_penalty_mins
            else:
                non_penalty_mins = 60-game.game.home_penalty_mins
                penalty_mins = game.game.home_penalty_mins

            # opponent_even_corsi_list.append(game.even_corsi/non_penalty_mins if non_penalty_mins>0 else 0)
            # opponent_pp_corsi_list.append(game.pp_corsi/penalty_mins if penalty_mins>0 else 0)

            opponent_games_list.append(game)
        opponent_games_list = opponent_games_list

        
        # opponent_even_corsi = mean(opponent_even_corsi_list)
        # opponent_pp_corsi = mean(opponent_pp_corsi_list)


        #recent home games

        

        home_away_games = [game for game in player_object.games if game.home==home_or_away]

        home_away_even_corsi_list = []
        home_away_pp_corsi_list = []
        home_away_games_list = []


        for game in home_away_games:
            if game.home==True:
                non_penalty_mins = 60-game.game.away_penalty_mins
                penalty_mins = game.game.away_penalty_mins
            else:
                non_penalty_mins = 60-game.game.home_penalty_mins
                penalty_mins = game.game.home_penalty_mins

            # home_away_even_corsi_list.append(game.even_corsi/non_penalty_mins if non_penalty_mins>0 else 0)
            # home_away_pp_corsi_list.append(game.pp_corsi/penalty_mins if penalty_mins>0 else 0)

            home_away_games_list.append(game)


        # home_away_even_corsi = mean(home_away_even_corsi_list)
        # home_away_pp_corsi = mean(home_away_pp_corsi_list)

        #games on day

        #CHANGE THIS WHEN READY TO TEST CURRENT GAMES

        games_on_day = [game for game in player_object.games if game.game.date.weekday()==tomorrow.weekday()][-15:]


        high_time = datetime.strptime((f'{player_game["time"].hour+1}{player_game["time"].minute}'),'%H%M').time()
        try:
            low_time = datetime.strptime((f'{player_game["time"].hour-1}{player_game["time"].minute}'),'%H%M').time()
        except ValueError:
            ipdb.set_trace()


        games_at_time = [game for game in player_object.games if low_time <= game.game.date.time() <= high_time][-15:]




        

        rest_days = []
        rest_even_corsi_list = []
        rest_pp_corsi_list = []
        current_date = tomorrow
        last_game = games_to_use[-1]
        day_of_last_game =last_game.game.date.weekday()
        current_day = current_date.weekday()
        last_game_day_of_month = last_game.game.date.day
        current_day_of_month = current_date.day
        weekdays_between = current_day - day_of_last_game
        if weekdays_between <0: 
            weekdays_between +=7
        days_between = current_day_of_month - last_game_day_of_month
        if  -7 <= days_between <= 7:
        
            for index, game in enumerate(games_to_use):
                if index>0:
                    prev_game = games_to_use[index-1]
                    prev_game_day_of_month = prev_game.game.date.day
                    prev_game_day_of_week = prev_game.game.date.weekday()
                    date_difference = game.game.date.day - prev_game_day_of_month
                    if date_difference < 0:
                        date_difference += 7
                    day_difference = game.game.date.weekday() - prev_game_day_of_week
                    if day_difference == days_between or date_difference==weekdays_between:
                        if game.home==True:
                            game.non_penalty_mins = 60-game.game.away_penalty_mins
                            game.penalty_mins = game.game.away_penalty_mins
                        else:
                            game.non_penalty_mins = 60-game.game.home_penalty_mins
                            game.penalty_mins = game.game.home_penalty_mins
                        rest_days.append(game)
        rest_days = rest_days[-15:]

        #lists so far
            #opponent_games
            #recent_games
            #home_away_games
            #rest_days
            #games_on_day
            #games_at_time
            #injury_games

        if len(recent_games)>1:
            print(f'Recent: {round(stdev([game.shots for game in recent_games]),4)}')
        if len(opponent_games)>1:
            print(f'Opponent: {round(stdev([game.shots for game in opponent_games]),4)}')
        if len(home_away_games)>1:
            print(f'Home_Away: {round(stdev([game.shots for game in home_away_games]),4)}')
        if len(games_on_day)>1:
            print(f'On Day: {round(stdev([game.shots for game in games_on_day]),4)}')
        if len(rest_days)>1:
            print(f'Rest: {round(stdev([game.shots for game in rest_days]),4)}')
        if len(games_at_time)>1:
            print(f'At Time: {round(stdev([game.shots for game in games_at_time]),4)}')
        if len(injury_games)>1:
            print(f'Injuries: {round(stdev([game.shots for game in injury_games]),4)}')
        print('\n')
        


        how_many_games = 2

        # game.even_corsi+game.pp_corsi

        stdev_array = [{"name":"opponent_games","array":opponent_games,"stdev":stdev([(game.even_corsi+game.pp_corsi) for game in opponent_games]) if len(opponent_games)>how_many_games else 500},
                {"name":"recent_games","array":recent_games,"stdev":stdev([(game.even_corsi+game.pp_corsi) for game in recent_games]) if len(recent_games)>how_many_games else 500},
                {"name":"home_away_games","array":home_away_games,"stdev":stdev([(game.even_corsi+game.pp_corsi) for game in home_away_games]) if len(home_away_games)>how_many_games else 500},
                {"name":"rest_days","array":rest_days,"stdev":stdev([(game.even_corsi+game.pp_corsi) for game in rest_days]) if len(rest_days)>how_many_games else 500},
                {"name":"games_on_day","array":games_on_day,"stdev":stdev([(game.even_corsi+game.pp_corsi) for game in games_on_day]) if len(games_on_day)>how_many_games else 500},
                {"name":"games_at_time","array":games_at_time,"stdev":stdev([(game.even_corsi+game.pp_corsi) for game in games_at_time]) if len(games_at_time)>how_many_games else 500},
                {"name":"injury_games","array":injury_games,"stdev":stdev([(game.even_corsi+game.pp_corsi) for game in injury_games]) if len(injury_games)>how_many_games else 500}
                ]


        sorted_stdev_array = sorted(stdev_array,key=itemgetter('stdev'))
        lowest_stdev = sorted_stdev_array[0]["stdev"]

        new_stdev_array = []
        arrays = 0

        for item in sorted_stdev_array:
            if item["stdev"]-0.17<lowest_stdev:
                new_stdev_array.extend(item["array"])
                arrays+=1

        print(arrays)
        



        recent_games.extend(opponent_games_list)
        recent_games.extend(home_away_games_list)
        recent_games.extend(rest_days)
        recent_games.extend(games_on_day)
        recent_games.extend(games_at_time)
        recent_games.extend(injury_games)


        all_tested_games = set(recent_games)
        uniq_tested_games = list(all_tested_games)

        full_games = set(new_stdev_array)
        uniq_full_games = list(full_games)

        average_shot_per_corsi = mean([game.shots/(game.even_corsi+game.pp_corsi) if (game.even_corsi+game.pp_corsi)>0 else 0 for game in uniq_tested_games])*team_mult_object["team_shots_per_corsi_mult"]


        full_even_corsi_list = []
        full_pp_corsi_list = []
        high_minutes = average_minutes+3
        low_minutes = average_minutes-3

        for game in uniq_full_games:
            
            if low_minutes < game.minutes < high_minutes:
                if game.home==True:
                    non_penalty_mins = 60-game.game.away_penalty_mins
                    penalty_mins = game.game.away_penalty_mins
                else:
                    non_penalty_mins = 60-game.game.home_penalty_mins
                    penalty_mins = game.game.home_penalty_mins

                full_even_corsi_list.append(game.even_corsi/non_penalty_mins if non_penalty_mins>0 else 0)
                full_pp_corsi_list.append(game.pp_corsi/penalty_mins if penalty_mins>0 else 0)

                average_even_corsi = mean(full_even_corsi_list)
                average_pp_corsi = mean(full_pp_corsi_list)

        if len(full_even_corsi_list)==0 or len(full_pp_corsi_list)==0:
            continue

        total_even_corsi = mean([average_even_corsi,median(full_even_corsi_list)])
        total_pp_corsi = mean([average_pp_corsi,median(full_pp_corsi_list)])



        # if len(rest_days) > 3:

        #     for game in rest_days:
        #         rest_even_corsi_list.append(game.even_corsi/game.non_penalty_mins if game.non_penalty_mins>0 else 0)
        #         rest_pp_corsi_list.append(game.pp_corsi/game.penalty_mins if game.penalty_mins>0 else 0)

            
        #     rest_even_corsi = mean(rest_even_corsi_list)
        #     rest_pp_corsi = mean(rest_pp_corsi_list)




        #     total_even_corsi = mean([home_away_even_corsi,opponent_even_corsi,recent_even_corsi,rest_even_corsi])
        #     total_pp_corsi = mean([home_away_pp_corsi,opponent_pp_corsi,recent_pp_corsi,rest_pp_corsi])

        # else:
        #     total_even_corsi = mean([home_away_even_corsi,opponent_even_corsi,recent_even_corsi])
        #     total_pp_corsi = mean([home_away_pp_corsi,opponent_pp_corsi,recent_pp_corsi])

        # if total_even_corsi < total_pp_corsi:

        #     if team_mult_object["team_penalty_mins_mult"]>1.05:
        #         new_pp_multiplier = (((total_pp_corsi - total_even_corsi)/total_pp_corsi)+1)*team_mult_object["team_penalty_mins_mult"]
        #     elif team_mult_object["team_penalty_mins_mult"]<0.95:
        #         new_pp_multiplier = (((total_pp_corsi-total_even_corsi)/total_pp_corsi)*team_mult_object["team_penalty_mins_mult"])
        #     else:
        #         new_pp_multiplier = team_mult_object["team_penalty_mins_mult"]
        # else:

        try:
            penalties_drawn = [team_mult["opposing_team_penalty_mins_mult"] for team_mult in team_mults if team_mult["team"]==player_team][0]
        except IndexError:
            continue
        new_pp_multiplier = team_mult_object["team_penalty_mins_mult"]*penalties_drawn


        corsi_estimate = (((total_pp_corsi*new_pp_multiplier)+(total_even_corsi))*team_mult_object["team_hits_mult"]*team_mult_object["team_block_mult"]*team_mult_object["team_corsi_mult"])*60
        

        sog_estimate = corsi_estimate*(average_shot_per_corsi)


        player_estimate_list.append({"name":player["name"],"team":player_team,"estimate":round(sog_estimate,2),"corsi_estimate":round(corsi_estimate,2),"actual":player["shots"],"corsi_per":round(average_shot_per_corsi,3),"ranker":sog_estimate+(average_shot_per_corsi)})

        # if player["name"]=="Adam Boqvist":
        #     ipdb.set_trace()





    sorted_player_estimate_list = sorted(player_estimate_list,key=itemgetter('estimate'))
    sorted_player_estimate_list.reverse()

    team_from_player_list = []
    final_player_list = []
    for thing in sorted_player_estimate_list:
        if thing["team"] not in team_from_player_list and thing["corsi_per"]>0.59:
            team_from_player_list.append(thing["team"])
            final_player_list.append(thing)
    # final_player_list = sorted_player_estimate_list

    for index,item in enumerate(final_player_list):
        # if item["corsi_per"] > 0.6 or (index==1 and item["estimate"] > 1.75*(sorted_player_estimate_list[1])):
        name=item["name"]
        team=item["team"]
        estimate = str(item["estimate"])
        corsi_estimate = str(item["corsi_estimate"])
        actual = str(item["actual"])
        corsi_per = str(item["corsi_per"])

        first = name.ljust(25,' ')
        fifth = team.ljust(25,' ')
        second = estimate.ljust(5,' ')
        third = actual.ljust(3,' ')
        fourth = corsi_estimate.ljust(3,' ')


        print(f"{first} {fifth}, Estimate: {second}, Actual {third} (Corsi Estimate: {fourth}, Shot Per Corsi: {corsi_per})")

    if sorted_player_estimate_list[0]["estimate"]>1.8*sorted_player_estimate_list[1]["estimate"]:
        print(f'\nRecommendation: {sorted_player_estimate_list[0]["name"]}')
    else:
        print(f'\nRecommendation: {sorted_player_estimate_list[0]["name"]} and {sorted_player_estimate_list[1]["name"]}')




        #possible high pp multiplier (only if avg_pp_corsi > avg_even_corsi)
            #multiply teams penalty_minute multipler by new_pp_multiplier = (((avg_pp_corsi-avg_even_corsi)/avg_pp_corsi)+1)*team_pp_multiplier
            #if low pp multiplier, possibly do the opposite without adding 1 new_pp_multiplier = (((avg_even_corsi-avg_pp_corsi)/avg_even_corsi))*team_pp_multiplier

            #more logic so future Brian can follow this
                #the only reason for the avg_pp_corsi is to adjust the penalty minute multiplier\
                #if the team penalty minute multiplier is high, the individual players pp corsi will weigh more
                #high team penalty minute multiplier and low player pp corsi: decrease the multiplier to take into account players individual pp gameility
                #high team penalty minute multiplier and high player pp corsi: increase the multiplier to take into acount players individual pp gameility
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
