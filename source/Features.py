import numpy as np


class Feature(object):
	def __init__(self, feature_list, features):
		self.num = 0
		self.feature_map = self.read_feature_list(feature_list)
		self.person_features = self.read_features(features)

	def read_feature_list(self, name):
		with open(name, 'r') as feature_file:
			feature_map = {}
			for i, line in enumerate(feature_file):
				self.num += 1
				line = line.strip()
				feature_map[line] = i
			return feature_map

	def read_features(self, name):
		with open(name, 'r') as features_file:
			person_features = []
			for line in features_file:
				line = line.strip().split(' ')
				person = line[0]
				features = line[1:]
				personal = [0]*self.num
				for feature in features:
					feature = feature.split(';')
					feature_index = self.feature_map[';'.join(feature[:-1])]
					feature_value = int(feature[-1])
					personal[feature_index] = int(feature[-1]) + 1
				person_features.append(personal)
			print person_features
			return person_features

if __name__ == '__main__':
	feature = Feature('featureList.txt', 'features.txt')
