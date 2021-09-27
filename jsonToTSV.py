from csv import *
from utils import loadSnacData

# csv documentation: https://docs.python.org/3/library/csv.html#writer-objects

def convertToTsv(constellations):
	'''
	Takes a list of SNAC constellation JSONs and returns a set of TSV rows
	containing certain fields
	'''
	rows = []
	# Add list of column headers
	header = ['Name Entry','Entity Type','SNAC ID','BiogHist']
	rows.append(header)
	for constellation in constellations:
		row = {} # Initialize dictionary to add to rows

		# Enter data into row's fields
		row['Name Entry'] = constellation['nameEntries'][0]['original']
		row['Entity Type'] = constellation['entityType']['term']
		row['SNAC ID'] = constellation['id']
		row['BiogHist'] = constellation["biogHists"][0]["text"]

		rows.append(row) # Add this row to the list of rows

	return rows

def writeTsvToFile(rows):
	pass

def main():
	# Import JSONs
	constellations = loadSnacData()

	# Create list of TSV rows from JSONs
	rows = convertToTsv(constellations)

	# Write rows to a file
	writeTsvToFile(rows)

main()
