from glob import glob
from utils import loadIdsToUpdate

def updateDataInFiles(idsToUpdate, arksToUpdate):
	"""Find and replace old identifiers across the files in snac_jsons folder"""
	# Do nothing if there are no identifiers to update
	if len(idsToUpdate) == 0:
		return None

	# Get list of filenames to edit
	filenames = glob("snac_jsons/*.json")

	# Print a helpful message
	print("Updating identifiers across", len(filenames), "files...")

	# Loop over the files, reading data from them, making changes, then writing
	# (Leave the JSON as strings, don't unpack it into dicts)
	counter = 0 # Keep track of how many files we've worked with
	for filename in filenames:
		# Print helpful message
		counter += 1
		print("Updating", filename, "(file", str(counter) + ")...\t", end="\r")

		# Read data from file
		with open(filename, "r") as f:
			filedata = f.read()

		# Loop over identifiers to update
		# Replacing each one in the JSON with the newer version
		for id in idsToUpdate:
			# Find SNAC ID in quotes to avoid replacing portions of longer IDs
			# (because SNAC IDs vary in length)
			quotedId = "\"" + id + "\""
			if quotedId in filedata:
				newQuotedId = "\"" + idsToUpdate[id] + "\""
				filedata = filedata.replace(quotedId, newQuotedId) #Replacement
		for ark in arksToUpdate:
			if ark in filedata:
				filedata = filedata.replace(ark, arksToUpdate[ark]) #Replacement

		# Write data back to file
		with open(filename, "w") as f:
			f.write(filedata)

	print("\nSuccessfully updated files.\n")

def main():
	print()

	# Load data from file
	newIdsAndArks = loadIdsToUpdate()

	# Unpack data loaded from file
	idsToUpdate = {item[0]: item[1] for item in newIdsAndArks}
	arksToUpdate = {item[2]: item[3] for item in newIdsAndArks}

	# Find-and-replace the IDs and Arks across the JSON files
	updateDataInFiles(idsToUpdate, arksToUpdate)


if __name__ == "__main__":
	main()
