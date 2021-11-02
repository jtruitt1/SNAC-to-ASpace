from utils import Relationship

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

		# Skip "associatedWith" relationships
		if relation.type == "associatedWith":
			continue

		# Get the inverse relationship
		inverse = relation.getInverse()

		# See if the inverse is in the list
		if inverse not in relationList:

			# Add it to the list of missing inverses if it isn't
			missingRecips.append(inverse)

#			print("\t".join([relation.source, relation.type, relation.target]))
#			print("\t".join([inverse.source, inverse.type, inverse.target]))
#			print("")

	#Print status message
	print("List compiled!")

	return missingRecips

def writeRelationshipsToFile(relationList, filename):

	print("Writing data to", filename+ "...")

	headerRow = "Source\tType\tTarget\n"

	with open(filename, "w") as f:
		f.write(headerRow)

		for link in relationList:
			row = "\t".join([link.source, link.type, link.target])
			f.write(row + "\n")

	print("Data successfully written!")

def main():
	print("")
	# Extract relationships from external file
	relationList = loadRelationsFromFile("relationshipTable.tsv")

	# Find missing reciprocal relationships
	print("")
	missingRecips = findMissingReciprocals(relationList)

	print("")
	# Write the list of missing reciprocals to a file
	writeRelationshipsToFile(missingRecips, "missingRelationships.tsv")

	print("")

main()
