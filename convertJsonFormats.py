"""
Read in a series of JSON files representing SNAC constellations;
convert into JSONs acceptable to the ArchivesSpace agent module.
"""
import json, requests
from asUtils import *
from glob import glob

def loadSnacData():
	"""
	insert docstring
	"""
	pass

def convertToAgents(constellations):
	"""
	insert docstring
	"""
	agents = []
	for constellation in constellations:
		agent = convertToAgent(constellation)
		agents.append(agent)

def convertToAgent(constellation):
	"""
	insert docstring
	"""
	pass

def writeJsons(agents):
	pass

def main():
	constellations = loadSnacData()
	agents = convertToAgents(constellations)
	writeJsons(agents)
