

#the idea is that: if the flank dies, does something happen
#if something negative happens when the flank dies - thats the combos fault
#if something positive happens when the flank dies - thats credit to the flank

import re

class gameState(object):

	CLASSES = ["Scout","Soldier","Demoman","Medic","heavyweapons","engineer","spy","Sniper","Pyro"]
	OFFCLASSING_CLASSES = ["Scout","Scout","Soldier","Soldier","Demoman","Medic","Scout","Scout","Soldier","Soldier","Demoman","Medic"]
	def __init__(self,teamids=[None]*12):
		#ignore koth for now, different mentality for measuring that
		midfight = 1
		points_owned = [2,2]
		r_scoot = teamids[0]
		r_scank = teamids[1]
		r_pock = teamids[2]
		r_roam = teamids[3]
		r_dem = teamids[4]
		r_med =	teamids[5]
		b_scoot = teamids[6]
		b_scank = teamids[7]
		b_pock = teamids[8]
		b_roam = teamids[9]
		b_dem = teamids[10]
		b_med =	teamids[11]


		kill = [-1,-1]
		recent_db = 0
		recent_dr = 0
		uber_r = 0
		uber_b = 0
		odlist = {key:[0,0,i-1] for i,key in enumerate(teamids)} #(offclassing, dead, position)



	def round_start(self):
		self.midfight=1

	def mid_end(self):
		self.midfight=0

	def get_state(self):
		return [self.midfight, (self.recent_dr,self.recent_db), (self.uber_r,self.uber_b), self.odlist,]


	def update_state(self, line):
		if " spawned " in line:
			steamid = re.findall('\[.*?\]', line)
			odindex = self.odlist[sid]
			position_index = odindex[2]
			cla = set(line).intersection(CLASSES)
			if OFFCLASSING_CLASSES[position_index]!=cla:
				self.odlist[sid] = (1,odindex[1],odindex[2])
			else:
				self.odlist[sid] = (0,odindex[1],odindex[2])

		if " killed " in line:
			steamids = re.findall('\[.*?\]', line)
			