'''
weapons.py
'''

from items import Equipment

import randomChoice

'''
====================
Weapons
====================
'''

class Weapon(Equipment):
	unidentifiedName = "Mysterious Weapon"
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False):
		Equipment.__init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False)
		self.equipSlot = 1

		'''
		====================
		Random stat distribution
		====================
		Set default upgrade values for all stats for weapons, in case a weapon somehow gets an unusual modifier.
		'''
		self.normalUpgradeOdds = {
		'physical damage':1,
		'armor penetration':1,
		'poison damage':1,
		'bleed chance':1,
		'attackSpeed':1,
		'critChance':1
		}

		self.specialUpgradeOdds = {
		'fire damage':1,
		'frost damage':1,
		'holy damage':1,
		'unholy damage':1
		}

		self.upgradePhysicalDamage = [1.0, 0,0,0,0,0,0,0,0]
		self.upgradeArmorPenetration = [0, 1, 0,0,0,0,0,0,0]
		self.upgradePoisonDamage = [0,0,0,0, 1, 0,0,0,0]
		self.upgradeBleedChance = [0,0,0,0,0, 0.05, 0,0,0]
		self.upgradeAttackSpeed = 2
		self.upgradeCritChance = 0.05

		self.upgradeFireDamage = [0,0, 1, 0,0,0,0,0,0]
		self.upgradeFrostDamage = [0,0,0, 1, 0,0,0,0,0]
		self.upgradeHolyDamage = [0,0,0,0,0,0, 1, 0,0]
		self.upgradeUnholyDamage = [0,0,0,0,0,0,0, 1, 0]

	def upgrade(self, level):
		upgradeOdds = dict(self.normalUpgradeOdds)

		for i in xrange(level):
			if i == 5:
				upgradeOdds.update(self.specialUpgradeOdds)
				# at level 5, add in the elemental modifiers

			upgrade = None
			choice = randomChoice.choose(upgradeOdds)

			if choice == 'physical damage':
				upgrade = {'add':{'attack':self.upgradePhysicalDamage}}
			
			if choice == 'armor penetration':
				upgrade = {'add':{'attack':self.upgradeArmorPenetration}}

			if choice == 'poison damage':
				upgrade = {'add':{'attack':self.upgradePoisonDamage}}
				
			if choice == 'bleed chance':
				upgrade = {'add':{'attack':self.upgradeBleedChance}}
				
			if choice == 'fire damage':
				upgrade = {'add':{'attack':self.upgradeFireDamage}}
				self.specialUpgradeOdds['fire damage'] += 2
				self.specialUpgradeOdds['frost damage'] = 0
				
			if choice == 'frost damage':
				upgrade = {'add':{'attack':self.upgradeFrostDamage}}
				self.specialUpgradeOdds['frost damage'] += 2
				self.specialUpgradeOdds['fire damage'] =0
				
			if choice == 'holy damage':
				upgrade = {'add':{'attack':self.upgradeHolyDamage}}
				self.specialUpgradeOdds['holy damage'] += 2
				self.specialUpgradeOdds['unholy damage'] = 0
				
			if choice == 'unholy damage':
				upgrade = {'add':{'attack':self.upgradeUnholyDamage}}
				self.specialUpgradeOdds['unholy damage'] += 2
				self.specialUpgradeOdds['holy damage'] = 0
				
			if choice == 'attackSpeed':
				upgrade = {'add':{'attackSpeed':self.upgradeAttackSpeed}}

			if choice == 'critChance':
				upgrade = {'add':{'critChance':self.upgradeCritChance}}

			if upgrade != None:
				self.addUpgrades(upgrade)


class Sword(Weapon):
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False):
		Weapon.__init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False)
		# upgrades well in physical damage, bleed chance
		# upgrades poorly in armor penetration

		#{'add':{'attack':[3.0,0,0,0,0,0.1,0,0,0]}}

		self.normalUpgradeOdds = {
		'physical damage':3,
		'armor penetration':1,
		'poison damage':1,
		'bleed chance':3,
		'attackSpeed':1,
		'critChance':1
		}

		self.specialUpgradeOdds = {
		'fire damage':2,
		'frost damage':2,
		'holy damage':1,
		'unholy damage':1
		}

		self.upgradePhysicalDamage = [1.5, 0,0,0,0,0,0,0,0]
		self.upgradeArmorPenetration = [0, .5, 0,0,0,0,0,0,0]
		self.upgradeBleedChance = [0,0,0,0,0, 0.1, 0,0,0]


class Mace(Weapon):
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False):
		Weapon.__init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False)
		# upgrades well in physical damage, holy damage, armor penetration
		# upgrades poorly in poison damage, critChance, bleed chance, attackSpeed
		
		'''
		{'add':{'attack':[3.0,2,0,0,0,0,0,0,0], 'attackSpeed':-2}}
		'''

		self.normalUpgradeOdds = {
		'physical damage':3,
		'armor penetration':3,
		'poison damage':1,
		'bleed chance':1,
		'attackSpeed':1,
		'critChance':1
		}

		self.specialUpgradeOdds = {
		'fire damage':1,
		'frost damage':1,
		'holy damage':3,
		'unholy damage':1
		}

		self.upgradePhysicalDamage = [1.5, 0,0,0,0,0,0,0,0]
		self.upgradeArmorPenetration = [0, 2, 0,0,0,0,0,0,0]
		self.upgradePoisonDamage = [0,0,0,0, .2, 0,0,0,0]
		self.upgradeBleedChance = [0,0,0,0,0, 0, 0,0,0]
		self.upgradeAttackSpeed = 0.5
		self.upgradeHolyDamage = [0,0,0,0,0,0, 2, 0,0]


class Spear(Weapon):
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False):
		Weapon.__init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False)
		# high base stats
		# upgrades poorly in armor penetration, poison damage, bleed damage, attack speed
		
		#modifier = {'add':{'attack':[5.0,0,0,0,0,0.1,0,0,0]}}

		self.normalUpgradeOdds = {
		'physical damage':4,
		'armor penetration':1,
		'poison damage':1,
		'bleed chance':1,
		'attackSpeed':1,
		'critChance':1
		}

		self.specialUpgradeOdds = {
		'fire damage':2,
		'frost damage':2,
		'holy damage':2,
		'unholy damage':2
		}

		self.upgradePhysicalDamage = [1.0, 0,0,0,0,0,0,0,0]
		self.upgradeArmorPenetration = [0, 0.5, 0,0,0,0,0,0,0]
		self.upgradePoisonDamage = [0,0,0,0, 0.5, 0,0,0,0]
		self.upgradeAttackSpeed = 1

		self.upgradeFireDamage = [0,0, 1, 0,0,0,0,0,0]
		self.upgradeFrostDamage = [0,0,0, 1, 0,0,0,0,0]
		self.upgradeHolyDamage = [0,0,0,0,0,0, 1, 0,0]
		self.upgradeUnholyDamage = [0,0,0,0,0,0,0, 1, 0]

class Dagger(Weapon):
	def __init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False):
		Weapon.__init__(self, game, x, y, char, name, color, level, equipSlot, modifier, blocks=False)
		# upgrades well in bleed, attackSpeed, critChance, poisonDamage
		# upgrades poorly in physical attack, armor penetration, fire, frost

		#'add':{'attack':[2.0,0,0,0,0,0,0,0,0], 'attackSpeed':4}, 'mult':{'critChance':0.5}

		self.normalUpgradeOdds = {
		'physical damage':1,
		'armor penetration':1,
		'poison damage':2,
		'bleed chance':2,
		'attackSpeed':2,
		'critChance':2
		}

		self.specialUpgradeOdds = {
		'fire damage':1,
		'frost damage':1,
		'holy damage':2,
		'unholy damage':2
		}

		self.upgradePhysicalDamage = [0.5, 0,0,0,0,0,0,0,0]
		self.upgradeArmorPenetration = [0, 0.5, 0,0,0,0,0,0,0]
		self.upgradePoisonDamage = [0,0,0,0, 1.5, 0,0,0,0]
		self.upgradeBleedChance = [0,0,0,0,0, 0.1, 0,0,0]
		self.upgradeAttackSpeed = 3
		self.upgradeCritChance = 0.05

		self.upgradeFireDamage = [0,0, 0.5, 0,0,0,0,0,0]
		self.upgradeFrostDamage = [0,0,0, 0.5, 0,0,0,0,0]