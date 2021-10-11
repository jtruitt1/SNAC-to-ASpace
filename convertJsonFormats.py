"""
Read in a series of JSON files representing SNAC constellations;
convert into JSONs acceptable to the ArchivesSpace agent module.
"""
import json, re
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
	i = 0
	length = str(len(constellations))
	for constellation in constellations:
		try:
			# Print status message
			i += 1
			print("Converting constellation", i, "of", length+"...", end="\r")
			agent = convertToAgent(constellation)
			if len(agent) > 0:
				agents.append(agent)
		except SnacError:
			continue
		except Exception as e:
			print("\n\n")
			raise e
	print()
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

	# Convert biogHist
	if "biogHists" in constellation:
		# Isolate biogHist in SNAC JSON
		biogHist = constellation["biogHists"][0]

		# Check biogHist for <biogHist> tag
		match = re.search("</?biogHist.+?>",biogHist)

		while match: # If <biogHist> found
			# Remove the tag
			biogHist = re.sub("</?biogHist.+?>","",biogHist)
			match = re.search("</?biogHist.+?>",biogHist)

		# CHECK FOR SOURCE TAG; CONVERT IF FOUND

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
	#print("inConvertPersonAgent")

	# Handle name entries
	agentNames = []
	for name in constellation["nameEntries"]:
		try:
			agentNames.append(convertPersonName(name))
		except KeyError:
			ark = constellation["ark"][-8:]
			print("ERROR: skipped an unparsed name in", ark)
			print(name)
		except SnacError:
			ark = constellation["ark"][-8:]
			print("ERROR: skipped an unparsed name in", ark)
			print(name)
			continue

	agent["names"] = agentNames

	return agent

def convertCorpAgent(constellation, agent):
	"""
	insert docstring
	"""
	print("inConvertCorpAgent")
	return agent

def convertPersonName(nameEntry):
	"""
	Convert a name entry from SNAC format to ASpace format

	@param nameEntry: a SNAC name entry in dict form

	@returns: an ASpace name entry in dict form
	"""

	# Check to see if name has been parsed
	if "components" not in nameEntry:
		# Raise an error if not
		raise SnacError

	# Initialize name dict to be returned
	agentName = {}

	# Go through the name components, assigning them to ASpace slots
	for component in nameEntry["components"]:
		if component["type"]["term"] == "Surname":
			agentName["primary_name"] = component["text"]

		if component["type"]["term"] == "NameAddition":
			agentName["title"] = component["text"]

		if component["type"]["term"] == "Forename":
			agentName["rest_of_name"] = component["text"]

		if component["type"]["term"] == "Numeration":
			agentName["number"] = component["text"]

		if component["type"]["term"] == "NameExpansion":
			agentName["fuller_form"] = component["text"]

		if component["type"]["term"] == "Date":
			agentName["dates"] = component["text"]

	# Handle rules, source, and language
	agentName["source"] = "snac"
	agentName["rules"] = "rda"
	# TODO: Language?
	if nameEntry["preferenceScore"] == "99":
		agentName["authorized"] = True
		agentName["is_display_name"] = True
	elif nameEntry["preferenceScore"] == "0":
		agentName["authorized"] = False
		agentName["is_display_name"] = False
	else:
		if agentName["contributors"]["type"]["term"] == "authorizedForm":
			agentName["authorized"] = True
			agentName["is_display_name"] = True
		else:
			agentName["authorized"] = False
			agentName["is_display_name"] = False

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
