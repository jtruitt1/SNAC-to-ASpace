from utils import loadSnacData

def getSubjects(constellations):
	"""
	Extract a list of subjects from a list of SNAC constellation JSONs

	@Param: constellations, a list of SNAC constellation JSONs in dict form
	@Returns: a dict of the form {(subj heading, subj SNAC ID): # occurrences}
	"""
	pass

def writeTable(dict, filename, headerRow):
	"""Write a dict of form {(x,y):z} to a tsv of form x\ty\tz"""
	pass

def main():
	print("\n")
	constellations = loadSnacData()
	subjects = getSubjects(constellations)
	headers = "SNAC Heading\tSNAC ID\tCount"
	writeTable(subjects, "snacSubjects.tsv", headers)
	print("\n")

main()
