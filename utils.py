from glob import glob
import json, requests

class apiError(Exception):
	"""
	Exception raised when an API call fails to retrieve desired data.

	Attributes:
		type: error type, as given in the API response
		message: error message, as given in the API response
	"""
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return str(self.message)

def loadSnacData():
	"""
	Read SNAC JSON data from files in the snac_jsons folder.

	Returns: constellations, a list of SNAC JSONs in dict form
	"""
	# Get list of filenames to read
	filenames = glob("snac_jsons/*.json")

	# Initialize array of constellations to eventually return
	constellations = []

	# Loop over filenames, reading the files & adding the data to constellations
	print("Reading {} JSON files...".format(len(filenames)))
	for filename in filenames:
		try:
			print("Reading {}".format(filename + "..."), end="")
			with open(filename) as f:
				constellations.append(json.load(f))
			print("\tdone",end="\r")
		except Exception as e:
			print("")
			raise e
	print("\nJSON files read successfully.\n")
	return constellations

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

def verifyApiSuccess(response):
	"""
	Raise an apiError if the API response passed as a param is an error

	@param: response, dict, a JSON response from a REST API
	"""
	if "error" in response:
		try:
			type = response["error"]["type"]
			message = response["error"]["message"]
			raise apiError(type + ": " + message)
		except TypeError:
			print(response)
			raise apiError("Seems like one of the weird ones")
