"""The configurations file. Study it, change it."""

import logging

# === EDITING ===

# If set to True, automatically saves to the database all changes done to 
# all instances. Note: if you manually change something, then you have to save
# it yourself. E.g.
# >>> myInstance.name = 'new name'
# >>> myInstance.save()
autoSave = True

# === LOADING ===

# Which objects libraries should be loaded at the start of the application.
libs = {'nature': ['animals']}

# Which media should be loaded
etcs = ['templates']

# Which templates should be loaded (implies templates are loaded from etc)
templates = []

# === LOGGING ===

# At least what should be logged? debug > info > warning > error > critial.
loggingLevel = logging.DEBUG

# How should it be logged (check python's logging documentation for mor info).
loggingFormat = "%(funcName)s() %(levelname)s: %(message)s"

# If it should it overwrite the last log.
loggingMode = 'w'
