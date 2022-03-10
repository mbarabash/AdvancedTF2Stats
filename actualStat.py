import gameState

def main():
    rounds = get_rounds()

    for line in rounds:
        





def get_rounds(logpath='log_3118292.log'):
    with open(logpath) as f:
        rounds = [None]*len(f.readlines())
        record = 0
        cont = 2
        for i, line in enumerate(f):
            #start recording when first round starts
            if "Round_Start" in line:
                record = 1
            #current score printed at the end of each round, stop recording till next round
            if "current score" in line:
                record = 0
                rounds[i] = line
            if record:
                rounds[i] = line

        return [x for x in rounds if x is not None]


main()