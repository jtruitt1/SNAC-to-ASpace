from glob import glob
import json

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
	print("Reading {} JSON files...")
	for filename in filenames:
		print("Reading {}".format(filename + "..."), end="")
		with open(filename) as f:
			constellations.append(json.load(f))
		print("\tdone")
	print("JSON files read successfully.\n")
	return constellations

def extractRelations(constellation):
		"""
		Given a SNAC constellation JSON, return a list of its relations

		Params: @constellation, a SNAC constellation in JSON form
		Returns: a list of lists in the form [srcArkID, relType, trgtArkID]
				 (if constellation has no relations, returns empty list)
		"""
		data = []


		if "relations" in constellation.keys():
			for relationship in constellation["relations"]:
				triple = [
					relationship["sourceArkID"][-8:], # 8-digit source ArkID
					relationship["type"]["term"], # Relationship type
					relationship["targetArkID"][-8:] # 8-digit target ArkID
				]
				data.append(triple)

		return data

def main():
	# Load data
	constellations = loadSnacData()

	# Loop over constellations, extracting their relationships into a list
	#	and compiling a list of their 8-digit Ark IDs
	output = []
	arks = []
	for constellation in constellations:
		output = output + extractRelations(constellation)
		arks.append(constellation["ark"][-8:])

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
		if target not in arks:
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
		for item in output:
			toWrite = ""
			for i in item:
				toWrite += i + "\t"
			f.write(toWrite+"\n")

main()
