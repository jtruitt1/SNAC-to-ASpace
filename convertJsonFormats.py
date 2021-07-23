"""
Read in a series of JSON files representing SNAC constellations;
convert into JSONs acceptable to the ArchivesSpace agent module.
"""
import json, requests
from glob import glob
from random import choices

def loadSnacData():
	"""
	Read SNAC JSON data from files in the snac_jsons folder.

	Returns: constellations, a list of SNAC JSONs in dict form
	"""
	# Get list of filenames to read
	filenames = glob("snac_jsons/*.json")

	# For testing purposes
	filenames = choices(filenames, k=5)

	# Initialize array of constellations to eventually return
	constellations = []

	# Loop over filenames, reading the files & adding the data to constellations
	print("Reading {} JSON files...")
	for filename in filenames:
		print("Writing {}".format(filename + "..."), end="")
		with open(filename) as f:
			constellations.append(json.load(f))
		print("\tdone")
	print("JSON files read successfully.\n")
	return constellations

def convertToAgents(constellations):
	"""
	Convert a list of SNAC constellations into ASpace Agents

	Param:	@constellations, a list of SNAC JSONs in dict form
	Returns: agents, a list of ASpace JSONs in dict form
	"""
	agents = []
	for constellation in constellations:
		agent = convertToAgent(constellation)
		if len(agent) > 0:
			agents.append(agent)
	return agents

def convertToAgent(constellation):
	"""
	Convert a JSON representing a SNAC constellation to one rep'ing an AS agent

	Param:	@constellation, a SNAC constellation JSON in dict form
	Returns: agent, an ASpace agent JSON in dict form
	"""

	## TODO: print a status message

	# Initialize agent dict to be returned
	agent = {}

	# Check SNAC record against AS agents
	## TODO:

	# Convert names (type-specific?)
	## TODO:

	# Convert sources
	## TODO:

	# Convert places
	## TODO:

	# Convert exist dates
	## TODO:


	# Take care of details specific to agent sub-types
	if constellation["entityType"]["term"] == "person":
		agent = convertPersonAgent(constellation, agent)
	elif constellation["entityType"]["term"] == "corporation":
		agent = convertCorpAgent(constellation, agent)

	return agent

def convertPersonAgent(constellation, agent):
	"""
	insert docstring
	"""
	print("inConvertPersonAgent")
	return agent

def convertCorpAgent(constellation, agent):
	"""
	insert docstring
	"""
	print("inConvertCorpAgent")
	return agent

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
	print("\n")
	constellations = loadSnacData()
	agents = convertToAgents(constellations)
	# writeJsons(agents)
	print("\n")

main()
