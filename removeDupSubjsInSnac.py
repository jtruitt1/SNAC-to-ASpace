"""
Remove duplicate subjects from constellations on SNAC.

Written by James Truitt of Swarthmore College's Friends Historical Library,
July 2022.
"""

import json, requests, secret
from utils import loadSnacData, apiError, postToApi, verifyApiSuccess
from apiEditUtils import checkOutConstellation, publishConstellation
from apiEditUtils import getUserInput, pushChangesToSnac

def compileEditList(constellations):
	"""
	Find out what SNAC constellations need to be updated & what edits they need.

	Check JSON files containing constellation data for duplicate subjects

	@param: constellations, a set of JSON-dicts containing SNAC data
	@return: a list of ids of constellations with duplicate subjects
	"""

	pass

def buildMinimalUpdateConstellation(constellation):
	"""
	Build a minimal constellation suitable for uploading modifications to SNAC

	This function takes a full constellation, checks it for duplicate subjects,
	and returns a barebones constellation containing the subjects to be deleted
	with the "operation" key set to "delete".

	@param: constellation, dict, a SNAC constellation JSON
	@return: a SNAC constellation JSON object in dict form
	"""
	# Create constellation with basic data
	miniConst = {
		"dataType": "Constellation",
        "ark": constellation["ark"],
        "id": constellation["id"],
        "version": constellation["version"],
		"subjects": []
	}

	# Add subjects that need to be deleted:

	# Loop over subjects in the full constellation,
	for subject in constellation["subjects"]:

		pass

	return miniConst

def makeUpdates(idList, apiKey, production = False):
	"""
	Remove duplicate subjects in constellations on SNAC.

	Make several API calls per constellation that needs to be updated.
	Accesses SNAC's development server by default.

	See here for walk-through example of how API calls work:
	https://github.com/snac-cooperative/Rest-API-Examples/blob/master/modification/json_examples/add_resource_and_relation.md

	@param: idList, list, ids of constellations with dup subjs to remove
	@param: apiKey, str, user API key to authenticate the modifications
	@param: production, bool, whether to use production or development server
	"""
	print("Making changes to", len(idList), "constellations...")
	# Validate arguments
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
	for snacID in idList:
		counter += 1

		# For limiting scope of test runs
		# if counter > 3:
		# 	break

		try:
			# Print status message
			print("Updating constellation", counter, "...", end="\r")

			##### CHECK OUT CONSTELLATIONS #####

			# Make API call to check out constellation
			response = checkOutConstellation(snacID, apiKey, baseUrl)

			# Verify that API call worked; raise an apiError if API call failed
			try:
				verifyApiSuccess(response)
			except apiError as e:
				msg = "\nCould not check out " + str(snacID)
				msg += " due to the following error:\n" + e.message
				raise apiError(msg)

			##### Make needed changes to constellation returned by API #####
			constellation = response["constellation"]
			miniConst = buildMinimalUpdateConstellation(constellation)

			##### PUSH CHANGES TO API #####

			# Make API call to push changes to SNAC using "update_constellation"
			response = pushChangesToSnac(miniConst, apiKey, baseUrl)

			# Verify that API call worked; raise and apiError if it failed
			try:
				verifyApiSuccess(response)
			except apiError as e:
				msg = "\nCould not update " + str(snacID)
				msg += " due to the following error:\n" + e.message
				raise apiError(msg)

			##### PUBLISH CHANGED CONSTELLATION ON SNAC #####

			# Get miniConst from the response to the update command
			miniConst = response["constellation"]


			# Make API call to publish, using "publish_constellation"
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
	devOrProd = getUserInput()

	# Set API Key, based on which server we're uploading to
	if production:
		apiKey = secret.prodKey
	else:
		apiKey = secret.devKey

	# Load constellation data
	constellations = loadSnacData()

	# Get list of which constellations to edit
	idsToEdit = compileEditList(constellations)

	# Make API calls to update constellations in SNAC
	makeUpdates(idsToEdit, apiKey, production = devOrProd)


if __name__ == "__main__":
	main()
