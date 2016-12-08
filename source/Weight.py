import numpy as np
from Features import *
from Egonet import *


class Weight(object):
	"""
	weight matrix class
	"""
	def __init__(self, feature, feature_list):
		self.network = Egonet()
		self.feature = Feature(feature_list, feature)
		self.matrices, self.weight = self.construct_matrices()
		self.calculate_adjacent()
		self.calculate_features()

	def construct_matrices(self):
		"""
		construct the matrices layout
		"""
		print 'construct matrices'
		matrices = {}
		weight = {}
		for central in self.network.central.keys():
			matrices[central] = {}
			size = len(self.network.central[central])
			weight[central] = np.zeros((size, size))
			matrices[central]['A'] = np.zeros((size,size))
			matrices[central]['D'] = {}
			for i in range(self.feature.num):
				matrices[central]['D'][i] = np.zeros((size,size))
		return matrices, weight
	
	def calculate_adjacent(self):
		"""
		calculate the adjacent matrix A
		"""
		print 'calculating adjacent matrix'
		for group in self.network.central:
			for person in self.network.central[group]:
				size = len(self.network.central[group])
				for friend in self.network.friends[person]:
					index_person = int(person)-int(group)-1
					index_friend = int(friend)-int(group)-1
					if index_person < 0 or index_person >= size:
						continue
					if index_friend < 0 or index_friend >= size:
						continue
					self.matrices[group]['A'][index_person][index_friend] = 1
					self.matrices[group]['A'][index_friend][index_person] = 1
					self.calculate_weight(1.0, group, index_person, index_friend)

	def calculate_features(self):
		"""
		calculate the features matrix D
		"""
		print 'calculate_features'
		for group in self.network.central:
			print 'centroid: {}'.format(group)
			size = self.matrices[group]['D']
			for person in self.network.central[group]:
				print 'centroid: {}, person: {}'.format(group, person)
				if person[-1] == ':':
					continue
				for other in self.network.central[group]:
					if other[-1] == ':':
						continue
					if person == other:
						continue
					for i in range(self.feature.num):
						if self.feature.person_features[int(other)][i] == self.feature.person_features[int(person)][i]:
							index_person = int(person)-int(group)-1
							index_other = int(other)-int(group)-1
							if index_person < 0 or index_person >= size:
								continue
							if index_other < 0 or index_other >= size:
								continue
							self.matrices[group]['D'][i][index_person][index_other] = 1
							self.matrices[group]['D'][i][index_other][index_person] = 1
							self.calculate_weight(1.0, group, index_person, index_other)

	def calculate_weight(self, weight, group, person, other):
		"""
		calculate the weight matrix M = W1*A + W2*F_0 + ... + W2*F_n
		"""
		# print 'Adding weight for group {}, index({},{})'.format(group, person, other)
		self.weight[group][person][other] += weight
		self.weight[group][other][person] += weight


if __name__ == '__main__':
	data = Weight('feature/features.txt', 'feature/feature_list.txt')



