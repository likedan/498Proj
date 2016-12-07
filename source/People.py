from Person import *

class People(object):
	"""
	people class that define a group of persons
	"""
	def __init__(self):
		"""
		initilize the central person and members
		"""
		self.members = {}
		self.central = []

	def find_person(self, person):
		"""
		find the person in group 
		"""
		if person not in self.members:
			self.members[person] = Person(person)
		return self.members[person]

