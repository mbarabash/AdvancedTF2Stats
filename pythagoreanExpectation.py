from api import Log, LogList, id_from_logs_url
import json
import sys
import math

#steamid64, limit=5, offset=0, steamid3
def main():
    # print("enter main")
    log_list = LogList(player=sys.argv[1], limit=sys.argv[2], offset=sys.argv[3])
    # print("log_list", log_list.__dict__ )
    other_steam_id = sys.argv[4]
    count = 0
    wins = 0
    rounds_for_total = 0
    rounds_against_total = 0
    midfights_for_total = 0
    midfights_against_total = 0
    ubers_used_total = 0
    ubers_dropped_total = 0
    med_deaths = 0
    their_med_deaths = 0

    for log in log_list.logs:

        next_log = Log(log['id'])
        # print(log['id'])
        if next_log.isnt_valid_game():
            continue
        if next_log.check_tie():
            continue
        team = next_log.get_team(other_steam_id)
        # print("passed checks")
        tup1 = next_log.get_rounds(team)
        tup2 = next_log.get_midfights(team)
        tup3 = next_log.get_ubers(team)
        tup4 = next_log.get_med_deaths(team)

        if tup1:
            count+=1
            rounds_for_total += tup1[0]
            rounds_against_total += tup1[1]
            wins+= tup1[2]
        if tup2:
            midfights_for_total+= tup2[0]
            midfights_against_total+=tup2[1]
        if tup3:   
            ubers_used_total += tup3[0]
            ubers_dropped_total+=tup3[1]
        if tup4:
            med_deaths += tup4[0]
            their_med_deaths += tup4[1]



    print("Percentage of games won:", wins/count)
    print("Number of games won out of total", wins, "out of", count, "games")
    print("Rounds for vs Rounds against:", (rounds_for_total,rounds_against_total))
    print("Pythagorean Expectation using Rounds and exponent 2:", rounds_for_total**2/(rounds_for_total**2+rounds_against_total**2))
    pythagenport = 1.5*math.log((rounds_for_total+rounds_against_total)/count)+.45
    print("Pythagenport value:", pythagenport)
    print("Pythagenport Expectation using Rounds:", rounds_for_total**pythagenport/(rounds_for_total**pythagenport+rounds_against_total**pythagenport))
    pythagenpat = ((rounds_for_total+rounds_against_total)/count)**.287
    print("Pythagenpat value:", pythagenpat)
    print("Pythagenpat Expectation using Rounds:", rounds_for_total**pythagenpat/(rounds_for_total**pythagenpat+rounds_against_total**pythagenpat))

    print("Mids for vs Mids against:", (midfights_for_total,midfights_against_total))
    print("Pythagorean Expectation using Midfights and exponent 2:", midfights_for_total**2/(midfights_for_total**2+midfights_against_total**2))
    pythagenport = 1.5*math.log((midfights_for_total+midfights_against_total)/count)+.45
    print("Pythagenport value:", pythagenport)
    print("Pythagenport Expectation using midfights:", midfights_for_total**pythagenport/(midfights_for_total**pythagenport+midfights_against_total**pythagenport))
    pythagenpat = ((midfights_for_total+midfights_against_total)/count)**.287
    print("Pythagenpat value:", pythagenpat)
    print("Pythagenpat Expectation using midfights:", midfights_for_total**pythagenpat/(midfights_for_total**pythagenpat+midfights_against_total**pythagenpat))

    print("Ubers used vs Ubers Dropped:", (ubers_used_total,ubers_dropped_total))
    print("Pythagorean Expectation using ubers and exponent 2:", ubers_used_total**2/(ubers_used_total**2+ubers_dropped_total**2))
    pythagenport = 1.5*math.log((ubers_used_total+ubers_dropped_total)/count)+.45
    print("Pythagenport value:", pythagenport)
    print("Pythagenport Expectation using ubers:", ubers_used_total**pythagenport/(ubers_used_total**pythagenport+ubers_dropped_total**pythagenport))
    pythagenpat = ((ubers_used_total+ubers_dropped_total)/count)**.287
    print("Pythagenpat value:", pythagenpat)
    print("Pythagenpat Expectation using ubers:", ubers_used_total**pythagenpat/(ubers_used_total**pythagenpat+ubers_dropped_total**pythagenpat))

    # print("Med Death Comparison:", (med_deaths,their_med_deaths))
    # print("Pythagorean Expectation using Med Deaths and exponent 2:", med_deaths**2/(med_deaths**2+their_med_deaths**2))
    # pythagenport = 1.5*math.log((med_deaths+their_med_deaths)/count)+.45
    # print("Pythagenport value:", pythagenport)
    # print("Pythagenport Expectation using Med Deaths:", med_deaths**pythagenport/(med_deaths**pythagenport+their_med_deaths**pythagenport))
    # pythagenpat = ((med_deaths+their_med_deaths)/count)**.287
    # print("Pythagenpat value:", pythagenpat)
    # print("Pythagenpat Expectation using Med Deaths:", med_deaths**pythagenpat/(med_deaths**pythagenpat+their_med_deaths**pythagenpat))



main()