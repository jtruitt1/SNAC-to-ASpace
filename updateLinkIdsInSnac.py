"""
Update outdated target IDs in constellation relationships on SNAC.

Written by James Truitt of Swarthmore College's Friends Historical Library,
November 2021.
"""

import json, requests, secret
from glob import glob
from utils import loadIdsToUpdate, apiError, postToApi, verifyApiSuccess
from apiEditUtils import checkOutConstellation, publishConstellation
from apiEditUtils import getUserInput

def makeDict(listOfLists):
	"""
	Convert a list of lists ([[A,B,C,D]]) into a dict ({A:{newId:B, newArk:D}})
	"""
	# Print status message
	print("Formatting loaded data...")

	# Initialize the dict we'll eventually return
	updateDict = {}

	for list in listOfLists:
		oldId, newId, newArk = list[0], list[1], list[3]
		updateDict[oldId] = {"newId": newId, "newArk": newArk}

	print("Data successfully formatted.\n")

	return updateDict

def compileEditList(idsToUpdate):
	"""
	Find out what SNAC constellations need to be updated & what edits they need.

	Check JSON files containing constellation data against a dict whose keys
	are outdated identifiers.

	@param: idsToUpdate, a dict w/ entries of the form
		outdatedId: {"newId":newId, "newArk":newArk}
	@return: a dict w/ entries of the form
		constellationToBeUpdatedID: {
			outdatedId1: {"newId":newId1, "newArk":newArk1},
			...
			outdatedIdN: {"newId":newIdN, "newArk":newArkN}}
	"""

	# Get list of filenames to read
	filenames = glob("snac_jsons/*.json")

	# Initialize the dict we'll return
	recordsToUpdate = {}

	# Print status message
	print("Checking", len(filenames), "constellations for outdated IDs...")

	# Loop over JSON files
	i = 0
	for filename in filenames:

		# Print status message
		i += 1
		short = filename.split("/").pop()
		print("Checking constellation {:3d}, id {:9}...".format(i, short),
			end="\r")

		# Read the file's data into a string
		with open(filename) as f:
			filedata = f.read()

		# Extract the record's SNAC ID, for the API call later
		snacID = json.loads(filedata)["id"]

		# Loop over the outdated IDs, seeing if any are in this record
		for outdatedId in idsToUpdate:

			# If one of the outdated IDs is in this record,
			if "\"" + outdatedId + "\"" in filedata:

				# Add record's ID (if needed) to the dict we're compiling
				if snacID not in recordsToUpdate:
					recordsToUpdate[snacID] = {}

				# Add outdated ID (& current IDs) to record's dict entry
				# {snacID: {outdatedId: idsToUpdate[outdatedId]}}
				recordsToUpdate[snacID][outdatedId] = idsToUpdate[outdatedId]

	print("Successfully compiled list of constellations to update.\n")
	return recordsToUpdate

	print("\nSuccessfully updated files.\n")

def validateIdentifiers(updateDict):
	"""Ensures all SNAC IDs and Arks in the dictionary are well-formed"""
	# Check snac IDs
	allSnacIds = []
	for snacID in updateDict:
		allSnacIds.append(snacID)
		for oldId in updateDict[snacID]:
			allSnacIds.append(oldId)
			allSnacIds.append(updateDict[snacID][oldID]["newId"])
	for snacID in allSnacIds:
			if isinstance(snacID, str):
				try:
					snacID = int(snacID)
				except ValueError:
					print("Error with the following Constellation ID:", snacID)
					print("Constellation ID must be a positive integer")
					return None

			if isinstance(snacID, int):
				if snacID <= 1:
					print("Error with the following Constellation ID:", snacID)
					print("Constellation ID must be a positive integer")
					return None
			else:
				print("Error with the following Constellation ID:", snacID)
				print("Constellation ID must be a positive integer")
				return None

	# Check all Arks
	for record in updateDict:
		for entry in record:
			newArk = updateDict[record][entry]["newArk"]
			if newArk[:-8] != "https://snaccooperative.org/ark:/99166/":
				raise Exception("Error: invalid ark: " + newArk)

def updateConstellation(updateDict):
	"""
	# TODO: Add doc string
	"""
	pass

def makeUpdates(updateDict, apiKey, production = False):
	"""
	Update outdated target IDs in constellation relationships on SNAC.

	Make several API calls per constellation that needs to be updated.
	Accesses SNAC's development server by default.


	See here for walk-through example of how API calls work:
	https://github.com/snac-cooperative/Rest-API-Examples/blob/master/modification/json_examples/add_resource_and_relation.md

	@param: updateDict, dict, data to update (see compileEditList for format)
	@param: apiKey, str, user API key to authenticate the modifications
	@param: production, bool, whether to use production or development server
	"""
	print("Making changes to", len(updateDict), "constellations...")
	return None

	# Validate arguments
	validateIdentifiers(updateDict)
	if not isinstance(apiKey, str):
		raise Exception("Error: API key must be a string.")

	# Set appropriate URL
	if production == True:
		baseUrl = "https://api.snaccooperative.org"
	else:
		baseUrl = "http://snac-dev.iath.virginia.edu/api/"

	return None

	# Loop over constellations to modify, making those API calls
	for snacID in updateDict:

		# Make API call to check out constellation
		response = checkOutConstellation(snacID, apiKey, baseUrl)

		# Verify that API call worked; raise an apiError if API call failed
		try:
			verifyApiSuccess(response)
		except apiError as e:
			msg = "\nCould not check out " + str(snacID)
			msg += " due to the following error:\n" + e.message
			raise apiError(msg)

		# Make needed changes to constellation returned by API
		constellation = response["constellation"]

		# Make API call to push those changes to SNAC

		# Verify that API call worked; raise and apiError if it failed

		# Make API call to publish constellation, using "publish_constellation"



def main():
	print()

	# Get user input about which server to use
	# TODO: borrow code from addRelations (or better, add util)
	apiKey = secret.devKey

	# Load identifier data from tsv file
	idsToUpdate = loadIdsToUpdate()

	# Reformat identifier data into a dict
	idsToUpdate = makeDict(idsToUpdate)

	# Get list of which constellations to edit & which changes to make
	updatesToMake = compileEditList(idsToUpdate)

	# Make API calls to update constellations in SNAC
	makeUpdates(updatesToMake, apiKey)


if __name__ == "__main__":
	main()
