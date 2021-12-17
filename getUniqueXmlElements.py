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

def getUniqueElements(tei):
	"""
	@param: tei, an XML file encoded according to the TEI standard
	@return: a list of unique tags
	"""
	# define namespace
	ns = {'x':'http://www.tei-c.org/ns/1.0'}

	# Get root element of tei
	root = tei.getroot()
	root.remove(root.find("x:teiHeader", ns))

	# Initialize list of unique elements
	uniqueTags = []

	for element in root.iter():
		tag = element.tag.split("}").pop()
		if tag not in uniqueTags:
			uniqueTags.append(tag)

	return uniqueTags

def main():
	print("\n")
	# Load the TEI data from files
	teis = loadData()
	print("\n")

	# Initialize a holder for our data
	uniqueTags = []
	for tei in teis:
		tagList = getUniqueElements(tei)
		for tag in tagList:
			if tag not in uniqueTags:
				uniqueTags.append(tag)

	uniqueTags.sort()
	for tag in uniqueTags:
		print(tag)

main()
