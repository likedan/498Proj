import numpy as np
import os

class Egonet(object):
	"""
	egonet class
	"""
	def __init__(self):
		"""
		initilized the central and friends
		"""
		self.central, self.friends = self.find_central('egonets')

	def find_central(self, directory):
		"""
		find the social network
		"""
		central = {}
		circle = {}
		for egonet_file in os.listdir(directory):
			cur = egonet_file[:egonet_file.find('.')]
			egonet_path = os.path.join(directory, egonet_file)
			circle[cur] = []
			central[cur] = []
			for line in open(egonet_path):
				line = line.strip().split(': ')
				person = line[0]
				central[cur].append(person) 
				if len(line) > 1:
					friends = line[1].split(' ')
					circle[person] = friends
				else:
					circle[person] = []
		return central, circle


if __name__ == '__main__':
	egonet = Egonet()
