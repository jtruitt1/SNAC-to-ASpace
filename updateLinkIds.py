import re, json, requests
from glob import glob
from utils import loadSnacData, apiError, postToApi, verifyApiSuccess

def getUniqueIdentifiers(constellations):
	"""
	Extract unique SNAC IDs & Arks (full url) from a list of SNAC constellations

	@param: constellations, a list of SNAC constellations in Dict form
	returns: a dict of unique SNAC IDs & Arks of the form {ID: Ark}
	"""
	length = len(constellations)
	print("Aggregating identifiers from", length, "constellations")

	# Initialize the container for all the ids & arks we find
	identifiers = {}

	# Loop over constellations
	for i in range(len(constellations)):
		constellation = constellations[i]

		# Print helpful message
		print("Processing constellation", i+1, "...", end="\r")

		# Add the constellation's id and ark to our container
		identifiers[constellation["id"]] = constellation["ark"]

		# To avoid errors, double-check that const has relations (it should)
		if "relations" in constellation:
			if len(constellation["relations"]) > 0:

				# Loop over relations, adding any new targets to our dict
				for relation in constellation["relations"]:
					targetId = relation["targetConstellation"]
					if targetId not in identifiers:
						identifiers[targetId] = relation["targetArkID"]

	print("\nSuccessfully aggregated", len(identifiers), "identifiers.\n")
	return identifiers

def verifyIdsAreCurrent(identifiers):
	"""
	Compile dict of outdated identifiers paired with their current forms

	Makes API calls to check if an identifier is up-to-date. (SNAC REST API,
	when given an outdated identifier, will return the correct constellation,
	but with the current identifiers). Assumes that SNAC ID and Ark can't
	change independently, i.e., that if one has changed, the other must have
	also changed.

	@param: identifiers, dict w/ SNAC ids as keys & corresp Arks as values
	@returns: a list of 2 dicts: {oldId:NewId} and {oldArk:newArk}
	"""
	print("Checking that identifiers are up to date...")
	# Initialize the dicts we're going to return
	idsToUpdate = {}
	arksToUpdate = {}

	# Loop over identifiers
	counter = 0	# Keep track of how many identifiers we've checked
	for id in identifiers:
		# To keep preliminary testing quick:
		# if counter > 99: break

		# Print helpful message:
		counter += 1
		print("Checking identifier", counter, "...", end="\r")

		# Make API call using identifier
		req = {"command": "read", "constellationid": id}
		response = postToApi(req, "https://api.snaccooperative.org/")

		# Raise an error if API call failed
		verifyApiSuccess(response)

		# Get constellation from API response
		constellation = response["constellation"]

		# Check identifiers from constellation against current ones
		if constellation["id"] != id:
			# If they don't match, add old & new SNAC Ids & Arks to our dicts
			idsToUpdate[id] = constellation["id"]
			ark = identifiers[id]
			arksToUpdate[ark] = constellation["ark"]

			# print(id, constellation["id"]) # For debugging purposes


	print("\nChecked identifiers. Found ", len(idsToUpdate), "out of date.\n")
	return [idsToUpdate, arksToUpdate]

def updateDataInFiles(idsToUpdate, arksToUpdate):
	"""Find and replace old identifiers across the files in snac_jsons folder"""
	# Do nothing if there are no identifiers to update
	if len(idsToUpdate) == 0:
		return None

	# Get list of filenames to edit
	filenames = glob("snac_jsons/*.json")

	# Print a helpful message
	print("Updating identifiers across", len(filenames), "files...")

	# Loop over the files, reading data from them, making changes, then writing
	# (Leave the JSON as strings, don't unpack it into dicts)
	counter = 0 # Keep track of how many files we've worked with
	for filename in filenames:
		# Print helpful message
		counter += 1
		print("Updating", filename, "(file", str(counter) + ")...\t", end="\r")

		# Read data from file
		with open(filename, "r") as f:
			filedata = f.read()

		# Loop over identifiers to update
		# Replacing each one in the JSON with the newer version
		for id in idsToUpdate:
			# Find SNAC ID in quotes to avoid replacing portions of longer IDs
			# (because SNAC IDs vary in length)
			quotedId = "\"" + id + "\""
			if quotedId in filedata:
				newQuotedId = "\"" + idsToUpdate[id] + "\""
				filedata = filedata.replace(quotedId, newQuotedId) #Replacement
		for ark in arksToUpdate:
			if ark in filedata:
				filedata = filedata.replace(ark, arksToUpdate[ark]) #Replacement

		# Write data back to file
		with open(filename, "w") as f:
			f.write(filedata)

	print("\nSuccessfully updated files.\n")

def main():
	print()

	# Load constellation data from JSON files
	constellations = loadSnacData()

	# Compile list of unique target SNAC IDs & Arks
	identifiers = getUniqueIdentifiers(constellations)

	# Compile dicts of old IDs & Arks keyed to the updated versions
	# (Use the API to read every ID & see if what's returned matches)
	newIdsAndArks = verifyIdsAreCurrent(identifiers)
	idsToUpdate, arksToUpdate = newIdsAndArks[0], newIdsAndArks[1]


	# Find-and-replace the IDs and Arks across the JSON files
	updateDataInFiles(idsToUpdate, arksToUpdate)


if __name__ == "__main__":
	main()
else:
	ids= {"85290808":"Haha you FOOLS!"}
	arks = {"http://n2t.net/ark:/99166/w6n9820p": "Try again! Ahaha"}
	updateDataInFiles(ids, arks)
