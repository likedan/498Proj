from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Ridge
from userData import Persons
from kmeans import KMeans
from evaluation import *

import similarityCalculator
import argparse
import collections
import os
import random

class Data:
    def __init__(self):
        self.friendMap = None
        self.originalPeople = None
        self.featureMap = None
        self.featureList = None
        self.trainingMap = None
        self.persons = Persons()

def loadEgoNets(directory):
    friendMap = collections.defaultdict(set)
    originalPeople = []
    persons = Persons()
    
    for egonetFile in os.listdir(directory):

        currentPerson = egonetFile[:egonetFile.find('.')]
        originalPeople.append(currentPerson)
        persons.addOriginalPerson(currentPerson)
               
        egonetFilePath = os.path.join(directory, egonetFile)

        for line in open(egonetFilePath):
            line = line.strip().split(':')
            currentFriend = line[0]

            friendMap[currentPerson].add(currentFriend)
            friendMap[currentFriend].add(currentPerson)
            persons.getPerson(currentPerson).addFriend(currentFriend)
            persons.getPerson(currentFriend).addFriend(currentPerson)
            
            friends = line[1].strip().split()

            for friend in friends:
                friendMap[currentFriend].add(friend)
                friendMap[friend].add(currentFriend)
                persons.getPerson(currentFriend).addFriend(friend)
                persons.getPerson(friend).addFriend(currentFriend)
            
                friendMap[currentPerson].add(friend)
                friendMap[friend].add(currentPerson)
                persons.getPerson(currentPerson).addFriend(friend)
                persons.getPerson(friend).addFriend(currentPerson)
            
    return friendMap, originalPeople, persons


"""
Input is a directory containing files with file names UserId.circles.
Each file contains lines of the form:

circleID: friend1 friend2 friend3 ...

describing the circles for UserId.

Returns a map from UserId -> a list of circles
"""
def loadTrainingData(directory):
    trainingMap = collections.defaultdict(list)

    for trainingFile in os.listdir(directory):
        currentPerson = trainingFile[:trainingFile.find('.')]

        trainingFilePath = os.path.join(directory, trainingFile)
        for line in open(trainingFilePath):
            parts = line.strip().split()
            trainingMap[currentPerson].append(parts[1:])

    return trainingMap

def loadFeatures(filename, persons = None):
    featureMap = collections.defaultdict(dict)
    for line in open(filename):
        parts = line.strip().split()
        currentPerson = parts[0]
        for part in parts[1:]:
            key = part[0:part.rfind(';')]
            value = part[part.rfind(';')+1:]
            featureMap[currentPerson][key] = value
            if persons != None:
                persons.getPerson(currentPerson).addFeature(key, value)
    return featureMap


"""
Input is a file name whose content is a list of all possible features, with one
feature per line.

Ouput is a list containing all the features.
"""
def loadFeatureList(filename, featureweight_filename):
    featureList = []
    feature_Wlist = {}
    for line in open(filename):
        featureList.append(line.strip())
    for line in open(featureweight_filename):
        line = line.strip()
        weight = line.split("--")
        feature_Wlist[weight[0]] = float(weight[1])
    return featureList, feature_Wlist


def writeSubmission(filename, circleMap, test=False):
    f = open(filename, 'w+')

    f.write('UserId,Predicted\n')

    for person, circles in circleMap.iteritems():

        line = person + ','

        if not test:
            for i in range(len(circles)):#circle in circles:
                for j in range(len(circles[i])):#friend in circles[i]:
                    line += circles[i][j]
                    if j != len(circles[i]) - 1:
                        line += ' '
                if i != len(circles) - 1:
                    line += ';'
        else:
            for friend in circles:
                line += friend + ' '
            line += ';'


        line += '\n'
        f.write(line)

    f.close()

def printMetricCommand(realOutput, testOutput):
    print '\nEvaluate using:'
    print 'python socialCircles_metric.py', realOutput, testOutput

def _compute_k_means_clusters(data, similarity_calculator, similarity_diff_threshold):
    computed_clusters = {}
    k_means = KMeans(data.persons, similarity_calculator)
    for personID in data.originalPeople:
        friends_of_person = data.persons.getPerson(personID).getFriends()
        if len(friends_of_person) > 250:
            k = 12
        else:
            k = 6
        clusters = k_means.computeClusters(friends_of_person, k, similarity_diff_threshold)
        computed_clusters[personID] = clusters
    return computed_clusters

def k_means_clustering(data, featureWeightMap):
    SimilarityCalc = similarityCalculator.SimilarityCalculator(featureWeightMap)
    attribute_clusters = _compute_k_means_clusters(data, SimilarityCalc.simiarity_according_to_attributes, 5)
    attribute_and_friendship_clusters = _compute_k_means_clusters(data, SimilarityCalc.simiarity_according_to_attributes_and_friendship, 10)
    weighted_attribute_and_friendship_clusters = _compute_k_means_clusters(data, SimilarityCalc.similarity_weighted_attributes_friendship, 3.5)

    return attribute_clusters, attribute_and_friendship_clusters, weighted_attribute_and_friendship_clusters

def _convert_kmeans_format(clusters):
    clusters_formatted = {}
    for original_person in clusters:
        circles = []
        for centroid in clusters[original_person]:
            circles.append( clusters[original_person][centroid] )
        clusters_formatted[original_person] = circles
    return clusters_formatted

def evaluate(result):
    print result
    result = dict(result)
    print result
    for (person, data) in result.iteritems():
        person_network = []
        file_name = "training/" + person + ".circles"
        with open(file_name) as f:
            for line in f:
                result = line.replace("\n", "")
                result_arr = result.split(" ")
                person_network.append(result_arr[1:])
        evaluate_obj = Evaluation(person_network, data)
        print person
        print evaluate_obj.get_score()

if __name__ == '__main__':

    # Input data locations.
    EGONET_DIR = 'egonets'
    TRAINING_DIR = 'training'
    FEATURE_FILE = 'features/features.txt'
    FEATURE_LIST_FILE = 'features/featureList.txt'
    FEATURE_WEIGHT_FILE = "feature_weights.txt"

    print 'Loading input data.'
    data = Data()

    # Load friend map.
    data.friendMap, data.originalPeople, data.persons = loadEgoNets(EGONET_DIR)

    # Load features.
    data.featureMap = loadFeatures(FEATURE_FILE, data.persons)

    # Load feature list
    data.featureList, featureWeightMap = loadFeatureList(FEATURE_LIST_FILE,FEATURE_WEIGHT_FILE)

    # Load training data.
    data.trainingMap = loadTrainingData(TRAINING_DIR)

    # List of people to calculate training data for.
    trainingPeople = []
    for key in data.trainingMap:
        trainingPeople.append(key)

    # List of the Kaggle submission people.
    kagglePeople = [origPerson for origPerson in data.originalPeople if origPerson
            not in trainingPeople]

    print 'Using k-means clustering metric.'
    attribute_clusters, attribute_and_friendship_clusters, weighted_attribute_and_friendship_clusters = k_means_clustering(data, featureWeightMap)
    
    attribute_clusters = _convert_kmeans_format(attribute_clusters)
    attribute_and_friendship_clusters = _convert_kmeans_format(attribute_and_friendship_clusters)
    weighted_attribute_and_friendship_clusters = _convert_kmeans_format(weighted_attribute_and_friendship_clusters)
    
    real_training_data = 'real_training_data.csv'
    kmeans_attrs = 'kmeans_attrs.csv'
    kmeans_attrs_friends = 'kmeans_attrs_friends.csv'
    kmeans_weighted_attrs_friends = 'kmeans_weighted_attrs_friends.csv'
    kmeans_kaggle_attrs = 'kmeans_kaggle_attrs.csv'
    kmeans_kaggle_attrs_friends = 'kmeans_kaggle_attrs_friends.csv'
    kmeans_kaggle_weighted_attrs_friends = 'kmeans_kaggle_weighted_attrs_friends.csv'

    writeSubmission(real_training_data, data.trainingMap)
    evaluate(data.trainingMap)

    # Validation tests
    writeSubmission(kmeans_attrs, {k:attribute_clusters[k] for k in data.trainingMap})
    writeSubmission(kmeans_attrs_friends, {k:attribute_and_friendship_clusters[k] for k in data.trainingMap})
    writeSubmission(kmeans_weighted_attrs_friends, {k:weighted_attribute_and_friendship_clusters[k] for k in data.trainingMap})
    
    # Kaggle submissions
    writeSubmission(kmeans_kaggle_attrs, {k:attribute_clusters[k] for k in
        data.originalPeople if k not in data.trainingMap})
    writeSubmission(kmeans_kaggle_attrs_friends,
            {k:attribute_and_friendship_clusters[k] for k in
                data.originalPeople if k not in data.trainingMap})
    writeSubmission(kmeans_kaggle_weighted_attrs_friends,
            {k:weighted_attribute_and_friendship_clusters[k] for k in
                data.originalPeople if k not in data.trainingMap})


    printMetricCommand(real_training_data, kmeans_attrs)
    printMetricCommand(real_training_data, kmeans_attrs_friends)
    printMetricCommand(real_training_data, kmeans_weighted_attrs_friends)
    print '\nKaggle submission files:', kmeans_kaggle_attrs, kmeans_kaggle_attrs_friends, kmeans_kaggle_weighted_attrs_friends

