from glob import glob
import json
from utils import loadSnacData

def extractRelations(constellation):
		"""
		Given a SNAC constellation JSON, return a list of its relations

		Params: @constellation, a SNAC constellation in JSON form
		Returns: a list of lists in the form [srcSnacID, relType, trgtSnacID]
				 (if constellation has no relations, returns empty list)
		"""
		data = []


		if "relations" in constellation.keys():
			for relationship in constellation["relations"]:
				triple = [
					relationship["sourceConstellation"], # SNAC ID
					relationship["type"]["term"], # Relationship type
					relationship["targetConstellation"] # SNAC ID
				]
				data.append(triple)

		return data

def main():
	# Load data
	constellations = loadSnacData()

	# Loop over constellations, extracting their relationships into a list
	#	and compiling a list of their SNAC IDs
	output = []
	ids = []
	for constellation in constellations:
		# Add get relation list from constellation; add contents to output list
		output = output + extractRelations(constellation)

		# Add the constellation's SNAC ID to the list we're keeping track of
		ids.append(constellation["id"])

	# Remove links to constellations not in our data set
	#	(loop over list backwards b/c we're modifying it)
	i = len(output)
	while i > 0:
		i -= 1
		# Get relationship
		link = output[i]

		# Get target of relationship
		target = link[2]

		# Delete the link if its target isn't in our dataset
		if target not in ids:
			del output[i]

	# Remove trailing periods from names
	for row in output:
		for i in range(len(row)):
			while row[i][-1]==".":
				row[i] = row[i][0:-1]

	# Write output to .tsv file
	header="source\tlabel\ttarget\t\n"
	with open("relationshipTable.tsv","w") as f:
		f.write(header)

		# Piece together string that will represent row of TSV
		for relationshipList in output:
			toWrite = "\t".join(relationshipList)
			f.write(toWrite+"\n")

if __name__ == '__main__':
    main()
