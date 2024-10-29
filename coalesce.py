 for game in rows:

            

            url_ending = game.select('a')[0].get("href")

            # ipdb.set_trace()

            box_score_url = f"https://www.hockey-reference.com{url_ending}"

            box_score = requests.get(box_score_url, headers={'User-Agent':"Mozilla/5.0"})

            box_score_data = BeautifulSoup(box_score.content.decode('utf-8'), "html.parser")
            with open("output.html", "w") as file:
                file.write(box_score_data.decode('utf-8'))


            away_players = box_score_data.select('tbody')[0].select('tr')
            home_players = box_score_data.select('tbody')[2].select('tr')

            players = []

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

            print(match)
            time.sleep(3.2)