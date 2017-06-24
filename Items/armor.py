'''
armor.py
'''
from items import Equipment
import randomChoice
'''
====================
Armor
====================
'''

class Armor(Equipment):
	unidentifiedName = "Mysterious Armor"
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False):
		Equipment.__init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False)
		self.equipSlot = 0

		'''
		====================
		Random stat distribution
		====================
		Set default upgrade values for all stats for armor.
		'''

		self.normalUpgradeOdds = {
		'physical defense':1,
		'poison resistance':1,
		'bleed resistance':1,
		'speed':0
		}

		self.specialUpgradeOdds = {
		'healthMax':0,
		'magicMax':0,
		'fire resistance':1,
		'frost resistance':1,
		'holy resistance':1,
		'unholy resistance':1
		}

		self.upgradePhysicalDefense = [1, 0,0,0,0,0,0]
		self.upgradePoisonResistance = [0,0,0, 0.1, 0,0,0]
		self.upgradeBleedResistance = [0,0,0,0, 0.1, 0,0]
		self.upgradeFireResistance = [0, 0.1, 0,0,0,0,0]
		self.upgradeFrostResistance = [0,0, 0.1, 0,0,0,0]
		self.upgradeHolyResistance = [0,0,0,0,0, 0.1, 0]
		self.upgradeUnholyResistance = [0,0,0,0,0,0, 0.1]
		self.upgradeHealthMax = 2
		self.upgradeMagicMax = 2
		self.upgradeSpeed = 1

	def upgrade(self, level):
		upgradeOdds = dict(self.normalUpgradeOdds)

		for i in xrange(level):
			if i == 5:
				upgradeOdds.update(self.specialUpgradeOdds)
				# at level 5, add in the elemental modifiers

			upgrade = None
			choice = randomChoice.choose(upgradeOdds)

			if choice == 'physical defense':
				upgrade = {'add':{'defense':self.upgradePhysicalDefense}}
			
			if choice == 'poison resistance':
				upgrade = {'add':{'defense':self.upgradePoisonResistance}}

			if choice == 'bleed resistance':
				upgrade = {'add':{'defense':self.upgradeBleedResistance}}

			if choice == 'fire resistance':
				upgrade = {'add':{'defense':self.upgradeFireResistance}}

			if choice == 'frost resistance':
				upgrade = {'add':{'defense':self.upgradeFrostResistance}}

			if choice == 'holy resistance':
				upgrade = {'add':{'defense':self.upgradeHolyResistance}}

			if choice == 'unholy resistance':
				upgrade = {'add':{'defense':self.upgradeUnholyResistance}}

			if choice == 'healthMax':
				upgrade = {'add':{'speed':self.upgradeHealthMax}}

			if choice == 'magicMax':
				upgrade = {'add':{'speed':self.upgradeMagicMax}}

			if choice == 'speed':
				upgrade = {'add':{'speed':self.upgradeSpeed}}

			if upgrade != None:
				self.addUpgrades(upgrade)


class Hauberk(Armor):
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False):
		Armor.__init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False)

		self.normalUpgradeOdds = {
		'physical defense':2,
		'poison resistance':1,
		'bleed resistance':2,
		'speed':0
		}

		self.specialUpgradeOdds = {
		'healthMax':0,
		'magicMax':0,
		'fire resistance':2,
		'frost resistance':2,
		'holy resistance':1,
		'unholy resistance':1
		}

		self.upgradePhysicalDefense = [.5, 0,0,0,0,0,0]
		self.upgradeBleedResistance = [0,0,0,0, 0.15, 0,0]
		self.upgradeFireResistance = [0, 0.05, 0,0,0,0,0]
		self.upgradeFrostResistance = [0,0, 0.05, 0,0,0,0]


class QuiltedJacket(Armor):
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False):
		Armor.__init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False)

		self.normalUpgradeOdds = {
		'physical defense':2,
		'poison resistance':1,
		'bleed resistance':1,
		'speed':0
		}

		self.specialUpgradeOdds = {
		'healthMax':0,
		'magicMax':0,
		'fire resistance':1,
		'frost resistance':1,
		'holy resistance':1,
		'unholy resistance':1
		}

		self.upgradePhysicalDefense = [0.5, 0,0,0,0,0,0]
		self.upgradeHolyResistance = [0,0,0,0,0, 0.05, 0]
		self.upgradeUnholyResistance = [0,0,0,0,0,0, 0.05]