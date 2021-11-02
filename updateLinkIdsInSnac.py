"""
Written by James Truitt of Swarthmore College's Friends Historical Library,
November 2021.
"""

import re, json, requests, secret
from glob import glob
from utils import loadIdsToUpdate, apiError, postToApi, verifyApiSuccess

import re, json, requests, secret

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
		snacId = json.loads(filedata)["id"]

		# Loop over the outdated IDs, seeing if any are in this record
		for list in idsToUpdate:
			outdatedId = list[0]

			# If one of the outdated IDs is in this record,
			if outdatedId in filedata:

				# Add record's ID (if needed) to the dict we're compiling
				if snacId not in recordsToUpdate:
					recordsToUpdate[snacId] = []

				# Append the outdated ID to this record's dict entry
				recordsToUpdate[snacId].append(outdatedId)

	print(recordsToUpdate)
	return recordsToUpdate

	print("\nSuccessfully updated files.\n")

def main():
	print()

	# Load identifier data from tsv file
	idsToUpdate = loadIdsToUpdate()

	# Get list of which constellations to edit & which changes to make
	updatesToMake = compileEditList(idsToUpdate)



if __name__ == "__main__":
	main()
