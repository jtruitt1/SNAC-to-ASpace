from argparse import *
import json
import xml.etree.ElementTree as ET

def printTree(element, indent=""):
	"""
	Given an xml element, prints it prettily
	"""
	print(indent+"<"+element.tag+">")
	indent = "-"+indent
	for item in element.attrib.keys():
		print(indent+"@"+item+"="+element.attrib[item])
	if element.text != None:
		print(indent+"\""+element.text+"\"")
	for subelem in element:
		printTree(subelem, indent)

def initializeEACCPF():
	"""
	Creates XML file with basic data for an EAC-CPF file exported from SNAC.

		@params: none
		@returns: eac, an xml object
	"""
	root = ET.Element("eac-cpf")
	eac = ET.ElementTree(root)
	root.set("xmlns", "urn:isbn:1-931666-33-4")
	root.set("xmlns:xlink","https://www.w3.org/1999/xlink")
	root.set("xmlns:snac","http://socialarchive.iath.virginia.edu/")
	return eac

def addDesNote(jsonElem,eacElem):
	"""
	Checks for a descriptive note in the JSON; adds it to the EAC if found.
	Params:
		@jsonElem, a JSON dict to check for a descriptive note
		@eacElem, the element of the EAC in which to insert any notes found
	returns: none
	side effects: inserts a <descriptiveNote> in eacElem if note content found
	"""
	if "note" in jsonElem.keys():
		descriptiveNote = ET.Element("descriptiveNote")
		descriptiveNote.text = jsonElem["note"]
		eacElem.append(descriptiveNote)

def jsonToEacMigration(json, eac):
	"""
	Moves agent data from a SNAC JSON structure to an EAC-CPF-std XML structure

		Params:
			@json, a dict containing a snac agent JSON
			@eac, an EAC-CPF XML object with some basic information filled out
		returns:
			@eac, an EAC-CPF XML object containing a limited set of the agent
				data appropriate for import into ArchivesSpace
	"""
	eac = migrateControl(json, eac)
	eac = migrateDescription(json, eac)
	return eac

def migrateControl(json, eac):
	"""
	Moves agent control data from a SNAC JSON to an EAC-CPF-standard XML

		Params:
			@json: a dict containing a snac agent JSON
			@eac: an EAC-CPF XML object with some basic information filled out
		@returns: eac, an EAC-CPF XML object with the <control> tag filled out
	"""
	root = eac.getroot()

	#Create and insert the <control> tag
	control = ET.Element("control")
	root.append(control)

	#Create and insert <recordId> tag in <control> (use ark ID)
	ark = ET.Element("recordId")
	ark.text = json["ark"]
	control.append(ark)

	#Create and insert <maintenanceStatus> in <control>
	maintenanceStatus = ET.Element("maintenanceStatus")
	maintenanceStatus.text=json["maintenanceStatus"]["term"]
	control.append(maintenanceStatus)

	#Create and insert <maintenanceAgency> in <control>
	maintenanceAgency = ET.Element("maintenanceAgency")
	control.append(maintenanceAgency)

	#Create and insert <agencyName> in <maintenanceAgency>
	agencyName = ET.Element("agencyName")
	agencyName.text=json["maintenanceAgency"]
	maintenanceAgency.append(agencyName)

	# Automatically set contents of <languageDeclaration> and add to <control>
	#	(on the assumption that it will always be English in Latin script)
	langDeclStr = """<languageDeclaration>
  <language languageCode="eng">English</language> <script scriptCode="Latn">
        Latin </script></languageDeclaration>"""
	languageDeclaration = ET.fromstring(langDeclStr)
	control.append(languageDeclaration)

	# Don't pull conventionDeclaration data from SNAC b/c it's mostly garbo
	## TODO: Generate convention declaration data for the EAC record

	#Create and insert <maintenanceHistory> in <control>
	maintenanceHistory = ET.Element("maintenanceHistory")
	control.append(maintenanceHistory)

	#Loop over maintenanceEvents in the json, adding every one to the eac
	for item in json["maintenanceEvents"]:
		#Create and insert <maintenanceEvent> in <maintenanceHistory>
		maintenanceEvent = ET.Element("maintenanceEvent")
		maintenanceHistory.append(maintenanceEvent)

		#Create and insert <eventType> in <maintenanceEvent>
		eventType = ET.Element("eventType")
		eventType.text = item["eventType"]["term"]
		maintenanceEvent.append(eventType)

		#Create and insert <eventDateTime> w/ attrib in <maintenanceEvent>
		eventDateTime = ET.Element("eventDateTime")
		eventDateTime.text = item["eventDateTime"]
		# Check for standardDateTime data; add it if found
		if "standardDateTime" in item.keys():
			eventDateTime.set("standardDateTime", item["standardDateTime"])
		maintenanceEvent.append(eventDateTime)

		#Create and insert <agentType> in <maintenanceEvent>
		agentType = ET.Element("agentType")
		agentType.text = item["agentType"]["term"]
		maintenanceEvent.append(agentType)

		#Create and insert <agent> in <maintenanceEvent>
		agent = ET.Element("agent")
		agent.text = item["agent"]
		maintenanceEvent.append(agent)

		#Check for eventDescription data
		if "eventDescription" in item.keys():
			#Create and insert <eventDescription> in <maintenanceEvent>
			eventDescription = ET.Element("eventDescription")
			eventDescription.text = item["eventDescription"]
			maintenanceEvent.append(eventDescription)

	#Create and insert <sources> in <control>
	sources = ET.Element("sources")
	control.append(sources)

	#Loop over sources in the json, adding every one to <sources>
	for item in json["sources"]:
		source = ET.Element("source")

		#If source has an attached URI, add @xlink:href & @xlink:type attribs
		if "uri" in item.keys():
			source.set("xlink:href", item["uri"])
			source.set("xlink:type", item["type"]["term"])

		#Add <sourceEntry> tag if source has a citation
		if "citation" in item.keys():
			sourceEntry = ET.Element("sourceEntry")
			sourceEntry.text = item["citation"]
			source.append(sourceEntry)

		#Add <descriptiveNote> if source has text
		if "text" in item.keys():
			descriptiveNote = ET.Element("descriptiveNote")
			source.append(descriptiveNote)

			#Check for <p> tag in text; insert if not there
			text = item["text"]
			if "<p>" in text:
				descriptiveNote.text = text
			else:
				ET.SubElement(descriptiveNote, "p")
				descriptiveNote[0].text = text
		sources.append(source)
	return eac

def migrateDescription(json, eac):
	"""
	Moves agent descriptive data from a SNAC JSON to an EAC-CPF-standard XML

		Params:
			@json: a dict containing a snac agent JSON
			@eac: an EAC-CPF XML object with some basic information filled out
		@returns: eac, an EAC-CPF XML object w/ <cpfDescription> tag filled out
	"""
	root = eac.getroot()

	# Create an insert <cpfDescription> tag
	cpfDescription = ET.Element("cpfDescription")
	root.append(cpfDescription)


	###### <identity> tag ######

	# Create and insert <identity> tag in <cpfDescription>
	identity = ET.Element("identity")
	cpfDescription.append(identity)

	# Create and insert <entityType> tag in <identity>
	entityType = ET.Element("entityType")
	entityType.text = json["entityType"]["term"]
	identity.append(entityType)

	# Create and insert a single placeholder <nameEntry>
	nameEntry = ET.Element("nameEntry")
	identity.append(nameEntry)
	part = ET.Element("part")
	# Use the unparsed SNAC name as a placeholder
	part.text = json["nameEntries"][0]["original"]
	nameEntry.append(part)

	# Check for sameAsRelations; add them as <entityId> tags if found
	if "sameAsRelations" in json.keys():
		# Loop over sameAsRelations
		for item in json["sameAsRelations"]:
			# Create and insert <entityId> tags in <identity>
			entityId = ET.Element("entityId")
			entityId.text = item["uri"]
			identity.append(entityId)

	# Add SNAC as an authority too
	entityId = ET.Element("entityId")
	entityId.text = json["ark"]
	identity.append(entityId)

	###### <description> tag ######

	# Create and insert <description> tag in <cpfDescription>
	description = ET.Element("description")
	cpfDescription.append(description)

	### <existDates> ###

	# Check for existDates data, and if found:
	if "dates" in json.keys():

		# Create and insert <existDates> tag in <description>
		existDates = ET.Element("existDates")
		description.append(existDates)

		# Check if we're dealing with a single date or a date range
		if "toDate" in json["dates"][0].keys():
			## Date Ranges ##

			# Create and insert <dateRange> tag in <existDates>
			dateRange = ET.Element("dateRange")
			existDates.append(dateRange)

			# Create and insert <fromDate> tag in <dateRange>
			fromDate = ET.Element("fromDate")
			if "fromDateOriginal" in json["dates"][0].keys():
				fromDate.text = json["dates"][0]["fromDateOriginal"]
			if "fromDate" in json["dates"][0].keys():
				fromDate.set("standardDate", json["dates"][0]["fromDate"])
			if "fromType" in json["dates"][0].keys():
				fromDate.set("localType", json["dates"][0]["fromType"]["term"])
			dateRange.append(fromDate)

			# Create and insert <toDate> tag in <dateRange>
			toDate = ET.Element("toDate")
			if "toDateOriginal" in json["dates"][0].keys():
				toDate.text = json["dates"][0]["toDateOriginal"]
			if "toDate" in json["dates"][0].keys():
				toDate.set("standardDate", json["dates"][0]["toDate"])
			if "toType" in json["dates"][0].keys():
				toDate.set("localType", json["dates"][0]["fromType"]["term"])
			dateRange.append(toDate)

		else:
			## Single Dates ##

			# Create and insert <date> tag in <existDates>
			date = ET.Element("date")
			existDates.append(date)

			# Wrap natural language text in <date> if present
			if "fromDateOriginal" in json["dates"][0].keys():
				date.text = json["dates"][0]["fromDateOriginal"]

			# Add machine readable date if present
			if "fromDate" in json["dates"][0].keys():
				date.set("standardDate", json["dates"][0]["fromDate"])

			# Add date type data if present
			if "fromType" in json["dates"][0].keys():
				date.set("localType", json["dates"][0]["fromType"]["term"])


	### <language(s)Used> ###

	#First, check that there is language used data
	if "languagesUsed" in json.keys():

		# Create <languagesUsed> if >1 lang; else add langs to <description>
		if len(json["languagesUsed"]) > 1:
			langContainer = ET.Element("languagesUsed")
			description.append(langContainer)
		else:
			langContainer = description

		# Add each <languageUsed> to the EAC
		for item in json["languagesUsed"]:
			# Create & insert <languageUsed> in <languageUsed> or <description>
			languageUsed = ET.Element("languageUsed")
			langContainer.append(languageUsed)

			# Create and insert <language> tag in <languageUsed>
			language = ET.Element("language")
			language.text = item["language"]["description"]
			language.set("languageCode", item["language"]["term"])
			languageUsed.append(language)

			# Create and insert <script> tag in <languageUsed>
			script = ET.Element("script")
			script.text = item["script"]["description"]
			script.set("scriptCode", item["script"]["term"])
			languageUsed.append(script)

	### <localDescriptions> ###

	# Create and insert <localDescriptions> tag in <description>
	localDescriptions = ET.Element("localDescriptions")
	description.append(localDescriptions)

	# Add gender data in <localDescriptions>
	# First, check that there is gender data
	if "genders" in json.keys():
		# Loop over those genders
		for item in json["genders"]:
			# Create and insert a <localDescription> tag in <localDescriptions>
			localDescription = ET.Element("localDescription")
			localDescription.set("localType", "gender")
			localDescriptions.append(localDescription)

			# Create and insert <term> tag in <localDescription>
			term = ET.Element("term")
			term.text = item["term"]["term"]
			localDescription.append(term)

	# Add associated subjects in <localDescriptions>
	# First, check that there is subject data
	if "subjects" in json.keys():
		# Loop over those subjects
		for item in json["subjects"]:
			# Create and insert a <localDescription> tag in <localDescriptions>
			localDescription = ET.Element("localDescription")
			localDescription.set("localType", "associatedSubject")
			localDescriptions.append(localDescription)

			# Create and insert <term> tag in <localDescription>
			term = ET.Element("term")
			term.text = item["term"]["term"]
			localDescription.append(term)

	### <places> ###

	# First, check JSON for place data
	if "places" in json.keys():
		# Create a <places> tag if there's more than one <place>
		if len(json["places"]) == 1:
			placeContainer = description
		else:
			placeContainer = ET.Element("places")
			description.append(placeContainer)

		# Add each of the places to the EAC
		for item in json["places"]:
			# Create and insert <place> tag in <places> or <description>
			place = ET.Element("place")
			placeContainer.append(place)
			addDesNote(item, place)

			# Create and insert <placeEntry> tag in <place>
			placeEntry = ET.Element("placeEntry")
			if "geoplace" in item.keys():
				placeEntry.text = item["geoplace"]["name"]
				if "latitude" in item["geoplace"].keys():
					placeEntry.set("latitude", item["geoplace"]["latitude"])
					placeEntry.set("longitude", item["geoplace"]["longitude"])
				if "countryCode" in item["geoplace"].keys():
					placeEntry.set("countryCode", item["geoplace"]["countryCode"])
			elif "original" in item.keys():
				placeEntry.text = item["original"]
			else:
				# Cannot identify place metadata
				msg = "Could not interprepret some place metadata in record "
				msg = msg + json["id"]
				print("\n", msg)
				break
			place.append(placeEntry)

	### <occupations> ###

	# First, check the JSON for occupation data
	if "occupations" in json.keys():
		# Create an <occupations> tag if there's more than one <occupation>
		if len(json["occupations"]) == 1:
			occuContainer = description
		else:
			occuContainer = ET.Element("occupations")
			description.append(occuContainer)

		# Add each of the occupations to the EAC
		for item in json["occupations"]:
			# Create and insert <occupation> tag in <occupations>/<description>
			occupation = ET.Element("occupation")
			occuContainer.append(occupation)

			# Create and insert <term> tag in <occupation>
			term = ET.Element("term")
			term.text = item["term"]["term"]
			occupation.append(term)

	### <biogHist> ###

	# First, check the JSON for biogHist data
	if "biogHists" in json.keys():
		# Get the content of the biogHist field
		text = json["biogHists"][0]["text"] # SNAC only allows for one BH note

		# Check to see if there's already a <biogHist> tag in text;
		if "</bioghist>" in text:
			# If there is, just convert that text to an XML element,
			#	add it to <description>, and call it a day
			biogHist = ET.fromstring(text)
			description.append(biogHist)
			return eac

		# Create an insert <biogHist> in <description>
		biogHist = ET.Element("biogHist")
		description.append(biogHist)

		# Check BH contents for <p>; insert if not found; add text either way
		if "</p>" in text:
			biogHist.text = text
		else:
			para = ET.Element("p")
			para.text = text
			biogHist.append(para)

	return eac

def writeXML(xml, filename):
	"""
	Writes an XML object to a file and turns (&lt; and &gt;) into (< and >)

	Params:
		XML, an XML object representing the data to be written
		filename, a string representing the desired file name
	"""

	#Write XML to file
	xml.write(filename, encoding="UTF-8", xml_declaration=True)

	# Run find & replace on file for (&lt; to <) and (&gt; to >)
	with open(filename, "r") as file:
		text = file.read()
	text = text.replace("&lt;", "<")
	text = text.replace("&gt;", ">")

	with open(filename, "w") as file:
		file.write(text)

def extractName(eac):
	"""
	Extract the contents of <cpfDescription><identity><nameEntry><part>

	Params: eac, an XML object conforming to the EAC standard
	"""
	for part in eac.iter("part"):
		return part.text
