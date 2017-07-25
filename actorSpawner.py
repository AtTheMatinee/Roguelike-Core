'''
actorSpawner.py
'''
import random
import actors
import monsters
import actorStats
import states
import libtcodpy as libtcod
'''
====================
Actor Spawner
====================
'''

# TODO: Actors with inventorySize > 0 will sometimes spawn with items
# TODO: Revamp how monsters work
'''
	Monsters spawn at a certain level, which is consistant among monsters of that type
	TODO: Monsters upgrade the same way that items do
		Since monsters upgrade according to their level, monsters will vary more between 
		instances as the levels get higher
	Monsters that spawn in with gear will have gear appropriate to their levels
'''

class ActorSpawner:
	def __init__(self,game):
		self.game = game

		self.spawnMethods = {
			'Alchemist':self.spawnHeroAlchemist,
			'Arbalest':self.spawnHeroArbalest,
			'Assassin':self.spawnHeroAssassin,
			'Barbarian':self.spawnHeroBarbarian,
			'Cleric':self.spawnHeroCleric,
			'Houndmaster':self.spawnHeroHoundmaster,
			'Knight':self.spawnHeroKnight,
			'Occultist':self.spawnHeroOccultist,
			'Magician':self.spawnHeroMagician,
			'Mercenary':self.spawnHeroMercenary,
			'Specialist':self.spawnHeroSpecialist,
			'Systems Test':self.spawnHeroTest,
			'Angel':self.spawnAngel,
			'Bloat':self.spawnBloat,
			'Cultist':self.spawnCultist,
			'Demon':self.spawnDemon,
			'Fire Elemental':self.spawnFireElemental,
			'Frost Elemental':self.spawnFrostElemental,
			'Gargoyle':self.spawnGargoyle,
			'Ghost':self.spawnGhost,
			'Golem':self.spawnGolem,
			'Mimic':self.spawnChest,
			'Mirehound':self.spawnMirehound,
			'Plague Rat':self.spawnPlagueRat,
			'Rougarou':self.spawnRougarou,
			'Snakeman':self.spawnSnakeman,
			'Snakeman Archer':self.spawnSnakemanArcher,
			'Swamp Hag':self.spawnSwampHag,
			'Wyrm':self.spawnWyrm
			}
		'''
			Lancer
			Sorceror
			Brute
			Archer
			Rogue
			Champion
		'''

	def spawn(self,x,y,key, new = True):
		level = 0
		if key in self.spawnMethods:
			actor = self.spawnMethods[key](x,y,level,new)

			# give the actor a reference to its own spawn key
			actor._spawnKey = key
			return actor


	def spawnAngel(self,x,y,level,new):
		pass

	def spawnAutomaton(self,x,y,level,new):
		# Drops bombs
		pass

	def spawnBloat(self,x,y,level,new):
		level = 2

		lootDrops = {'Potion':0.3,'Grenade':0.5}
		bloat = monsters.Bloat(self.game,x,y,'b',"Bloat",libtcod.light_red,level,faction = "Abominations",stats = actorStats.Stats("Bloat"),state = states.AI(1,1,1,0,1,0,0),drops = lootDrops)
		bloat.deathState = states.DeathState(bloat)

		if new == True:
			# add starting spells
			for spell in ['Explode']:
				s = self.game.spellSpawner.spawn(bloat, spell)
				bloat.spells.append(s)

		return bloat

	def spawnCultist(self,x,y,level,new):
		pass

	def spawnDemon(self,x,y,level,new):
		pass

	def spawnHeroAlchemist(self,x,y,level,new):
		hero = actors.Hero(self.game,x,y,'@',"Hero",libtcod.white,level,faction = "Hero",stats = actorStats.Stats("Hero Alchemist"),surviveMortalWound = True, inventorySize = 20, canEquipArmor = True, canEquipWeapons = True, playerControlled = True)
		hero.deathState = states.DeathState(hero)
		
		if new == True:
			# add equipment
			weapon = self.game.itemSpawner.spawn(x,y,'Light Weapon',0,False)
			hero.equipItem(weapon)

			#armor = self.game.itemSpawner.spawn(x,y,'Robes',0,False)
			#hero.equipItem(armor)

			# add items to inventory
			for item in [("Health Potion",0),('Medicine',0),('Toxin',0),('Potion',0)]:
				gear,itemLevel = item
				g = self.game.itemSpawner.spawn(x,y,gear,itemLevel,False)
				g.moveToInventory(hero)
				g.__class__.identified = True

			# add starting spells
			for spell in []:
				s = self.game.spellSpawner.spawn(hero, spell)
				hero.spells.append(s)

		return hero

	def spawnHeroArbalest(self,x,y,level,new):
		hero = actors.Hero(self.game,x,y,'@',"Hero",libtcod.white,level,faction = "Hero",stats = actorStats.Stats("Hero Arbalest"),surviveMortalWound = True, inventorySize = 20, canEquipArmor = True, canEquipWeapons = True, playerControlled = True)
		hero.deathState = states.DeathState(hero)
		
		if new == True:
			# add equipment
			weapon = self.game.itemSpawner.spawn(x,y,'Light Crossbow',0,False)
			hero.equipItem(weapon)

			armor = self.game.itemSpawner.spawn(x,y,'Light Armor',0,False)
			hero.equipItem(armor)

			# add items to inventory
			for item in [('Potion',0),('Wooden Bolt',0),('Wooden Bolt',0),('Steel Bolt',0)]:
				gear,itemLevel = item
				g = self.game.itemSpawner.spawn(x,y,gear,itemLevel,False)
				g.moveToInventory(hero)
				#g.__class__.identified = True

			# add starting spells
			for spell in []:
				s = self.game.spellSpawner.spawn(hero, spell)
				hero.spells.append(s)

		return hero

	def spawnHeroAssassin(self,x,y,level,new):
		hero = actors.Hero(self.game,x,y,'@',"Hero",libtcod.white,level,faction = "Hero",stats = actorStats.Stats("Hero Assassin"),surviveMortalWound = True, inventorySize = 20, canEquipArmor = True, canEquipWeapons = True, playerControlled = True)
		hero.deathState = states.DeathState(hero)
		
		if new == True:
			# add equipment
			weapon = self.game.itemSpawner.spawn(x,y,'Dagger',0,False)
			hero.equipItem(weapon)

			#armor = self.game.itemSpawner.spawn(x,y,'Armor',0,False)
			#hero.equipItem(armor)

			# add items to inventory
			for item in [("Poison",0),('Poison',1)]:
				gear,itemLevel = item
				g = self.game.itemSpawner.spawn(x,y,gear,itemLevel,False)
				g.moveToInventory(hero)
				g.__class__.identified = True

			# add starting spells
			for spell in []:
				s = self.game.spellSpawner.spawn(hero, spell)
				hero.spells.append(s)

		return hero

	def spawnHeroBarbarian(self,x,y,level,new):
		hero = actors.Hero(self.game,x,y,'@',"Hero",libtcod.white,level,faction = "Hero",stats = actorStats.Stats("Hero Barbarian"),surviveMortalWound = True, inventorySize = 20, canEquipArmor = True, canEquipWeapons = True, playerControlled = True)
		hero.deathState = states.DeathState(hero)
		
		if new == True:
			# add equipment
			weapon = self.game.itemSpawner.spawn(x,y,'Heavy Weapon',0,False)
			hero.equipItem(weapon)

			armor = self.game.itemSpawner.spawn(x,y,'Light Armor',0,False)
			hero.equipItem(armor)

			# add items to inventory
			for item in []:
				gear,itemLevel = item
				g = self.game.itemSpawner.spawn(x,y,gear,itemLevel,False)
				g.moveToInventory(hero)
				#g.__class__.identified = True

			# add starting spells
			for spell in []:
				s = self.game.spellSpawner.spawn(hero, spell)
				hero.spells.append(s)

		return hero

	def spawnHeroCleric(self,x,y,level,new):
		hero = actors.Hero(self.game,x,y,'@',"Hero",libtcod.white,level,faction = "Hero",stats = actorStats.Stats("Hero Cleric"),surviveMortalWound = True, inventorySize = 20, canEquipArmor = True, canEquipWeapons = True, playerControlled = True)
		hero.deathState = states.DeathState(hero)
		
		if new == True:
			# add equipment
			weapon = self.game.itemSpawner.spawn(x,y,'Mace',0,False)
			hero.equipItem(weapon)

			#armor = self.game.itemSpawner.spawn(x,y,'Church Robes',0,False)
			#hero.equipItem(armor)

			# add items to inventory
			for item in []:
				gear,itemLevel = item
				g = self.game.itemSpawner.spawn(x,y,gear,itemLevel,False)
				g.moveToInventory(hero)
				#g.__class__.identified = True

			# add starting spells
			for spell in ['Self Heal']:
				s = self.game.spellSpawner.spawn(hero, spell)
				hero.spells.append(s)

		return hero

	def spawnHeroHoundmaster(self,x,y,level,new):
		hero = actors.Hero(self.game,x,y,'@',"Hero",libtcod.white,level,faction = "Hero",stats = actorStats.Stats("Hero Houndmaster"),surviveMortalWound = True, inventorySize = 20, canEquipArmor = True, canEquipWeapons = True, playerControlled = True)
		hero.deathState = states.DeathState(hero)
		
		if new == True:
			# add equipment
			weapon = self.game.itemSpawner.spawn(x,y,'Melee Weapon',0,False)
			hero.equipItem(weapon)

			#armor = self.game.itemSpawner.spawn(x,y,'Armor',0,False)
			#hero.equipItem(armor)

			# add items to inventory
			for item in []:
				gear,itemLevel = item
				g = self.game.itemSpawner.spawn(x,y,gear,itemLevel,False)
				g.moveToInventory(hero)
				#g.__class__.identified = True

			# add starting spells
			for spell in []: # Charm Dog Spell
				s = self.game.spellSpawner.spawn(hero, spell)
				hero.spells.append(s)

			# spawn dogs

		return hero

	def spawnHeroKnight(self,x,y,level,new):
		hero = actors.Hero(self.game,x,y,'@',"Hero",libtcod.white,level,faction = "Hero",stats = actorStats.Stats("Hero Knight"),surviveMortalWound = True, inventorySize = 20, canEquipArmor = True, canEquipWeapons = True, playerControlled = True)
		hero.deathState = states.DeathState(hero)
		
		if new == True:
			# add equipment
			weapon = self.game.itemSpawner.spawn(x,y,'Sword',1,False)
			hero.equipItem(weapon)

			# shield = self.game.itemSpawner.spawn(x,y,'Shield',0,False)
			# hero.equipItem(shield)

			armor = self.game.itemSpawner.spawn(x,y,'Armor',1,False)
			hero.equipItem(armor)

			# add items to inventory
			for item in []:
				gear,itemLevel = item
				g = self.game.itemSpawner.spawn(x,y,gear,itemLevel,False)
				g.moveToInventory(hero)
				#g.__class__.identified = True

			# add starting spells
			for spell in []:
				s = self.game.spellSpawner.spawn(hero, spell)
				hero.spells.append(s)

		return hero

	def spawnHeroOccultist(self,x,y,level,new):
		hero = actors.Hero(self.game,x,y,'@',"Hero",libtcod.white,level,faction = "Hero",stats = actorStats.Stats("Hero Occultist"),surviveMortalWound = True, inventorySize = 20, canEquipArmor = True, canEquipWeapons = True, playerControlled = True)
		hero.deathState = states.DeathState(hero)
		
		if new == True:
			# add equipment
			weapon = self.game.itemSpawner.spawn(x,y,'Light Weapon',0,False)
			hero.equipItem(weapon)

			#armor = self.game.itemSpawner.spawn(x,y,'Robes',0,False)
			#hero.equipItem(armor)

			# add items to inventory
			for item in []:
				gear,itemLevel = item
				g = self.game.itemSpawner.spawn(x,y,gear,itemLevel,False)
				g.moveToInventory(hero)
				#g.__class__.identified = True

			# add starting spells
			for spell in ['Self Heal','Firebolt','Fireball']:
				s = self.game.spellSpawner.spawn(hero, spell)
				hero.spells.append(s)

		return hero

	def spawnHeroMagician(self,x,y,level,new):
		hero = actors.Hero(self.game,x,y,'@',"Hero",libtcod.white,level,faction = "Hero",stats = actorStats.Stats("Hero Magician"),surviveMortalWound = True, inventorySize = 20, canEquipArmor = True, canEquipWeapons = True, playerControlled = True)
		hero.deathState = states.DeathState(hero)
		
		if new == True:
			# add equipment
			weapon = self.game.itemSpawner.spawn(x,y,'Light Weapon',0,False)
			hero.equipItem(weapon)

			#armor = self.game.itemSpawner.spawn(x,y,'Armor',0,False)
			#hero.equipItem(armor)

			# add items to inventory
			for item in []:
				gear,itemLevel = item
				g = self.game.itemSpawner.spawn(x,y,gear,itemLevel,False)
				g.moveToInventory(hero)
				#g.__class__.identified = True

			# add starting spells
			for spell in ['Self Heal','Firebolt','Fireball']:
				s = self.game.spellSpawner.spawn(hero, spell)
				hero.spells.append(s)

		return hero

	def spawnHeroMercenary(self,x,y,level,new):
		hero = actors.Hero(self.game,x,y,'@',"Hero",libtcod.white,level,faction = "Hero",stats = actorStats.Stats("Hero Mercenary"),surviveMortalWound = True, inventorySize = 20, canEquipArmor = True, canEquipWeapons = True, playerControlled = True)
		hero.deathState = states.DeathState(hero)
		
		if new == True:	
			# add equipment
			weapon = self.game.itemSpawner.spawn(x,y,'Melee Weapon',0,False)
			hero.equipItem(weapon)

			armor = self.game.itemSpawner.spawn(x,y,'Armor',0,False)
			hero.equipItem(armor)

			# add items to inventory
			for item in [("Medicine",0)]:
				gear,itemLevel = item
				g = self.game.itemSpawner.spawn(x,y,gear,itemLevel,False)
				g.moveToInventory(hero)
				#g.__class__.identified = True

			# add starting spells
			for spell in ['Self Heal','Firebolt','Fireball']:
				s = self.game.spellSpawner.spawn(hero, spell)
				hero.spells.append(s)

		return hero

	def spawnHeroSpecialist(self,x,y,level,new):
		hero = actors.Hero(self.game,x,y,'@',"Hero",libtcod.white,level,faction = "Hero",stats = actorStats.Stats("Hero Specialist"),surviveMortalWound = True, inventorySize = 20, canEquipArmor = True, canEquipWeapons = True, playerControlled = True)
		hero.deathState = states.DeathState(hero)
		
		if new == True:
			# add equipment
			weapon = self.game.itemSpawner.spawn(x,y,'Light Weapon',0,False)
			hero.equipItem(weapon)

			armor = self.game.itemSpawner.spawn(x,y,'Light Armor',0,False)
			hero.equipItem(armor)

			# add items to inventory
			for item in [('Smokebomb',0),('Grenade',0),('Bomb',0)]: # spellbombs
				gear,itemLevel = item
				g = self.game.itemSpawner.spawn(x,y,gear,itemLevel,False)
				g.moveToInventory(hero)
				g.__class__.identified = True

			# add starting spells
			for spell in []:
				s = self.game.spellSpawner.spawn(hero, spell)
				hero.spells.append(s)

		return hero

	def spawnHeroTest(self,x,y,level,new):
		hero = actors.Hero(self.game,x,y,'@',"Hero",libtcod.white,level,faction = "Hero",stats = actorStats.Stats("Hero Systems Test"),surviveMortalWound = True, inventorySize = 20, canEquipArmor = True, canEquipWeapons = True, playerControlled = True)
		hero.deathState = states.DeathState(hero)
		
		if new == True:
			# add equipment
			weapon = self.game.itemSpawner.spawn(x,y,'Melee Weapon',0,False)
			hero.equipItem(weapon)

			armor = self.game.itemSpawner.spawn(x,y,'Armor',0,False)
			hero.equipItem(armor)

			# add items to inventory
			for item in [("Health Potion",0),('Health Potion',0),('Potion',0),('Invisibility Potion',0),('Light Crossbow',0),('Wooden Bolt',0),('Smokebomb',0),('Grenade',0)]:
				gear,itemLevel = item
				g = self.game.itemSpawner.spawn(x,y,gear,itemLevel,False)
				g.moveToInventory(hero)
				#g.__class__.identified = True

			# add starting spells
			for spell in ['Self Heal','Firebolt','Fireball','Explode','Invisibility']:
				s = self.game.spellSpawner.spawn(hero, spell)
				hero.spells.append(s)

			allStatusEffects = False
			import statusEffects
			if allStatusEffects == True:
				#import statusEffects
				for SE in [statusEffects.Flaming,statusEffects.Wet,statusEffects.Invisible,statusEffects.Poisoned,
					statusEffects.Bleeding,statusEffects.Flamable,statusEffects.Regenerating,statusEffects.MortallyWounded,
					statusEffects.Frozen,statusEffects.Afraid,statusEffects.Confused]:
					hero.addStatusEffect(SE,1,False)
				
		return hero


	def spawnFireElemental(self,x,y,level,new):
		pass

	def spawnFrostElemental(self,x,y,level,new):
		pass

	def spawnGargoyle(self,x,y,level,new):
		pass

	def spawnGhost(self,x,y,level,new):
		# Fear spell, Find Player Spell, Invisibility Spell, debuff spell
		level = 3

		lootDrops = {'Potion':0.6,'Invisibility Potion':0.3} # Scrolls
		ghost = monsters.Ghost(self.game,x,y,'g',"Ghost",libtcod.lightest_cyan,level,faction = "Ghosts",stats = actorStats.Stats("Ghost"),state = states.AI(0.7,0.6,0.4,0.5,0.5,0,0),drops = lootDrops)
		ghost.deathState = states.DeathState(ghost)

		if new == True:
			# add starting spells
			for spell in ['Locate Player','Invisibility','Fear']:
				s = self.game.spellSpawner.spawn(ghost, spell)
				ghost.spells.append(s)

		return ghost

	def spawnGolem(self,x,y,level,new):
		# drops spellbombs
		pass

	def spawnKnight(self,x,y,level,new):
		pass

	def spawnChest(self,x,y,level,new):
		# Spell Mimic, something else that really nasty
		pass

	def spawnMirehound(self,x,y,level,new):
		lootDrops = {'Health Potion':0.5}
		mirehound = monsters.Dog(self.game,x,y,'h',"Mirehound",libtcod.light_amber,level,faction = "Mirehounds",stats = actorStats.Stats("Mirehound"),state = states.AI(0.7,0.5,0.5,1,0,0,0),drops = lootDrops)
		mirehound.deathState = states.DeathState(mirehound)
		return mirehound

	def spawnPlagueRat(self,x,y,level,new):
		lootDrops = {'Health Potion':0.1,'Antidote':0.5} # antidote
		plagueRat = monsters.Animal(self.game,x,y,'r',"Plague Rat",libtcod.light_amber,level,faction = "Plague Rats",stats = actorStats.Stats("Plague Rat"),state = states.AI(0.7,0.5,0.5,1,0,0,0))
		plagueRat.deathState = states.DeathState(plagueRat)
		return plagueRat

	def spawnRougarou(self,x,y,level,new):
		rougarou = monsters.Rougarou(self.game,x,y,'R',"Rougarou",libtcod.grey,level,stats = actorStats.Stats("Rougarou"),state = states.AI(1,0.5,0.5,1,0.5,0,0))
		return rougarou

	def spawnSnakeman(self,x,y,level,new):
		level = 1

		lootDrops = {'Sword':0.2,'Health Potion':0.5}
		snakeman = monsters.Snakeman(self.game,x,y,'S',"Snakeman",libtcod.desaturated_sea,level,faction = "Snakemen",stats = actorStats.Stats("Snakeman"),state = states.AI(0.9,0.5,0.5,1,0,0,0),drops = lootDrops, inventorySize = 4, canEquipArmor = True, canEquipWeapons = True)
		snakeman.deathState = states.DeathState(snakeman)

		if new == True:
			# add equipment
			if random.random() <= .2:
				weapon = self.game.itemSpawner.spawn(x,y,'Serpent Sword',level,False)
				weapon.moveToInventory(snakeman)

		return snakeman

	def spawnSnakemanArcher(self,x,y,level,new):
		level = 2

		lootDrops = {'Wooden Bolts':0.75,'Health Potion':0.5}
		snakeman = actors.Monster(self.game,x,y,'S',"Snakeman Archer",libtcod.desaturated_red,level,faction = "Snakemen",stats = actorStats.Stats("Snakeman"),state = states.AI(0.9,0.8,0.8,0.5,0.5,7,2),drops = lootDrops, inventorySize = 4, canEquipArmor = True, canEquipWeapons = True)
		snakeman.deathState = states.DeathState(snakeman)

		if new == True:
			for name, level in [('Light Crossbow',0),('Steel Bolt',0),('Wooden Bolt',0)]:
				item = self.game.itemSpawner.spawn(x,y,name,level,False)
				item.moveToInventory(snakeman)

			# add equipment
			if random.random() <= .2:
				weapon = self.game.itemSpawner.spawn(x,y,'Serpent Sword',level,False)
				weapon.moveToInventory(snakeman)

		return snakeman

	def spawnSnakemanChampion(self,x,y,level,new):
		level = 3

		lootDrops = {'Sword':0.2,'Health Potion':0.5} #shield
		snakeman = actors.Monster(self.game,x,y,'S',"Snakeman Champion",libtcod.desaturated_blue,level,faction = "Snakemen",stats = actorStats.Stats("Snakeman"),state = states.AI(0.9,0.5,0.5,1,0.5,0,0),drops = lootDrops, inventorySize = 4,surviveMortalWound = False, canEquipArmor = True, canEquipWeapons = True)
		snakeman.deathState = states.DeathState(snakeman)
		
		if new == True:
			# add equipment
			weapon = self.game.itemSpawner.spawn(x,y,'Serpent Sword',level,False)
			snakeman.equipItem(weapon)

			# Shield
			# Armor

		return snakeman

	def spawnSwampHag(self,x,y,level,new):
		# uses poisoned mire spells
		# drops scrolls and occasionally wands
		pass

	def spawnWitch(self,x,y,level,new):
		# drops scrolls, wands, magical equipment, and occasionally spellbooks
		pass

	def spawnWyrm(self,x,y,level,new):
		pass
		# Wyrms can be fire or frost elementals


class MobSpawner:
	def __init__(self,game):
		self.game = game
		self.actorSpawner = ActorSpawner(game)

	def spawnMob(self,level):
		pass