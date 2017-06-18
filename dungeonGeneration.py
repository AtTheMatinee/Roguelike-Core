import libtcodpy as libtcod
import random

class RoomAddition:
	'''
	What I'm calling the Room Addition algorithm is an attempt to 
	recreate the dungeon generation algorithm used in Brogue, as
	discussed at https://www.rockpapershotgun.com/2015/07/28/how-do-roguelikes-generate-levels/
	I don't think Brian Walker has ever given a name to his
	dungeon generation algorithm, so I've taken to calling it the 
	Room Addition Algorithm, after the way in which it builds the 
	dungeon by adding rooms one at a time to the existing dungeon.
	This isn't a perfect recreation of Brian Walker's algorithm,
	but I think it's good enough to demonstrait the concept.
	'''
	def __init__(self):
		self.ROOM_MAX_SIZE = 18 # max height and width for cellular automata rooms
		self.ROOM_MIN_SIZE = 16 # min size in number of floor tiles, not height and width
		self.MAX_NUM_ROOMS = 30

		self.SQUARE_ROOM_MAX_SIZE = 12
		self.SQUARE_ROOM_MIN_SIZE = 6

		self.CROSS_ROOM_MAX_SIZE = 12
		self.CROSS_ROOM_MIN_SIZE = 6

		self.cavernChance = 0.40 # probability that the first room will be a cavern
		self.CAVERN_MAX_SIZE = 35 # max height an width

		self.wallProbability = 0.45
		self.neighbors = 4

		self.squareRoomChance = 0.2
		self.crossRoomChance = 0.15

		self.buildRoomAttempts = 500
		self.placeRoomAttempts = 20
		self.maxTunnelLength = 12

		self.includeShortcuts = True
		self.shortcutAttempts = 500
		self.shortcutLength = 5
		self.minPathfindingDistance = 50

	def generateLevel(self,level,mapWidth,mapHeight,seed):
		# set the seed
		if seed != None:
			random.seed(seed)

		self.rooms = []
		self.level = level

		# Generate an array of solid walls
		self.level.terrain = [[0
			for y in range(mapHeight)]
				for x in range(mapWidth)]
		for y in xrange(mapHeight):
			for x in xrange(mapWidth):
				self.level.setBlocksMovementTrue(x,y)
				self.level.setBlocksSightTrue(x,y)
				self.level.setHasBeenExploredFalse(x,y)

		# generate the first room
		room = self.generateRoom()
		roomWidth,roomHeight = self.getRoomDimensions(room)
		roomX = (mapWidth/2 - roomWidth/2)-1
		roomY = (mapHeight/2 - roomHeight/2)-1
		self.addRoom(roomX,roomY,room)

		# generate other rooms
		for i in range(self.buildRoomAttempts):
			room = self.generateRoom()
			# try to position the room, get roomX and roomY
			roomX,roomY,wallTile,direction, tunnelLength = self.placeRoom(room,mapWidth,mapHeight)
			if roomX and roomY:
				self.addRoom(roomX,roomY,room)
				self.addTunnel(wallTile,direction,tunnelLength)
				if len(self.rooms) >= self.MAX_NUM_ROOMS:
					break

		if self.includeShortcuts == True:
			self.addShortcuts(mapWidth,mapHeight)

		self.placeStaircases(mapWidth,mapHeight)

	def generateRoom(self):
		# select a room type to generate
		# generate and return that room
		if self.rooms:
			#There is at least one room already
			choice = random.random()

			if choice <self.squareRoomChance:
				room = self.generateRoomSquare()
			elif self.squareRoomChance <= choice < (self.squareRoomChance+self.crossRoomChance):
				room = self.generateRoomCross() 
			else:
				room = self.generateRoomCellularAutomata()

		else: #it's the first room
			choice = random.random()
			if choice < self.cavernChance:
				room = self.generateRoomCavern()
			else:
				room = self.generateRoomSquare()

		return room

	def generateRoomCross(self):
		roomHorWidth = (random.randint(self.CROSS_ROOM_MIN_SIZE+2,self.CROSS_ROOM_MAX_SIZE))/2*2

		roomVirHeight = (random.randint(self.CROSS_ROOM_MIN_SIZE+2,self.CROSS_ROOM_MAX_SIZE))/2*2

		roomHorHeight = (random.randint(self.CROSS_ROOM_MIN_SIZE,roomVirHeight-2))/2*2

		roomVirWidth = (random.randint(self.CROSS_ROOM_MIN_SIZE,roomHorWidth-2))/2*2

		room = [[1
			for y in xrange(roomVirHeight)]
				for x in xrange(roomHorWidth)]

		# Fill in horizontal space
		virOffset = roomVirHeight/2 - roomHorHeight/2
		for y in xrange(virOffset,roomHorHeight+virOffset):
			for x in xrange(0,roomHorWidth):
				room[x][y] = 0

		# Fill in virtical space
		horOffset = roomHorWidth/2 - roomVirWidth/2
		for y in xrange(0,roomVirHeight):
			for x in xrange(horOffset,roomVirWidth+horOffset):
				room[x][y] = 0

		return room

	def generateRoomSquare(self):
		roomWidth = random.randint(self.SQUARE_ROOM_MIN_SIZE,self.SQUARE_ROOM_MAX_SIZE)
		roomHeight = random.randint(max(int(roomWidth*0.5),self.SQUARE_ROOM_MIN_SIZE),min(int(roomWidth*1.5),self.SQUARE_ROOM_MAX_SIZE))
		
		room = [[1
			for y in range(roomHeight)]
				for x in range(roomWidth)]

		room = [[0
			for y in range(1,roomHeight-1)]
				for x in range(1,roomWidth-1)]

		return room

	def generateRoomCellularAutomata(self):
		while True:
			# if a room is too small, generate another
			room = [[1
				for y in range(self.ROOM_MAX_SIZE)]
					for x in range(self.ROOM_MAX_SIZE)]

			# random fill map
			for y in range (2,self.ROOM_MAX_SIZE-2):
				for x in range (2,self.ROOM_MAX_SIZE-2):
					if random.random() >= self.wallProbability:
						room[x][y] = 0

			# create distinctive regions
			for i in range(4):
				for y in range (1,self.ROOM_MAX_SIZE-1):
					for x in range (1,self.ROOM_MAX_SIZE-1):

						# if the cell's neighboring walls > self.neighbors, set it to 1
						if self.getAdjacentWalls(x,y,room) > self.neighbors:
							room[x][y] = 1
						# otherwise, set it to 0
						elif self.getAdjacentWalls(x,y,room) < self.neighbors:
							room[x][y] = 0

			# floodfill to remove small caverns
			room = self.floodFill(room)

			# start over if the room is completely filled in
			roomWidth,roomHeight = self.getRoomDimensions(room)
			for x in range (roomWidth):
				for y in range (roomHeight):
					if room[x][y] == 0:
						return room

	def generateRoomCavern(self):
		while True:
			# if a room is too small, generate another
			room = [[1
				for y in range(self.CAVERN_MAX_SIZE)]
					for x in range(self.CAVERN_MAX_SIZE)]

			# random fill map
			for y in range (2,self.CAVERN_MAX_SIZE-2):
				for x in range (2,self.CAVERN_MAX_SIZE-2):
					if random.random() >= self.wallProbability:
						room[x][y] = 0

			# create distinctive regions
			for i in range(4):
				for y in range (1,self.CAVERN_MAX_SIZE-1):
					for x in range (1,self.CAVERN_MAX_SIZE-1):

						# if the cell's neighboring walls > self.neighbors, set it to 1
						if self.getAdjacentWalls(x,y,room) > self.neighbors:
							room[x][y] = 1
						# otherwise, set it to 0
						elif self.getAdjacentWalls(x,y,room) < self.neighbors:
							room[x][y] = 0

			# floodfill to remove small caverns
			room = self.floodFill(room)

			# start over if the room is completely filled in
			roomWidth,roomHeight = self.getRoomDimensions(room)
			for x in range (roomWidth):
				for y in range (roomHeight):
					if room[x][y] == 0:
						return room

	def floodFill(self,room):
		'''
		Find the largest region. Fill in all other regions.
		'''
		roomWidth,roomHeight = self.getRoomDimensions(room)
		largestRegion = set()

		for x in range (roomWidth):
			for y in range (roomHeight):
				if room[x][y] == 0:
					newRegion = set()
					tile = (x,y)
					toBeFilled = set([tile])
					while toBeFilled:
						tile = toBeFilled.pop()

						if tile not in newRegion:
							newRegion.add(tile)

							room[tile[0]][tile[1]] = 1

							# check adjacent cells
							x = tile[0]
							y = tile[1]
							north = (x,y-1)
							south = (x,y+1)
							east = (x+1,y)
							west = (x-1,y)

							for direction in [north,south,east,west]:

								if room[direction[0]][direction[1]] == 0:
									if direction not in toBeFilled and direction not in newRegion:
										toBeFilled.add(direction)

					if len(newRegion) >= self.ROOM_MIN_SIZE:
						if len(newRegion) > len(largestRegion):
							largestRegion.clear()
							largestRegion.update(newRegion)
		
		for tile in largestRegion:
			room[tile[0]][tile[1]] = 0

		return room

	def placeRoom(self,room, mapWidth, mapHeight): #(self,room,direction,)
		roomX = None
		roomY = None

		roomWidth, roomHeight = self.getRoomDimensions(room)

		# try n times to find a wall that lets you build room in that direction
		for i in xrange(self.placeRoomAttempts):
			# try to place the room against the tile, else connected by a tunnel of length i

			wallTile = None
			direction = self.getDirection()
			while not wallTile:
				'''
				randomly select tiles until you find
				a wall that has another wall in the
				chosen direction and has a floor in the 
				opposite direction.
				'''
				#direction == tuple(dx,dy)
				tileX = random.randint(1,mapWidth-2)
				tileY = random.randint(1,mapHeight-2)
				if ((self.level.getBlocksMovement(tileX,tileY) == True) and
					(self.level.getBlocksMovement((tileX+direction[0]),(tileY+direction[1])) == True) and
					(self.level.getBlocksMovement((tileX-direction[0]),(tileY-direction[1])) == False)):
					wallTile = (tileX,tileY)

			#spawn the room touching wallTile
			startRoomX = None
			startRoomY = None
			 
			while not startRoomX and not startRoomY:
				x = random.randint(0,roomWidth-1)
				y =  random.randint(0,roomHeight-1)
				if room[x][y] == 0:
					startRoomX = wallTile[0] - x
					startRoomY = wallTile[1] - y

			#then slide it until it doesn't touch anything
			for tunnelLength in xrange(self.maxTunnelLength):
				possibleRoomX = startRoomX + direction[0]*tunnelLength
				possibleRoomY = startRoomY + direction[1]*tunnelLength

				enoughRoom = self.getOverlap(room,possibleRoomX,possibleRoomY,mapWidth,mapHeight)

				if enoughRoom:
					roomX = possibleRoomX 
					roomY = possibleRoomY 

					# moved tunnel code into self.generateLevel()

					return roomX,roomY, wallTile, direction, tunnelLength

		return None, None, None, None, None

	def addRoom(self,roomX,roomY,room):
		roomWidth,roomHeight = self.getRoomDimensions(room)
		for x in range (roomWidth):
			for y in range (roomHeight):
				if room[x][y] == 0:
					self.level.setBlocksMovementFalse(roomX+x, roomY+y)
					self.level.setBlocksSightFalse(roomX+x, roomY+y)

		# Fill the room with monsters and objects
		self.level.populateRoom(roomX,roomY,roomWidth,roomHeight,room)
		self.rooms.append(room)

	def addTunnel(self,wallTile,direction,tunnelLength):
		# carve a tunnel from a point in the room back to 
		# the wall tile that was used in its original placement
		
		startX = wallTile[0] + direction[0]*tunnelLength
		startY = wallTile[1] + direction[1]*tunnelLength
		#self.level[startX][startY] = 1
		
		for i in range(self.maxTunnelLength):
			x = startX - direction[0]*i
			y = startY - direction[1]*i
			self.level.setBlocksMovementFalse(x,y)
			self.level.setBlocksSightFalse(x,y)

			# If you want doors, this is where the code should go
			if ((x+direction[0]) == wallTile[0] and 
				(y+direction[1]) == wallTile[1]):
				break

		# Populate Tunnel
		
	def getRoomDimensions(self,room):
		if room:
			roomWidth = len(room)
			roomHeight = len(room[0])
			return roomWidth, roomHeight
		else:
			roomWidth = 0
			roomHeight = 0
			return roomWidth, roomHeight

	def getAdjacentWalls(self, tileX, tileY, room): # finds the walls in 8 directions
		wallCounter = 0
		for x in range (tileX-1, tileX+2):
			for y in range (tileY-1, tileY+2):
				if (room[x][y] == 1):
					if (x != tileX) or (y != tileY): # exclude (tileX,tileY)
						wallCounter += 1
		return wallCounter

	def getDirection(self):
		# direction = (dx,dy)
		north = (0,-1)
		south = (0,1)
		east = (1,0)
		west = (-1,0)

		direction = random.choice([north,south,east,west])
		return direction

	def getOverlap(self,room,roomX,roomY,mapWidth,mapHeight):
		'''
		for each 0 in room, check the cooresponding tile in
		self.level.terrain and the eight tiles around it. Though slow,
		that should insure that there is a wall between each of
		the rooms created in this way.
		<> check for overlap with self.level.terrain
		<> check for out of bounds
		'''
		roomWidth, roomHeight = self.getRoomDimensions(room)
		for x in range(roomWidth):
			for y in range(roomHeight):
				if room[x][y] == 0:
					# Check to see if the room is out of bounds
					if ((1 <= (x+roomX) < mapWidth-1) and
						(1 <= (y+roomY) < mapHeight-1)):
						#Check for overlap with a one tile buffer
						if self.level.getBlocksMovement(x+roomX-1, y+roomY-1) == False: # top left
							return False
						if self.level.getBlocksMovement(x+roomX, y+roomY-1) == False: # top center
							return False
						if self.level.getBlocksMovement(x+roomX+1, y+roomY-1) == False: # top right
							return False

						if self.level.getBlocksMovement(x+roomX-1, y+roomY) == False: # left
							return False
						if self.level.getBlocksMovement(x+roomX, y+roomY) == False: # center
							return False
						if self.level.getBlocksMovement(x+roomX+1, y+roomY) == False: # right
							return False																				
		
						if self.level.getBlocksMovement(x+roomX-1, y+roomY+1) == False: # bottom left
							return False
						if self.level.getBlocksMovement(x+roomX, y+roomY+1) == False: # bottom center
							return False
						if self.level.getBlocksMovement(x+roomX+1, y+roomY+1) == False: # bottom right
							return False							

					else: #room is out of bounds
						return False
		return True

	def addShortcuts(self,mapWidth,mapHeight):
		'''
		I use libtcodpy's built in pathfinding here, since I'm
		already using libtcodpy for the iu. At the moment, 
		the way I find the distance between
		two points to see if I should put a shortcut there
		is horrible, and its easily the slowest part of this
		algorithm. If I think of a better way to do this in
		the future, I'll implement it.
		'''
		
		#initialize the libtcodpy map
		libtcodMap = libtcod.map_new(mapWidth,mapHeight)
		self.recomputePathMap(mapWidth,mapHeight,libtcodMap)

		for i in xrange(self.shortcutAttempts):
			# check i times for places where shortcuts can be made
			while True:
				#Pick a random floor tile
				floorX = random.randint(self.shortcutLength+1,(mapWidth-self.shortcutLength-1))
				floorY = random.randint(self.shortcutLength+1,(mapHeight-self.shortcutLength-1))
				if self.level.getBlocksMovement(floorX,floorY) == False: 
					if (self.level.getBlocksMovement(floorX-1,floorY) == True or
						self.level.getBlocksMovement(floorX+1,floorY) == True or
						self.level.getBlocksMovement(floorX,floorY-1) == True or
						self.level.getBlocksMovement(floorX,floorY+1) == True):
						break

			# look around the tile for other floor tiles
			for x in xrange(-1,2):
				for y in xrange(-1,2):
					if x != 0 or y != 0: # Exclude the center tile
						newX = floorX + (x*self.shortcutLength)
						newY = floorY + (y*self.shortcutLength)
						if self.level.getBlocksMovement(newX,newY) == False:
						# run pathfinding algorithm between the two points
							#back to the libtcodpy nonesense
							pathMap = libtcod.path_new_using_map(libtcodMap)
							libtcod.path_compute(pathMap,floorX,floorY,newX,newY)
							distance = libtcod.path_size(pathMap)

							if distance > self.minPathfindingDistance:
								# make shortcut
								self.carveShortcut(floorX,floorY,newX,newY)
								self.recomputePathMap(mapWidth,mapHeight,libtcodMap)


		# destroy the path object
		libtcod.path_delete(pathMap)

	def placeStaircases(self,mapWidth,mapHeight):
		downStairsX = None
		downStairsY = None
		upStairsX = None
		upStairsY = None
		longestDistance = 0

		#initialize the libtcodpy map
		libtcodMap = libtcod.map_new(mapWidth,mapHeight)
		self.recomputePathMap(mapWidth,mapHeight,libtcodMap)

		# try n times
		for i in xrange(20):
			# pick a random point
			while True:
				tempX1 = random.randint(8,mapWidth-8)
				tempY1 = random.randint(8,mapHeight-8)
				if self.level.getBlocksMovement(tempX1,tempY1) == False: 
					break

			# try n times
			for i in xrange(20):
				# pick another random point
				while True:
					tempX2 = random.randint(8,mapWidth-8)
					tempY2 = random.randint(8,mapHeight-8)
					if self.level.getBlocksMovement(tempX2,tempY2) == False: 
						break

				# if pathingDistance between the two points is greater
				# than the longest pathing distance, set the stair coordinates
				# to the two points, else continue
				pathMap = libtcod.path_new_using_map(libtcodMap)
				libtcod.path_compute(pathMap,tempX1,tempY1,tempX2,tempY2)
				distance = libtcod.path_size(pathMap)

				if distance > longestDistance:
					downStairsX = tempX1
					downStairsY = tempY1
					upStairsX = tempX2
					upStairsY = tempY2
					longestDistance = distance

		self.level.placeStairs(downStairsX,downStairsY,upStairsX,upStairsY)
		
		# destroy the path object
		libtcod.path_delete(pathMap)

	def recomputePathMap(self,mapWidth,mapHeight,libtcodMap):
		for x in xrange(mapWidth):
			for y in xrange(mapHeight):
				if self.level.getBlocksMovement(x,y) == True:
					libtcod.map_set_properties(libtcodMap,x,y,False,False)
				else:
					libtcod.map_set_properties(libtcodMap,x,y,True,True)

	def carveShortcut(self,x1,y1,x2,y2):
		if x1-x2 == 0:
			# Carve virtical tunnel
			for y in xrange(min(y1,y2),max(y1,y2)+1):
				self.level.setBlocksMovementFalse(x1,y)
				self.level.setBlocksSightFalse(x1,y)
				#self.level[x1][y] = 0

		elif y1-y2 == 0:
			# Carve Horizontal tunnel
			for x in xrange(min(x1,x2),max(x1,x2)+1):
				self.level.setBlocksMovementFalse(x,y1)
				self.level.setBlocksSightFalse(x,y1)
				#self.level[x][y1] = 0

		elif (y1-y2)/(x1-x2) == 1:
			# Carve NW to SE Tunnel
			x = min(x1,x2)
			y = min(y1,y2)
			while x != max(x1,x2):
				x+=1
				self.level.setBlocksMovementFalse(x,y)
				self.level.setBlocksSightFalse(x,y)
				#self.level[x][y] = 0
				y+=1
				self.level.setBlocksMovementFalse(x,y)
				self.level.setBlocksSightFalse(x,y)
				#self.level[x][y] = 0

		elif (y1-y2)/(x1-x2) == -1:
			# Carve NE to SW Tunnel
			x = min(x1,x2)
			y = max(y1,y2)
			while x != max(x1,x2):
				x += 1
				self.level.setBlocksMovementFalse(x,y)
				self.level.setBlocksSightFalse(x,y)
				#self.level[x][y] = 0
				y -= 1
				self.level.setBlocksMovementFalse(x,y)
				self.level.setBlocksSightFalse(x,y)
				#self.level[x][y] = 0

	def checkRoomExists(self,room):
		roomWidth, roomHeight = self.getRoomDimensions(room)
		for x in range(roomWidth):
			for y in range(roomHeight):
				if room[x][y] == 0:
					return True
		return False