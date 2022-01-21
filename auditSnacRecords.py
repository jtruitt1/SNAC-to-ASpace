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

def checkForMultipleDates(constellations):
	for constellation in constellations:
		if "dates" in constellation:
			if len(constellation["dates"]) > 1:
				print(constellation["ark"], "has multiple date entries")
			elif len(constellation["dates"]) == 0:
				print(constellation["ark"], "has no date entries")
		else:
			print(constellation["ark"], "has no date entries")

def checkForMultiplePlaces(constellations):
	"""Check for multiple places listed as birth or as death"""
	for constellation in constellations:
		hasBirthPlace, hasDeathPlace = False, False
		if "places" in constellation:
			for place in constellation["places"]:
				if "role" in place:
					if place["role"]["term"] == "Birth":
						if hasBirthPlace:
							print(constellation["ark"], "has multiple birthplaces")
						else:
							hasBirthPlace = True
					if place["role"]["term"] == "Death":
						if hasDeathPlace:
							print(constellation["ark"], "has multiple deathplaces")
						else:
							hasDeathPlace = True


def main():
	constellations = loadSnacData()

	validateBiogHist(constellations)
	checkForGender(constellations)
	checkForRelationships(constellations)
	checkForPaChester(constellations)
	checkForMultipleDates(constellations)
	checkForMultiplePlaces(constellations)



main()
