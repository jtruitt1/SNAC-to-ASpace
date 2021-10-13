

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

def loadRelationsFromFile(filename):
	"""
	Loads data from an external TSV & turns it into Relationship objects.

	@param: filename, the name of a TSV file w/ a header row
			rows should be formatted source, relationship type, target
	@return: a list of Relationship objects
	"""
	# Initialize the list we'll return
	relationList = []

	# Print status message
	print("Loading relationship data from", filename + "...")

	# Open the file, read into a list of lines
	with open(filename) as f:
		data = f.read().split("\n")

	del data[0] # Delete header row

	# Loop over the lines,
	for line in data:

		# (skipping empty lines)
		if line == "":
			continue

		# splitting each line by tabs,
		args = line.split("\t")

		# feeding the data into a Relationship object,
		relation = Relationship(args[0], args[2], args[1])

		# and appending that obj to the list that will be returned
		relationList.append(relation)

	# Print status message
	print("Relationship data successfully loaded.")

	return relationList

def findMissingReciprocals(relationList):
	"""
	Check for non-reciprocal relationships in a list of Relationship objs.

	For every item in the list, check to see if its inverse is in the list.
	@param: relationList, a list of Relationship objects
	@return: a list of Relationship objs which, if added to relationList,
				would ensure that all relationships had an inverse
	"""

	# Initialize list to return
	missingRecips = []

	# Print a status message
	print("Checking for relationships without reciprocals…")

	for relation in relationList:

		# Get the inverse relationship
		inverse = relation.getInverse()

		# See if the inverse is in the list
		if inverse not in relationList:

			# Add it to the list of missing inverses if it isn't
			missingRecips.append(inverse)

	#Print status message
	print("List compiled!")

	return missingRecips

def main():
	print("")
	# Extract relationships from external file
	relationList = loadRelationsFromFile("relationshipTable.tsv")

	# Find missing reciprocal relationships
	missingRecips = findMissingReciprocals(relationList)

	# Write the list of missing reciprocals to a file

	print("")

main()
