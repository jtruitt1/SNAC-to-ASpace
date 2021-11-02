"""
Written by James Truitt of Swarthmore College's Friends Historical Library,
November 2021.
"""

import requests, json, argparse, secret

from snacUtils import Relationship, loadRelationsFromFile, apiError

def getUserInput():
	"""
	Ask the user whether to use the production server or the development server.

	@returns: True if we're using the production server, False otherwise
	"""
	# Define valid user responses
	affirmative = ["y", "yes", "ye", "true"]
	negative = ["n", "no", "false"]

	# Print a message
	msg = "\nWhat server do we want to make changes to?\n"
	msg += "If we're really sure this will work, we can write to the "
	msg += "production server.\n"
	msg += "Otherwise, we should write to the development server.\n"
	print(msg)

	# Loop until we get either an affirmative or a negative answer
	while True:

		# Get user input
		answer = input("Write to production server? Y/N\t").lower()

		# If user says they want to write to production server:
		if answer in affirmative:

			# Double check that they really mean it
			print("\nChanges to the production server can't be easily undone.")
			msg = "Are you still sure you want to write to "
			msg += "the production server?\t"
			answer = input(msg)

			if answer in affirmative:
				print("Production server it is then.")
				return True

			elif answer in negative:
				print("Change of plans noted.")
				print("Development server it is then.")
				return False

			else:
				msg = "Sorry, not sure what that means. "
				msg+= "Let's start again from the top.\n"
				print(msg)

		elif answer in negative:
			print("Development server it is then.")
			return False

		else:
			print("Sorry, not sure what that means. Let's try again.\n")

def convertToJson(relation):
	"""
	Turn a Relationship object into the corresponding SNAC JSON, in dict form
	"""
	# print("in convertToJson")

	dict = {
		"operation": "insert",
		"dataType": "ConstellationRelation",
		"sourceConstellation": relation.source,
		"targetConstellation": relation.target,
		"type": {
			"id": relation.getTypeId(),
			"term": relation.type,
			"type": "relation_type"
		}
	}

	return dict

def splitBySource(relationList):
	"""
	Organize a list of relationships by their sources.

	Given a list of SNAC relationship JSONs in dict form, return a dict of form
	{source1: [Rel1 w/ s1, Rel 2 w/ s1, …], s2: [Rel1 w/ s2, Rel2 w/ s2, …], …}
	"""
	# print("in splitBySource")

	# Initialize dict to return
	sourceList = {}

	for link in relationList:
		source = link.source
		if source not in sourceList:
			sourceList[source] = [link]
		else:
			sourceList[source].append(link)

	return sourceList

def postToApi(data, baseUrl):
	"""
	Make a POST call to a REST API and return the response

	@param: data, dict, JSON data to be passed in the call
	@param: baseUrl, str, the URL of the API to call
	@return the API response in dict form
	"""
	data = json.dumps(data) # Turn the dictionary into JSON
	r = requests.put(baseUrl, data = data) # MAKE THE API REQUEST!!!!!
	response = json.loads(r.text) # Turn the response from JSON into a dict
	return response

def checkOutConstellation(snacID, apiKey, baseUrl):
	"""
	Check a constellation out of SNAC to allow further edits.

	Side effects: Tries to change data on the dev or prod SNAC server

	For more details on the SNAC API and this command, see:
		https://github.com/snac-cooperative/Rest-API-Examples/blob/master/modification/json_examples/add_resource_and_relation.md
		https://snac-dev.iath.virginia.edu/api_help#edit

	@param: snacID, int, SNAC ID of the constellation to update
	@param: apiKey, str, user API key to authenticate the request
	@param: baseUrl, str, the URL of the SNAC REST API to call (dev vs. prod)
	@return: response, the server's response to the API call
	"""
	req = {
	    "command": "edit",
	    "constellationid": snacID,
	    "apikey": apiKey
	}

	response = postToApi(req, baseUrl) # MAKE THE API CALL!!!!!!!

	return response

def buildMinimalConstellation(snacID, version, ark, relationships):
	"""
	Build a minimal constellation suitable for uploading modifications to SNAC

	@param: snacID, int, SNAC ID of the constellation to update
	@param: version, str, the version number of the constellation to update
	@param: ark, str, the full ark ID url starting w/ ""http://n2t.net/ark:/"
	@return: a JSON object in dict form
	"""
	# Create constellation from arguments
	constellation = {
		"dataType": "Constellation",
        "ark": ark,
        "id": snacID,
        "version": version,
		"relations": relationships
	}

	return constellation

def pushChangesToSnac(miniConst, apiKey, baseUrl):
	"""
	Make changes to a SNAC constellation that a user has already checked out

	Side effects: Tries to change data on the dev or prod SNAC server

	For more details on the SNAC API and this command, see:
		https://github.com/snac-cooperative/Rest-API-Examples/blob/master/modification/json_examples/add_resource_and_relation.md
		https://snac-dev.iath.virginia.edu/api_help#update_constellation

	@param: miniConst, a barebones constellation in dict form
		Ex of barebones requirements: {
			"dataType": "Constellation",
			"ark": "http://n2t.net/ark:/99166/[…]",
			"id": […],
			"version": "[…]",
			[material to insert, tagged w/ "operation": "insert"]
			}
	@param: apiKey, str, user API key to authenticate the request
	@param: baseUrl, str, the URL of the SNAC REST API to call (dev vs. prod)
	@return: response, the server's response to the API call
	"""

	req = {
	"command": "update_constellation",
	"constellation": miniConst,
	"apikey": apiKey
	}

	response = postToApi(req, baseUrl)

	return response

def publish_constellation(miniConst, apiKey, baseUrl):
	"""
	Publish a constellation checked out to a user

	Side effects: Tries to change data on the dev or prod SNAC server

	For more details on the SNAC API and this command, see:
		https://github.com/snac-cooperative/Rest-API-Examples/blob/master/modification/json_examples/add_resource_and_relation.md
		https://snac-dev.iath.virginia.edu/api_help#publish_constellation

	@param: miniConst, the constellatn returned by pushing changes, in dict form
	@param: apiKey, str, user API key to authenticate the request
	@param: baseUrl, str, the URL of the SNAC REST API to call (dev vs. prod)
	@return: response, the server's response to the API call
	"""
	req = {
	"command": "publish_constellation",
	"constellation": miniConst,
	"apikey": apiKey
	}

	response = postToApi(req, baseUrl)

	return response

def verifyApiSuccess(response):
	"""Raise an apiError if the API response passed as a param is an error"""
	if "error" in response:
		try:
			type = response["error"]["type"]
			message = response["error"]["message"]
			raise apiError(type + ": " + message)
		except TypeError:
			print(response)
			raise apiError("Seems like one of the weird ones")

def insertRelations(snacID, apiKey, relationships, production = False):
	"""
	Add CPF relationships to a SNAC constellation by making several API calls.

	See here for walk-through example of how API calls work:
	https://github.com/snac-cooperative/Rest-API-Examples/blob/master/modification/json_examples/add_resource_and_relation.md

	Accesses the Development server by default.

	@param: snacID, int, SNAC ID of the constellation to update
	@param: apiKey, str, user API key to authenticate the modifications
	@param: relationships, list of Relationship objects
	@param: production, bool, whether to use production or development server
	"""
	# print("in insertRelations")
	##### Validate & process arguments #######

	## Validate arguments ##

	# Make sure SNAC ID is a positive int; raise error if unable to make it one
	if isinstance(snacID, str):
		try:
			snacID = int(snacID)
		except ValueError:
			print("Error with the following Source ID:", snacID)
			print("Source Constellation ID must be a positive integer")
			print("No relations with this source could be added")
			return None

	if isinstance(snacID, int):
		if snacID <= 1:
			print("Error with the following Source ID:", snacID)
			print("Source Constellation ID must be a positive integer")
			print("No relations with this source could be added")
			return None
	else:
		print("Error with the following Source ID:", snacID)
		print("Source Constellation ID must be a positive integer")
		print("No relations with this source could be added")
		return None

	# Validate API key
	if not isinstance(apiKey, str):
		print("Error: API key must be a string.")
		raise KeyboardInterrupt

	# Set appropriate URL
	if production == True:
		baseUrl = "https://api.snaccooperative.org"
	else:
		baseUrl = "http://snac-dev.iath.virginia.edu/api/"


	##### Make API calls #####

	# Make API call to check out constellation using "edit" command
	response = checkOutConstellation(snacID, apiKey, baseUrl)

	# Verify that API call worked; raise an apiError if API call failed
	try:
		verifyApiSuccess(response)
	except apiError as e:
		msg = "\nCould not check out " + str(snacID)
		msg += " due to the following error:\n" + e.message
		raise apiError(msg)

	# Save the ark, id, and version from the response
	response = response["constellation"]
	id = response["id"]
	version = response["version"]
	ark = response["ark"]

	# Convert each relationship object into a dict representing SNAC JSON form
	for i in range(len(relationships)):
		relationships[i] = convertToJson(relationships[i])

	# Use those attributes to build a minimal constellation JSON that includes
	# the information we want to add, & the OPERATION attr (see walkthrough)
	miniConst = buildMinimalConstellation(id, version, ark, relationships)

	# Make API call to push our changes, using "update_constellation" command
	response = pushChangesToSnac(miniConst, apiKey, baseUrl)

	# Verify that last API call worked; raise an apiError if not
	try:
		verifyApiSuccess(response)
	except apiError as e:
		msg = "\nCould not update " + str(snacID)
		msg += " due to the following error:\n" + e.message
		raise apiError(msg)

	# Get miniConst from response to update command
	miniConst = response["constellation"]

	# Make API call to publish constellation using "publish_constellation" command
	response = publish_constellation(miniConst, apiKey, baseUrl)

	# Check to see if command succeeded
	try:
		verifyApiSuccess(response)
	except apiError as e:
		msg = "\nCould not publish " + str(snacID)
		msg += " due to the following error:\n" + e.message
		raise apiError(msg)

def main():
	print("")

	# Unpack argument to get name of tsv file
	parser = argparse.ArgumentParser()
	msg = "TSV file with 3 columns (source, type, & target)"
	parser.add_argument("filename", help=msg)
	args = parser.parse_args()
	filename = args.filename

	# Load relationship data from a TSV file into a list of Relationship objs
	relationList = loadRelationsFromFile(filename)

	# Group relationships by source (i.e., by agent to modify)
	sourceList = splitBySource(relationList)

	# Ask user which server we should use, development or production
	useProduction = getUserInput()

	# Take appropriate actions based on user response
	if useProduction == True:
		apiKey = secret.prodKey # Set appropriate API key
		prod = True # Set parameter to be passed to insertRelations

	else:
		apiKey = secret.devKey # Set appropriate API key
		prod = False # Set parameter to be passed to insertRelations

	# Print a message
	relCount = len(relationList)
	srcCount = len(sourceList)
	print("\nAdding", relCount, "relations to", srcCount, "constellations...")

	# Declare variables to track successes & failures of API calls
	successCount = 0
	errors = []

	# Make the API calls
	for i in range(srcCount):
		print("Updating constellation", i+1, "...", end="\r")

		agent = list(sourceList)[i]
		try:
			insertRelations(agent, apiKey, sourceList[agent], production=prod)
			successCount += 1

		# If there's an API error, log it and move on to next constellation
		except apiError as e:
			errors.append(e)
			continue

	# Print message
	print("\nSuccessfully updated", successCount, "constellations.")

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

main()