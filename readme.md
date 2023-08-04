# Readme
This project contains a number of scripts for working with SNAC data and (hopefully) eventually porting it into ArchiveSpace. Below is documentation for a number of workflows. 

Most of these work by downloading constellations from SNAC in bulk and analysing the files locally. For workflows where changes are to be made in SNAC, those changes are first made locally and then pushed to SNAC via the API.

## Ensure SNAC relationships are reciprocal
By default, SNAC relationships are only coded one way, on a single constellation. For example, if constellation A has a "parentOf" relationship to constellation B, it is not guaranteed that B will have a "childOf" relationship to A. This workflow allows the automated adding of reciprocal relationships through API calls.

1. Delete any files in the `snac_jsons` folder.
2. Run `getSnacData.py`. This script pulls in the list of [constellations to include](https://github.com/swat-ds/obf-site/blob/main/content/constellationsForInclusion.tsv) from the Hunt obf-site repository, extracts the SNAC IDs from that list, makes API calls to each of them, and writes the resulting JSONs the `snac_jsons` folder.
3. Run `extractRelations.py`. This script reads in the data from a group of JSON files representing SNAC constellations and writes the relationship data they contain to a TSV titled `relationshipTable.tsv`.
4. Run `analyseRelationships.py`. This script loads relationship data from `relationshipTable.tsv`, analyses it, and writes missing reciprocal relationships to `missingRelationships.tsv`.
5. Run `python3 addRelationsToSNAC.py missingRelationships.tsv`; when prompted, chose to use the production server. This script loads relationship data from `missingRelationships.tsv` (or whatever TSV you specify when invoking it) and makes a series of API calls to add those relationships to SNAC constellations.