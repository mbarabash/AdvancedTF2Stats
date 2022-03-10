from api import Log, LogList, id_from_logs_url
import json
import sys
import math
import numpy as np

#steamid64, limit=5, offset=0, steamid3
#python winningCorrelation.py 76561198099463706 50 0 [U:1:139197978]
#b4nny python winningCorrelation.py 76561197970669109 50 0 [U:1:10403381]
#weeb_wacker python winningCorrelation.py 76561198187098041 50 0 [U:1:226832313]
#gunga python winningCorrelation.py 76561198874064784 50 0 [U:1:913799056]
#soupcan python winningCorrelation.py 76561198380821817 50 0 [U:1:420556089]
#yumyum python winningCorrelation.py 76561198150567198 50 0 [U:1:190301470]
#aim python winningCorrelation.py 76561198026627032 50 0 [U:1:66361304]
#segamw python winningCorrelation.py 76561198308183330 50 0 [U:1:347917602]
#cadet python winningCorrelation.py 76561198068141943 50 0 [U:1:107876215]
#kuhnockers python winningCorrelation.py 76561198073630276 50 0 [U:1:113364548]
#jefferado python winningCorrelation.py 76561198072321938 50 0 [U:1:112056210]
#golden python winningCorrelation.py 76561198065575278 100 0 [U:1:105309550]
def main():
    # print("enter main")
    log_list = LogList(player=sys.argv[1], limit=sys.argv[2], offset=sys.argv[3])
    # print("log_list", log_list.__dict__ )
    other_steam_id = sys.argv[4]
    num_var = 7 #vars
    mat = np.zeros((1+num_var,int(sys.argv[2]))) #if they won+ the current number of parameters being measured
    count = 0

    for i,log in enumerate(log_list.logs):

        next_log = Log(log['id'])
        # print(log['id'])
        if next_log.isnt_valid_game():
            continue
        if next_log.check_tie():
            continue
        team = next_log.get_team(other_steam_id)
        # print("passed checks")
        rounds_tup = next_log.get_rounds(team)
        midfights = next_log.get_midfights(team)
        ubers = next_log.get_ubers(team)
        meddeaths = next_log.get_med_deaths(team)
        kills = next_log.get_kills(team)
        caps = next_log.get_pc(team)
        demodpm = next_log.get_demo_damage(team)
        airshots = next_log.get_airshots(team)

        # won = 0
        if not (rounds_tup or midfights or ubers or meddeaths or kills or caps or demodpm or airshots):
            continue
        if rounds_tup[2]==1:
            # won = 1
            mat[0,i]=1

        count+=1
        if midfights[0]>midfights[1]:
            mat[1,i]=1
        if ubers[0]>ubers[1]:
            mat[2,i]=1
        if meddeaths[0]>meddeaths[1]:
            mat[3,i]=1
        if kills[0]>kills[1]:
            mat[4,i]=1
        #the winning team should always have more captures, this is for the sake of completeness
        if caps[0]>caps[1]:
            mat[5,i]=1
        if demodpm[0]>demodpm[1]:
            mat[6,i]=1
        if airshots[0]>airshots[1]:
            mat[7,i]=1

    corr = np.corrcoef(mat[:,0:count])
    # for i in range(num_var):
    #     corr[i] = np.corrcoef(mat[0],mat[i+1])
    print("Number of games:"+str(count))

    print("Correlation of winning to a particular general stat:")
    ls = ["Midfights","Ubers Used", "Med Deaths", "Kills", "Control Point Captures", "Demoman DPM", "Airshots"]
    for i in range(num_var):
        print("The correlation of winning to "+ls[i]+" is: "+ str(corr[i+1,0]))
    # print(corr)

main()