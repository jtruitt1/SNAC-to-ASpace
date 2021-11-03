"""
Written by James Truitt of Swarthmore College's Friends Historical Library,
November 2021.
"""

import re, json, requests, secret
from glob import glob
from utils import loadIdsToUpdate, apiError, postToApi, verifyApiSuccess
from apiEditUtils import checkOutConstellation, publishConstellation
from apiEditUtils import getUserInput

def makeDict(listOfLists):
	"""
	# TODO: add docstring
	"""
	print("In makeDict")
	return {"1234":["this","isn't","done"], "5678":["still","not","done"]}

def compileEditList(idsToUpdate):
	"""
	# TODO: Add doc string
	"""
	# TODO: Print status message

	# Get list of filenames to read
	filenames = glob("snac_jsons/*.json")

	# Initialize the dict we'll return
	recordsToUpdate = {}

	# Loop over JSON files
	for filename in filenames:

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
					recordsToUpdate[snacID] = []

				# Append the outdated ID to this record's dict entry
				recordsToUpdate[snacID].append(outdatedId)

	return recordsToUpdate

	print("\nSuccessfully updated files.\n")

def makeUpdates(updateDict, apiKey, production = False):
	"""
	# TODO: add docstring
	"""
	print("In makeUpdates")

	# TODO: print message

	for constellation in updateDict:
		# Make API call to check out constellation

		# Loop over identifiers to be updated in the constellation
		for snacID in updateDict[constellation]:
			editConstellation()

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
