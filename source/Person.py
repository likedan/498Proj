class Person(object):
	"""
	person class that define each person
	"""
	def __init__(self, person):
		"""
		initilize the features and friends of a person
		"""
		self.person = person
		self.friends = set()
		self.features = {}

	def add_friend(self, friend):
		"""
		add one more friend into group
		"""
		return self.friends.add(friend)

