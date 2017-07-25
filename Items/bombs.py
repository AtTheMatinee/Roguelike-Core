'''
bombs.py
'''
from items import Item
import Items
import objects
import libtcodpy as libtcod
'''
====================
Bombs
====================
'''

class Bomb(Item):
	identified = False
	def __init__(self, game, x, y, char, name, color, level, timer, blocks=False, properNoun = False):
		Item.__init__(self, game, x, y, char, name, color, level, blocks)
		self.resetTimer = timer
		self.timer = timer
		self.armed = False
		self.actor = None

	def use(self,actor):
		self.dropFromInventory(actor)

	def dropFromInventory(self,actor):
		self.timer = self.resetTimer
		self.armed = True
		self.actor = actor
		Item.dropFromInventory(self,actor)
		actor.game.message(actor.getName(True).title()+" dropped a "+self.getName(False))

	def tick(self):
		if self.armed == True:
			if self.timer == 0:
				self.effect()
				return

			self.timer -= 1

	def effect(self):
		print self.actor
		if self.actor != None:
			self.identify(self.actor)

		self.destroy()

	def destroy(self):
		self.game._currentLevel.removeItem(self)
		self.game._currentLevel.removeObject(self)
		self.game.removeObject(self)

class Grenade(Bomb):
	def effect(self):
		physicalDam =8 + (4*self.level)
		armorPenetration = int(self.level*1.5)
		fireDam = self.level
		damage = [physicalDam,armorPenetration,fireDam,0,0,0,0,0,0]
		volume = self.volume = 15 + 3*self.level

		objects.Explosion(self.game, self.x, self.y, libtcod.yellow, damage, volume)
		print 'explosion'

		self.identify(self.actor)
		self.destroy()

class GasGrenade(Bomb):
	pass

class Smokebomb(Bomb):
	def effect(self):
		volume = 15 + 2*self.level
		objects.SmokeCloud(self.game, self.x, self.y, 'smoke', libtcod.dark_grey, volume)

		self.identify(self.actor)
		self.destroy()

class FlachetteGrenade(Bomb):
	pass
	# Does physical damage and bleed damage

class FlashGrenade(Bomb):
	pass
	# confuses any actor withing its effective range

class Spellbomb(Bomb):
	def __init__(self, game, x, y, char, name, color, level, timer, blocks=False, properNoun = False):
		Bomb.__init__(self, game, x, y, char, name, color, level, timer)
		self.spell = Items.spells.Spell(self.game,self.name,self)
		self.spell.magicCost = 0

	def effect(self):
		# Note: this implementation only works if the spell requires no target
		self.spell.cast()

		self.identify(self.actor)
		self.destroy()