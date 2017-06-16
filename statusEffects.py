'''
statusEffects.py
'''
import libtcodpy as libtcod
'''
====================
Status Effects
====================
'''

'''
Status Effect Tags
	Flamable
		become flaming if dealt fire damage
	Wet
		become frozen if dealt frost damage
		adds fire defense mult buff
	Frozen
		does frost damage up front
		adds speed mult debuff and physical defense add buff
	Flaming
		does fire damage per turn
		adds fire damage mult buff and fire resistance mult debuff modifiers
	Poisoned
		does 2 damage per turn for n turns, where n is the poison damage dealt
	Bleeding
		does 1/10 of actor's health in unblockable damage 
		per turn for up to 5 turns, stacks
	Explosive
	Invisible
	Undead
		become flaming when dealt holy damage
	Cursed
	Blessed
'''

class StatusEffect(object):
	def __init__(self,actor,timer):
		self.actor = actor
		self.game = actor.game
		self.timer = int(timer)

	def effect(self):
		if self.timer == 0:
			self.actor.removeStatusEffect(self)
			self.game.message("The status effect has worn off.")
			return
			
		self.timer -= 1


# ==== Status Effects ====
class Poisoned(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)

		# message
		self.game.message(self.actor.getName(True)+" is poisoned.",libtcod.violet)

	def effect(self):
		if self.timer == 0:
			self.actor.removeStatusEffect(self)
			self.game.message(self.actor.getName(True)+" is no longer poisoned.",libtcod.light_violet)
			return

		# take poison damage
		self.actor.takeDamage([0,0,0,0, 2, 0,0,0,0])

		self.timer -= 1


class Bleeding(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)

		# does hal of your current health over ten turns
		self.damage = max(0.5,self.actor.stats.get("healthCurrent")/20)
		
		# message
		self.game.message(self.actor.getName(True)+" is bleeding.",libtcod.violet)

	def effect(self):
		if self.timer == 0:
			self.actor.removeStatusEffect(self)
			self.game.message(self.actor.getName(True)+" is no longer bleeding.",libtcod.light_violet)
			return

		# take bleed damage
		self.actor.takeDamage([0,0,0,0,0,0,0,0,self.damage])
		
		self.timer -= 1


class Frozen(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)

		# message
		self.game.message(self.actor.getName(True)+" is frozen.",libtcod.violet)

		# Take Frost Damage (20 damage up front)
		self.actor.takeDamage([0,0,0, 20, 0,0,0,0,0])

		modifier = {'add':{'defense':[4,0,0,0,0,0,0]},'mult':{'speed':-0.33}}
		self.actor.stats.addModifier(self, modifier)

	def effect(self):
		if self.timer == 0:
			self.actor.stats.removeModifier(self)
			self.actor.removeStatusEffect(self)
			self.game.message(self.actor.getName(True)+" is no longer frozen.",libtcod.light_violet)
			return
			
		self.timer -= 1


class Flaming(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)

		self.damage = 2 # take 2 damage per turn for 10 turns

		# message
		self.game.message(self.actor.getName(True)+" is on fire.",libtcod.violet)

		modifier = {'add':{'attack': [0,0, 2, 0,0,0,0,0,0]} ,'mult':{'defense':[-0.5,0,-0.5,-0.5,-0.5,-0.5,-0.5]}}
		self.actor.stats.addModifier(self, modifier)

	def effect(self):
		if self.timer == 0:
			self.actor.stats.removeModifier(self)
			self.actor.removeStatusEffect(self)
			self.game.message(self.actor.getName(True)+" is no longer on fire.",libtcod.light_violet)
			return

		# Take Fire Damage
		self.actor.takeDamage([0,0, self.damage, 0,0,0,0,0,0])
			
		self.timer -= 1


# ==== Buffs ====

# ==== Debuffs ====

class MortallyWounded(StatusEffect):
	def __init__(self,actor,timer):
		StatusEffect.__init__(self,actor,timer)

		# message
		self.game.message(self.actor.getName(True)+" is mortally wounded.",libtcod.red)

		# Add Modifier
		n = self.actor.stats.get('healthMax')/2
		modifier = {'add':{'healthMax':-n}}
		self.actor.stats.addModifier(self, modifier)

	def effect(self):
		if self.timer == 0:
			self.actor.stats.removeModifier(self)
			self.actor.removeStatusEffect(self)
			self.game.message(self.actor.getName(True)+" is no longer mortally wounded.")
			return

		self.timer -= 1