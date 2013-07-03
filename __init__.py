"""ppdRPG - A python platform for developping role playing games.

To start development, adjust the configurations at config.py and then
import ppdRPG and from ppdRPG import *. Create the instances you want to 
and code your game accessing them using ppdRPG.db['Class']['instanceName']

"""

import sys
import os
import logging
import shelve
import configs

__all__ = ['lib', 'etc']
_gameroot = os.path.abspath(__file__)[:-12]
_shelves = _gameroot+'/dbs'
_logs= _gameroot+'/log'

sys.path.append(_gameroot)

for i in [_shelves, _logs]:
	if not os.path.exists(i):
		os.makedirs(i)

logging.basicConfig(
					filename = _logs+'/lastrun.log',
					filemode = configs.loggingMode,
					level = configs.loggingLevel,
					format = configs.loggingFormat
					)

db = shelve.open(_shelves+'/main.db',writeback=True)

class _Object:
	"""Interacts with the database, saving and removing instances from it."""
		
	def __init__(self, extraArgs, autoSave=configs.autoSave):
		
		self.extraArgs = extraArgs

		if autoSave:
			self.save()
	
	def verifyDoubleEntry(self):
		"""Verifies if self.instanceName is already on the database."""
		
		try:			
			for i in db[self.type_]:				
				if i == self.instanceName:					
					raise Exception("There's already a %s with instanceName %s"\
						"on the database." % (self.type_, self.instanceName))				
		except KeyError:
			pass

		return None
				
	def save(self):
		"""Saves the instance to the database."""		
		
		logging.info("Saving %s to the database." % (self.instanceName))

		try:
			db[self.type_][self.instanceName] = self
		except KeyError:
			db[self.type_] = {}
			db[self.type_][self.instanceName] = self

	def delete(self):
		"""Deletes the instance from the database.
		
		Note that the instance itself is not deleted.
		"""
		
		logging.info("Removing %s from the database." % (self.instanceName))
		
		del db[self.type_][self.instanceName]
