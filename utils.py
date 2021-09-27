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
