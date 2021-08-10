from extractRelations import loadSnacData
import xml.etree.ElementTree as ET

def validateBiogHist(constellations):
	for item in constellations:
		try:
			dummy = item["biogHists"][0]
			root = ET.fromstring("<bio>"+dummy["text"]+"</bio>")
			del dummy
		except LookupError:
			print("No biogHist for\t\t\t"+item["ark"])
		except ET.ParseError:
			print("biogHist misformatted in\t"+item["ark"])

def checkForGender(constellations):
	for item in constellations:
		if "genders" in item.keys():
			if len(item["genders"]) > 0:
				continue
		print("Missing gender info:\t" + item["ark"])

def checkRelSources(constellations):
	for constellation in constellations:
		if "relations" in constellation.keys():
			for relation in constellation["relations"]:
				print(relation["sourceArkID"])
				print(constellation["ark"])
				print()
				if relation["sourceArkID"] != constellation["ark"]:
					print(relation)

def main():
	constellations = loadSnacData()

	#checkForGender(constellations)
	checkRelSources(constellations)


main()
