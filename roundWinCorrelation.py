from api import Log, LogList, id_from_logs_url
import json
import sys
import math
import numpy as np
def main():
    log_list = LogList(player=sys.argv[1], limit=sys.argv[2], offset=sys.argv[3])
    other_steam_id = sys.argv[4]
    num_var = 4 #vars
    mat = np.zeros((1+num_var,int(sys.argv[2])*9)) #if they won+ the current number of parameters being measured
    #length is the number of games time max number of rounds per game
    count = 0
    index = 0
    for log in log_list.logs:

        next_log = Log(log['id'])
        # print(log['id'])
        if next_log.isnt_valid_game():
            continue
        if next_log.isnt_5cp():
            continue
        rounds = next_log.get_individual_rounds()
        for r in rounds:
            winner = r['winner']
            if winner=="None":
                continue
            if r['firstcap']=="None":
                continue
            mat[0,index] = -1 if winner=='Blue' else 1

            mat[1,index] = -1 if r['firstcap']=='Blue' else 1
                
            if r['team']['Red']['ubers']==r['team']['Blue']['ubers']:
                mat[2,index] = 0
            else:
                mat[2,index] = 1 if r['team']['Red']['ubers']>r['team']['Blue']['ubers'] else -1
            if r['team']['Red']['kills']==r['team']['Blue']['kills']:
                mat[3,index] = 0
            else:
                mat[3,index] = 1 if r['team']['Red']['kills']>r['team']['Blue']['kills'] else -1
            if r['team']['Red']['dmg']==r['team']['Blue']['dmg']:
                mat[4,index] = 0
            else:
                mat[4,index] = 1 if r['team']['Red']['dmg']>r['team']['Blue']['dmg'] else -1
            index = index + 1
    # np.savetxt("rwc.csv",mat[:,0:index],delimiter=',')
    corr = np.corrcoef(mat[:,0:index])
    print("Number of rounds:"+str(index))
    print("Correlation of winning a round to a particular general stat:")
    ls = ["Midfights","Ubers Used", "Kills", "Damage"]
    for i in range(num_var):
        print("The correlation of winning to "+ls[i]+" is: "+ str(corr[i+1,0]))
    # print(corr)

main()

#steamid64, limit=5, offset=0, steamid3
#python roundWinCorrelation.py 76561198099463706 50 0 [U:1:139197978]
#b4nny python roundWinCorrelation.py 76561197970669109 50 0 [U:1:10403381]
#weeb_wacker python roundWinCorrelation.py 76561198187098041 50 0 [U:1:226832313]
#gunga python roundWinCorrelation.py 76561198874064784 50 0 [U:1:913799056]
#soupcan python roundWinCorrelation.py 76561198380821817 50 0 [U:1:420556089]
#yumyum python roundWinCorrelation.py 76561198150567198 50 0 [U:1:190301470]
#aim python roundWinCorrelation.py 76561198026627032 50 0 [U:1:66361304]
#segamw python roundWinCorrelation.py 76561198308183330 50 0 [U:1:347917602]
#cadet python roundWinCorrelation.py 76561198068141943 50 0 [U:1:107876215]
#kuhnockers python roundWinCorrelation.py 76561198073630276 50 0 [U:1:113364548]
#jefferado python roundWinCorrelation.py 76561198072321938 50 0 [U:1:112056210]
#golden python roundWinCorrelation.py 76561198065575278 100 0 [U:1:105309550]

        #should have made it so that getting a stat requires a round, and 
        #made a helper function that uses a function as an input to make
        #the helper cycle over each round. whatever im low on time

        # team = next_log.get_team(other_steam_id)

        # print("passed checks")