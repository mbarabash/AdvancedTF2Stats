#Some code in this file (in particular for getting logs) taken from
#https://github.com/JonathanAllenRay



import requests
import json

#Jonathan Rays Code
#gets list of desired logs
class LogList(object):
    
    def __init__(self, title=None, tfmap=None, uploader=None, player=None, limit=1000, offset=0):
        base_url = "http://logs.tf/api/v1/log?"
        title_parameter = "title=" + title + "&" if title != None else ""
        map_parameter = "map=" + tfmap + "&" if tfmap != None else ""
        uploader_parameter = "uploader=" + uploader + "&" if uploader != None else ""
        player_parameter = "player=" + player + "&" if player != None else ""
        limit_parameter = "limit=" + str(limit) + "&"
        offset_parameter = "offset=" + str(offset)
        url = base_url + title_parameter + map_parameter + uploader_parameter + player_parameter + limit_parameter + offset_parameter
        data = requests.get(url)
        self.__dict__ = data.json()
        
class Log(object):

    def __init__(self, log_id):
        self.base_url = "http://logs.tf/json/"
        url = self.base_url + str(log_id)
        data = requests.get(url)
        self.__dict__ = data.json()

    def game_type(self):
        players = len(self.players)
        if players >= 18:
            return "HL"
        elif players == 4 or players == 5:
            return "ULTIDUO"
        elif players == 12 or players == 13:
            return "6"
        else:
            total_time = self.length
            play_time = 0
            for player in self.players:
                for element in self.players[player]['class_stats']:
                    play_time += element['total_time']
                if (total_time / 2) > play_time:
                    players -= 1
            if players == 12 or players == 13:
                return "6"
            else:
                return "OTHER"

    def get_team(self,player):
        return self.players[player]['team']

#End Jonathan Rays code

    #return tuple of (# mids won, # mids lost)
    def get_midfights(self, team):
        blu_mids, red_mids = 0, 0
        #check if the number of midfights won and score is the same 
        # if the score is 4-3 but 8 rounds were played, the incomplete round should be ignored

        score = (-1,-1)
        for cycle in self.rounds:
            #ignore dead rounds
            if (cycle['team']['Blue']['score'],cycle['team']['Red']['score'])==score:
                continue
            score = (cycle['team']['Blue']['score'],cycle['team']['Red']['score'])
            mid = cycle['firstcap']
            if mid=='Blue':
                blu_mids+=1
            else:
                red_mids+=1
        if team=='Red':
            mids_won, mids_lost = red_mids, blu_mids
        else: mids_lost, mids_won = red_mids, blu_mids 
        return(mids_won, mids_lost)

    #return True if tie
    def check_tie(self):
        if self.teams['Red']['score']==self.teams['Blue']['score']:
            print("tie game, skipping...")
            return 1
        return 0

    #return tuple of (# rounds won, # rounds lost, win)
    #win is 1 or 0.
    def get_rounds(self,team):
        
        if team == 'Red':
            opposing_rounds_won = self.teams['Blue']['score']
            rounds_won = self.teams['Red']['score']
        else:
            opposing_rounds_won = self.teams['Red']['score']
            rounds_won = self.teams['Blue']['score']
        if rounds_won>opposing_rounds_won:
            win=1 
        else: win=0
        return (rounds_won, opposing_rounds_won, win)

    def get_individual_rounds(self):
        rounds = []
        for rnd in self.rounds:
            rounds.append(rnd)
        return rounds


    def isnt_5cp(self):
        map_name = self.info['map']
        # print(map_name)
        if 'cp_' in map_name:
            # print("accepted")
            return 0
        return 1

    #checks if game is a real 6s game. For the purposes of constructing advanced statistics,
    #we exclude games that are not:
    #6s games (teams have 6 players per team, 12 total)
    #games that last less than 5 minutes (outlier logs)
    #does not have the standard team composition
    def isnt_valid_game(self):
        if len(self.players)!=12:
            # print("not 12 players")
            return 1
        if self.length<60*4:
            # print("too short")
            return 1
        classes = {'soldier':4, 'scout':4,'medic':2,'demoman':2}
        for player in self.players:
            pclass = self.players[player]['class_stats'][0]['type']
            # print(pclass)
            if pclass not in classes:
                return 1
            classes[pclass]-=1
        for i in classes.values():
            # print("i:", i)
            if i!=0:
                return 1
        return 0

    # def get_psc_kills(self,team):
    #     for player in self.players:
    #         if self.players[player]['class_stats'][0]['type']!='demoman':
    #             continue
    #         if self.players[player]['team']!=team:
    #             enemy_dmg = self.players[player]['dapm']
    #             continue
    #         team_dmg = self.players[player]['dapm']
    #     return (team_dmg,enemy_dmg)

    def get_airshots(self,team):
        airshots_us = 0
        airshots_them = 0
        for player in self.players:
            if self.players[player]['team']!=team:
                airshots_them += self.players[player]['as']
                continue
            airshots_us += self.players[player]['as']
        return (airshots_us,airshots_them)

    def get_demo_damage(self,team):
        for player in self.players:
            if self.players[player]['class_stats'][0]['type']!='demoman':
                continue
            if self.players[player]['team']!=team:
                enemy_dmg = self.players[player]['dapm']
                continue
            team_dmg = self.players[player]['dapm']
        return (team_dmg,enemy_dmg)

    def get_pc(self,team):
        red_caps = self.teams['Red']['caps']
        blue_caps = self.teams['Blue']['caps']
        if team == 'Red':
            return (red_caps, blue_caps)
        return (blue_caps, red_caps)

    def get_kills(self, team):
        red_kills = self.teams['Red']['kills']
        blue_kills = self.teams['Blue']['kills']
        if team == 'Red':
            return (red_kills, blue_kills)
        return (blue_kills, red_kills)

    def get_ubers(self, team):
        for player in self.players:
            if self.players[player]['class_stats'][0]['type']!='medic':
                continue
            if self.players[player]['team']!=team:
                enemy_ubers = sum(self.players[player]['ubertypes'].values())
                continue
            ubers_used = sum(self.players[player]['ubertypes'].values())
        return (ubers_used,enemy_ubers)
        
    def get_med_deaths(self, team):
        deaths = (0,0)
        for player in self.players:
            if self.players[player]['class_stats'][0]['type']!='medic':
                continue
            if self.players[player]['team']!=team:
                their_deaths = self.players[player]['deaths']
                continue
            our_deaths = self.players[player]['deaths']
        return (our_deaths,their_deaths)

    def get_damage(self,team):
        red_damage = self.teams['Red']['dmg']
        blue_damage = self.teams['Blue']['dmg']
        if team == 'Red':
            return (red_damage, blue_damage)
        return (blue_damage, red_damage)
    
#All code below is Jonathan Rays

    # def get_scout_medic_combos(self):
    #     scout_medic_combos = dict()
    #     for medic in self.healspread:
    #         top_heal_scout = ''
    #         top_heal = 0
    #         for player in self.healspread[medic]:
    #             if self.healspread[medic][player] > top_heal and self.played_scout(player):
    #                 top_heal = self.healspread[medic][player]
    #                 top_heal_scout = player
    #         if top_heal_scout != '':
    #             scout_medic_combos[top_heal_scout] = medic
    #     return scout_medic_combos

    # #return ID:TEAM
    # def get_played_class(self, played_class, team, role=None):
    #     result = []
    #     for player in self.players:
    #         if self.players[player]['class_stats'][0]['type'] == played_class and self.players[player]['team'] == team:
    #             result.append(player)
    #     if role == 'flank':
    #         bot_heal_player = ''
    #         bot_heal = 99999999
    #         for player in result:
    #             medic = self.get_players_med(player)
    #             if medic != '' and player != '' and self.healspread[medic][player] < bot_heal:
    #                 bot_heal = self.healspread[medic][player]
    #                 bot_heal_player = player
    #         if bot_heal_player != '':
    #             result = []
    #             result.append(bot_heal_player)
    #     elif role == 'combo':
    #         top_heal_player = ''
    #         top_heal = 0
    #         for player in result:
    #             medic = self.get_players_med(player)                        
    #             if medic != '' and player != '' and self.healspread[medic][player] > top_heal:
    #                 top_heal = self.healspread[medic][player]
    #                 top_heal_player = player
    #         if top_heal_player != '':
    #             result = []
    #             result.append(top_heal_player)

    #     return result



    # def played_scout(self, player):
    #     if player in self.players.keys() and self.players[player]['class_stats'][0]['type'] == 'scout':
    #         return True
    #     else:
    #         return False    

    # def get_players_med(self, player):
    #     primary_medic = ''
    #     top_heal = 0
    #     for medic in self.healspread:
    #         if player in self.healspread[medic] and self.healspread[medic][player] > top_heal:
    #             top_heal = self.healspread[medic][player]
    #             primary_medic = medic
    #     return primary_medic





class LogUploader(object):

    def __init__(self, title, tfmap, key, logfile=None, file_path=None, uploader="LogsTFAPIWrapper", updatelog=None):
        self.url = 'http://logs.tf/upload'
        file_to_upload = logfile
        if logfile == None and file_path != None:
            file_to_upload = open(file_path, 'rb').read()

        self.files = {'logfile': file_to_upload, 
                'title': title,
                'map': tfmap,
                'key': key,
                'uploader': uploader
                }
        if updatelog != None:
            files['updatelog'] = updatelog

    def upload_log(self):
        response = requests.post(self.url, files=self.files, data=self.files, verify=False)
        print(response.json()) 

def id_from_logs_url(url):
    url = url.replace('https://logs.tf/', '')
    if '#' in url:
        return url.split('#')[0]
    else:
        return url
