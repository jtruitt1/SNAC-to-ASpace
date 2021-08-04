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

def main():
	constellations = loadSnacData()

	output = []
	for item in constellations:
		if "relations" in item.keys():
			for link in item["relations"]:
				data = [
				#link["sourceConstellation"],
				item["nameEntries"][0]["original"],
				link["type"]["term"],
				#link["targetConstellation"],
				link["content"]
				]
				output.append(data)

	#remove trailing periods
	for row in output:
		for i in range(len(row)):
			while row[i][-1]==".":
				row[i] = row[i][0:-1]

	#print output
	header="source\tlabel\ttarget\t\n"
	with open("relationshipTable.tsv","w") as f:
		f.write(header)

		for item in output:
			toWrite = ""
			for i in item:
				toWrite += i + "\t"
			f.write(toWrite+"\n")

if __name__ == '__main__':
    main()
