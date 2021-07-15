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
	"""
	Given a list of JSON objects, write each one to a separate file

	Param: jsons, a list of JSON objects represented as Python dicts
	"""
	print("Writing {} JSON objects to file...".format(len(jsons)))

	# Loop over JSONs
	for item in jsons:
		# Create filename
		directory = "as_jsons/"
		entName = item["id"] ## TODO: figure out proper key for AS
		filename = directory+entName+".json"

		# Write file
		print("Writing {}".format(filename[14:] + "..."), end="")
		try:
			with open(filename, 'w', encoding='utf-8') as f:
				json.dump(item, f, ensure_ascii=False, indent=4)
		except (FileNotFoundError):
			with open(filename, 'x', encoding='utf-8') as f:
				json.dump(item, f, ensure_ascii=False, indent=4)
		print("\tDone.")

def main():
	constellations = loadSnacData()
	agents = convertToAgents(constellations)
	writeJsons(agents)
