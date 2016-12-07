from kmeans import KMeans
from evaluation import *
from dataStructure import *
from math import sqrt
import similarityCalculator

# def writeSubmission(filename, circleMap, test=False):
#     f = open(filename, 'w+')
#
#     f.write('UserId,Predicted\n')
#
#     for person, circles in circleMap.iteritems():
#
#         line = person + ','
#
#         if not test:
#             for i in range(len(circles)):#circle in circles:
#                 for j in range(len(circles[i])):#friend in circles[i]:
#                     line += circles[i][j]
#                     if j != len(circles[i]) - 1:
#                         line += ' '
#                 if i != len(circles) - 1:
#                     line += ';'
#         else:
#             for friend in circles:
#                 line += friend + ' '
#             line += ';'
#
#         line += '\n'
#         f.write(line)
#
#     f.close()

def convert_to_output_format(clusters):
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
        total += evaluate_obj.get_score()
    print total / float(len(result))

if __name__ == '__main__':

    print 'Loading input data.'
    data = DataStructure()

    # List of people to calculate training data for.
    trainingPeople = []
    for key in data.trainingDict:
        trainingPeople.append(key)

    SimilarityCalc = similarityCalculator.SimilarityCalculator(len(data.featureList))

    training_clusters = {}
    k_means = KMeans(data.people, SimilarityCalc.similarity_weighted_attributes_friendship)

    for personID in data.originalPeople:
        friends_of_person = data.people.getPerson(personID).friends
        #approximate number of centers
        k = int(sqrt(len(friends_of_person))) + 1
        clusters = k_means.computeClusters(friends_of_person, k, 3.5)
        training_clusters[personID] = clusters

    training_clusters = convert_to_output_format(training_clusters)

    evaluate({k:training_clusters[k] for k in data.trainingDict})

    testingPeople = [origPerson for origPerson in data.originalPeople if origPerson
            not in trainingPeople]
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
