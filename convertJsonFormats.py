"""
Read in a series of JSON files representing SNAC constellations;
convert into JSONs acceptable to the ArchivesSpace agent module.
"""
import json, requests
from glob import glob
from random import choices
from utils import loadSnacData

class SnacError(Exception):
	"""Raise when there's a non-fatal conversion error & we want to skip."""

	def __init__(self):
		super(SnacError, self).__init__()

def convertToAgents(constellations):
	"""
	Convert a list of SNAC constellations into ASpace Agents

	Param:	@constellations, a list of SNAC JSONs in dict form
	Returns: agents, a list of ASpace JSONs in dict form
	"""
	agents = []
	for constellation in constellations:
		try:
			agent = convertToAgent(constellation)
			if len(agent) > 0:
				agents.append(agent)
		except SnacError:
			continue
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

	convertPersonName(constellation, agent)

	return agent

def convertCorpAgent(constellation, agent):
	"""
	insert docstring
	"""
	print("inConvertCorpAgent")
	return agent

def convertPersonName(constellation, agent):
	"""
	Get preferred name from SNAC JSON; add its data to ASpace agent JSON.

	@param constellation: a SNAC constellation JSON of the person type
	@param agent: a JSON representing an ASpace agent

	@returns: a dict containing the name info
	"""
	# Get preferred name from the constellation
	constName = constellation["nameEntries"][0]

	# Check to see if name has been parsed
	if "components" not in constName:
		# Raise an error if not
		ark = constellation["ark"][-8]
		print("ERROR: preferred name of", ark, "is unparsed")
		raise SnacError

	# Initialize name dict to be returned
	agentName = {}

	# Go through the name components, assigning them to ASpace slots
	for item in constName["components"]:
		try:
			if item["type"]["term"] == "Surname":
				agentName["primary_name"] = item["text"]

			if item["type"]["term"] == "NameAddition":
				agentName["title"] = item["text"]

			if item["type"]["term"] == "Forename":
				agentName["rest_of_name"] = item["text"]

			if item["type"]["term"] == "Numeration":
				agentName["number"] = item["text"]

			if item["type"]["term"] == "NameExpansion":
				agentName["fuller_form"] = item["text"]

			if item["type"]["term"] == "Date":
				agentName["dates"] = item["text"]
		except KeyError:
			print("KeyError": )

	return agentName

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
