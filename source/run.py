from kmeans import KMeans
from evaluation import *
from dataStructure import *
from math import sqrt
import similarityCalculator
import json

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

    data = DataStructure()

    SimilarityCalc = similarityCalculator.SimilarityCalculator(len(data.featureList))
    training_clusters = {}
    kmean = KMeans(data.people, SimilarityCalc.similarity_weighted_attributes_friendship)

    for personID in data.originalPeople:
        friends_of_person = data.people.getPerson(personID).friends
        #approximate number of centers
        k = int(sqrt(len(friends_of_person))) + 1
        clusters = kmean.fit(friends_of_person, k, 3.5)
        training_clusters[personID] = clusters

    training_clusters = convert_to_output_format(training_clusters)

    result_for_trainingset = {k:training_clusters[k] for k in data.trainingDict}
    evaluate(result_for_trainingset)

    with open('trainingset_result.json', 'w+') as outfile:
        json.dump(result_for_trainingset, outfile)
    #evaluate the testing result
    result_for_testing = {k:training_clusters[k] for k in data.originalPeople if k not in data.trainingDict}
    # evaluate(result_for_trainingset)
    # with open('testingset_result.json', 'w+') as outfile:
    #     json.dump(result_for_testing, outfile)
