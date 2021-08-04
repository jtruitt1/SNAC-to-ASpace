from extractRelations import loadSnacData
import xml.etree.ElementTree as ET

def main():
    constellations = loadSnacData()

    for item in constellations:
        try:
            dummy = item["biogHists"][0]
            root = ET.fromstring("<bio>"+dummy["text"]+"</bio>")
            del dummy
        except LookupError:
            print("No biogHist for\t\t\t"+item["ark"])
        except ET.ParseError:
            print("biogHist misformatted in\t"+item["ark"])

main()
