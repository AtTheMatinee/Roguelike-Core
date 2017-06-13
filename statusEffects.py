'''
statusEffects.py
'''
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

class StatusEffect:
	def __init__(self,actor,timer):
		self.actor = actor
		self.game = actor.game
		self.timer = timer

	def effect(self):
		if self.timer == 0:
			self.actor.removeStatusEffect(self)
			self.game.message("The status effect has worn off.")

		self.timer -= 1

# Status Effects

# Buffs

# Debuffs