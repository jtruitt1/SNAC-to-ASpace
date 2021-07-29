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

def extractData(constellation):
	"""
	Given a SNAC constellation JSON, return various data pieces

	Params: @constellation, a SNAC constellation in JSON form
	Returns: data, a list of attribute values
	"""
	# Initialize the list we'll eventually return
	data = []

	# Get 8-digit ArkID
	data.append(constellation["ark"][-8:])

	# Get name
	data.append(constellation["nameEntries"][0]["original"])

	# Get gender
	if "genders" in constellation.keys():
		data.append(constellation["genders"][0]["term"]["term"])
	else:
		data.append("")

	# Get occupations
	data.append("")
	if "occupations" in constellation.keys():
		for occu in constellation["occupations"]:
			data[-1] += occu["term"]["term"] + ";"
		data[-1] = data[-1][:-1] # Strip trailing separator
	else:
		data.append("")

	# Get subjects
	data.append("")
	if "subjects" in constellation.keys():
		for subj in constellation["subjects"]:
			data[-1] += subj["term"]["term"] + ";"
		data[-1] = data[-1][:-1] # Strip trailing separator
	else:
		data.append("")

	# Get monthly meeting
	data.append(getMonthlyMeeting(constellation))

	return data

def getMonthlyMeeting(constellation):
	"""
	Given a SNAC constellation JSON,
	a) determine if it contains a link to a Quaker monthly meeting, and
	b) return a string of associated pre-separation monthly meetings

	Params: @constellation, a SNAC constellation in JSON form
	Returns: meetingName, the name of the relevant monthly meeting
			 (Or "Unknown" if none found)
	"""
	# Make sure the constellation has relationships
	if "relations" in constellation.keys():
		# Initialize list of meetings
		meetingList = []

		# Loop over relationships, checking if the target is a monthly meeting
		for link in constellation["relations"]:
			if "monthly meeting" in link["content"].lower():
				# If the target is a monthly meeting, add it to the meeting list
				meetingList.append(link["content"])



		# Loop over mtg list, removing ones w/ "Hicksite" or "Orthodox" in name
		# 	(this is because those relationships are probably spurious, since
		# 	Hicksite & Orthodox only emerged after John Hunt's death)
		# And add the mtg name to a string we'll eventually return
		#	(loop over the list backward, since we're changing it as we go)

		i = len(meetingList)
		meetings = ""
		while i > 0:
			i -= 1
			mtg = meetingList[i]
			if "Hicksite" in mtg:
				del meetingList[i]
			if "Orthodox" in mtg:
				del meetingList[i]
			meetings += mtg + ";"

		# Return the list of meetings if there are any qualifying ones
		if len(meetings) > 0:
			meetings = meetings[:-1] # Strip trailing separator
			return meetings

	# If the record lacks meeting affiliations
	return "Unknown"

def main():
	# Load constellation data
	constellations = loadSnacData()

	# Loop over constellations, extracting data and adding it to "output" list
	output = []
	for item in constellations:
		if item["entityType"]["term"] == "person":
			output.append(extractData(item))

	# Write output to .tsv file
	header="id\tlabel\tGender\tOccupations\tSubjects\tMonthly Meeting\t\n"
	with open("dataTable.tsv","w") as f:
		f.write(header)

		for item in output:
			toWrite = ""
			for i in item:
				toWrite += i + "\t"
			f.write(toWrite+"\n")

main()
