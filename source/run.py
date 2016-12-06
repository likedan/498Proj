from userData import Persons
from kmeans import KMeans
from evaluation import *
from dataStructure import *

import similarityCalculator

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

def k_means_clustering(data, featureCount):
    SimilarityCalc = similarityCalculator.SimilarityCalculator(featureCount)
    attribute_and_friendship_clusters = _compute_k_means_clusters(data, SimilarityCalc.similarity_weighted_attributes_friendship, 3.5)

    return attribute_and_friendship_clusters

def _convert_kmeans_format(clusters):
    clusters_formatted = {}
    for original_person in clusters:
        circles = []
        for centroid in clusters[original_person]:
            circles.append( clusters[original_person][centroid] )
        clusters_formatted[original_person] = circles
    return clusters_formatted

def evaluate(result):
    result = dict(result)
    total = 0.0
    for (person, data) in result.iteritems():
        person_network = []
        file_name = "training/" + person + ".circles"
        with open(file_name) as f:
            for line in f:
                result = line.replace("\n", "")
                result_arr = result.split(" ")
                person_network.append(result_arr[1:])
        evaluate_obj = Evaluation(person_network, data)
        #print person
        #print evaluate_obj.get_score()
        total += evaluate_obj.get_score()
    print total / float(len(result))

if __name__ == '__main__':

    print 'Loading input data.'
    data = DataStructure()

    # List of people to calculate training data for.
    trainingPeople = []
    for key in data.trainingMap:
        trainingPeople.append(key)

    # List of the Kaggle submission people.
    kagglePeople = [origPerson for origPerson in data.originalPeople if origPerson
            not in trainingPeople]

    attribute_and_friendship_clusters = k_means_clustering(data, len(data.featureList))
    attribute_and_friendship_clusters = _convert_kmeans_format(attribute_and_friendship_clusters)

    evaluate({k:attribute_and_friendship_clusters[k] for k in data.trainingMap})
    # writeSubmission(real_training_data, data.trainingMap)
    #
    #
    # # Validation tests
    # writeSubmission(kmeans_attrs, {k:attribute_clusters[k] for k in data.trainingMap})
    # writeSubmission(kmeans_attrs_friends, {k:attribute_and_friendship_clusters[k] for k in data.trainingMap})
    # writeSubmission(kmeans_weighted_attrs_friends, {k:weighted_attribute_and_friendship_clusters[k] for k in data.trainingMap})
    # # Kaggle submissions
    # writeSubmission(kmeans_kaggle_attrs, {k:attribute_clusters[k] for k in
    #     data.originalPeople if k not in data.trainingMap})
    # writeSubmission(kmeans_kaggle_attrs_friends,
    #         {k:attribute_and_friendship_clusters[k] for k in
    #             data.originalPeople if k not in data.trainingMap})
    #
    # writeSubmission(kmeans_kaggle_weighted_attrs_friends,
    #         {k:weighted_attribute_and_friendship_clusters[k] for k in
    #             data.originalPeople if k not in data.trainingMap})
