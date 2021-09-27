from csv import *
from utils import loadSnacData

# csv documentation: https://docs.python.org/3/library/csv.html#writer-objects

def convertToTsv(constellations):
	"""
	Takes a list of SNAC constellation JSONs and returns a set of TSV rows
	containing certain fields
	"""
	rows = []
	# TODO: Add list of column headers
	header = []
	for constellation in constellations:


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
