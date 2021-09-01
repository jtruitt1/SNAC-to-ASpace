"""
A suite of programs to perform analysis on the TEI-markup Hunt Journals.

James Truitt
July 2021
"""

from glob import glob
import xml.etree.ElementTree as ET

def loadData():
	print("Loading XML data...")
	# Get list of TEI filenames
	filenames = glob("../Hunt/obf-site/src/assets/pid-tei/*.xml")

	# Initialize container for xml data
	xmls = []

	# Loop over filenames, extracting the XML data in each & adding it to xmls
	for filename in filenames:
		print("Reading {}".format(filename + "..."), end="")
		xml = ET.parse(filename)
		xmls.append(xml)
		print("\tdone")

	print("XML data successfully loaded!")
	return xmls

def getBoolCooccurrences(tei):
	"""
	For each div in the XML, returns a list of all the Ark IDs in that div

	@param: tei, an XML file encoded according to the TEI standard
	@return: a list of lists of Ark Ids
	"""
	# define namespace
	ns = {'x':'http://www.tei-c.org/ns/1.0'}

	# Get root element of tei
	root = tei.getroot()

	# Get iterable of divs
	body = root[1].find("x:body", ns)
	divs = body.iterfind("x:div", ns)

	# Create container for entries
	entries = []

	# Loop over divs, extracting persName tags
	for div in divs:
		# Create a container for the persNames
		entryNames = []
		#print(div.find('{http://www.tei-c.org/ns/1.0}p'))
		for para in div.iterfind('{http://www.tei-c.org/ns/1.0}p'):
			for name in para.iterfind('{http://www.tei-c.org/ns/1.0}persName'):
				if name.attrib["key"] in entryNames:
					continue
				else:
					entryNames.append(name.attrib["key"])
		entries.append(entryNames)
	return entries

def getCountCoocurrences(tei):
	return []

def main():
	print("\n")
	# Load the TEI data from files
	teis = loadData()
	print("\n")

	# Initialize a holder for our data
	data = []

	print("Extracting Ark Id lists from TEI...\t")
	# Loop over the TEI files
	for journal in teis:
		# From each TEI, extract set of sets of ARKids cooccurring in entries
		collocs = getBoolCooccurrences(journal)

		# Add that set to data holder
		data += collocs
	print("done!\n")

	# Create a parallel list of numbers of names per entry
	# lengths = []
	# for entry in data:
	# 	lengths.append(len(entry))
	# print(lengths)

	print("Filter out empty entries...\t")
	# Filter entries without names out of data
	# (loop over list backward, removing empty lists)
	i = len(data)
	while i > 0:
		i += -1
		if len(data[i]) == 0:
			del data[i]
	print("done!\n")

	#### Calculate some statistics #####


	# Loop over entries to count occurrences of each name
	namecounts = {}
	for entry in data:
		for name in entry:
			if name in namecounts.keys():
				namecounts[name] += 1
			else:
				namecounts[name] = 1

	nameList = list(namecounts.keys())
	nameList.sort(key=namecounts.__getitem__)

	# Print list of names
	for name in nameList:
		print(name+"\t"+str(namecounts[name]))

	## Create cooccurrence matrix ##

	# # Initialize matrix
	# matrix = [[0 for i in nameList] for j in nameList]
	#
	# # Loop over data and add to matrix
	# for entry in data:
	# 	for name1 in entry:
	# 		mainIndex1 = nameList.index(name1)
	# 		entryIndex = entry.index(name1)
	# 		for name2 in entry:
	# 			mainIndex2 = nameList.index(name2)
	# 			matrix[mainIndex1][mainIndex2] += 1
	#
	# # Print matrix
	# for i in nameList:
	# 	print("_"+i, end="")
	# print("")
	# for i in range(len(nameList)):
	# 	print(nameList[i], end="_")
	# 	for k in range(len(nameList)):
	# 		print(matrix[i][k], end="_")
	# 	print("")

	print("Analyzing coocurrence data...\t",end="")
	# Create a list of name pairs
	namePairs = {}
	for i in nameList:
		index = nameList.index(i)
		for k in nameList[index+1:]:
			key = i +'\t'+ k
			namePairs[key] = 0

	keys = list(namePairs.keys())
	# keys.sort()

	# Initalize the TSV that will eventually get written to a file
	output = "Source\tTarget\tWeight\n"

	# Loop over name-pairs, counting their occurrence in the data
	for pair in keys:
		for entry in data:
			# Check to see if both halves of the key occur in this entry
			if pair[:8] in entry and pair[-8:] in entry:
				namePairs[pair] += 1

		if namePairs[pair] > 0:
			output += pair+'\t'+ str(namePairs[pair]) +'\n'
	print("done!\n")

	print("Writing data to cooccurrences.tsv...\t")
	with open("cooccurrences.tsv","w") as f:
		f.write(output)
	print("done!\n")

main()
