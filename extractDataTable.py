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
	Given a SNAC constellation JSON, return a various data pieces

	Params: @constellation, a SNAC constellation in JSON form
	Returns: data, a list of attribute values
	"""
	# Initialize the list we'll eventually return
	data = []

	# Get SNACID
	data.append(constellation["id"])

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

	# Get subjects
	data.append("")
	if "subjects" in constellation.keys():
		for subj in constellation["subjects"]:
			data[-1] += subj["term"]["term"] + ";"
		data[-1] = data[-1][:-1] # Strip trailing separator

	# Get monthly meeting
	data.append(getMonthlyMeeting(constellation))

	return data

def getMonthlyMeeting(constellation):
	"""
	Given a SNAC constellation JSON,
	a) determine if it contains a link to a Quaker monthly meeting, and
	b) return the name of the monthly meeting with the latest foundation date
	(this ensures that people who joined later-branching meetings are well
	grouped)

	Params: @constellation, a SNAC constellation in JSON form
	Returns: meetingName, the name of the relevant monthly meeting
			 (Or "Unknown" if none found)
	"""
	if "relations" in constellation.keys():
		meetingList = []
		for link in constellation["relations"]:
			if "monthly meeting" in link["content"].lower():
				meetingList.append(link["content"])
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
		if len(meetings) > 0:
			meetings = meetings[:-1] # Strip trailing separator
			return meetings

	return "Unknown"

def main():
	constellations = loadSnacData()

	output = []
	for item in constellations:
		if item["entityType"]["term"] == "person":
			output.append(extractData(item))

	#print output
	header="id\tlabel\tGender\tOccupations\tSubjects\tMonthly Meeting\t\n"
	with open("dataTable.tsv","w") as f:
		f.write(header)

		for item in output:
			toWrite = ""
			for i in item:
				toWrite += i + "\t"
			f.write(toWrite+"\n")

main()
