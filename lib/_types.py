"""Types of basic objects.

This are merely classes that provide actions to specific types of objects.
"""

from ppdRPG import configs
from ppdRPG import _Object
import logging

class Mobile(_Object):
	"""_Objects that can be moved, such as Thing, Npc, Player, but NOT Place."""
	
	
	def __init__(self):
		pass
		
	def move(self,place,position=None,autoSave=configs.autoSave):
		"""Move from a position to another taking into account what is on the
		destination and on Place.bans
		"""
		
		logging.debug("Moving %s to %s on %s." % (self.instanceName, 
												position, place.instanceName))
		
		if position == None:
			position = [0,0]

		try:
			if self in place.bans:
				raise Exception("%s is not allowed in %s" % (self.instanceName,
															place.instanceName))

			elif not position in place.availablePositions():
				raise Exception("Position occupied by %s" % (
										place.matrix[position[0]][position[1]]))

			# If the object is already on the place, just move it
			elif place.contains(self):
				place.moveObj(self.position,position)
				self.position = position
				self.place = place

			# Else, add it to the place at position and remove it from it's
			# current place, if it is in one.
			else:
				try:
					self.place.matrix[self.position[0]][self.position[1]]=False
				except AttributeError:
					pass

				place.matrix[position[0]][position[1]] = self
				self.position = position
				self.place = place
		except IndexError:
			raise Exception("Position outside of place.")

		if autoSave:
			self.save()
			place.save()
   
	def walk(self,x,y):
		"""Walk left, right, up, down, diagonals."""
			
		xs = [-1,0,1]
		ys = xs
			
		if not x in xs or not y in ys:
			raise Exception('Cannot jump spaces.')

		position = [self.position[0] + y, self.position[1] + x]
		self.move(self.place,position)
	
	def reach(self, destination, currentPosition=None, 
			visitedPositions=None, unvisitedPositions=None):
		"""Go from source to destination on the place matrix considering 
		what is on the way.
		
		It finds a sub-optimal path from source to destination and either
		move the object to the destination or return an error if there
		is no possible path.
		"""
			
		try:
			if self.place.matrix[destination[0]][destination[1]] != False:
				raise Exception('Position unavailable.')
		except IndexError:
			raise Exception("Position outside of %s." % (
													self.place.instanceName))

		if currentPosition == None:
			currentPosition = self.position[:]
		if visitedPositions == None:
			visitedPositions = currentPosition[:]
		if unvisitedPositions == None:
			unvisitedPositions = []
			
		currentNeighbors = [[currentPosition[0], currentPosition[1]+1], # Migi
							[currentPosition[0], currentPosition[1]-1], # Hidari
							[currentPosition[0]+1, currentPosition[1]], # Ue
							[currentPosition[0]-1, currentPosition[1]], # Shita
							[currentPosition[0]+1, currentPosition[1]+1], # /\>
							[currentPosition[0]-1, currentPosition[1]-1], # \/<
							[currentPosition[0]+1, currentPosition[1]-1], # /\>
							[currentPosition[0]-1, currentPosition[1]+1]] # \/>

		# Points outside the matrix do not exist, hence are not neighbors. 
		# Walls and objects neither. Nor are positions already visited.
		toBeDeleted = []
		for i in currentNeighbors:
			if i[0] < 0 or i[1] < 0: # List[-1] exists, but is not a neighbor.
				toBeDeleted.append(i)
			else:
				try:
					if (i in visitedPositions or 
							not self.place.matrix[i[0]][i[1]] == False):
						toBeDeleted.append(i)
				except IndexError:
					toBeDeleted.append(i)
		for i in toBeDeleted:
			currentNeighbors.remove(i)

		# It is possible to go back and visit unvisited positions.
		currentNeighbors += unvisitedPositions

		# If there are no neighbors, we are stuck.
		if not currentNeighbors:
			raise Exception('There is no way to reach the destination.')

		# Else, explore said possibilities.
		else:
			# If the destination is within reach, move to it.
			if destination in currentNeighbors:
				self.move(self.place,destination)
				return None
			# Else, move to the possibility closest to the destination.
			else:
				# Create a dictionaty of {node : distance to the destination}.
				nodes = {}
				for i in currentNeighbors:
					# The number of movements to reach the destination
					# (distance from it), being able to walk on a line
					# or on a diagonal, is equal to the biggest of either
					# the number of columns, or the number of lines
					# between the source and the destination.
					if abs(destination[0]-i[0]) >= abs(destination[1]-i[1]):
						distance = abs(destination[0]-i[0])
					else:
						distance = abs(destination[1]-i[1])
					try:
						nodes[distance].append(i)
					except KeyError:
						nodes[distance] = []
						nodes[distance].append(i)

				# Set current position as the (first) possibility with
				# the smalles distance to the destination.
				currentPosition = nodes[min(nodes)][0]
				visitedPositions.append(currentPosition)

				# Add unvisited possibilities to the unvisitedPositions
				# list (if not already in it or if it was visited)
				k = currentNeighbors.index(currentPosition)
				for i in currentNeighbors[:k] + currentNeighbors[k+1:]:
					if (not i in visitedPositions and 
						not i in unvisitedPositions):
						unvisitedPositions.append(i)
				
				try:
					unvisitedPositions.remove(currentPosition)
				except ValueError:
					pass

				# Now in the new position, repeat everything until either
				# we reach the destination or get stuck.
				self.reach(destination,currentPosition, 
							visitedPositions,unvisitedPositions)
				return None

class Usable(_Object):
	"""Objects that can be used by a player, a npc...
	
	Places do not inherit this class. It is intended for the Thing class and
	it's childs only.
	"""
	
	
	def __init__(self, used=None, bans=None):
		
		if used == None:		# Who used it.
			self.used = []
		else:
			self.used = used
		if bans == None:		# Who is not allowed to use it.
			self.bans = []
		else:
			self.bans = bans
	
	def use(self, obj):
		"""Append obj to usedlist if it's allowed to use self.
		
		Use objInstance.use(thingInstance) if you want an object to use a thing.
		"""
		
		if not obj in self.bans:
			self.used.append(obj)
			return None
		else:
			raise Exception("%s is not allowed to use %s." % (
											obj.instanceName, self.name))
		
	def usedBy(self, obj):
		"""Was this used by obj?"""
		
		if obj in self.used:
			return True
		else:
			return False
