

class Relationship:
	"""Represents a relationship between SNAC constellations"""

	def __init__(self, source, target, type):
		self.source = source
		self.target = target
		self.type = type

	def getInverse(self):
		inverseList = {
			"almaMaterOf":"alumnusOrAlumnaOf",
			"alumnusOrAlumnaOf":"almaMaterOf",
			"ancestorOf":"descendantOf",
			"auntOrUncleOf":"nieceOrNephewOf",
			"child-in-law of":"parent-in-law of",
			"childOf":"parentOf",
			"conferredHonorsTo":"honoredBy",
			"descendantOf":"ancestorOf",
			"employeeOf":"employerOf",
			"employerOf":"employeeOf",
			"foundedBy":"founderOf",
			"founderOf":"foundedBy",
			"grandchildOf":"grandparentOf",
			"grandparentOf":"grandchildOf",
			"hasHonoraryMember":"honoraryMemberOf",
			"hasMember":"memberOf",
			"Hierarchical-child":"Hierarchical-parent",
			"Hierarchical-parent":"Hierarchical-child",
			"honoraryMemberOf":"hasHonoraryMember",
			"honoredBy":"conferredHonorsTo",
			"investigatedBy":"investigatorOf",
			"investigatorOf":"investigatedBy",
			"memberOf":"hasMember",
			"nieceOrNephewOf":"auntOrUncleOf",
			"ownedBy":"ownerOf",
			"ownerOf":"ownedBy",
			"parent-in-law of":"child-in-law of",
			"parentOf":"childOf",
			"predecessorOf":"successorOf",
			"successorOf":"predecessorOf"
		}

		# Check if the relationship's type has an inverse
		if self.type in inverseList:
			# Get the inverse type if there is one, and return the inverse rel
			inverseType = inverseList[self.type]
			return Relationship(self.target, self.source, inverseType)
		else:
			return Relationship(self.target, self.source, self.type)

	def __eq__(self, other):
		if self.type == other.type:
			if self.target == other.target:
				if self.source == other.source:
					return True
		return False
