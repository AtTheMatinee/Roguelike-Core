'''
gameUI.py
'''
import libtcodpy as libtcod

import textbox

import random

from config import *

import gameLoop

import statusEffects

import Items

import objects

import descriptions

#import actors

#import worldMap

#import dungeonGeneration

import commands

INVENTORY_WIDTH = 30

'''
====================
User Interface
====================
'''
'''
TODO: Option to switch horizontal panel from bottom to top
TODO: Option to switch virtical panel from right to left
TODO: spell hoykeys (Should be easy after key rebinding is implemented)
TODO: Mouselook on an enemy pops it to the top of the enemy information panel
TODO: Virtical panel shows player stats, equipment, and hotkeys (if bound)
'''

class UserInterface:
	def __init__(self):
		# =====================
		# System Initialization
		# =====================
		libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
		libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'MIRE', False) 
		libtcod.sys_set_fps(FRAMERATE_LIMIT)
		self.con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
		
		# bottom panel
		self.horPanel = libtcod.console_new(HORIZONTAL_PANEL_WIDTH, HORIZONTAL_PANEL_HEIGHT)
		# side panel
		self.virPanel = libtcod.console_new(VIRTICAL_PANEL_WIDTH, VIRTICAL_PANEL_HEIGHT)
		# panel text alignments
		self._leftAlign = -1
		self._centerAlign = 0
		self._rightAlign = 1
		self._topAlign = -1
		self._bottomAlign = 1

		# In-Game Menu states
		self._playing = 0
		self._inventoryMenu = 1
		self._throwMenu = 2
		self._dropMenu = 3
		self._targetState = 4
		self._spellMenu = 5

		# Hero Panel status tracker
		self.reevaluateHeroStatusEffects = False
		self.heroStatusEffects = 0
		self._SEPoisoned = 1
		self._SEBleeding = 2
		self._SEFrozen = 4
		self._SEFlaming = 8
		self._SEWet = 16
		self._SEFlamable = 32
		#self._SEStunned = 256
		#self._SEConfised = 128
		self._SEMortallyWounded = 64


		self.setColorScheme(ColorScheme.DEFAULT)
		self.keyboardIntermediary = KeyboardCommands()


		self.keyboard = libtcod.Key()
		self.mouse = libtcod.Mouse()

		# ====================
		# ====================

		# Menu
		splash = SplashScreen(self)
		splash.process()
		main = MainMenu(self)
		main.process()

	def mainLoop(self):
		self.heroStatusEffects = 0
		while not libtcod.console_is_window_closed():

			#Input
			libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, self.keyboard, self.mouse)
			exit = self.handleInput(self.keyboard)
			if (exit): break

			if self._gameState == self._playing:
				#Update
				self.game.process()

			#Render
			self.renderAll()

			# Overlays

			# Menus
			if self._gameState == self._inventoryMenu:
				self.inventoryMenu('Press the key next to an item to use it, or any other key to cancel.\n')

			elif self._gameState == self._dropMenu:
				self.dropMenu('Press the key next to an item to drop it, or any other key to cancel.\n')

			elif self._gameState == self._throwMenu:
				self.throwMenu('Press the key next to an item to throw it, or any other key to cancel.\n')

			elif self._gameState == self._spellMenu:
				self.spellMenu('Press the key next to a spell to cast it, or any other key to cancel.\n')

			libtcod.console_flush()

			for object in self.game._currentLevel._objects:
				object.clear()

		# clear all windows
		libtcod.console_clear(self.con)
		libtcod.console_clear(self.horPanel)
		libtcod.console_clear(self.virPanel)
		libtcod.console_clear(0)
		libtcod.console_flush()

		self.game.saveGame()
			
	def handleInput(self,keyboard):
		if self._gameState == self._playing:
			# Non-rebindable Keys
			if (keyboard.vk	== libtcod.KEY_ESCAPE): return True #Exit Game	

			# Rebindable Keys
			# Check for every key
			# if that key is pressed, and it is bound, issue the bound command

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

			elif (keyboard.vk == libtcod.KEY_SPACE):
				keycode = 'SPACE'

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
				elif (keyboard.c == ord("<")):
					keycode = '<'
				elif (keyboard.c == ord(">")):
					keycode = '>'

			if keycode != None:
				# TODO: if SHIFT: keycode = "SHIFT_" + keycode
				# TODO: if CTRL: keycode = "CTRL_" + keycode
				# TODO: if ALT: keycode = "ALT_" + keycode
				self.keyboardIntermediary.dispatch(self,keycode,hero)

	def getNamesUnderMouse(self):
		#get the names of all objects at the mouse's coordinates
		(x,y) = (self.mouse.cx,self.mouse.cy)
		names = [obj.getName(False) for obj in self.game.hero.nearbyObjects
		if obj.x == x and obj.y == y]

		#combine the names, separated by a comma and space
		names = ', '.join(names)
		return names.title()

	def renderAll(self):
		if self.fovRecompute:
			self.fovRecompute = False
			self.game.map.fovRecompute(self.game.hero.x, self.game.hero.y)

			# ==== Render Level ====
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
		# ==== Horizontal Panel ====
		libtcod.console_set_default_background(self.horPanel, libtcod.black)
		libtcod.console_clear(self.horPanel)
		self.renderBoarderAroundConsole(self.horPanel,HORIZONTAL_PANEL_WIDTH, HORIZONTAL_PANEL_HEIGHT,UI_PRIMARY_COLOR)
		lable = " L O G " #chr(libtcod.CHAR_TEEW)+" L O G "+chr(libtcod.CHAR_TEEE)
		self.lableConsole(self.horPanel,HORIZONTAL_PANEL_WIDTH, HORIZONTAL_PANEL_HEIGHT,UI_PRIMARY_COLOR,self._centerAlign,self._topAlign,lable)
		self.printGameMessages()

		# ==== Virtical Panel ====
		libtcod.console_set_default_background(self.virPanel, libtcod.black)
		libtcod.console_clear(self.virPanel)
		self.renderBoarderAroundConsole(self.virPanel,VIRTICAL_PANEL_WIDTH, VIRTICAL_PANEL_HEIGHT, UI_PRIMARY_COLOR)
		self.renderMonsterPanel(self.virPanel,VIRTICAL_PANEL_WIDTH,VIRTICAL_PANEL_HEIGHT)

		# Health Bar
		#self.renderHealthBar(self.virPanel,2,2,V_PANEL_BAR_WIDTH,self.game.hero)
		self.renderHeroPanel(self.virPanel,VIRTICAL_PANEL_WIDTH)

		'''
		# My failed attemp at a look command
		# Names of objects under mouse
		if (self.game.hero.nearbyObjects != None):
			names = self.getNamesUnderMouse()
			if names != None:
				
				# TODO: Change x, y, and alignment depending on how long the name is
				# and how close it is to the edge of the console.
				x = self.mouse.cx + 1
				y = self.mouse.cy
				alignment = libtcod.LEFT
				libtcod.console_set_default_foreground(self.con,UI_PRIMARY_COLOR)
				libtcod.console_print_ex(self.con, x, y, libtcod.black, alignment, names)
				self.flag_printedNames = True
				
			elif self.flag_printedNames == True:
				# TODO: clean up map outside of fov (might barrow code from the menu methods)
				self.fovRecompute = True
				self.flag_printedNames = False
		'''

		# ==== Blit Consoles to Screen ====
		libtcod.console_blit(self.horPanel, 0, 0, HORIZONTAL_PANEL_WIDTH, HORIZONTAL_PANEL_HEIGHT, 0, 0, HORIZONTAL_PANEL_Y)
		libtcod.console_blit(self.virPanel, 0, 0, VIRTICAL_PANEL_WIDTH, VIRTICAL_PANEL_HEIGHT, 0, VIRTICAL_PANEL_X, 0)
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

	def newGame(self,heroClass,seed,heroName):
		self._gameState = self._playing

		if seed == None:
			seed = random.random()
		self.game = gameLoop.GameLoop(self,MAP_WIDTH,MAP_HEIGHT,seed)
		self.game.newGame(heroClass,heroName)

		self.fovRecompute = True
		self.generateNoiseMap()

	def loadGame(self):
		self._playing = 0
		self._inventoryMenu = 1
		self._gameState = self._playing

		self.game = gameLoop.GameLoop(self,MAP_WIDTH,MAP_HEIGHT,seed)

		self.fovRecompute = True
		self.generateNoiseMap()

		# Load old game._messages
		# Load old game.hero
		# Load old game._currentLevel
		# Load old game._currentActor

	def renderStatusBar(self,panel,x, y, total_width, name, value, maxValue, bar_color, back_color):
		if maxValue <= 0: 
			bar_width = 0
		else:
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
			name + ': ' + str(int(value)) + '/' + str(int(maxValue)))

	def renderHealthBar(self,panel,x, y, width, actor):
		hp = actor.stats.get("healthCurrent")
		hpMax = actor.stats.get("healthMax")
		self.renderStatusBar(panel,x,y,width,"HP",hp,hpMax,libtcod.red,libtcod.darker_red)

	def renderMagicBar(self,panel,x, y, width, actor):
		mp = actor.stats.get("magicCurrent")
		mpMax = actor.stats.get("magicMax")
		self.renderStatusBar(panel,x,y,width,"MP",mp,mpMax,libtcod.darker_blue,libtcod.darkest_blue)

	def menu(self,width,header,options):
		if len(options) > 26: raise ValueError('Limit options to 26')

		headerHeight = libtcod.console_get_height_rect(self.con, 0, 0, width, MAP_HEIGHT, header)
		height = len(options) + headerHeight

		# Create off screen console
		self.window = libtcod.console_new(width+4,height+4)

		# Print the header
		libtcod.console_set_default_foreground(self.window, libtcod.white)
		libtcod.console_print_rect_ex(self.window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

		# Print options
		y = headerHeight
		letterIndex = ord('a')
		for optionText in options:
			text = '('+chr(letterIndex)+')'+optionText
			libtcod.console_print_ex(self.window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
			y += 1
			letterIndex += 1

		# blit the window to the root
		x = SCREEN_WIDTH/2 - width/2
		y = SCREEN_HEIGHT/2 - height/2
		libtcod.console_blit(self.window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
		libtcod.console_delete(self.window)

		if self.keyboard.c:
			self._gameState = self._playing

			return self.keyboard.c - ord('a')

	def inventoryMenu(self,header):
		inventory = self.game.hero.inventory
		if len(inventory) <= 0:
			options = ['Inventory is empty']

		else:
			options = [item.getName(False,showLevel = True) for item in inventory]

		index = self.menu(INVENTORY_WIDTH,header,options)

		if (len(inventory) > 0) and (0 <= index < len(options)):
			item = inventory[index]
			self.game.hero.setNextCommand(commands.UseCommand(self.game.hero,item))

	def targetTile(self, maxRange = None):
		# create an offscreen console (for drawing the line)
		self.window = libtcod.console_new(MAP_WIDTH,MAP_HEIGHT)
		# set every cell's background to the transparency color
		color = UI_PRIMARY_COLOR*0.95 # Transparency color (guarenteed not to equal UI_PRIMARY_COLOR)
		libtcod.console_set_key_color(self.window, color)
		libtcod.console_set_default_background(self.window, color)
		libtcod.console_clear(self.window)

		while True:
			libtcod.console_flush()
			libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,self.keyboard,self.mouse)
			self.renderAll()

			# clear the overlay console
			libtcod.console_clear(self.window)
			
			(x,y) = (self.mouse.cx, self.mouse.cy)
			if not (0 <= x < MAP_WIDTH) or not (0 <= y < MAP_HEIGHT):
				x = self.game.hero.x
				y = self.game.hero.y

			# Draw a line from the hero to the mouse location
			libtcod.line_init(self.game.hero.x, self.game.hero.y, x, y)
			lineX,lineY = libtcod.line_step()
			while (not lineX is None) and not (self.game._currentLevel.getBlocksMovement(lineX,lineY)):
				
				# set the background color of those cells
				libtcod.console_set_char_background(self.window, lineX, lineY, UI_PRIMARY_COLOR, libtcod.BKGND_SET)

				if ((self.game._currentLevel.getHasObject(lineX,lineY)) or
					not libtcod.map_is_in_fov(self.game.map.fov_map, lineX, lineY) or
					((maxRange != None) and (self.game.hero.chessboardDistance(lineX,lineY) >= maxRange)) ):
					break
				lineX,lineY = libtcod.line_step()

			libtcod.console_blit(self.window, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0, 0, 0.6)

			if ( (self.mouse.lbutton_pressed) and
			 (libtcod.map_is_in_fov(self.game.map.fov_map,x,y)) and
			 (maxRange == None or (self.game.hero.chessboardDistance(x,y) <= maxRange)) ):
				libtcod.console_delete(self.window)
				return (x,y)

			if self.mouse.rbutton_pressed or self.keyboard.vk == libtcod.KEY_ESCAPE:
				libtcod.console_delete(self.window)
				return (None,None)

	def throwMenu(self,header):
		inventory = self.game.hero.inventory
		if len(inventory) <= 0:
			options = ['Inventory is empty']

		else:
			options = [item.getName(False,showLevel = True) for item in inventory]

		index = self.menu(INVENTORY_WIDTH,header,options)

		if (len(inventory) > 0) and (0 <= index < len(options)):
			item = inventory[index]

			# choose target method
			targetX,targetY = self.targetTile()
			if targetX != None:
				self.game.hero.setNextCommand(commands.ThrowCommand(self.game.hero, targetX, targetY, item))

	def dropMenu(self,header):
		inventory = self.game.hero.inventory
		if len(inventory) <= 0:
			options = ['Inventory is empty']

		else:
			options = [item.getName(False,showLevel = True) for item in inventory]

		index = self.menu(INVENTORY_WIDTH,header,options)

		if (len(inventory) > 0) and (0 <= index < len(options)):
			item = inventory[index]
			self.game.hero.setNextCommand(commands.DropCommand(self.game.hero,item))

	def spellMenu(self,header):
		spellList = self.game.hero.spells
		if len(spellList) <= 0:
			options = ['No Spells Known']

		else:
			options = [spell.name+' {'+str(spell.magicCost)+'}' for spell in spellList]

		index = self.menu(INVENTORY_WIDTH,header,options)

		if (len(spellList) > 0) and (0 <= index < len(options)):
			spell = spellList[index]
			self.game.hero.setNextCommand(commands.CastSpellCommand(self.game.hero,spell))

	def renderBoarderAroundConsole(self,console,width,height,color):
		'''
		Draws a simple, single line boarder around the perimeter of the console.
		The numbers in the console_put_char_ex() call can be changed to draw different
		boarders.
		'''
		# Horizontal lines (196)
		for y in [0,height-1]:
			for x in xrange(1,width-1):
				libtcod.console_put_char_ex(console, x, y, 196, color, libtcod.BKGND_NONE)

		# Virtical lines (179)
		for x in [0, width-1]:
			for y in xrange(1,height-1):
				libtcod.console_put_char_ex(console, x, y, 179, color, libtcod.BKGND_NONE)

		# Draw corners
		libtcod.console_put_char_ex(console, 0, 0, 218, color, libtcod.BKGND_NONE)
		libtcod.console_put_char_ex(console, width-1, 0, 191, color, libtcod.BKGND_NONE)
		libtcod.console_put_char_ex(console, 0, height-1, 192, color, libtcod.BKGND_NONE)
		libtcod.console_put_char_ex(console, width-1, height-1, 217, color, libtcod.BKGND_NONE)

	def lableConsole(self,console,width,height,color,xAlignment,yAlignment,lable):
		'''
		Use this to label the individual console panels with their names
		and with any hotkeys that effect them.
		'''
		lableLength = len(lable)

		if xAlignment == self._leftAlign:
			xStart = 2
		elif xAlignment == self._centerAlign:
			xStart = (width-lableLength)/2
		elif xAlignment == self._rightAlign:
			xStart = width - 2 - lableLength
		else: return

		if yAlignment == self._topAlign:
			y = 0
		elif yAlignment == self._bottomAlign:
			y = height-1
		else: return

		for i in range(lableLength):
			x = xStart + i
			c = lable[i]
			libtcod.console_put_char_ex(console, x, y, c, color, libtcod.BKGND_NONE)

	def printGameMessages(self):
		# print the game messages
		# TODO: ability to scroll back through old messages
		y = 1
		for (line,color) in self.game._messages:
			libtcod.console_set_default_foreground(self.horPanel, color)
			libtcod.console_print_ex(self.horPanel, MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
			y += 1

	def renderMonsterPanel(self,panel,width,height):
		listLength = len(self.game.hero.nearbyActors)
		if listLength > 0:
			i = 0
			for actor in self.game.hero.nearbyActors: #TODO: calculate how many monsters I can fit here
				y = 19 + i*6
				if y >= height - 6: break
				if self.game.factions.getRelationship(self.game.hero.faction, actor.faction) == self.game.factions._hostile:
					self.renderMonsterInformation(panel,width,y,actor,False)
					i += 1

	def renderHeroPanel(self,panel,width):
		hero = self.game.hero
		libtcod.console_set_default_foreground(panel,libtcod.white)
		y=2

		# ==== Hero Name ====
		libtcod.console_print_ex(panel, width/2, y, libtcod.BKGND_NONE, libtcod.CENTER, hero.name)
		# ==== Health Bar ====
		y+=2
		self.renderHealthBar(panel,2,y,width-4, hero)
		# Magic Bar
		y+=1
		self.renderMagicBar(panel,2,y,width-4,hero)

		# ==== Equipment ====
		y+=2
		if hero.equipSlots[0] != None:
			armorName = hero.equipSlots[0].getName(False)
		else:
			armorName = 'Clothes'
		libtcod.console_print_ex(panel, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, armorName)

		y+=1
		if hero.equipSlots[1] != None:
			weaponName = hero.equipSlots[1].getName(False)
		else:
			weaponName = 'Unarmed'
		libtcod.console_print_ex(panel, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, weaponName)

		if hero.equipSlots[2] != None:
			y+=2
			libtcod.console_print_ex(panel, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, hero.equipSlots[2].getName(False))
			if isinstance(hero.equipSlots[2],Items.rangedWeapons.RangedWeapon):
				ammo = hero.equipSlots[2].loadedAmmoType
				if ammo != None and hero.equipSlots[2].loadedRounds > 0:
					y += 1
					ammoText = ammo.getName(False)+' ('+str(hero.equipSlots[2].loadedRounds)+')'
					libtcod.console_print_ex(panel, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, ammoText)

		# ==== Stats ====
		y+=2
		attack = int(hero.stats.get('attack')[0] + hero.stats.get('attack')[3] +
			hero.stats.get('attack')[4] + hero.stats.get('attack')[5] +
			hero.stats.get('attack')[7] + hero.stats.get('attack')[8])
		attackBase = hero.stats.getBaseStat('attack')[0]
		libtcod.console_print_ex(panel, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, 'ATK: '+str(attack)+' ('+str(attackBase)+')')
		
		y+=1
		defense = int(hero.stats.get('defense')[0])
		defenseBase = hero.stats.getBaseStat('defense')[0]
		libtcod.console_print_ex(panel, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, 'DEF: '+str(defense)+' ('+str(defenseBase)+')')
		
		y+=1
		speed = int(hero.stats.get('speed'))
		speedBase = hero.stats.getBaseStat('speed')
		libtcod.console_print_ex(panel, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, 'SPD: '+str(speed)+' ('+str(speedBase)+')')

		# ==== Status Effects ====
		if self.reevaluateHeroStatusEffects == True:
			self.recomputeHeroStatusEffects(hero)

		statusEffects = self.listHeroStatusEffects()
		if len(statusEffects) > 0:
			statKeys = statusEffects.keys()
			statColors = statusEffects.values()

			y += 2
			for i in xrange( min( 3, len(statusEffects) ) ):
				x = 3 + (i*5)
				text = statKeys[i]
				color = statColors[i]
				libtcod.console_set_default_foreground(panel,color)
				libtcod.console_print_ex(panel, x, y, libtcod.BKGND_NONE, libtcod.LEFT, text)

		if len(statusEffects) > 3:
			y += 1
			for i in xrange( min( 3, len(statusEffects)-3 ) ):
				x = 3 + (i*5)
				text = statKeys[3+i]
				color = statColors[3+i]
				libtcod.console_set_default_foreground(panel,color)
				libtcod.console_print_ex(panel, x, y, libtcod.BKGND_NONE, libtcod.LEFT, text)

		if len(statusEffects) > 6:
			y+=1
			for i in xrange( min( 3, len(statusEffects)-6 ) ):
				x = 3 + (i*5)
				text = statKeys[6+i]
				color = statColors[6+i]
				libtcod.console_set_default_foreground(panel,color)
				libtcod.console_print_ex(panel, x, y, libtcod.BKGND_NONE, libtcod.LEFT, text)

		# Experience
		y += 2
		exp = hero.experience
		expToNextLevel = '?'
		libtcod.console_set_default_foreground(panel,libtcod.white)
		libtcod.console_print_ex(panel, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, 'EXP: '+str(exp)+'/'+str(expToNextLevel))

		# Floor
		#y += 2
		#depth = self.game._currentLevel.levelDepth +1
		#libtcod.console_print_ex(panel, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, 'Depth: '+str(depth))


	def recomputeHeroStatusEffects(self,hero):
		# use a bitmask to keep track of which status effects the hero is aflicted with.
		if any(isinstance(se, statusEffects.Flaming) for se in hero.statusEffects):
			self.heroStatusEffects = self.heroStatusEffects | self._SEFlaming
		else:
			self.heroStatusEffects = self.heroStatusEffects & ~ self._SEFlaming

		if any(isinstance(se, statusEffects.Frozen) for se in hero.statusEffects):
			self.heroStatusEffects = self.heroStatusEffects | self._SEFrozen
		else:
			self.heroStatusEffects = self.heroStatusEffects & ~ self._SEFrozen

		if any(isinstance(se, statusEffects.Poisoned) for se in hero.statusEffects):
			self.heroStatusEffects = self.heroStatusEffects | self._SEPoisoned
		else:
			self.heroStatusEffects = self.heroStatusEffects & ~ self._SEPoisoned

		if any(isinstance(se, statusEffects.Bleeding) for se in hero.statusEffects):
			self.heroStatusEffects = self.heroStatusEffects | self._SEBleeding
		else:
			self.heroStatusEffects = self.heroStatusEffects & ~ self._SEBleeding

		if any(isinstance(se, statusEffects.Flamable) for se in hero.statusEffects):
			self.heroStatusEffects = self.heroStatusEffects | self._SEFlamable
		else:
			self.heroStatusEffects = self.heroStatusEffects & ~ self._SEFlamable

		if any(isinstance(se, statusEffects.Wet) for se in hero.statusEffects):
			self.heroStatusEffects = self.heroStatusEffects | self._SEWet
		else:
			self.heroStatusEffects = self.heroStatusEffects & ~ self._SEWet

		if any(isinstance(se, statusEffects.MortallyWounded) for se in hero.statusEffects):
			self.heroStatusEffects = self.heroStatusEffects | self._SEMortallyWounded
		else:
			self.heroStatusEffects = self.heroStatusEffects & ~ self._SEMortallyWounded
		# Confused
		# Stunned

		self.reevaluateHeroStatusEffects = False

	def listHeroStatusEffects(self):
		statusEffects = {}

		if bool((self.heroStatusEffects & self._SEFlaming) != 0):
			statusEffects.update({'FIRE':libtcod.orange})

		if bool((self.heroStatusEffects & self._SEFrozen) != 0):
			statusEffects.update({'FRZN':libtcod.light_blue})

		if bool((self.heroStatusEffects & self._SEPoisoned) != 0):
			statusEffects.update({'PSND':libtcod.sea})

		if bool((self.heroStatusEffects & self._SEBleeding) != 0):
			statusEffects.update({'BLDG':libtcod.crimson})

		if bool((self.heroStatusEffects & self._SEFlamable) != 0):
			statusEffects.update({'FLMB':libtcod.amber})

		if bool((self.heroStatusEffects & self._SEWet) != 0):
			statusEffects.update({'WET ':libtcod.azure})

		if bool((self.heroStatusEffects & self._SEMortallyWounded) != 0):
			statusEffects.update({'MWND':libtcod.red})

		return statusEffects

	def renderMonsterInformation(self,panel,width,y,actor,displayStats):
		'''
		   ==== Mirehound ====  
		 ####HP:#11/15####
		 ATK: 2  DEF: 0  SPD: 8
		'''
		name = actor.getName(False)
		bannerSides = max(0, (width-len(name)-4) / 2 )
		nameBanner = bannerSides*'=' + ' ' + name + ' ' + bannerSides*'='
		libtcod.console_set_default_foreground(panel,libtcod.white)
		libtcod.console_print_ex(panel, 1, y, libtcod.BKGND_NONE, libtcod.LEFT, nameBanner)
		
		self.renderHealthBar(panel,2,y+1,width-4,actor)
		
		# Stats
		if displayStats == True:
			attack = actor.stats.get('attack')[0]
			attackBase = actor.stats.getBaseStat('attack')[0]
			libtcod.console_print_ex(panel, 3, y+2, libtcod.BKGND_NONE, libtcod.LEFT, 'ATK: '+str(attack)+' ('+str(attackBase)+')')
			
			defense = actor.stats.get('defense')[0]
			defenseBase = actor.stats.getBaseStat('defense')[0]
			libtcod.console_print_ex(panel, 3, y+3, libtcod.BKGND_NONE, libtcod.LEFT, 'DEF: '+str(defense)+' ('+str(defenseBase)+')')
			
			speed = actor.stats.get('speed')
			speedBase = actor.stats.getBaseStat('speed')
			libtcod.console_print_ex(panel, 3, y+4, libtcod.BKGND_NONE, libtcod.LEFT, 'SPD: '+str(speed)+' ('+str(speedBase)+')')
			

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

class ColorScheme:
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
		'D':self.OpenDropMenu,
		'E':None,
		'F':self.FireRangedWeapon,
		'G':self.PickUpItem,
		'H':self.WalkWest,
		'I':self.OpenInventory,
		'J':self.WalkSouth,
		'K':self.WalkNorth,
		'L':self.WalkEast,
		'M':None,
		'N':self.WalkSouthEast,
		'O':None,
		'P':None,
		'Q':None,
		'R':self.FireRangedWeapon,
		'S':self.OpenSpellMenu,
		'T':self.OpenThrowMenu,
		'U':self.WalkNorthEast,
		'V':None,
		'W':self.Wait,
		'X':None,
		'Y':self.WalkNorthWest,
		'Z':None,
		'0':self.test1,
		'1':None,
		'2':None,
		'3':None,
		'4':None,
		'5':None,
		'6':None,
		'7':None,
		'8':None,
		'9':self.test2,
		';':None,
		',':None,
		'.':self.Wait,
		"'":None,
		'[':None,
		']':None,
		'-':None,
		'=':None,
		'<':self.GoUpStairs,
		'>':self.GoDownStairs,
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

	def PickUpItem(self,ui,hero):
		hero.setNextCommand(commands.PickUpCommand(hero, hero.x, hero.y))

	def OpenInventory(self,ui,hero):
		ui._gameState = ui._inventoryMenu
		ui.keyboard.c = libtcod.KEY_NONE

	def OpenDropMenu(self,ui,hero):
		ui._gameState = ui._dropMenu
		ui.keyboard.c = libtcod.KEY_NONE

	def OpenThrowMenu(self,ui,hero):
		ui._gameState = ui._throwMenu
		ui.keyboard.c = libtcod.KEY_NONE

	def OpenSpellMenu(self,ui,hero):
		ui._gameState = ui._spellMenu
		ui.keyboard.c = libtcod.KEY_NONE

	def GoUpStairs(self,ui,hero):
		hero.setNextCommand(commands.GoUpStairsCommand(hero))
		#libtcod.console_clear(ui.con)
		ui.fovRecompute = True

	def GoDownStairs(self,ui,hero):
		hero.setNextCommand(commands.GoDownStairsCommand(hero))
		#libtcod.console_clear(ui.con)
		ui.fovRecompute = True

	def FireRangedWeapon(self,ui,hero):
		if hero.equipSlots[2] != None and isinstance(hero.equipSlots[2],Items.rangedWeapons.RangedWeapon):
			maxRange = hero.equipSlots[2].maxRange
		else:
			maxRange = None

		target = None
		targetX,targetY = ui.targetTile(maxRange)
		if targetX != None:
			for actor in ui.game._currentLevel._actors:
				if actor.x == targetX and actor.y == targetY:
					target = actor

		if target != None:
			hero.setNextCommand(commands.FireRangedWeaponCommand(hero,target))

	def test1(self,ui,hero):
		pass 
		#objects.PoisonCloud(ui.game, hero.x, hero.y, 'cloud', libtcod.green, 20)
		objects.Fire(ui.game, hero.x, hero.y,'torch',libtcod.flame)

	def test2(self,ui,hero):
		#objects.SmokeCloud(ui.game, hero.x, hero.y, 'smoke', libtcod.dark_gray, 20)
		pass

class MainMenu:
	def __init__(self,ui):
		self.ui = ui
		self.cursor = 0

	def process(self):
		options = ['(C)ontinue','(N)ew Game','(O)ptions','(E)xit']

		width = 24
		height = len(options)+2



		while not libtcod.console_is_window_closed():
			self.renderLogo()			

			# Print options
			window = libtcod.console_new(width,height)

			libtcod.console_set_default_foreground(window, UI_PRIMARY_COLOR)

			y = 1
			for i in xrange(len(options)):
				if i == self.cursor:
					text = '@ '+options[i]
				else:
					text = '  '+options[i]
				libtcod.console_print_ex(window, width/2-8, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
				y += 1

			# blit the window to the root
			x = SCREEN_WIDTH/2 - width/2
			y = (SCREEN_HEIGHT - height)*2/3
			libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.6)
			libtcod.console_delete(window)

			libtcod.console_flush()

			libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, self.ui.keyboard, self.ui.mouse)


			if self.ui.keyboard.c or self.ui.keyboard.vk:
				# move cursor
				if ( (self.ui.keyboard.vk == libtcod.KEY_UP) or
					(self.ui.keyboard.vk == libtcod.KEY_LEFT) ):

					self.cursor = (self.cursor-1) % len(options)

				if ((self.ui.keyboard.vk == libtcod.KEY_DOWN) or
					(self.ui.keyboard.vk == libtcod.KEY_RIGHT) ):

					self.cursor = (self.cursor+1) % len(options)

				# select option
				if ( (self.ui.keyboard.c == ord('c')) or
					( (self.ui.keyboard.vk == libtcod.KEY_ENTER) and
					(self.cursor == 0) ) ):
					self.clearConsoles()
					pass

				if ( (self.ui.keyboard.c == ord('n')) or
					( (self.ui.keyboard.vk == libtcod.KEY_ENTER) and
					(self.cursor == 1) ) ):
					self.clearConsoles()
					n = NewGameMenu(self.ui)
					heroClass,seed,heroName = n.process()

					if heroClass != None:
						self.ui.newGame(heroClass,seed,heroName) # (heroClass,seed)
						self.ui.mainLoop()
					

				if ( (self.ui.keyboard.c == ord('o')) or
					( (self.ui.keyboard.vk == libtcod.KEY_ENTER) and
					(self.cursor == 2) ) ):
					self.clearConsoles()
					pass

				elif ( (self.ui.keyboard.c == ord('e')) or 
					( (self.ui.keyboard.vk == libtcod.KEY_ENTER) and
					(self.cursor == 3) )  ):
					# exit
					break

	def renderLogo(self):
		logoLength = len(LOGO[0])
		logo = libtcod.console_new(logoLength,20)
		
		y=0
		for line in LOGO:
			libtcod.console_print_ex(logo, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
			y += 1

		logoX = (SCREEN_WIDTH-logoLength)/2
		libtcod.console_blit(logo,0,0,logoLength,20,0,logoX,10,1,0)
		libtcod.console_delete(logo)

	def clearConsoles(self):
		libtcod.console_clear(0)
		libtcod.console_flush()


class NewGameMenu:
	def __init__(self,ui):
		self.ui = ui

		self.heroClasses = [
			'Alchemist',
			'Arbalest',
			'Assassin',
			'Barbarian',
			'Cleric',
			'Houndmaster',
			'Knight',
			'Occultist',
			'Magician',
			'Mercenary',
			'Specialist',
			'Systems Test'
		]

		self.descriptions = {
			'Alchemist':'001',
			'Arbalest':'002',
			'Assassin':'003',
			'Barbarian':'004',
			'Cleric':'005',
			'Houndmaster':'006',
			'Knight':'007',
			'Occultist':'008',
			'Magician':'009',
			'Mercenary':'010',
			'Specialist':'011',
			'Systems Test':'000'
		}

		self.seed = random.random()
		self.heroName = 'Hero'
		self.selection = 0
		self.cursor = 0

	def process(self):
		'''
		LeftWindow:

		  Class  
		_________
		Alchemist
		Arbalest
		Assassin
		Barbarian
		Cleric
		Houndmaster TODO
		Knight
		Occultist
		Magician
		Mercenary
		Specialist
		Systems Test

		  Seed  
		________
		3829094375

		==============

		BottomWindow: 

		(C)ontinue | (R)eturn

		RightWindow:
		'Hero Name'

		wordwraped description in
		bordered text box.

		'''
		while not libtcod.console_is_window_closed():
			self.renderLogo()			

			# ==== Render Left Window
			self.renderLeftWindow()

			# ==== Render Right Window ====
			self.renderRightWindow()

			# ==== Render Bottom Window ====
			self.renderBottomWindow()

			libtcod.console_flush()

			libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, self.ui.keyboard, self.ui.mouse)

			if self.ui.keyboard.c or self.ui.keyboard.vk:
				# move cursor
				if ( (self.ui.keyboard.vk == libtcod.KEY_UP) or
					(self.ui.keyboard.vk == libtcod.KEY_LEFT) ):

					self.cursor = (self.cursor-1) % (len(self.heroClasses)+4)

				if ((self.ui.keyboard.vk == libtcod.KEY_DOWN) or
					(self.ui.keyboard.vk == libtcod.KEY_RIGHT) ):

					self.cursor = (self.cursor+1) % (len(self.heroClasses)+4)

				# select options
				# choose class
				if ( (self.ui.keyboard.vk == libtcod.KEY_ENTER) and
					(self.cursor < len(self.heroClasses))):
					self.selection = self.cursor

				# enter seed
				if ( (self.ui.keyboard.vk == libtcod.KEY_ENTER) and
					(self.cursor == len(self.heroClasses))):						
					
					text = self.textbox(0,24,1,self.seedX,self.seedY,UI_PRIMARY_COLOR)
					if len(text) > 0:
						self.seed = text

				# enter hero name
				if ( (self.ui.keyboard.vk == libtcod.KEY_ENTER) and
					(self.cursor == len(self.heroClasses)+3)):

					text = self.textbox(0,18,1,self.heroNameX,self.heroNameY,UI_PRIMARY_COLOR)
					if len(text) > 0:
						self.heroName = text

				if ( (self.ui.keyboard.c == ord('c')) or
					( (self.ui.keyboard.vk == libtcod.KEY_ENTER) and
					(self.cursor == len(self.heroClasses)+1) ) ):
					self.clearConsoles()
					return self.heroClasses[self.selection], self.seed, self.heroName

				if ( (self.ui.keyboard.c == ord('r')) or 
					(self.ui.keyboard.vk == libtcod.KEY_ESCAPE) or
					( (self.ui.keyboard.vk == libtcod.KEY_ENTER) and
					(self.cursor == len(self.heroClasses)+2) ) ):
					self.clearConsoles()
					return None,None, self.heroName

	def clearConsoles(self):
		libtcod.console_clear(0)
		libtcod.console_flush()

	def renderLogo(self):
		logoLength = len(LOGO[0])
		logo = libtcod.console_new(logoLength,20)
		
		y=0
		for line in LOGO:
			libtcod.console_print_ex(logo, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
			y += 1

		logoX = (SCREEN_WIDTH-logoLength)/2
		libtcod.console_blit(logo,0,0,logoLength,20,0,logoX,10,1,0)
		libtcod.console_delete(logo)

	def renderLeftWindow(self):
		leftWindowHeight = len(self.heroClasses)+13
		leftWindowWidth = 32

		# ==== Render Left Window ====

		leftWindow = libtcod.console_new(leftWindowWidth,leftWindowHeight)

		libtcod.console_set_default_foreground(leftWindow, UI_PRIMARY_COLOR)

		# ==== Class Selection ====
		y = 1
		libtcod.console_print_ex(leftWindow, 4, y, libtcod.BKGND_NONE, libtcod.LEFT, 'CLASS')
		# Draw line under 'CLASS'
		y += 2
		for i in xrange(10):
			libtcod.console_put_char_ex(leftWindow, 1+i, y, 196, UI_PRIMARY_COLOR, libtcod.BKGND_NONE)

		# print class options
		y+=2
		for i in xrange(len(self.heroClasses)):
			text = self.heroClasses[i].upper()
			if self.cursor == i:
				text = '@ '+text
			else: 
				text = '  '+text

			if i == self.selection:
				libtcod.console_set_default_foreground(leftWindow,UI_PRIMARY_COLOR*10)

			libtcod.console_print_ex(leftWindow, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
			libtcod.console_set_default_foreground(leftWindow,UI_PRIMARY_COLOR)
			y += 1

		# ==== Optional Seed Input ====

		# print 'SEED'
		y += 3
		libtcod.console_print_ex(leftWindow, 4, y, libtcod.BKGND_NONE, libtcod.LEFT, 'SEED')
		# Draw line under 'SEED'
		y += 2
		for i in xrange(10):
			libtcod.console_put_char_ex(leftWindow, 1+i, y, 196, UI_PRIMARY_COLOR, libtcod.BKGND_NONE)
		y += 2
		textboxOffset = y # used to create a text box over the seed
		
		# print the seed
		text = str(self.seed)
		if self.cursor == len(self.heroClasses):
			text = '@ '+ text
		else:
			text = '  '+ text
		libtcod.console_print_ex(leftWindow, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)


		# blit the window to the root
		x = SCREEN_WIDTH/8
		self.seedX = x + 2 # used to create a text box over the seed
		y = min((SCREEN_HEIGHT*3/7),(SCREEN_HEIGHT - leftWindowHeight))
		self.seedY = y + textboxOffset # used to create a text box over the seed
		libtcod.console_blit(leftWindow, 0, 0, leftWindowWidth, leftWindowHeight, 0, x, y, 1.0, 0.6)
		libtcod.console_delete(leftWindow)

	def renderRightWindow(self):
		rightWindowWidth = 24
		rightWindowHeight = 32

		# ==== Render Right Window ====
		rightWindow = libtcod.console_new(rightWindowWidth,rightWindowHeight)

		libtcod.console_set_default_foreground(rightWindow, UI_PRIMARY_COLOR)


		# ==== Print Hero Name ====
		text = str(self.heroName)
		if self.cursor == len(self.heroClasses)+3:
			text = '@ '+ text 
		else:
			text = '  '+ text
		libtcod.console_print_ex(rightWindow, rightWindowWidth/2-2, 1, libtcod.BKGND_NONE, libtcod.CENTER, text)

		# ==== Draw line ====
		for i in xrange(rightWindowWidth-2):
			libtcod.console_put_char_ex(rightWindow, 1+i, 3, 196, UI_PRIMARY_COLOR, libtcod.BKGND_NONE)

		# ==== Print Class Descriptions ====
		heroClass = self.heroClasses[self.selection]
		key = self.descriptions[heroClass]
		text = descriptions.get(key)

		#libtcod.console_print_ex(rightWindow, 3, 5, libtcod.BKGND_NONE, libtcod.LEFT, text)
		libtcod.console_print_ex(rightWindow, rightWindowWidth/2, 5, libtcod.BKGND_NONE, libtcod.CENTER, text)


		# blit the window to the root
		x = SCREEN_WIDTH*7/8 - rightWindowWidth
		self.heroNameX = 4 + x # used to create a text box over the hero name

		y = min((SCREEN_HEIGHT*3/7),(SCREEN_HEIGHT - rightWindowHeight))
		self.heroNameY = 1 + y # used to create a text box over the hero name

		libtcod.console_blit(rightWindow, 0, 0, rightWindowWidth, rightWindowHeight, 0, x, y, 1.0, 0.6)
		libtcod.console_delete(rightWindow)


	def renderBottomWindow(self):
		bottomWindowHeight = 7
		bottomWindowWidth = 32

		# ==== Render Bottom Window ====
		bottomWindow = libtcod.console_new(bottomWindowWidth,bottomWindowHeight)

		libtcod.console_set_default_foreground(bottomWindow, UI_PRIMARY_COLOR)


		# print text
		y=3
		if self.cursor == len(self.heroClasses)+1:
			continueText = '@ (C)ontinue  '
		else:
			continueText = '  (C)ontinue  '
		if self.cursor == len(self.heroClasses)+2:
			returnText = ' @ (R)eturn'
		else:
			returnText = '   (R)eturn'
		text = continueText+'|' + returnText
		libtcod.console_print_ex(bottomWindow, bottomWindowWidth/2, y, libtcod.BKGND_NONE, libtcod.CENTER, text)

		# render bar above text
		y = 2
		x = 6
		barLength = 8
		for i in xrange(barLength):
			libtcod.console_put_char_ex(bottomWindow, x+i, y, 196, UI_PRIMARY_COLOR*0.25, libtcod.BKGND_NONE)
		x = 22
		barLength = 6
		for i in xrange(barLength):
			libtcod.console_put_char_ex(bottomWindow, x+i, y, 196, UI_PRIMARY_COLOR*0.25, libtcod.BKGND_NONE)
		
		# render bar below text
		y = 4
		x = 6
		barLength = 8
		for i in xrange(barLength):
			libtcod.console_put_char_ex(bottomWindow, x+i, y, 196, UI_PRIMARY_COLOR*0.25, libtcod.BKGND_NONE)
		x = 22
		barLength = 6
		for i in xrange(barLength):
			libtcod.console_put_char_ex(bottomWindow, x+i, y, 196, UI_PRIMARY_COLOR*0.25, libtcod.BKGND_NONE)

		# blit the window to the root
		x = SCREEN_WIDTH/2 -(bottomWindowWidth/2)
		y = (SCREEN_HEIGHT*6/7-1)
		libtcod.console_blit(bottomWindow, 0, 0, bottomWindowWidth, bottomWindowHeight, 0, x, y, 1.0, 0.6)
		libtcod.console_delete(bottomWindow)

	def textbox(self,console,width,height,x,y,color):
		t = textbox.Textbox(width,height)
		while True:
			text = t.update(console, x, y, UI_PRIMARY_COLOR)
			if text != None:
				return text

class OptionsMenu:
	def __init__(self,ui):
		self.ui = ui

	def process(self):
		pass
		'''
		Screen Options
			Font Size
			Full Screen (On/Off)
			Colorblind Mode (On/Off)
			Particle Effects (On/Off)
			Restore Defaults
		Controls
			Rebind Keys
			Restore Defaults
		Audio
			Volume Sliders
			Sound Test
			Restore Defaults

		* automatically save selections in separate file
		'''

	def clearConsoles(self):
		libtcod.console_clear(0)
		libtcod.console_flush()
	pass

class SplashScreen:
	def __init__(self,ui):
		self.ui = ui

	def process(self):
		# Plays before the main menu
		# (C)ontinue (actually works with any key)
		# Can be skipped by pressing any button
		# Fades out into the main menu

		logoLength = len(LOGO[0])
		logo = libtcod.console_new(logoLength,20)
		
		y=0
		for line in LOGO:
			libtcod.console_print_ex(logo, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
			y += 1

		logoX = (SCREEN_WIDTH-logoLength)/2
		libtcod.console_blit(logo,0,0,logoLength,20,0,logoX,10,1,0)
		libtcod.console_delete(logo)


if __name__ == "__main__":
	ui = UserInterface()
	ui.mainLoop()

'''
TODO:
Gough Ghast - boss
Sir Kalagrain - boss, Knight
Deacon Deleto - boss, Occultist 
Wyrm - "W"
Kalagrain Knights - attack together
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
Doors - object "+" when closed, "D" when open
Special Door - object "="
Talismans

"Leveling Up" with special items that perminantly increase a single stat

LONG TERM TODO:

Traps "^" or "*"
	groups of traps:
		single
		line
		block
		monefield
Bonfires - object

Oil - object, makes things flamable
Alters - object

Crafting
vision cones
	vision cone length
	vision cone angle
	visionConeIsVisible = False

Dialogue trees
	walk into NPCs to talk or press action button

Particle effect engine
	updated every ui.renderAll cycle
	blits to a new overlay panel
	iterates over a list of particles, updating and drawing them
	particles
		<> have an apparance, which can be changed by the update method
		<> have a delay, only after which they begin rendering
		<> have a duration, which counts down after the delay reaches 0
		<> are removed from the list of particles when duration reaches zero
'''
'''
Entrance to the dungeon
.............
..#########..
..#.......#..
..#.&...&.#..
..#.......#..
..#...>...#..
..#.......#..
..#.&...&.#..
..#.......#..
.............

'''
