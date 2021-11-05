"""
Utility functions useful when making changes to data in SNAC. Most require a
valid API key to work.

Written by James Truitt at the Friends Historical Library of Swarthmore College,
November 2021.
"""

from utils import postToApi, apiError

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
			[material to add/change, tagged "operation": "insert"/"update"]
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

def publishConstellation(miniConst, apiKey, baseUrl):
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
