from utils import loadSnacData

def getSubjects(constellations):
	"""
	Extract a list of subjects from a list of SNAC constellation JSONs

	@Param: constellations, a list of SNAC constellation JSONs in dict form
	@Returns: a dict of the form {(subj heading, subj SNAC ID): # occurrences}
	"""
	# Start by initializing the dict of subjects we'll eventually return
	subjects = {}

	# Loop over constellations:
	for constellation in constellations:

		# If the constellation doesn't have a "subjects" entry, skip it
		if "subjects" not in constellation:
			continue

		# Also skip it if there aren't any entries in "subjects":
		if len(constellation["subjects"]) == 0:
			continue

		# Now that we know there are subjects, let's loop over them:
		for subject in constellation["subjects"]:
			# Unpack subject
			id = subject["term"]["id"]
			heading = subject["term"]["term"]

			# Check for this subj in the dict
			if (id, heading) in subjects:

				# Increase the count if it's there
				subjects[(id, heading)] += 1

			else:
				# Otherwise, create an entry in the dict w/ value 1
				subjects[(id, heading)] = 1

	return subjects

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

	print("Extracting subjects from constellations...")
	subjects = getSubjects(constellations)
	print("Subjects successfully extracted.\n")

	print("Writing subjects to snacSubjects.tsv...")
	headers = "SNAC Heading\tSNAC ID\tCount\n"
	writeTable(subjects, "snacSubjects.tsv", headers)
	print("File successfully written.")
	print("\n")

main()
