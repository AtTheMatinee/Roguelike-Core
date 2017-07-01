'''
actorStats.py
'''
'''
====================
Stats
====================
'''
# attack = [physical, armorPenetration, fire, frost, poison, bleed, holy, unholy, unblockable]
# defense = [physical, fire, frost, poison, bleed, holy, unholy]
class StatsTable:
	data = {
	"None":
		{
		"healthCurrent":10,
		"healthMax":10,
		"magicCurrent":0,
		"magicMax":0,
		"speed":6,
		"attack":[2,0,0,0,0,0,0,0,0],
		"attackSpeed":0,
		"defense":[0,0,0,0,0,0,0],
		"critChance":0
		},
	"Gargoyle":
		{
		"healthCurrent":20,
		"healthMax":20,
		"magicCurrent":0,
		"magicMax":15,
		"speed":6,
		"attack":[8.0,0,0,0,0,0,0,0,0],
		"attackSpeed":-4,
		"defense":[12,0.5,0.5,0.5,0.5,0,0],
		"critChance":0
		},
	"Ghost":
		{
		"healthCurrent":10,
		"healthMax":10,
		"magicCurrent":0,
		"magicMax":20,
		"speed":6,
		"attack":[4.0,0,0,0,0,0,0,4,0],
		"attackSpeed":0,
		"defense":[0,0.5,0.5,1,1,-1,-1],
		"critChance":0
		},
	"Hero":
		{
		"healthCurrent":20,
		"healthMax":20,
		"magicCurrent":10,
		"magicMax":10,
		"speed":6,
		"attack":[2,0,0,0,0,0,0,0,0],
		"attackSpeed":0,
		"defense":[2,0,0,0,0,0,0],
		"critChance":0.05
		},
	"Plague Rat":
		{
		"healthCurrent":10,
		"healthMax":10,
		"magicCurrent":0,
		"magicMax":0,
		"speed":5,
		"attack":[0,0,0,0,2,0,0,0,0],
		"attackSpeed":0,
		"defense":[1,0,0,.5,0,0,0],
		"critChance":0.05
		},
	"Mirehound":
		{
		"healthCurrent":6,
		"healthMax":6,
		"magicCurrent":0,
		"magicMax":0,
		"speed":8,
		"attack":[2,0,0,0,0,0.1,0,0,0],
		"attackSpeed":2,
		"defense":[0,0,0,0,0,0,0],
		"critChance":0.05
		},
	"Rougarou":
		{
		"healthCurrent":26,
		"healthMax":26,
		"magicCurrent":0,
		"magicMax":0,
		"speed":10,
		"attack":[12,4,0,0,0,0.1,0,0,0],
		"attackSpeed":2,
		"defense":[6,0,0,0,0,0,0],
		"critChance":0.1
		},
	"Snakeman":
		{
		"healthCurrent":20,
		"healthMax":20,
		"magicCurrent":0,
		"magicMax":0,
		"speed":5,
		"attack":[4,0,0,0,0,0,0,0,0],
		"attackSpeed":-4,
		"defense":[2,0,0,.5,0,0,0],
		"critChance":0.05
		}
	}

class Stats:
	def __init__(self, statTableID):	
		self.statBase = {}
		self.initializeStats(statTableID)

		self.statMod = {}

	def initializeStats(self,statTableID):
		if statTableID not in StatsTable.data:
			statTableID = "None"

		for stat,value in StatsTable.data[statTableID].items():
			self.setBaseStat(stat,value)

	def getBaseStat(self,stat):
		return self.statBase[stat]

	def setBaseStat(self,stat,value):
		self.statBase[stat] = value

	def addModifier(self,id,mod):
		# Check if mod includes an add modifier
		if 'add' in mod:
			add = mod['add']
		else:
			add = {}

		# Check if mod includes a mult modifier
		if 'mult' in mod:
			mult = mod['mult']
		else:
			mult = {}

		self.statMod[id] = {
		'add':add,
		'mult':mult
		}

	def removeModifier(self,id):
		if id in self.statMod:
			del self.statMod[id]

	def get(self,stat):
		# attack and defense require special processes
		if (stat == 'attack') or (stat == 'defense'):
			# returns the modified version of a stat
			total = list(self.statBase[stat]) #list() creates a copy of self.statBase[stat]. if it is omitted, you accidently copy the reference to the list instead of its values
			
			multiplier = [0]*len(total)

			# Get the total of each kind of modifier
			for key,value in self.statMod.items():
				if stat in value['add']:
					if len(total) == len(value['add'][stat]):
						# total the values
						for i in xrange(len(total)):
							total[i] += value['add'][stat][i]

					else: print "stat modifier has an incorrect number of items"

				if stat in value['mult']:
					if len(total) == len(value['mult'][stat]):
						# total the values
						for i in xrange(len(total)):
							multiplier[i] += value['mult'][stat][i]

					else: print "stat modifier has an incorrect number of items"

			# add total and total*multiplier
			for i in xrange(len(total)):
				total[i] += total[i]*multiplier[i]
			return total


		# Do normal Stats
		else:
			# returns the modified version of a stat
			if stat in self.statBase:
				total = self.statBase[stat]
			else:
				total = 0
				print "Error: base stat "+str(stat)+" was not found."
			
			multiplier = 0

			# Get the total of each kind of modifier
			for key,value in self.statMod.items():
				if stat in value['add']:
					total += value['add'][stat]
				if stat in value['mult']:
					multiplier += value['mult'][stat]

			return total + (total * multiplier)
