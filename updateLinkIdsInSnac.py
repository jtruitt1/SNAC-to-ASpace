"""
Update outdated target IDs in constellation relationships on SNAC.

Written by James Truitt of Swarthmore College's Friends Historical Library,
November 2021.
"""

import json, requests, secret
from glob import glob
from utils import loadIdsToUpdate, apiError, postToApi, verifyApiSuccess
from apiEditUtils import checkOutConstellation, publishConstellation
from apiEditUtils import getUserInput, pushChangesToSnac

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
			allSnacIds.append(updateDict[snacID][oldId]["newId"])
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
		for entry in updateDict[record]:
			newArk = updateDict[record][entry]["newArk"]
			if newArk[:-8] != "http://n2t.net/ark:/99166/":
				# TODO: Remove the following line of debugging code
				if newArk != "http://snaccooperative.org/ark:/99999/ZGJ5mc63":
					raise Exception("Error: invalid ark: " + newArk)

def buildMinimalUpdateConstellation(constellation, updateDict):
	"""
	Build a minimal constellation suitable for uploading modifications to SNAC

	This function takes a full constellation and a list of changes, and returns
	a barebones constellation containing the relations to be updated with the
	"operation" key set to "update".

	@param: constellation, dict, a SNAC constellation JSON
	@param: updateDict, dict w/ entries oldID: {"newId":newId, "newArk":newArk}
	@return: a SNAC constellation JSON object in dict form
	"""
	# Create constellation with basic data
	miniConst = {
		"dataType": "Constellation",
        "ark": constellation["ark"],
        "id": constellation["id"],
        "version": constellation["version"],
		"relations": []
	}

	# Add relationships that need to be updated:

	# Loop over relationships in the full constellation,
	for relation in constellation["relations"]:

		# checking their targets against the list of outdated identifiers
		for outdatedId in updateDict:
			if outdatedId == relation["targetConstellation"]:
				# On a match,

				# Update the relationship's target SNAC ID & Ark ID
				newId = updateDict[outdatedId]["newId"]
				newArk = updateDict[outdatedId]["newArk"]
				relation["targetConstellation"] = newId
				relation["targetArkID"] = newArk

				# Add "operation": "update" to the relationship
				relation["operation"] = "update"

				# Add the relation to the miniConst
				miniConst["relations"].append(relation)

				# Move on to the next relationship in the constellation
				break

	return miniConst

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
	# Validate arguments
	validateIdentifiers(updateDict)
	if not isinstance(apiKey, str):
		raise Exception("Error: API key must be a string.")

		return None

	# Set appropriate URL
	if production == True:
		baseUrl = "https://api.snaccooperative.org"
	else:
		baseUrl = "http://snac-dev.iath.virginia.edu/api/"

	# Declare variables to track successes & failures of API calls
	successCount = 0
	errors = []

	# Loop over constellations to modify, making those API calls
	counter = 0
	for snacID in updateDict:
		counter += 1

		# For limiting scope of test runs
		# if counter > 3:
		# 	break

		try:
			# Print status message
			print("Updating constellation", counter, "...", end="\r")

			# Get list of updates to be made
			updates = updateDict[snacID]

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
			miniConst = buildMinimalUpdateConstellation(constellation, updates)

			# Make API call to push changes to SNAC using "update_constellation"
			response = pushChangesToSnac(miniConst, apiKey, baseUrl)

			# Verify that API call worked; raise and apiError if it failed
			try:
				verifyApiSuccess(response)
			except apiError as e:
				msg = "\nCould not update " + str(snacID)
				msg += " due to the following error:\n" + e.message
				raise apiError(msg)

			# Get miniConst from response to update command
			miniConst = response["constellation"]

			# Make API call to publish constellation, using "publish_constellation"
			response = publishConstellation(miniConst, apiKey, baseUrl)

			# Verify that API call worked; raise and apiError if it failed
			try:
				verifyApiSuccess(response)
			except apiError as e:
				msg = "\nCould not update " + str(snacID)
				msg += " due to the following error:\n" + e.message
				raise apiError(msg)

			# Note that modifications to this constellation have succeeded.
			successCount += 1

		# If there's an API error, log it and move on to next constellation
		except apiError as e:
			errors.append(e)
			continue
		except Exception as e:
			print("\nFatal error encountered on constellation", snacID)
			raise e

	# Print message
	print("Successfully updated", successCount, "constellations.")

	# Print list of API errors encountered
	numErrors = len(errors)
	if numErrors > 0:
		if numErrors == 1:
			print("Encountered 1 error:")
		else:
			print("Encountered", numErrors, "errors:")
		for error in errors:
			print(error)

	print("")

def main():
	print()


	# Get user input about which server to use
	production = getUserInput()

	# Set API Key, based on which server we're uploading to
	if production:
		apiKey = secret.prodKey
	else:
		apiKey = secret.devKey

	# Load identifier data from tsv file
	idsToUpdate = loadIdsToUpdate()

	# Reformat identifier data into a dict
	idsToUpdate = makeDict(idsToUpdate)

	# Get list of which constellations to edit & which changes to make
	updatesToMake = compileEditList(idsToUpdate)

	# Make API calls to update constellations in SNAC
	makeUpdates(updatesToMake, apiKey, production = production)


if __name__ == "__main__":
	main()
