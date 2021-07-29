"""
Gets data from SNAC and writes it to a file w/ JSON data and a file w/ a list
of SNAC IDs
"""
import json, requests
import xml.etree.ElementTree as ET
from JSONtoEACCPF import *
from base64 import b64decode


def retrieveSnacAgent(snacID):
	"""
	Given a SNAC agent's ID number, pull its full JSON record from SNAC.

	This function retrieves a JSON record from the SNAC Cooperative database.
	To do so it uses the "download_constellation" API command and then
	converts the 64-bit encoded file into a string.
	("download_constellation" is used because the API command "read" does not
	return maintenance info	and the API command "constellation_history" does
	not reliably return records with fields like "maintenanceAgent".
	"download_constellation", on the other hand, returns all of the data
	needed to make an EAC file, neatly wrapped up in JSON format)
	Param: @snacID, the SNAC ID of the agent in question
	Returns: snacConstellation, a SNAC agent JSON in dict form
	"""
	# Prep data for API request
	baseURL = "https://api.snaccooperative.org/"
	input = {"command": "download_constellation",
	"constellationid": snacID, "type": "constellation_json"}
	toPost = json.dumps(input)

	# Make API request
	output = requests.post(baseURL, data=toPost).json()

	# Convert file downloaded from API into JSON dict format
	binary = output['file']["content"]
	text = str(b64decode(binary), encoding="utf-8")
	snacConstellation = json.loads(text)

	return snacConstellation

def getSnacAgentsFromList(snacIds):
	"""
	Given a list of snacIDs, return a list of constellation JSONs via API calls

	Params: @snacIDs, a list containing SNAC IDs
	Returns: snacConstellations, a list of SNAC agent JSONs in dict form
	"""
	numRelated = len(snacIds)
	i = 0

	# Pull full JSONs of listed constellations from SNAC into a list

	snacConstellations = [] # Initialize list to return

	print("Fetching {} related constellations from SNAC...".format(numRelated))

	for ID in snacIds:
		# Get constellation via API request
		i += 1
		print("Fetching constellation {}, id {}...".format(i, ID), end="")
		agent = retrieveSnacAgent(ID)
		# Append constellation to list
		snacConstellations.append(agent)

	print("Successfully fetched all constellations!")

	return snacConstellations

def getIdList(url):
	"""
	Given the url of a file listing of SNAC agents IDs, returns a list of IDs

	Params: @url, the "raw." github url of a TSV whose first column is SNAC IDs
	Returns: a list of ID strings
	"""
	pass

def getRelatedSnacAgents(mainID):
	"""
	Given a SNAC agent's ID number, pull the full JSON record of that
	constellation and those of all related agents.

	Param: @mainID, the SNAC ID of the central agent
	Returns: snacConstellations, a list of SNAC agent JSONs in dict form
	"""

	# Get main record from SNAC
	print("\nRetrieving main constellation from SNAC...")
	mainConstellation = retrieveSnacAgent(mainID)
	print("Main constellation retrieved.\n\n")

	# Extract list of related constellation ids from main record
	snacIds = [mainConstellation["id"]]
	for entry in mainConstellation["relations"]:
		# Get the constellation ID
		id = entry["targetConstellation"]
		# Add the ID to the list
		snacIds.append(id)
	# Remove duplicate IDs
	snacIds = list(set(snacIds))

	numRelated = len(snacIds)

	# Pull full JSONs of related constellations from SNAC into a list
	snacConstellations = [mainConstellation] # Initialize list
	print("Fetching {} related constellations from SNAC...".format(numRelated))
	for i in range(numRelated): # Loop over list of IDs
		# Print relevant message
		print("\rFetching constellation {}...".format(i+1), end="")
		# Get relevant ID
		id = snacIds[i]
		# Get constellation via API request
		relConstellation = retrieveSnacAgent(id)
		# Add retrieved constellation to list of constellations
		snacConstellations.append(relConstellation)

	print("\nRetrieved all constellations\n\n")

	return snacConstellations

def writeJsons(jsons):
	"""
	Given a list of JSON objects, write each one to a separate file

	Param: jsons, a list of JSON objects represented as Python dicts
	"""
	print("Writing {} JSON objects to file...".format(len(jsons)))

	# Loop over JSONs
	for item in jsons:
		# Create filename
		directory = "snac_jsons/"
		entName = item["id"]
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

def convertSnacToEac(snacConstellations):
	"""
	Converts a set of SNAC constellations into a set of EAC-CPF XML objects

	Param: snacConstellations, a list of SNAC agent JSONs in dict form
	Returns: eacs, a list of XML objects conforming to the EAC-CPF standard
	"""
	print("Converting SNAC constellations to EAC records...")
	# Initialize a set of EACs
	eacs = []

	i = 0
	for json in snacConstellations:
		# Print a status message
		i += 1
		name = json["nameEntries"][0]["original"]
		if len(name) > 32:
			name = name[:32]
		print("\rConverting constellation {} ({:50})...".format(i,name),end="")

		# Do the conversion work
		eacTemplate = initializeEACCPF()
		eacWithData = jsonToEacMigration(json, eacTemplate)
		eacs.append(eacWithData)

	print("\nConverted {} constellations.\n\n".format(len(eacs)))

	return eacs

def writeEACs(eacs):
	"""
	Given a list of EAC object, write each one to a separate file

	Param: eacs, a list of XML objects conforming to the EAC standard
	"""

	print("Writing {} EAC objects to file...".format(len(eacs)))
	eacs.sort(key = extractName) # Sort the list so the output looks nice
	# Loop over the EACs, performing the same operations on each one
	for eac in eacs:
		# Create filename
		directory = "eacsForAspace/"
		entName = extractName(eac) # Get the entity's name from the EAC
		entName = entName.replace(" ", "") # Strip spaces
		entName = entName.replace(",", "") # Strip commas
		if len(entName) > 128:
			entName = entName[:127] # Impose length limit on file names
		filename = directory+entName+".xml"

		while '..' in filename:
			filename = filename.replace('..', '.')

		# Write file
		print("Writing {:45}".format(filename[14:] + "..."), end="")
		writeXML(eac, filename)
		print(" Done.")

	print("\nAll EACs successfully written.\n\n")

def extractName(eac):
	"""
	Extract the contents of <cpfDescription><identity><nameEntry><part>

	Params: eac, an XML object conforming to the EAC standard
	"""
	for part in eac.iter("part"):
		return part.text

def main():
	huntID = 85290808

	# Get data on agents from SNAC in JSON form
	snacConstellations = getRelatedSnacAgents(huntID)

	# Write SNAC jsons to files
	writeJsons(snacConstellations)

	# Convert JSON constellations to EAC format
	#eacs = convertSnacToEac(snacConstellations)

	# Write EAC objects to individual files
	#writeEACs(eacs)

	# TODO: Write JSONs to files
	# (avoids need to requery SNAC for next step of import)


if __name__ == '__main__':
    main()
