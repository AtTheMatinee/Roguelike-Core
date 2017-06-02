'''
gameUI.py
'''
import libtcodpy as libtcod

import random

import gameLoop

#import objects

#import actors

#import worldMap

#import dungeonGeneration

import commands

SCREEN_WIDTH = 80 #100 #80
SCREEN_HEIGHT = 60 #75 #60

MAP_WIDTH = 60 #80 #50
MAP_HEIGHT = 50 #60 #50

HORIZONTAL_PANEL_HEIGHT = SCREEN_HEIGHT - MAP_HEIGHT
HORIZONTAL_PANEL_Y = SCREEN_HEIGHT - HORIZONTAL_PANEL_HEIGHT
H_PANEL_BAR_WIDTH = 20

VIRTICAL_PANEL_WIDTH = SCREEN_WIDTH - MAP_WIDTH
VIRTICAL_PANEL_W = SCREEN_WIDTH - VIRTICAL_PANEL_WIDTH
V_PANEL_BAR_WIDTH = VIRTICAL_PANEL_WIDTH - 4


'''
====================
User Interface
====================
'''
#TODO: Option to switch horizontal panel from bottom to top
#TODO: Option to switch virtical panel from right to left

class UserInterface:
	def __init__(self):
		libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
		libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False) #TODO: Change Game Name
		self.con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
		
		# bottom panel
		self.horPanel = libtcod.console_new(SCREEN_WIDTH, HORIZONTAL_PANEL_HEIGHT)

		self.setColorScheme(ColorScheme.DEFAULT)
		self.keyboardIntermediary = KeyboardCommands()


		self.keyboard = libtcod.Key()
		self.mouse = libtcod.Mouse()
		self.paused = False

		self.game = gameLoop.GameLoop(self,MAP_WIDTH,MAP_HEIGHT)

		self.fovRecompute = True
		self.generateNoiseMap()

	def mainLoop(self):
		'''
		TODO: When I implement menus, I will need to isolate the
		parts of this loop that pertain to the game loop from the 
		parts that render changes to the console
		'''
		while not libtcod.console_is_window_closed():

			#Input
			libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, self.keyboard, self.mouse)
			exit = self.handleInput(self.keyboard)
			if (exit): break

			if not self.paused:
				#Update
				self.game.process()

			#Render
			self.renderAll()

			libtcod.console_flush()

			for object in self.game._objects:
				object.clear()

	def handleInput(self,keyboard):
		# Non-rebindable Keys
		if (keyboard.vk	== libtcod.KEY_ESCAPE): return True #Exit Game	

		# Rebindable Keys
		# Check for every key
		# if that key is pressed, and it is bound, issue the bound command
		# TODO: Use init file to load in custom and Default keyboard bindings
		hero = self.game.hero
		keycode = None

		if (keyboard.vk == libtcod.KEY_0):
			keycode = '0'
		elif (keyboard.vk == libtcod.KEY_1):
			keycode = '1'
		elif (keyboard.vk == libtcod.KEY_2):
			keycode = '2'
		elif (keyboard.vk == libtcod.KEY_3):
			keycode = '3'
		elif (keyboard.vk == libtcod.KEY_4):
			keycode = '4'
		elif (keyboard.vk == libtcod.KEY_5):
			keycode = '5'
		elif (keyboard.vk == libtcod.KEY_6):
			keycode = '6'
		elif (keyboard.vk == libtcod.KEY_7):
			keycode = '7'
		elif (keyboard.vk == libtcod.KEY_8):
			keycode = '8'
		elif (keyboard.vk == libtcod.KEY_9):
			keycode = '9'

		elif (keyboard.vk == libtcod.KEY_KP0):
			keycode = 'KP0'
		elif (keyboard.vk == libtcod.KEY_KP1):
			keycode = 'KP1'
		elif (keyboard.vk == libtcod.KEY_KP2):
			keycode = 'KP2'
		elif (keyboard.vk == libtcod.KEY_KP3):
			keycode = 'KP3'
		elif (keyboard.vk == libtcod.KEY_KP4):
			keycode = 'KP4'
		elif (keyboard.vk == libtcod.KEY_KP5):
			keycode = 'KP5'
		elif (keyboard.vk == libtcod.KEY_KP6):
			keycode = 'KP6'
		elif (keyboard.vk == libtcod.KEY_KP7):
			keycode = 'KP7'
		elif (keyboard.vk == libtcod.KEY_KP8):
			keycode = 'KP8'
		elif (keyboard.vk == libtcod.KEY_KP9):
			keycode = 'KP9'

		elif (keyboard.vk == libtcod.KEY_UP):
			keycode = 'UP'
		elif (keyboard.vk == libtcod.KEY_DOWN):
			keycode = 'DOWN'
		elif (keyboard.vk == libtcod.KEY_LEFT):
			keycode = 'LEFT'
		elif (keyboard.vk == libtcod.KEY_RIGHT):
			keycode = 'RIGHT'

		elif keyboard.c:
			for c in "abcdefghijklmnopqrstuvwxyz":
				if keyboard.c == ord(str(c)):
					keycode = c.capitalize()
					break

			if (keyboard.c == ord(",")):
				keycode = ','
			elif (keyboard.c == ord(".")):
				keycode = '.'
			elif (keyboard.c == ord(";")):
				keycode = ';'
			elif (keyboard.c == ord("'")):
				keycode = "'"
			elif (keyboard.c == ord("[")):
				keycode = '['
			elif (keyboard.c == ord("]")):
				keycode = ']'
			elif (keyboard.c == ord("-")):
				keycode = '-'
			elif (keyboard.c == ord("+")):
				keycode = '+'

		if keycode != None:
			# TODO: if SHIFT: keycode = "SHIFT_" + keycode
			# TODO: if CTRL: keycode = "CTRL_" + keycode
			# TODO: if ALT: keycode = "ALT_" + keycode
			self.keyboardIntermediary.dispatch(self,keycode,hero)

	def renderAll(self):
		if self.fovRecompute:
			self.fovRecompute = False
			self.game.map.fovRecompute(self.game.hero.x, self.game.hero.y)

			# ==== Render Level ====
			# TODO: use noiseMap to alter color values of tiles
			for y in range(MAP_HEIGHT):
				for x in range(MAP_WIDTH):
					visible = libtcod.map_is_in_fov(self.game.map.fov_map, x, y)
					wall = self.game._currentLevel.getBlocksSight(x,y)
					if not visible:
						# outside of FOV
						if self.game._currentLevel.getHasBeenExplored(x,y) == True:
							if wall:
								color = self.color_dark_wall_back * self.noiseMap[x][y]
								libtcod.console_put_char_ex(self.con, x, y, '#', self.color_dark_wall_fore, color)
							else:
								libtcod.console_put_char_ex(self.con, x, y, '.', self.color_dark_ground_fore, self.color_dark_ground_back)


					else:
						if wall:
							color = self.color_light_wall_back * self.noiseMap[x][y]
							libtcod.console_put_char_ex(self.con, x, y, '#', self.color_light_wall_fore, color)
						else:
							libtcod.console_put_char_ex(self.con, x, y, '.', self.color_light_ground_fore, self.color_light_ground_back)
						self.game._currentLevel.setHasBeenExploredTrue(x,y)

		# ==== Render Objects ====
		for object in self.game._currentLevel._objects:
			object.draw()

		# ==== Render GUI panels ====
		libtcod.console_set_default_background(self.horPanel, libtcod.black)
		libtcod.console_clear(self.horPanel)

		# Health Bar
		self.renderHealthBar(self.horPanel,1,1,H_PANEL_BAR_WIDTH,self.game.hero)

		# ==== Blit Console to Screen ====
		libtcod.console_blit(self.horPanel, 0, 0, SCREEN_WIDTH, HORIZONTAL_PANEL_HEIGHT, 0, 0, HORIZONTAL_PANEL_Y)
		libtcod.console_blit(self.con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

	def setColorScheme(self, colorScheme):
		self.color_dark_wall_fore = colorScheme[0]
		self.color_dark_wall_back = colorScheme[1]
		self.color_dark_ground_fore = colorScheme[2]
		self.color_dark_ground_back = colorScheme[3]
		self.color_light_wall_fore = colorScheme[4]
		self.color_light_wall_back = colorScheme[5]
		self.color_light_ground_fore = colorScheme[6]
		self.color_light_ground_back = colorScheme[7]

	def renderStatusBar(self,panel,x, y, total_width, name, value, maxValue, bar_color, back_color):
		bar_width = int(float(value) / maxValue * total_width)

		# Render the background
		libtcod.console_set_default_background(panel, back_color)
		libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

		# Render the bar on top
		libtcod.console_set_default_background(panel, bar_color)
		if bar_width > 0:
			libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

		# Print the name of the bar, centered, over the bar
		libtcod.console_set_default_foreground(panel, libtcod.white)
		libtcod.console_print_ex(panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
			name + ': ' + str(value) + '/' + str(maxValue))

	def renderHealthBar(self,panel,x, y, width, actor):

		hp = actor.stats.get("healthCurrent")
		hpMax = actor.stats.get("healthMax")
		self.renderStatusBar(panel,x,y,width,"HP",hp,hpMax,libtcod.red,libtcod.darker_red)

	def bindKey(self,command,key):
		pass

	def generateNoiseMap(self):
		'''
		Generates an array, self.noiseMap, that has the 
		exact same dimensions as the level. This map is 
		to alter the apearance of each map tile by adding
		the value of the noise map to that of the tile's
		normal color.
		'''
		self.noiseMap = [[1
			for y in xrange(MAP_HEIGHT)]
				for x in xrange(MAP_WIDTH)]
		for x in xrange(MAP_WIDTH):
			for y in xrange(MAP_HEIGHT):
				self.noiseMap[x][y] = (0.5+random.random())

class ColorScheme():
	DEFAULT = [
	libtcod.black, 				# color_dark_wall_fore
	libtcod.violet,			# color_dark_wall_back
	libtcod.grey, 				# color_dark_ground_fore
	libtcod.darkest_violet,			# color_dark_ground_back
	libtcod.black, 				# color_light_wall_fore
	libtcod.red,			# color_light_wall_back
	libtcod.white, 				# color_light_ground_fore
	libtcod.black 				# color_light_ground_back
	]

class KeyboardCommands:
	# go between that allows for key rebinding
	def __init__(self):
		#TODO: Read from an init file
		self._keyBinding = {
		'A':None,
		'B':self.WalkSouthWest,
		'C':None,
		'D':None,
		'E':None,
		'F':None,
		'G':None,
		'H':self.WalkWest,
		'I':None,
		'J':self.WalkSouth,
		'K':self.WalkNorth,
		'L':self.WalkEast,
		'M':None,
		'N':self.WalkSouthEast,
		'O':None,
		'P':None,
		'Q':None,
		'R':None,
		'S':None,
		'T':None,
		'U':self.WalkNorthEast,
		'V':None,
		'W':self.Wait,
		'X':None,
		'Y':self.WalkNorthWest,
		'Z':None,
		'0':None,
		'1':None,
		'2':None,
		'3':None,
		'4':None,
		'5':None,
		'6':None,
		'7':None,
		'8':None,
		'9':None,
		';':None,
		',':None,
		'.':self.Wait,
		"'":None,
		'[':None,
		']':None,
		'-':None,
		'=':None,
		'KP0':None,
		'KP1':self.WalkSouthWest,
		'KP2':self.WalkSouth,
		'KP3':self.WalkSouthEast,
		'KP4':self.WalkWest,
		'KP5':self.Wait,
		'KP6':self.WalkEast,
		'KP7':self.WalkNorthWest,
		'KP8':self.WalkNorth,
		'KP9':self.WalkNorthEast,
		'ESCAPE':None,
		'BACKSPACE':None,
		'TAB':None,
		'ENTER':None,
		'SHIFT':None,
		'CONTROL':None,
		'ALT':None,
		'SPACE':None,
		'UP':self.WalkNorth,
		'DOWN':self.WalkSouth,
		'LEFT':self.WalkWest,
		'RIGHT':self.WalkEast,
		}

	def dispatch(self,ui,keycode,hero):
		if self._keyBinding[keycode] != None:
			self._keyBinding[keycode](ui,hero)

	def WalkNorthWest(self,ui,hero):
		hero.setNextCommand(commands.WalkCommand(hero,-1,-1)) # NORTH WEST
		ui.fovRecompute = True

	def WalkNorth(self,ui,hero):
		hero.setNextCommand(commands.WalkCommand(hero,0,-1)) # NORTH WEST
		ui.fovRecompute = True

	def WalkNorthEast(self,ui,hero):
		hero.setNextCommand(commands.WalkCommand(hero,1,-1)) # NORTH WEST
		ui.fovRecompute = True

	def WalkWest(self,ui,hero):
		hero.setNextCommand(commands.WalkCommand(hero,-1,0)) # NORTH WEST
		ui.fovRecompute = True

	def WalkEast(self,ui,hero):
		hero.setNextCommand(commands.WalkCommand(hero,1,0)) # NORTH WEST
		ui.fovRecompute = True

	def WalkSouthWest(self,ui,hero):
		hero.setNextCommand(commands.WalkCommand(hero,-1,1)) # NORTH WEST
		ui.fovRecompute = True

	def WalkSouth(self,ui,hero):
		hero.setNextCommand(commands.WalkCommand(hero,0,1)) # NORTH WEST
		ui.fovRecompute = True

	def WalkSouthEast(self,ui,hero):
		hero.setNextCommand(commands.WalkCommand(hero,1,1)) # NORTH WEST
		ui.fovRecompute = True

	def Wait(self,ui,hero):
		hero.setNextCommand(commands.WaitCommand(hero))
		ui.fovRecompute = False


ui = UserInterface()
ui.mainLoop()

'''
TODO:
NAME = Mire
AI class
	monsters sometimes attack other monsters
Gough Ghast - boss
Sir Kalgrain - boss, Knight
Deacon Deleto - boss, Occultist 
Wyrm - "W"
Kalgrain Knights - attack together
Snakemen - generic enemy "S"
Angels and Demons - special enemies
	drop Angel feathers and demon ribs
Fire Elemental
	Spawns on fire
	Can use selfImmolation spell
Mobs of enemies
	spawns n monsters in area size r
	monsters share an alert status and knowledge of player
Mimic - special enemies, have the power to look like another object
A monster that moves four times faster than the hero, but can't turn well
Enemy Generators
Special Map Tiles:
	Water "~"
	Pits " "
	Spikes "^"
	Ice
	Flowers '"'
Level difficulty = Dungeon difficulty + floor
Doors - object "+" when closed, "D" when open
Special Door - object "="
Potions
Pick Up - command
Throw - command
Use - command

LONG TERM TODO:
Spells
	Spells that you don't have the magic for drain health instead
	Spell Upgrades
		Dropped by bosses
Traps "^" or "*"
	groups of traps:
		single
		line
		block
		monefield
Bonfires - object
Regular Fires - object
Oil - object, makes things flamable
Alters - object
Character Classes - only really effect beginning
	Healer
		Starts with Heal AOE
	Priest
		Starts with Blessed weapon
	Occultist
		Starts with powerful spells, but low magic, so they must rely on blood-casting
	Alchemist
		Starts with some potions identified
	Magi
		Starts with some spells and highest Magic

Crafting
vision cones
	vision cone length
	vision cone angle
	visionConeIsVisible = False
Subclasses for Level which:
	decide which level generator to use
	set the default color scheme in the UI object
World Map Generator
	procedurally generates regions around special locations
Regions:
	Swamp
	Fen
	Forest

Special Locations/ Ruins (procedurally mapped, semi-planned):
	Dungeons
	Towns
	Ruins
	Burial Mounds
	Temples
	Pyramids

Ingrediants
	Sugar Vine
	White Angelbell
	Red Angelbell

Dialogue trees
	walk into NPCs to talk or press action button
'''