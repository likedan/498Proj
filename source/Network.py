import collections
import os
from Person import *
from People import *

class Network:
    """ network class"""
    def __init__(self, testing):
        """
        initialize network structure
        """
        self.network, self.central, self.people = self.read_egonets('egonets')
        self.features = self.load_features('feature/features.txt', self.people)
        self.feature_list = self.load_feature_list('feature/feature_list.txt')
        self.training_data = self.load_training_data(testing)

    def read_egonets(self, directory):
        """
        function to read the egonet from text file
        """
        # init variables
        social_network = collections.defaultdict(set)
        central = []
        persons = People()

        # traverse and parse each egonet
        for egonet_file in os.listdir(directory):
            cur = egonet_file[:egonet_file.find('.')]
            central.append(cur)
            persons.central.append(cur)
            egonet_path = os.path.join(directory, egonet_file)
            # parse data in each egonet file
            for line in open(egonet_path):
                line = line.strip().split(':')
                cur_friend = line[0]
                social_network[cur].add(cur_friend)
                social_network[cur_friend].add(cur)
                persons.find_person(cur).add_friend(cur_friend)
                persons.find_person(cur_friend).add_friend(cur)
                friends = line[1].strip().split()

                # for person in each circle
                for friend in friends:
                    social_network[cur_friend].add(friend)
                    social_network[friend].add(cur_friend)
                    persons.find_person(cur_friend).add_friend(friend)
                    persons.find_person(friend).add_friend(cur_friend)

                    social_network[cur].add(friend)
                    social_network[friend].add(cur)
                    persons.find_person(cur).add_friend(friend)
                    persons.find_person(friend).add_friend(cur)

        return social_network, central, persons

    def load_training_data(self, directory):
        """
        function to load circles
        """
        # load the data
        training_network = collections.defaultdict(list)
        for training_file in os.listdir(directory):
            cur = training_file[:training_file.find('.')]
            training_filePath = os.path.join(directory, training_file)
            # parse the data
            for line in open(training_filePath):
                parts = line.strip().split()
                training_network[cur].append(parts[1:])
        return training_network

    def load_features(self, filename, persons=None):
        """
        function to load features
        """
        feature_map = collections.defaultdict(dict)
        for line in open(filename):
            parts = line.strip().split()
            cur = parts[0]
            for part in parts[1:]:
                key = part[0:part.rfind(';')]
                value = part[part.rfind(';') + 1:]
                feature_map[cur][key] = value
                if persons != None:
                    persons.find_person(cur).features[key] = value
        return feature_map

    def load_feature_list(self, filename):
        """
        function to load index of features
        """
        feature_list = []
        for line in open(filename):
            feature_list.append(line.strip())
        return feature_list

