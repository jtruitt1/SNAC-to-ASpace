from extractRelations import loadSnacData
import xml.etree.ElementTree as ET

def validateBiogHist(constellations):
	for item in constellations:
		try:
			dummy = item["biogHists"][0]
			root = ET.fromstring("<bio>"+dummy["text"]+"</bio>")
			# print first child of <bio>
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
		if "relations" in constellation:
			for relation in constellation["relations"]:
				print(relation["sourceArkID"])
				print(constellation["ark"])
				print()
				if relation["sourceArkID"] != constellation["ark"]:
					print(relation)

def checkForRelationships(constellations):
	for constellation in constellations:
		if "relations" not in constellation:
			print("Has no relationships:\t" + constellation["ark"])


def checkForPaChester(constellations):
	chesterString = "Chester Monthly Meeting (Society of Friends : 1681-1827)"
	for constellation in constellations:
		if "relations" in constellation:
			for relation in constellation["relations"]:
				target = relation["targetConstellation"]
				content = relation["content"]
				if target == "61920242" or content == chesterString:
					print(constellation["ark"], "is linked to Chester MM in PA")

def main():
	constellations = loadSnacData()

	validateBiogHist(constellations)
	checkForGender(constellations)
	checkForRelationships(constellations)
	checkForPaChester(constellations)



main()
