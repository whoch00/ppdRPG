"""The four basic types of objects - Place, Npc, Thing, Player.

All objects are child classes of these.

"""

from ppdRPG import _Object
from ppdRPG import configs
from _types import Mobile

class Place(_Object):
	"""A location. Every object (but places) is placed on a Place instance."""

	
	def __init__(self, instanceName, matrix, name=None, 
				bans=None, extraArgs=None, autoSave=configs.autoSave):
		
		if name == None:
			self.name = instanceName
		self.type_ = Place
		self.instanceName = instanceName
		self.verifyDoubleEntry()
		
		if bans == None:
			self.bans = []
		else:
			self.bans = bans
		if extraArgs == None:
			self.extraArgs = {}
		else:
			self.extraArgs = extraArgs
		
		# Matrix supplied
		try:			
			matrix[0][0]
			self.matrix = matrix
		# [x,y] supplied, generate an empty room
		except TypeError:			
			self.x = matrix[0]
			self.y = matrix[1]
			self.matrix = []
			
			for i in xrange(0,self.x):
				self.matrix.append([])
				for j in xrange(0,self.y):
					self.matrix[i].append(False)

		_Object.__init__(self, self.extraArgs)
		
	def ban(self, list_):
		"""Add an object to the place's ban list, 
		forbidding it to be moved to the place.
		"""

		for i in list_:
			if i in self.bans:
				pass
			else:
				self.bans.append(i)

	def allow(self, list_):
		"""Remove a name from the place's ban list, 
		allowing it to be moved to the place.
		"""

		for i in list_:
			try:
				self.bans.remove(i)
			except ValueError:
				pass

	def availablePositions(self):
		"""Returns a list of unoccupied indexes of self.matrix"""
		
		availablePositions=[]
		x=0
		y=0
		
		for i in self.matrix:
			for j in i:
				if j == False:
					availablePositions.append([x,y])
				y+=1
			y=0
			x+=1

		return availablePositions
	
	def contains(self, obj):
		"""Tells if there's a specific object in the place.	"""
		
		for i in xrange(0,len(self.matrix)):
			if obj in self.matrix[i]:
				return True
		return False
	
	def moveObj(self, objposition, endposition):
		"""This moves an object on the place matrix to another position 
		and sets the former position to False, regardless of what is 
		in the object's initial position or in the destination.
		"""
		
		try:
			self.matrix[endposition[0]][endposition[1]] = (
				self.matrix[objposition[0]][objposition[1]])
			self.matrix[objposition[0]][objposition[1]] = False
		except IndexError:
			print "Position is outside the place."
		
		return None

class Npc(_Object, Mobile):
	"""Non-player characters."""
	
	
	def __init__(self, instanceName, place, name=None, 
				position=None, extraArgs=None, 
				autoSave=configs.autoSave):
		
		if name == None:
			self.name = instanceName
		self.type_ = Npc
		self.instanceName = instanceName
		self.verifyDoubleEntry()
		
		if position == None:
			self.position = [0,0]
		else:
			self.position = position
		if extraArgs == None:
			self.extraArgs = {}
		else:
			self.extraArgs = extraArgs
		
		# Sets self.place and self.position
		# Saves if autoSave = True (because the place also needs to be updated).
		self.move(place,position)
		
		_Object.__init__(self, self.extraArgs)

	def say(self,msg):
		"""Say something."""
		
		print "%s says:" % (self.name)
		return msg
	
	def introduce(self,msg=None):
		"""Hi, I'm npc."""
		
		if msg == None:
			msg = "Hi, I'm %s" % (self.name)
		return self.say(msg)

class Thing(_Object, Mobile):
	"""An object (thing).
	
	This class does not inherits the Usable one. If you want an usable thing,
	use one provided in the library or create your own, since different things
	have different uses.
	"""
	
	
	def __init__(self, instanceName, place, name=None, 
				position=None, extraArgs=None):
		
		if name == None:
			self.name = instanceName
		self.type_ = Thing
		self.instanceName = instanceName
		self.verifyDoubleEntry()
		
		self.place = place
		if position == None:
			self.position = [0,0]
		else:
			self.position = position
		if extraArgs == None:
			self.extraArgs = {}
		else:
			self.extraArgs = extraArgs
		
		_Object.__init__(self, self.extraArgs)

class Player(_Object, Mobile):
	"""A player (user-controled)."""
	
	
	# To be done in the future.

class Group(_Object):
	"""A group of instances with special privileges.
	
	This is a special Class in the basic.py file, it does not accept extraArgs
	and is only used to group instances of other classes into groups with
	special privileges or duties, according to the developer's choice.
	"""
	
	def __init__(self, instanceName, name=None, members=None, 
				bans=None, autoSave=configs.autoSave):
		
		self.type_ = Group
		self.instanceName = instanceName
		self.verifyDoubleEntry()
		
		self.extraArgs = None
		
		if name == None:
			self.name = instanceName	
		if members == None:
			self.members = []
		else:
			self.members = members
		if bans == None:
			self.bans = []
			
		_Object.__init__(self, self.extraArgs)
		
	def add(self, instancesList):
		"""Add a list of instances to the group's member's list."""
		
		for i in instancesList:
			if i in self.bans:
				print "%s is not allowed in %s. Please issue %s.allow(%s)\
					first." % (i, self.name, self.name, i)
			elif i in self.members:
				print "%s already in %s" % (i, self.name)
			else:
				self.members.append(i)
	
	def ban(self, instancesList):
		"""Ban a list of instances from the groups's member's list."""
		
		for i in instancesList:
			if i in self.members:
				self.members.remove(i)
			elif i in self.bans:
				print "%s already banned from %s" % (i, self.name)
			else:
				self.bans.append(i)
				
	def allow(self, instancesList):
		"""Allow a list of instances to the groups's member's list."""
		
		for i in instancesList:
			if not i in self.bans:
				print "%s already allowed in %s" % (i, self.name)
			else:
				self.bans.remove(i)
