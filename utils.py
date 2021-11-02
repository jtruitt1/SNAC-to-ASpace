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

class Relationship:
	"""Represents a relationship between SNAC constellations"""

	def __init__(self, source, target, type):
		self.source = source
		self.target = target
		self.type = type

	def getInverse(self):
		inverseList = {
			"almaMaterOf":"alumnusOrAlumnaOf",
			"alumnusOrAlumnaOf":"almaMaterOf",
			"ancestorOf":"descendantOf",
			"auntOrUncleOf":"nieceOrNephewOf",
			"child-in-law of":"parent-in-law of",
			"childOf":"parentOf",
			"conferredHonorsTo":"honoredBy",
			"descendantOf":"ancestorOf",
			"employeeOf":"employerOf",
			"employerOf":"employeeOf",
			"foundedBy":"founderOf",
			"founderOf":"foundedBy",
			"grandchildOf":"grandparentOf",
			"grandparentOf":"grandchildOf",
			"hasHonoraryMember":"honoraryMemberOf",
			"hasMember":"memberOf",
			"Hierarchical-child":"Hierarchical-parent",
			"Hierarchical-parent":"Hierarchical-child",
			"honoraryMemberOf":"hasHonoraryMember",
			"honoredBy":"conferredHonorsTo",
			"investigatedBy":"investigatorOf",
			"investigatorOf":"investigatedBy",
			"memberOf":"hasMember",
			"nieceOrNephewOf":"auntOrUncleOf",
			"ownedBy":"ownerOf",
			"ownerOf":"ownedBy",
			"parent-in-law of":"child-in-law of",
			"parentOf":"childOf",
			"predecessorOf":"successorOf",
			"successorOf":"predecessorOf"
		}

		# Check if the relationship's type has an inverse
		if self.type in inverseList:
			# Get the inverse type if there is one, and return the inverse rel
			inverseType = inverseList[self.type]
			return Relationship(self.target, self.source, inverseType)
		else:
			return Relationship(self.target, self.source, self.type)

	def __eq__(self, other):
		if self.type == other.type:
			if self.target == other.target:
				if self.source == other.source:
					return True
		return False

	def __str__(self):
		return ", ".join([self.source, self.type, self.target])

	def getTypeId(self):
		typeIDList = {
			"acquaintanceOf": "28227",
			"almaMaterOf": "28229",
			"alumnusOrAlumnaOf": "28230",
			"ancestorOf": "28232",
			"associatedWith": "28234",
			"auntOrUncleOf": "28236",
			"biologicalParentOf": "28237",
			"child-in-law Of": "28238",
			"child-in-law of": "28238",
			"childOf": "28239",
			"conferredHonorsTo": "28240",
			"correspondedWith": "28243",
			"createdBy": "28245",
			"creatorOf": "28246",
			"descendantOf": "28248",
			"employeeOf": "28250",
			"employerOf": "28251",
			"foundedBy": "28253",
			"founderOf": "28254",
			"grandchildOf": "28255",
			"grandparentOf": "28256",
			"hasFamilyRelationTo": "400456",
			"hasHonoraryMember": "28260",
			"hasMember": "28261",
			"Hierarchical-child": "28263",
			"Hierarchical-parent": "28264",
			"honoraryMemberOf": "28265",
			"honoredBy": "28266",
			"investigatedBy": "28267",
			"investigatorOf": "28268",
			"isSuccessorOf": "400459",
			"leaderOf": "28269",
			"memberOf": "28271",
			"nieceOrNephewOf": "28272",
			"ownedBy": "400478",
			"ownerOf": "28274",
			"parent-in-law Of": "28275",
			"parent-in-law of": "28275",
			"parentOf": "28276",
			"participantIn": "28277",
			"politicalOpponentOf": "28279",
			"predecessorOf": "28280",
			"relativeOf": "28281",
			"sibling-in-law Of": "28282",
			"sibling-in-law of": "28282",
			"siblingOf": "28283",
			"sibling of": "28283",
			"spouseOf": "28284",
			"subordinateOf": "28290",
			"successorOf": "28291"
		}
		return typeIDList[self.type]

	typeUriList = {
		"acquaintanceOf":"",
		"almaMaterOf":"",
		"alumnusOrAlumnaOf":"",
		"ancestorOf":"",
		"associatedWith":"http://socialarchive.iath.virginia.edu/control/term#associatedWith",
		"auntOrUncleOf":"",
		"biologicalParentOf":"",
		"child-in-law Of":"",
		"childOf":"",
		"conferredHonorsTo":"",
		"correspondedWith":"http://socialarchive.iath.virginia.edu/control/term#correspondedWith",
		"createdBy":"",
		"descendantOf":"",
		"employeeOf":"",
		"employerOf":"",
		"foundedBy":"",
		"founderOf":"",
		"grandchildOf":"",
		"grandparentOf":"",
		"hasFamilyRelationTo":"",
		"hasHonoraryMember":"",
		"hasMember":"",
		"Hierarchical-child":"",
		"Hierarchical-parent":"",
		"honoraryMemberOf":"",
		"honoredBy":"",
		"investigatedBy":"",
		"investigatorOf":"",
		"isSuccessorOf":"",
		"leaderOf":"",
		"memberOf":"",
		"nieceOrNephewOf":"",
		"ownedBy":"",
		"ownerOf":"",
		"parent-in-law Of":"",
		"parentOf":"",
		"participantIn":"",
		"politicalOpponentOf":"",
		"predecessorOf":"",
		"relativeOf":"",
		"sibling-in-law Of":"",
		"siblingOf":"",
		"spouseOf":"",
		"subordinateOf":"",
		"successorOf":""
	}


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

def loadIdsToUpdate():
	"""
	Loads data from a .tsv (A\tB\tC\tD) into a list of lists ([[A,B,C,D]])
	"""
	print("Reading data from file...")
	# Initialize the list we'll return
	identifiers = {}

	# Read data from file
	filename = "idsToUpdate.tsv"
	with open(filename) as f:
		rows = f.read().split("\n")

	# Discard header row
	del rows[0]

	# Delete last line if it's blank
	if rows[-1] == "":
		del rows[-1]

	# Loop over row strings, turning them into lists & adding them to main list
	for row in rows:
		identifiers.append(row.split("\t"))


	print("Data successfully read.\n")
	return identifiers
