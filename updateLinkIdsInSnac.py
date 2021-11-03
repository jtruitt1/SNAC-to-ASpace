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
			outdatedIdN: {"newId":newIdN, "newArk":newArkN}
		}
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

def updateConstellation(updateDict):
	"""
	# TODO: Add doc string
	"""
	pass

def makeUpdates(updateDict, apiKey, production = False):
	"""
	# TODO: add docstring
	"""
	print("In makeUpdates")

	# TODO: print message
	pass
	for constellation in updateDict:
		# Make API call to check out constellation
		response = checkOutConstellation()

		# Loop over identifiers to be updated in the constellation
		for snacID in updateDict[constellation]:
			updateConstellation(updateDict, 3, 7)

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

	return None


if __name__ == "__main__":
	main()
