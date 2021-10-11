from utils import loadSnacData

def getoccupations(constellations):
	"""
	Extract a list of occupations from a list of SNAC constellation JSONs

	@Param: constellations, a list of SNAC constellation JSONs in dict form
	@Returns: a dict of the form {(occu heading, occu SNAC ID): # occurrences}
	"""
	# Start by initializing the dict of occupations we'll eventually return
	occupations = {}

	# Loop over constellations:
	for constellation in constellations:

		# If the constellation doesn't have a "occupations" entry, skip it
		if "occupations" not in constellation:
			continue

		# Also skip it if there aren't any entries in "occupations":
		if len(constellation["occupations"]) == 0:
			continue

		# Now that we know there are occupations, let's loop over them:
		for occupation in constellation["occupations"]:
			# Unpack occupation
			id = occupation["term"]["id"]
			heading = occupation["term"]["term"]

			# Check for this occu in the dict
			if (id, heading) in occupations:

				# Increase the count if it's there
				occupations[(id, heading)] += 1

			else:
				# Otherwise, create an entry in the dict w/ value 1
				occupations[(id, heading)] = 1

	return occupations

def writeTable(dict, filename, headerRow):
	"""Write a dict of form {(x,y):z} to a tsv of form x\ty\tz"""
	with open(filename, "w") as f:
		f.write(headerRow)
		for entry in dict:
			row = "\t".join([entry[0], entry[1], str(dict[entry])]) + "\n"
			f.write(row)

def main():
	print("\n")
	constellations = loadSnacData()

	print("Extracting occupations from constellations...")
	occupations = getoccupations(constellations)
	print("occupations successfully extracted.\n")

	print("Writing occupations to snacOccupations.tsv...")
	headers = "SNAC Heading\tSNAC ID\tCount\n"
	writeTable(occupations, "snacOccupations.tsv", headers)
	print("File successfully written.")
	print("\n")

main()
