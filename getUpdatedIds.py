"""
Given a folder of SNAC constellations in JSON form ("snac_jsons"),
find all of the identifiers they use. Create a list of out-of-date IDs
(SNAC IDs and Arks) coupled with their updated forms (using API calls), and
write them to a TSV named "idsToUpdate.tsv" of the form ID, Ark, new ID, new Ark

Written by James Truitt of Swarthmore College's Friends Historical Library,
November 2021.
"""

import re, json, requests, secret
from glob import glob
from utils import loadSnacData, apiError, postToApi, verifyApiSuccess, apiError

import re, json, requests


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
	Compile list of outdated identifiers paired with their current forms

	Makes API calls to check if an identifier is up-to-date. (SNAC REST API,
	when given an outdated identifier, will return the correct constellation,
	but with the current identifiers). Assumes that SNAC ID and Ark can't
	change independently, i.e., that if one has changed, the other must have
	also changed.

	@param: identifiers, dict w/ SNAC ids as keys & corresp Arks as values
	@returns: list of lists, each of the form [oldId, newId, oldArk, newArk]
	"""
	print("Checking that identifiers are up to date...")
	# Initialize the list of lists we're going to return
	idsToUpdate = []

	# Loop over identifiers
	counter = 0	# Keep track of how many identifiers we've checked
	for currentId in identifiers:
		# To keep preliminary testing quick:
		# if counter > 4: break

		# Print helpful message:
		counter += 1
		print("Checking identifier", counter, "...", end="\r")

		# Make API call using identifier
		req = {"command": "read", "constellationid": currentId}
		response = postToApi(req, "https://api.snaccooperative.org/")

		# Raise an error if API call failed
		verifyApiSuccess(response)

		# Get constellation from API response
		constellation = response["constellation"]

		# Check identifiers from constellation against current ones
		if constellation["id"] != currentId:
			# If they don't match, add old & new SNAC Ids & Arks to the list
			newEntry = [
				currentId, 				# Outdated ID
				constellation["id"],	# Updated ID
				identifiers[currentId],	# Outdated Ark
				constellation["ark"]	# Updated Ark
			]
			idsToUpdate.append(newEntry)


	print("\nChecked identifiers. Found ", len(idsToUpdate), "out of date.\n")
	return idsToUpdate

def writeDataToFile(idsToUpdate):
	"""
	Write a list of lists to a .tsv file
	"""
	# Skip this step if there are no ids to update
	if len(idsToUpdate) == 0:
		return None

	filename = "idsToUpdate.tsv"
	header = "\t".join(["Old ID", "New ID", "Old Ark", "New Ark\n"])
	rowsAsStrings = ["\t".join(idsToUpdate[i]) for i in range(len(idsToUpdate))]
	body = "\n".join(rowsAsStrings)

	print("Writing identifiers to", filename, "...")

	with open(filename, "w") as f:
		f.write(header)
		f.write(body)

	print("Data written successfully.\n")

def main():
	print()

	# Load constellation data from JSON files
	constellations = loadSnacData()

	# Compile list of unique target SNAC IDs & Arks
	identifiers = getUniqueIdentifiers(constellations)

	# Compile dicts of old IDs & Arks keyed to the updated versions
	# (Use the API to read every ID & see if what's returned matches)
	idsToUpdate = verifyIdsAreCurrent(identifiers)

	# Write identifiers to a TSV
	writeDataToFile(idsToUpdate)


if __name__ == "__main__":
	main()
