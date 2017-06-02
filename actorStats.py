'''
actorStats.py
'''
'''
====================
Stats
====================
'''
class StatsTable:
	data = {
	"None":
		{
		"health":10,
		"healthMax":10,
		"magic":0,
		"magicMax":0,
		"speed":6,
		"attack":[2,0,0,0,0,0,0],
		"attackSpeed":0,
		"defense":[0,0,0,0,0,0],
		"critChance":0
		},
	"Hero":
		{
		"health":20,
		"health":20,
		"magic":10,
		"magicMax":10,
		"speed":6,
		"attack":[2,0,0,0,0,0,0],
		"attackSpeed":0,
		"defense":[0,0,0,0,0,0],
		"critChance":0.05
		},
	"Mirehound":
		{
		"health":8,
		"healthMax":8,
		"magic":0,
		"magicMax":0,
		"speed":1,#0,
		"attack":[3,0,0,0,0,0,0],
		"attackSpeed":2,
		"defense":[0,0,0,0,0,0],
		"critChance":0.05
		},
	"Rougarou":
		{
		"health":36,
		"healthMax":40,
		"magic":0,
		"magicMax":0,
		"speed":8,
		"attack":[18,0,0,0,0,0,0],
		"attackSpeed":2,
		"defense":[6,0,0,0,0,0],
		"critChance":0.1
		},
	"Snakeman":
		{
		"health":20,
		"healthMax":20,
		"magic":0,
		"magicMax":0,
		"speed":4,
		"attack":[6,0,0,0,0,0,0],
		"attackSpeed":-4,
		"defense":[4,0,0,0,0,0],
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
