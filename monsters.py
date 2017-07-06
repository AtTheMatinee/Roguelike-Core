'''
monsters.py
'''
from actors import Monster
'''
====================
Monsters
====================
'''
class Animal(Monster):
	pass

class Dog(Animal):
	pass

class Elemental(Monster):
	def hasTakenTurn(self):
		self.takeDamage([0,0,0,0,0,0,0,0,2])
		Monster.hasTakenTurn(self)

	# Takes damage every turn
	# heals 100% from their element
	# have a lot of elemental spells
	# have a spell that casts their elemental status effect on themself so they heal while it's in effect


class Ghost(Monster):
	def takeDamage(self, damage):
		'''
		damage = [physical, armorPenetration, fire, frost, poison, bleed, holy, unholy, unblockable]
		defense = [physical, fire, frost, poison, bleed, holy, unholy]
		'''
		defense = self.stats.get("defense")

		# ==========
		# !!! look for status effect flags with: if any(isinstance(instance,statusEffect) for instance in self.statusEffects)
		# ==========

		# ==== Fire ====
		fireDam = damage[2] - float(damage[2]*defense[1]) # inflicts inflamed
		if (fireDam >= 1) and (random.random() <= 0.05):
			self.addStatusEffect(statusEffects.Flaming,10,False)

		# ==== Frost ====
		frostDam = damage[3] - float(damage[3]*defense[2]) # inflicts frozen
		if (frostDam >= 1) and (random.random() <= 0.05):
			self.addStatusEffect(statusEffects.Frozen,10,False)

		# ==== Poison ====
		poisonDam = damage[4] - float(damage[4]*defense[3]) # inflicts poison
		if (poisonDam >= 1) and (random.random() <= 0.1):
			self.addStatusEffect(statusEffects.Poisoned,int(poisonDam)*2,False)

		# ==== Bleed ====
		bleedChance = damage[5] - float(damage[5]*defense[4]) # does not do damage, only inflicts bleed status
		if bleedChance > 0 and random.random() <= bleedChance:
			self.addStatusEffect(statusEffects.Bleeding,10,True)

		# ==== Holy ====
		holyDam = damage[6] - float(damage[6]*defense[5])
		
		# ==== Unholy ====
		unholyDam = damage[7] - float(damage[7]*defense[6])


		totalDam = (fireDam + frostDam + poisonDam + holyDam + unholyDam + damage[8])

		health = self.stats.get("healthCurrent")
		health = min(health-totalDam,self.stats.get("healthMax"))
		self.stats.setBaseStat("healthCurrent",health)
		self.checkDeath()


class Snakeman(Monster):
	pass